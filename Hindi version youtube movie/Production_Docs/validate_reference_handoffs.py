"""Validate all reference inputs and every adjacent Hindi movie handoff."""

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image

from build_reference_handoffs import (BASE, FOLDER, MAX_REFERENCE_PIXELS, MAX_REFERENCE_SIDE,
                                    PACKAGE, PASTE_MARKER, ROOT, SHOT, URL, git_text,
                                    reference_size)
from hindi_dialogue_catalog import NARRATION
from localize_hindi import DEVANAGARI, LATIN, SPEECH, VOICES, translate_line, validate_native_payloads


def main():
    manifest = json.loads((PACKAGE / 'Production_Docs/REFERENCE_HANDOFF_MANIFEST.json').read_text(encoding='utf-8'))
    records = manifest['records']
    assert len(records) == 312
    assert manifest['source_commit'] == BASE
    assert manifest['reference_image_max_pixels'] == MAX_REFERENCE_PIXELS
    assert manifest['reference_image_max_side'] == MAX_REFERENCE_SIDE
    assert reference_size(3136, 3586) == (2640, 3024)
    for original in ((3136, 3586), (4176, 4742), (4176, 1274), (1024, 1024)):
        width, height = reference_size(*original)
        assert max(width, height) <= MAX_REFERENCE_SIDE
        assert width * height <= MAX_REFERENCE_PIXELS
        assert width <= original[0] and height <= original[1]
    combined_path = PACKAGE / 'Hindi_YouTube_16x9_ALL_312_REFERENCE_HANDOFF_CLEAN.txt'
    blocks = re.split(r'\n\n--------\n\n', combined_path.read_text(encoding='utf-8').strip())
    assert len(blocks) == 312
    sheets = {}
    speech_count = quoted_count = 0
    for i, record in enumerate(records):
        number = i + 1
        assert record['part'] == number
        path = FOLDER / f'Part_{number:03}_Dola_URL.txt'
        text = path.read_text(encoding='utf-8')
        original = git_text(path)
        preparation, body = text.split(PASTE_MARKER + '\n', 1)
        assert blocks[i].strip() == text.strip()
        assert 'DOLA STATUS' not in blocks[i]
        assert 'HINDI YOUTUBE TITLE / DESCRIPTION AFTER DOWNLOAD' not in blocks[i]
        assert 'FORMAT: YOUTUBE 16:9' in body
        assert 'Duration: exactly 30 seconds' in body
        assert 'LANGUAGE: HINDI VOICES; ENGLISH INSTRUCTIONS' in body
        assert 'Model: Seedance 2.5' in body
        assert 'SPOKEN LANGUAGE: HINDI ONLY' in body
        assert 'already written in Hindi' in body
        assert 'Translate every' not in body
        assert 'young emotional American woman' not in body
        assert record['speech_language'] == 'Hindi'
        assert record['speech_script'] == 'Devanagari'
        assert record['authored_narrator_line'] == NARRATION[number]['line']
        assert record['authored_narrator_line'] in body
        quoted_count += validate_native_payloads(body, record['title'])
        assert body.count('ADULT WARDROBE AND DISTINCT IDENTITIES:') == 1
        assert 'Children retain their original age-appropriate clothes.' in body
        assert record['wardrobe']['scope'].startswith('Adult human women only')
        assert 'All clothing is opaque and fully lined.' in body
        for style in record['wardrobe']['styles']:
            assert style in body
        assert not re.search(r'Use active skill|Dola|SKILL\.md|skill file', body, re.I)
        assert not re.search(r'https?://|DOLA STATUS|AFTER DOWNLOAD', body)
        assert body.count('OPENING HANDOFF IN:') == 1
        assert body.count('ENDING HANDOFF OUT:') == 1
        assert 'OPENING CONTINUITY LOCK:' not in body
        assert 'REFERENCE IMAGE STRICT LOCK:' not in body
        assert 'DIRECT GITHUB RAW - DOLA CAN ACCESS' not in body
        assert 'SUSPENSE HOOK LOCK:' not in body
        urls = URL.findall(preparation)
        assert len(urls) == 1, (number, urls)
        assert unquote(urlsplit(urls[0]).path.split('/main/', 1)[1]) == (
            PACKAGE / record['reference_board']).relative_to(ROOT).as_posix()
        assert record['image_input_count_required'] == 1
        assert record['image_input_count_with_handoff'] <= 2
        assert record['max_image_inputs'] == 3
        assert 'at most THREE images' in body
        assert not re.search(r'https?://\S*EndFrame', text)
        if number > 1:
            assert record['incoming'] == records[i - 1]['outgoing'], number
            assert record['incoming']['id'] == f'CUT_{number - 1:03}_{number:03}'
            assert record['incoming']['completed_event'] in body
        if number < 312:
            assert record['outgoing']['next'] == number + 1
            assert record['outgoing']['next_action'] in body
        else:
            assert record['outgoing'] is None
            assert 'No next-part hook or new threat' in body
        # Preserve every speech slot (including indented montage speech), but
        # require literal Hindi rather than asking the generator to translate.
        original_speech = list(SPEECH.finditer(original))
        output_speech = list(SPEECH.finditer(body))
        assert len(original_speech) == len(output_speech), number
        assert len(output_speech) == len(re.findall(r'(?m)^\s*DIALOGUE ', body)), number
        for source, output in zip(original_speech, output_speech):
            assert (source['start'], source['end']) == (output['start'], output['end']), number
            assert output['speaker'] == source['speaker'], (number, output[0])
            payload = output['payload'].strip('"')
            assert DEVANAGARI.search(payload) and not LATIN.search(payload), (number, output[0])
            assert output['voice'] == VOICES[source['speaker']]
            assert not DEVANAGARI.search(output['voice'])
            expected_source = re.search(r'"([^"\n]+)"', source['payload'])[1]
            expected = translate_line(expected_source, number, record['title'], source['speaker'],
                                      int(source['end']) - int(source['start']))
            assert payload == expected, (number, output[0])
            assert len(payload.split()) <= 3 * (int(output['end']) - int(output['start'])), (number, output[0])
        speech_count += len(output_speech)
        cursor = 0
        for shot in SHOT.finditer(body):
            start, end = int(shot[1]), int(shot[2])
            assert start <= cursor and start < end <= 30, (number, cursor, shot[0])
            cursor = max(cursor, end)
        assert cursor == 30, number
        key = record['reference_board']
        if key not in sheets:
            sheet_path = PACKAGE / key
            assert sheet_path.stat().st_size < 20_000_000
            with Image.open(sheet_path) as image:
                assert max(image.size) <= MAX_REFERENCE_SIDE, (key, image.size)
                assert image.width * image.height <= MAX_REFERENCE_PIXELS, (key, image.size)
                assert image.size == (record['reference_image_width'], record['reference_image_height'])
                image.verify()
            sheets[key] = record['panels']
        assert sheets[key] == record['panels']
        for panel in record['panels']:
            assert f"Panel {panel['panel']}: {panel['name']}" in body
            assert (ROOT / panel['source']).is_file()
        original_refs = {unquote(u.split('/main/', 1)[1]) for u in URL.findall(original)}
        assert original_refs <= {p['source'] for p in record['panels']}
    assert len(sheets) == manifest['unique_labelled_reference_sheets']
    assert len(sheets) == len(list((PACKAGE / 'Reference_Sheets').glob('*.jpg')))
    print(f'PASS: 312 individual prompts; 312 clean combined blocks; {len(sheets)} valid named JPG boards; '
          '311 matching boundaries; one required image per part, at most three; all local timelines cover 0-30s; '
          f'Hindi 16:9 preserved; {speech_count} native Hindi speech slots and {quoted_count} Hindi voice '
          'payloads checked; instructions, speaker labels and screen text remain English; source speech timings retained; '
          'final closure preserved; '
          'direct Seedance 2.5 image-and-text prompts with no skill dependency; '
          'all image links above the copy heading, no links or status notes below it; '
          'adult wardrobe rules and unchanged child costumes checked; '
          'all boards at most 8.0 MP and 4096 px on the longest side.')


if __name__ == '__main__':
    main()
