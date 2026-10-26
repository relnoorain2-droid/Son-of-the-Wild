"""Build the English 30-second movie from the matching Hindi story and boards.

Existing 15-second exports and the Hindi package are read-only inputs. The
English 30-second output contains 312 numbered parts and one 004Aextra insert.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'YouTube movie'
HINDI = ROOT / 'Hindi version youtube movie'
OUTPUT = PACKAGE / 'Prompts_16x9'
COMBINED = PACKAGE / 'English_YouTube_16x9_30SEC_312_PLUS_004Aextra.txt'
REELS = ROOT / 'ZDola_Combined_Prompts/English_9x16_ALL_312_CLEAN.txt'
sys.path.insert(0, str(HINDI / 'Production_Docs'))
sys.path.insert(0, str(ROOT / 'scripts'))
from revised_hindi_dialogue import LINES
from split_pending_15s import dialogue_lines
from merge_reel_corrections import parse_sections

DEVANAGARI = re.compile(r'[\u0900-\u097f]')
HEADING = 'PROMPT TO COPY AND PASTE (SEEDANCE 2.5)'
SPEECH = re.compile(r'(?s)\nSPOKEN HINDI:\n(.*?)\n\nVOICE DELIVERY:')
SHOT = re.compile(r'(?m)^(\d+)-(\d+)s: (.+)$')
URL = re.compile(r'https://raw\.githubusercontent\.com/\S+')

# The Hindi adaptation deliberately revised these lines, so the English must
# follow that final version rather than accidentally restoring older wording.
ENGLISH_OVERRIDES = {
    (22,1): 'Mother, why are those people coming toward us?',
    (24,1): 'Why are these guards following me?',
    (150,0): 'This says Mom.',
    (150,1): 'Yes. And you wrote it.',
    (153,0): 'We nearly missed this little foal.',
    (269,0): 'I will go with my companions protecting me. I will not be afraid to speak to him.',
}


def collect_english():
    blocks = [b.strip() for b in re.split(r'(?m)^-------\s*$', REELS.read_text(encoding='utf-8-sig')) if b.strip()]
    assert len(blocks) == 312
    result, transliterations = [], {}
    for number, block in enumerate(blocks, 1):
        sections = parse_sections(block)
        speech = '\n'.join(v for k,v in sections if k in ('SPOKEN AUDIO','SPOKEN DIALOGUE','AUDIO'))
        original = dialogue_lines(speech)
        hindi = LINES.get(number, [])
        assert len(original) == len(hindi), (number, original, hindi)
        lines = []
        for index, ((speaker, words), translated) in enumerate(zip(original, hindi)):
            english = ENGLISH_OVERRIDES.get((number,index), words)
            if translated:
                lines.append((speaker, english))
                transliterations[translated] = english
        result.append(lines)
    transliterations['लिली कार्टर।'] = 'Lily Carter'
    return result, transliterations


def clear_ambiguous_wording(text):
    text = text.replace('ADULT WARDROBE AND DISTINCT IDENTITIES:', 'CHARACTER WARDROBE AND DISTINCT IDENTITIES:')
    text = text.replace('adult human women', 'women in the scene')
    text = text.replace('Adult human outfit styling', 'Outfit styling')
    text = text.replace('adult human outfit styling', 'outfit styling')
    text = text.replace('adult outfit styling', 'outfit styling')
    text = text.replace('adult human', 'person')
    text = text.replace('young adult woman', 'young woman')
    text = text.replace('young adult male', 'young male')
    text = text.replace('young adult', 'young')
    text = text.replace('adult female', 'female')
    text = text.replace('adult women', 'women aged 21 or older')
    text = text.replace('adult woman', 'woman aged 21 or older')
    text = text.replace('Adult Frost', 'Fully grown Frost').replace('adult Frost', 'fully grown Frost')
    text = text.replace('adult stage', 'fully grown stage').replace('adult years', 'later grown years')
    text = text.replace('adult volunteers', 'grown volunteers').replace('adult faces', 'grown faces')
    text = text.replace('adult voice', 'grown voice').replace('adult references', 'grown references')
    text = text.replace('adult identities', 'established identities').replace('adult is actually', 'person is actually')
    text = re.sub(r'\badult\b', 'grown', text, flags=re.I)
    text = text.replace('miniature grown baby', 'baby with grown-up proportions')
    text = text.replace('miniature grown', 'miniature grown-up')
    text = text.replace('grown child', 'fully grown Frost')
    text = text.replace('grown faces', 'older-stage faces')
    text = text.replace('grown references', 'fully grown references')
    text = text.replace('warm natural grown English female voice', 'warm natural English female voice')
    text = re.sub(r',\s*no nudity', '', text, flags=re.I)
    text = re.sub(r',\s*nudity', '', text, flags=re.I)
    text = text.replace('no inappropriate bedroom content, ', '').replace('No inappropriate bedroom content, ', '')
    return text


def translate_prompt(number, lines, words):
    source = HINDI / 'Prompts_16x9_Hindi' / f'Part_{number:03}_Dola_URL.txt'
    text = source.read_text(encoding='utf-8')
    preparation, body = text.split(HEADING, 1)
    for hindi, english in sorted(words.items(), key=lambda pair:len(pair[0]), reverse=True):
        body = body.replace(hindi, english)
    body = body.replace('LANGUAGE: HINDI VOICES; ENGLISH INSTRUCTIONS', 'LANGUAGE: ENGLISH VOICES AND INSTRUCTIONS')
    body = body.replace('SPOKEN LANGUAGE: HINDI ONLY.', 'SPOKEN LANGUAGE: ENGLISH ONLY.')
    body = body.replace('Dialogue is already written in Hindi.', 'Dialogue is already written in English.')
    body = body.replace('SPOKEN HINDI', 'SPOKEN ENGLISH')
    body = body.replace('Hindi dialogue section', 'English dialogue section')
    body = body.replace('natural Hindi lip-sync', 'natural English lip-sync')
    body = body.replace('Hindi female voice', 'English female voice').replace('Hindi male voice', 'English male voice')
    body = body.replace('Hindi bass-baritone', 'English bass-baritone').replace('Hindi bass voice', 'English bass voice')
    body = body.replace('natural Hindi voice', 'natural English voice').replace('natural Hindi,', 'natural English,')
    body = body.replace('Hindi girl voice', 'English girl voice').replace('Hindi boy voice', 'English boy voice')
    body = body.replace('Hindi male', 'English male').replace('Hindi female', 'English female')
    body = body.replace('Deliver each line in the corresponding action pause, with only its speaker lip-syncing.',
                        'Deliver each line in the corresponding action pause; visible speakers lip-sync, and a narrator remains off-screen.')
    spoken = '\n'.join(f'{speaker}: "{english}"' for speaker,english in lines)
    if not spoken:
        spoken = 'No dialogue or narration. Breathing, motivated effects and score only; no speaking mouth movements.'
    body, count = SPEECH.subn(lambda _: '\nSPOKEN ENGLISH:\n' + spoken + '\n\nVOICE DELIVERY:', body)
    # Replace after changing the heading; SPEECH was originally Hindi.
    if count == 0:
        body, count = re.subn(r'(?s)\nSPOKEN ENGLISH:\n(.*?)\n\nVOICE DELIVERY:',
                              lambda _: '\nSPOKEN ENGLISH:\n' + spoken + '\n\nVOICE DELIVERY:', body)
    assert count == 1, number
    body = clear_ambiguous_wording(body)
    if number == 4:
        body = revised_wedding(body)
    elif number == 5:
        body = re.sub(r'(?m)^Previous completed event, context only:.*$',
                      'Previous completed event, context only: Damian stands beside the uneasy red-haired bride, poised to present her to the court.', body)
    assert not DEVANAGARI.search(body), number
    assert 'HINDI ONLY' not in body and 'Hindi lip-sync' not in body and 'SPOKEN HINDI' not in body
    return preparation + HEADING + body


def revised_wedding(body):
    start = body.index('\nSCENE:\n')
    end = body.index('\nVOICE DELIVERY:', start)
    updated = '''
SCENE:
The first red-haired bride, age 25, and Damian stand at the altar in a magnificent but strangely silent wedding hall. Rose remains partly hidden at the side. The bride willingly takes part in one brief ceremonial lip kiss, yet remains uncertain about the marriage. Magnus silently watches from his throne.

SOUND AND CAMERA:
Distant wedding bells, soft steps, gown fabric and restrained ceremonial strings. Medium and medium-wide shots preserve both faces. The mood remains beautiful and tense. No cheering, added speeches or face-distorting close-ups.

SHOT PLAN:
0-5s: Wide hall with stone columns, candles and banners. Damian and the same red-haired bride are already beside each other at the altar. Magnus watches; the guests are quiet. The off-screen narrator speaks once.
5-11s: Medium two-shot. Damian smiles politely and speaks his line. The bride glances toward the silent guests.
11-15s: Damian turns toward her and pauses. She gives a small affirmative nod and leans toward him of her own accord. He responds gently. No restraint or grabbing.
15-17s: One natural, gentle, mutually welcomed lip kiss, clearly visible in a steady medium shot. They separate naturally; no prolonged or repeated kiss.
17-23s: Damian resumes his polished smile toward the court. The bride breathes and becomes guarded again. Magnus watches with restrained approval. No dialogue.
23-27s: Rose watches silently from a concealed side doorway. She and the bride briefly meet eyes; Rose lowers her gaze.
27-30s: Damian stands beside the uneasy red-haired bride, poised to present her to the court. His hand remains lowered; do not begin Part 005's hand-raising action. Natural fabric and breathing continue.

SPOKEN ENGLISH:
NARRATOR, off-screen, 0-5s: "The wedding bells rang, but the city did not celebrate."
PRINCE DAMIAN, 5-11s: "Stand beside me. The court must see that all is well."
'''
    body = body[:start] + '\n' + updated + body[end:]
    body = re.sub(r'(?m)^Complete this local event:.*$',
                  'Complete this local event: Damian stands beside the uneasy red-haired bride, poised to present her to the court.', body)
    return body


def extra_prompt():
    text = (HINDI/'Prompts_16x9_Hindi/Part_004Aextra_The_Wedding_Night.txt').read_text(encoding='utf-8')
    prep, body = text.split('PROMPT TO COPY AND PASTE',1)
    body = body.replace('SPOKEN LANGUAGE: Hindi only.', 'SPOKEN LANGUAGE: English only.')
    body = body.replace('SPOKEN HINDI', 'SPOKEN ENGLISH')
    body = body.replace('his single Hindi line', 'his single English line')
    body = body.replace('her one Hindi line', 'her one English line')
    body = body.replace('two Hindi lines', 'two English lines')
    body = body.replace('Hindi male voice', 'English male voice').replace('Hindi female voice', 'English female voice')
    body = body.replace('यह पल सिर्फ हमारा है।', 'This moment belongs to us.')
    body = body.replace('यहीं रहो, मेरे पास।', 'Stay here, close to me.')
    body = body.replace('No narrator, background speech, dialogue subtitles or spoken title.',
                        'No narrator, background speech, dialogue subtitles or spoken title. The two specified English time cards are silent editorial text, not dialogue.')
    body = body.replace('These are silent editorial cards, not spoken words or subtitles.',
                        'These are silent editorial cards, not spoken words or dialogue subtitles.')
    body = body.replace('She relaxes and smiles. Keep the nightdress',
                        'She relaxes and smiles. After her line, they share one brief gentle lip kiss, both leaning in willingly. Keep the nightdress')
    body = body.replace('There is no nudity, undressing or depiction of sexual activity.',
                        'Both remain clothed; private intimacy is implied by the fade and sleeping shot.')
    body = clear_ambiguous_wording(body)
    assert not DEVANAGARI.search(body) and 'Hindi' not in body
    return prep + 'PROMPT TO COPY AND PASTE' + body


def main():
    lines, words = collect_english()
    source_hashes = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (
        REELS, HINDI/'Hindi_YouTube_16x9_ALL_312_REFERENCE_HANDOFF_CLEAN.txt',
        HINDI/'Production_Docs/REFERENCE_HANDOFF_MANIFEST.json',
        PACKAGE/'English_YouTube_16x9_15SEC_PARTS_001_312_CLEAN.txt',
        PACKAGE/'English_YouTube_16x9_15SEC_PARTS_313_624_CLEAN.txt')}
    OUTPUT.mkdir(exist_ok=True)
    texts = []
    for number in range(1,313):
        text = translate_prompt(number, lines[number-1], words)
        (OUTPUT/f'Part_{number:03}_Dola_URL.txt').write_text(text, encoding='utf-8')
        texts.append(text.strip())
    extra = extra_prompt()
    (OUTPUT/'Part_004Aextra_The_Wedding_Night.txt').write_text(extra, encoding='utf-8')
    blocks = texts[:4] + [extra.strip()] + texts[4:]
    COMBINED.write_text('\n\n-------\n\n'.join(blocks)+'\n',encoding='utf-8')
    manifest = {'parts':312,'extra':'004Aextra','total_prompts':313,'seconds_per_part':30,
                'aspect_ratio':'16:9','language':'English','reference_source':'Hindi version youtube movie/Reference_Sheets',
                'source_hashes':source_hashes,'generated_videos':0,
                'note':'Same reference boards and story as the Hindi YouTube set. Part 004 follows the user-supplied ceremonial kiss revision. 004Aextra is an optional flash-forward insert.'}
    (PACKAGE/'Production_Docs/ENGLISH_30SEC_MATCHING_HINDI_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    validate()


def validate():
    manifest=json.loads((PACKAGE/'Production_Docs/ENGLISH_30SEC_MATCHING_HINDI_MANIFEST.json').read_text(encoding='utf-8'))
    blocks=re.split(r'\n\n-------\n\n',COMBINED.read_text(encoding='utf-8').strip())
    assert len(blocks)==313
    checked_boards = set()
    for number in range(1,313):
        path=OUTPUT/f'Part_{number:03}_Dola_URL.txt'
        text=path.read_text(encoding='utf-8')
        assert text.strip()==blocks[number-1 if number<=4 else number]
        prep,body=text.split(HEADING,1)
        hindi=(HINDI/'Prompts_16x9_Hindi'/f'Part_{number:03}_Dola_URL.txt').read_text(encoding='utf-8').split(HEADING,1)[0]
        assert URL.findall(prep)==URL.findall(hindi) and len(URL.findall(prep))==1,number
        board = ROOT / unquote(urlsplit(URL.findall(prep)[0]).path.split('/main/',1)[1])
        if board not in checked_boards:
            with Image.open(board) as image:
                assert max(image.size) <= 4096 and image.width * image.height <= 8_000_000
                image.verify()
            checked_boards.add(board)
        assert not DEVANAGARI.search(body) and 'SPOKEN HINDI' not in body and 'HINDI ONLY' not in body,number
        assert 'FORMAT: YOUTUBE 16:9' in body and 'Duration: exactly 30 seconds' in body
        shot_body=body.split('\nSHOT PLAN:\n',1)[1].split('\nSPOKEN ENGLISH:',1)[0]
        cursor=0
        for match in SHOT.finditer(shot_body):
            assert int(match[1])==cursor and int(match[2])>cursor,(number,match[0],cursor)
            cursor=int(match[2])
        assert cursor==30,number
    extra=(OUTPUT/'Part_004Aextra_The_Wedding_Night.txt').read_text(encoding='utf-8')
    assert extra.strip()==blocks[4] and not DEVANAGARI.search(extra)
    assert 'one brief gentle lip kiss' in extra and 'silent editorial text' in extra
    extra_hindi=(HINDI/'Prompts_16x9_Hindi/Part_004Aextra_The_Wedding_Night.txt').read_text(encoding='utf-8')
    assert URL.findall(extra)==URL.findall(extra_hindi) and len(URL.findall(extra))==1
    extra_board=ROOT/unquote(urlsplit(URL.findall(extra)[0]).path.split('/main/',1)[1])
    with Image.open(extra_board) as image:
        assert max(image.size)<=4096 and image.width*image.height<=8_000_000
        image.verify()
    extra_shots=extra.split('EXACT 30-SECOND SHOT PLAN',1)[1].split('SPOKEN ENGLISH - EXACT WORDS',1)[0]
    cursor=0
    for match in SHOT.finditer(extra_shots):
        assert int(match[1])==cursor and int(match[2])>cursor,match[0]
        cursor=int(match[2])
    assert cursor==30
    assert '15-17s: One natural, gentle' in blocks[3]
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in manifest['source_hashes'].items())
    print('PASS: 312 numbered English 30-second prompts plus 004Aextra, 313 combined blocks, same Hindi reference boards, complete timelines and English-only speech. Source packages unchanged.')


if __name__=='__main__':
    validate() if '--validate' in sys.argv else main()
