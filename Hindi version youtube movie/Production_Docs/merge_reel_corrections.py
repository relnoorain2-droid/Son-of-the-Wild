"""Merge the corrected Reels story with office Hindi reference-board delivery.

Only the Hindi YouTube package is written. Original character images and office
boards remain intact. Boards are assembled from existing images, never redrawn.
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote

from PIL import Image
import build_reference_handoffs as boards
from revised_hindi_dialogue import LINES

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from split_pending_15s import dialogue_lines

SOURCE = ROOT / 'ZDola_Combined_Prompts/English_9x16_ALL_312_CLEAN.txt'
MANIFEST = PACKAGE / 'Production_Docs/REFERENCE_HANDOFF_MANIFEST.json'
COMBINED = PACKAGE / 'Hindi_YouTube_16x9_ALL_312_REFERENCE_HANDOFF_CLEAN.txt'
MARKER = 'PROMPT TO COPY AND PASTE (SEEDANCE 2.5)'
HEADER = re.compile(r'(?m)^([A-Z][A-Z 0-9(),/:-]*):[ \t]*\n')
SHOT = re.compile(r'(?m)^(\d+)-(\d+)s: (.+)$')
URL = re.compile(r'https://raw\.githubusercontent\.com/\S+')

STYLE = '''PHOTOREALISM AND IDENTITY:
Render a photorealistic live-action appearance, with physically believable fantasy creatures. Natural human skin pores, subtle facial asymmetry, real eye proportions, individual hair strands, realistic fabric and natural light. No cartoon, anime, doll face, plastic skin, game-avatar appearance, exaggerated eyes or painted textures. Medium shots keep faces readable; no extreme face close-ups or distorted wide-angle portraits. Match each person's own reference identity throughout the scene. Clothing changes only at a written change; retain mud, tears, wetness and props at each edit.
Only characters explicitly acting in the local shot plan appear. A reference panel is an identity guide, not an instruction to add its person to the scene. Keep Rose, Grace and Martha distinct. Rose is a castle maid: only show her when locally required, concealed at a side doorway or pillar, never roaming into bedrooms or interrupting every scene. Only the Hindi dialogue section authorizes speech. Background figures never borrow another person's dialogue.
Only when the local shots include Frost, show exactly one at the written age stage. Never introduce him before birth or into scenes where he is absent. His father's Bigfoot genes explain his accelerated growth; age changes only at written time passages. Keep upright Bigfoot anatomy, broad hands and feet, snow-white fur and blue eyes. No dog muzzle, paws, tail, human replacement, miniature adult baby or extra child. When requested, Bruno remains the black-furred Bigfoot with his own identity. His later spirit is not a living resurrection.
'''

def parse_sections(text):
    matches = list(HEADER.finditer(text))
    return [(m[1], text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()) for i,m in enumerate(matches)]

def landscape(text):
    text = text.replace('9:16', '16:9').replace('VERTICAL', 'LANDSCAPE')
    text = re.sub(r'\bvertical\b', 'landscape', text, flags=re.I)
    text = text.replace('English', 'Hindi')
    text = text.replace('Hyper-realistic cinematic 3D animation', 'Photorealistic live-action appearance')
    text = text.replace('Unreal Engine 5 quality', 'physically believable lighting')
    text = text.replace('short simple Hindi sentences', 'short natural Hindi sentences')
    return text

def prepare_parts():
    blocks = [b.strip() for b in re.split(r'(?m)^-------\s*$', SOURCE.read_text(encoding='utf-8-sig')) if b.strip()]
    assert len(blocks) == 312
    parts = []
    for number, block in enumerate(blocks, 1):
        title = re.match(r'PART (\d{3}) - "([^"]+)"', block)
        assert int(title[1]) == number
        sections = parse_sections(block)
        speech = '\n'.join(v for k,v in sections if k in ('SPOKEN AUDIO','SPOKEN DIALOGUE','AUDIO'))
        original = dialogue_lines(speech)
        translated = LINES.get(number, [])
        assert len(original) == len(translated), (number, original, translated)
        lines = [(speaker, words) for (speaker,_),words in zip(original, translated) if words]
        source_shots = next(v for k,v in sections if k == 'SHOT PLAN')
        # Translate matching inline speech too; staging never authorizes extra speech.
        for (_,english), hindi in zip(original, translated):
            source_shots = source_shots.replace(english, hindi or '[silent reaction]')
        if number == 6:
            source_shots = source_shots.replace('Rose watches from the doorway edge, partly hidden.', 'The doorway stays empty; Rose is absent.')
        if number == 11:
            source_shots = source_shots.replace('Rose is only a half-hidden figure in the corridor shadow; she does not enter the room.', 'Rose and Magnus are absent from this scene.')
            source_shots = source_shots.replace('muddy bootprints cross the stone floor toward the stable door.', 'At the foot of the servant stairway, the bride notices muddy bootprints crossing toward the stable door.')
        if number == 12:
            source_shots = source_shots.replace("a small child behind a curtain mouths, 'not another one,'", 'a child behind a curtain silently watches')
        if number == 24:
            source_shots = source_shots.replace("Rose whispers 'not again' as Lily turns toward her.", 'Rose silently lowers her eyes as Lily turns toward her.')
        if number == 29:
            source_shots = source_shots.replace('She enters quickly, frightened but determined.', 'She remains outside the doorway, frightened but determined; Lily approaches from inside.')
            source_shots = source_shots.replace('Lily and Rose freeze in silence, eyes on the door handle.', 'Rose withdraws into the corridor shadow; Lily freezes inside, eyes on the door handle.')
        shots = [(int(m[1]),int(m[2]),landscape(m[3])) for m in SHOT.finditer(source_shots)]
        assert shots and shots[0][0] == 0 and shots[-1][1] == 30
        refs = list(dict.fromkeys(unquote(u.split('/main/',1)[1]) for u in URL.findall(block)))
        # References absent from the local action should not invite extra actors.
        if number in (2,6,11):
            refs = [r for r in refs if 'S11_Rose' not in r and (number != 11 or 'C02_KingMagnus' not in r)]
        if number in (6,11):
            refs.append('Characters_Dola_1024/Main/C03_PrinceDamian/C03_PrinceDamian_FACE.png')
        if any('VEX' in s.upper() for s,_ in lines) and not any('S07_' in r for r in refs):
            refs.append('Characters_Dola_1024/Supporting/S07_CaptainVex/S07_CaptainVex_FULL.png')
        extras = []
        skipped = {'SHOT PLAN','SPOKEN AUDIO','SPOKEN DIALOGUE','VIDEO','STYLE LOCK','CAMERA LOCK','ROSE PLACEMENT LOCK','DIALOGUE RULE','FORMAT','VIDEO LENGTH','SELF-CONTAINED PART RULE'}
        for key,value in sections:
            if key in skipped or key.startswith('REFERENCE IMAGE') or key.startswith('IMPORTANT - DOWNLOAD'):
                continue
            if key == 'AUDIO':
                # Keep motivated ambience, but place all audible words in one section.
                value = re.sub(r'[^.\n]*?:\s*"[^"\n]+"', '', value)
                value = value.split('Speak only the explicitly written line')[0].strip()
            value = re.sub(r'(?m)^PROMPT TO PASTE IN DOLA.*$', '', value)
            value = re.sub(r'(?m)^FORMAT:.*$|^VIDEO LENGTH:.*$', '', value)
            if key == 'SCENE' and number == 29:
                value = 'Rose warns Lily from outside her doorway after Damian leaves; Lily listens from inside.'
            if number < 86:
                value = re.sub(r'(?m)^From Part 086 onward the main force.*\n?', '', value)
            if 68 <= number <= 80:
                value = value.replace(
                    "At Part 067's peaceful-days passage, explicitly show her changing from her damaged wedding dress into the forest-reference outfit and replacing her lost shoe with simple matching footwear.",
                    'The change from her damaged wedding gown to these forest clothes and replacement footwear has already happened. Do not replay it.'
                )
            if value.strip():
                extras.append(key + ':\n' + landscape(value.strip()))
        # Part 031 has important unheaded cast restrictions before OPENING.
        if number == 31:
            extras.insert(0, 'LOCAL CAST: Exactly one person, Lily in her damaged wedding gown. No Bruno, guards, Rose, mother, bear or visible wolves.')
        parts.append({'number':number, 'title':title[2], 'shots':shots, 'lines':lines,
                      'references':refs, 'context':'\n\n'.join(extras), 'source_sha256':hashlib.sha256(block.encode()).hexdigest()})
    return parts

def voice(speaker, part):
    key = speaker.lower()
    if 'frost' in key:
        stage = ('gentle boy voice' if part['number'] < 170 else
                 'youthful teenage boy voice' if part['number'] < 184 else 'deep heroic male voice')
        return f'Frost: {stage}, natural Hindi, appropriate to this scene'
    if 'bruno' in key: return 'Bruno: deep, warm, restrained Hindi bass voice'
    if 'lily' in key: return 'Lily: natural young adult Hindi female voice'
    if 'magnus' in key: return 'Magnus: older commanding Hindi bass-baritone'
    if 'damian' in key: return 'Damian: smooth controlled young adult Hindi male voice'
    if 'narrator' in key: return 'Narrator: restrained cinematic Hindi male voice'
    for name, description in (
        ('martha', 'warm mature Hindi female voice'),
        ('grace', 'caring mature Hindi female voice'),
        ('rose', 'quiet older Hindi female voice'),
        ('orin', 'ancient resonant Hindi male voice, measured and wise'),
        ('joe', 'older textured Hindi male voice, conversational and distinct from Orin'),
        ('hank', 'grounded middle-aged Hindi male voice'),
        ('vex', 'clipped commanding Hindi male voice'),
        ('sarah', 'natural young Hindi girl voice'),
        ('tommy', 'natural young Hindi boy voice'),
    ):
        if name in key:
            return re.sub(r'\([^)]*\)', '', speaker).strip() + ': ' + description
    return re.sub(r'\([^)]*\)', '', speaker).strip() + ': distinct natural Hindi voice matching reference age and character'

def local_costume(part):
    """Describe only the relevant reference outfits, without global scene imports."""
    n = part['number']
    refs = part['references']
    result = [
        'REFERENCE COSTUME AND APPEARANCE:',
        'Preserve the face, age, hairstyle, outfit design, colors and established coverage of each character requested by this scene. '
        'Use realistic fabric, well-fitted tailoring and natural proportions. Match dirt, wetness, tears and accessories across a continuous scene. '
        'A style description does not add a person or change the written action.',
    ]
    if any(re.search(r'/(?:C01_Lily|V0[1-4]_Lily_)', r) for r in refs):
        result.append(
            'Lily Carter is a 23-year-old woman with the same reference face and honey-blonde hair. '
            'Keep her elegant, attractive film-star appearance through flattering fit, natural grooming, '
            'expressive eyes and realistic light appropriate to the setting. Preserve the approved neckline '
            'and any shoulders visible in that outfit, with opaque fabric and the same silhouette. '
            'Show emotion through face, posture and story action; retain exhaustion, dirt or injuries when written.'
        )
        if 31 <= n <= 50 and any('/V01_Lily_Wedding/' in r for r in refs):
            result.append('Lily retains her cream-ivory wedding gown during this escape, with the existing mud, torn hem and missing shoe where written. A clean portrait does not reset these details.')
        elif n <= 80 and any('/V02_Lily_Forest/' in r for r in refs):
            result.append('Retain the same approved blue forest dress in connected scenes. The established change out of the wedding gown happens once at the written time passage; do not switch clothes between connected shots. Warm firelight may softly flatter her face when the setting supports it.')
        elif 75 <= n <= 126:
            result.append('Use the exact local pregnancy stage: the early uncertainty is not a late-pregnancy belly. Later pregnancy, labor and memories follow their local timeline and reference outfit. Keep the same youthful face; use practical layers where written.')
        else:
            result.append('Use the local young-mother or celebration outfit from the approved reference and prior accepted frame. A future or past costume panel never changes her current outfit mid-shot.')
        if n in (62, 66, 74, 76, 77, 78):
            result.append('Use warm cinematic light and restrained chemistry for the written mutual affection. Follow only the local gestures, retaining the same clothes and recognizable faces throughout.')
    if any('/S11_Rose/' in r for r in refs):
        result.append('Rose retains her older face, grey hair, maid cap, black dress and white apron. She appears or speaks only when requested in this local scene.')
    if any('/S02_MarthaHayes/' in r for r in refs):
        result.append('Martha retains her own older face, glasses, white curls and reference clothes. She is distinct from Rose and Grace.')
    return '\n'.join(result) + '\n\n'


def main():
    parts = prepare_parts()
    old = json.loads(MANIFEST.read_text(encoding='utf-8'))
    first_update = 31
    protected = {}
    for record in old['records'][:first_update-1]:
        path = PACKAGE/'Prompts_16x9_Hindi'/f"Part_{record['part']:03}_Dola_URL.txt"
        protected[path.relative_to(PACKAGE).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        board_path = PACKAGE/record['reference_board']
        protected[record['reference_board']] = hashlib.sha256(board_path.read_bytes()).hexdigest()
    # Reuse a matching office board exactly; otherwise use the same labelled layout.
    available = {tuple(p['source'] for p in r['panels']): (PACKAGE/r['reference_board'],r['panels']) for r in old['records']}
    cache, records, prompts = {}, [], []
    for i,part in enumerate(parts):
        n = part['number']
        if n < first_update:
            records.append(old['records'][i])
            prompts.append((PACKAGE/'Prompts_16x9_Hindi'/f'Part_{n:03}_Dola_URL.txt').read_text(encoding='utf-8').strip())
            continue
        refs = tuple(sorted(set(part['references'])))
        for relative in refs: assert (ROOT/relative).is_file(), relative
        if refs not in cache:
            if refs in available:
                target,panels = available[refs]
            else:
                target = PACKAGE/'Reference_Sheets'/f'Reel_Corrected_{n:03}.jpg'
                panels = boards.sheet(refs,target)
            cache[refs] = target,panels
        target,panels = cache[refs]
        url = boards.RAW + quote(target.relative_to(ROOT).as_posix(),safe='/') + '?v=reel-sync-20261026'
        mapping = '\n'.join(f"Panel {p['panel']}: {p['name']} ({Path(p['source']).name})." for p in panels)
        previous = records[-1]['local_shots'][-1][2] if records else None
        following = parts[i+1]['shots'][0][2] if i<311 else None
        opening = f'Previous completed event, context only: {previous}\n' if previous else 'Movie opening: no prior frame.\n'
        opening += f"First local action: {part['shots'][0][2]}\n"
        ending = f"Complete this local event: {part['shots'][-1][2]}\n"
        ending += f'Next opening, context only: {following}' if following else 'Final movie closure. No next-part hook or new threat.'
        shots = '\n'.join(f'{a}-{b}s: {action}' for a,b,action in part['shots'])
        spoken = '\n'.join(f'{speaker}: "{words}"' for speaker,words in part['lines']) or 'No dialogue or narration. Breathing, motivated effects and score only; no speaking mouth movements.'
        voices = '\n'.join(dict.fromkeys(voice(s,part) for s,_ in part['lines']))
        wardrobe = local_costume(part)
        bride = ('BRIDE IDENTITY: Before Lily arrives, the bride is ONLY the red-haired third adult woman from the left in S09_Brides_FULL.png. Preserve her face, braid and ivory gown across Parts 002-015. She is not Lily. Other women in that panel are not extra wives.\n\n' if 2<=n<=15 else '')
        special = ('LOCAL CAST EXCLUSION: Rose is absent, with no off-screen warning or substitute older woman.\n\n' if n in (2,6,11) else '')
        text = (f'PART {n:03} - "{part["title"]}"\nFROST: Son of the Wild\n\n'
                f'REFERENCE IMAGES - PREPARE ABOVE THE COPY LINE\nImage 1 (required combined reference board): {target.name}\n{url}\n'
                'Download and inspect this board, then attach it as ONE image. Use the labels to map the panels. '
                'Optional image 2: the actual approved previous end frame, if available. Optional image 3: a face detail. '
                'At most three images total. No skill file is needed. Stop at the ------- separator.\n\n'
                + MARKER + '\n\n' + f'PART {n:03} - "{part["title"]}"\n'
                'FORMAT: YOUTUBE 16:9\nDuration: exactly 30 seconds\nLANGUAGE: HINDI VOICES; ENGLISH INSTRUCTIONS\n'
                'SPOKEN LANGUAGE: HINDI ONLY. Dialogue is already written in Hindi. Speak only the exact words in SPOKEN HINDI below, once each. '
                'English shot instructions and labels are silent. Quoted text elsewhere is staging or context, never an additional line. '
                'No improvised narration, background warnings, repeated catchphrases or title reading. Use natural Hindi lip-sync and comfortable pauses.\n\n'
                'SEPARATE GENERATION + REFERENCE MAPPING:\nThis prompt is complete in a fresh chat. Attachment 1 is a labelled reference board:\n'
                + mapping + '\nRead labels ABOVE panels. Create a fresh moving scene; never animate the collage, render panel labels, blend faces or put every panel character on screen. '
                'Location-panel background people are not additional cast. Image 2, if supplied, is an actual approved end frame; never claim one is attached when absent.\n\n'
                + wardrobe + bride + special + STYLE + '\n'
                + 'OPENING HANDOFF IN:\n' + opening +
                'Preserve pose, eyeline, camera side, carried objects, damage and wetness for a same-scene join. '
                'Follow explicit local time/location changes; establish the new setting without replaying completed events. '
                'A written memory is clearly a memory, not a second birth, resurrection, first meeting or repeated attack.\n\n'
                + part['context'] + '\n\nSHOT PLAN:\n' + shots + '\n\nSPOKEN HINDI:\n' + spoken + '\n\n'
                + 'VOICE DELIVERY:\n' + (voices or 'No speaking voices.') +
                '\nKeep a stable approved voice preset per character when available. Deliver each line in the corresponding action pause, with only its speaker lip-syncing. '
                'Do not fill quiet or action scenes with dialogue. Finish speech before the edit; avoid overlapping voices.\n\n'
                + 'ENDING HANDOFF OUT:\n' + ending + '\nKeep the final pose readable with natural movement, not a freeze or repeated loop. '
                'Do not begin the next scene. Same-scene ambience continues without a new music introduction. '
                'Use the full 0-30s timeline with purposeful action and reactions.\n')
        (PACKAGE/'Prompts_16x9_Hindi'/f'Part_{n:03}_Dola_URL.txt').write_text(text,encoding='utf-8')
        prompts.append(text.strip())
        with Image.open(target) as im: width,height = im.size
        records.append({'part':n,'title':part['title'],'reference_board':target.relative_to(PACKAGE).as_posix(),
                        'panels':panels,'reference_image_width':width,'reference_image_height':height,
                        'image_input_count_required':1,'max_image_inputs':3,'local_shots':part['shots'],
                        'previous_ending':previous,'next_opening':following,'spoken_hindi':part['lines'],
                        'source_sha256':part['source_sha256']})
        if n%50==0: print(f'Prepared {n}/312 Hindi prompts',flush=True)
    COMBINED.write_text('\n\n-------\n\n'.join(prompts)+'\n',encoding='utf-8')
    report = {'date':'2026-10-27','source':'ZDola_Combined_Prompts/English_9x16_ALL_312_CLEAN.txt',
              'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'office_base_commit':'20c3602',
              'parts':312,'aspect_ratio':'16:9','duration_seconds_per_part':30,
              'required_images_per_part':1,'maximum_images_per_request':3,
              'unique_labelled_reference_sheets':len({r['reference_board'] for r in records}),'speech_language':'Hindi','speech_script':'Devanagari',
              'reviewed_parts':[31,312], 'completed_parts_preserved':[1,30],
              'protected_files_sha256':protected,
              'runtime_dialogue_translation_required':False,'method':'Corrected Reels scenes and identities, authored Hindi adaptation, office combined-board workflow. No video renders verified.',
              'records':records}
    MANIFEST.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (PACKAGE/'Production_Docs/REFERENCE_IMAGE_INDEX.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f); writer.writerow(['part','title','attach_image_1','optional_attach_image_2_after_render','max_images'])
        for r in records: writer.writerow([f"{r['part']:03}",r['title'],r['reference_board'],f"Part_{r['part']-1:03}_EndFrame.png" if r['part']>1 else '',3])
    validate()

def validate():
    report=json.loads(MANIFEST.read_text(encoding='utf-8'))
    parts=report['records']; assert len(parts)==312
    blocks=re.split(r'\n\n-------\n\n',COMBINED.read_text(encoding='utf-8').strip())
    assert len(blocks)==312
    utterances=[]
    for relative,expected in report.get('protected_files_sha256',{}).items():
        assert hashlib.sha256((PACKAGE/relative).read_bytes()).hexdigest()==expected, relative
    for i,r in enumerate(parts):
        n=i+1; text=(PACKAGE/'Prompts_16x9_Hindi'/f'Part_{n:03}_Dola_URL.txt').read_text(encoding='utf-8')
        assert text.strip()==blocks[i]
        prep,body=text.split(MARKER,1)
        assert len(URL.findall(prep))==1 and not URL.search(body)
        assert not re.search(r'9:16|cinematic 3D animation|Unreal Engine|DOLA STATUS|AFTER DOWNLOAD',body)
        assert 'FORMAT: YOUTUBE 16:9' in body and 'Duration: exactly 30 seconds' in body
        if n>=31:
            assert 'REFERENCE COSTUME AND APPEARANCE:' in body
            assert not re.search(r'consummation|royal first-night|ADULT WARDROBE|glamorous, flattering costume',body)
        cursor=0
        for a,b,action in r['local_shots']:
            assert a==cursor and a<b<=30,(n,a,b,cursor)
            cursor=b
        assert cursor==30
        if i: assert r['previous_ending']==parts[i-1]['local_shots'][-1][2]
        if i<311: assert r['next_opening']==parts[i+1]['local_shots'][0][2]
        for speaker,line in r['spoken_hindi']:
            assert re.search(r'[\u0900-\u097f]',line) and not re.search('[A-Za-z]',line),(n,line)
            utterances.append(line)
        if n in (2,5,6,11): assert not any('rose' in s.lower() for s,_ in r['spoken_hindi'])
        with Image.open(PACKAGE/r['reference_board']) as im:
            assert max(im.size)<=4096 and im.width*im.height<=8_000_000
            im.verify()
        for panel in r['panels']:
            assert (ROOT/panel['source']).is_file()
            assert f"Panel {panel['panel']}: {panel['name']}" in body
    repeated=[line for line,count in Counter(utterances).items() if count>1]
    assert not repeated,repeated
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==report['source_sha256']
    print(f'PASS: 312 prompts, 311 paired handoffs, {len(utterances)} unique Hindi lines, all boards within 8MP/4096px; English source unchanged.')

if __name__=='__main__':
    validate() if '--validate' in sys.argv else main()
