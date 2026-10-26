"""Validate all reference inputs and every adjacent Hindi movie handoff."""

import json
import re
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

from build_reference_handoffs import BASE, FOLDER, PACKAGE, PASTE_MARKER, ROOT, SHOT, URL, git_text


def main():
    manifest = json.loads((PACKAGE / 'Production_Docs/REFERENCE_HANDOFF_MANIFEST.json').read_text(encoding='utf-8'))
    records = manifest['records']
    assert len(records) == 312
    assert manifest['source_commit'] == BASE
    combined_path = PACKAGE / 'Hindi_YouTube_16x9_ALL_312_REFERENCE_HANDOFF_CLEAN.txt'
    blocks = re.split(r'\n\n--------\n\n', combined_path.read_text(encoding='utf-8').strip())
    assert len(blocks) == 312
    sheets = {}
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
        assert 'LANGUAGE: HINDI OUTPUT ONLY' in body
        assert 'Model: Seedance 2.5' in body
        assert 'SPOKEN LANGUAGE: HINDI ONLY' in body
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
        assert unquote(urls[0].split('/main/', 1)[1]) == (
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
        # No dialogue is silently dropped by this reference/continuity update.
        original_speech = re.findall(r'(?m)^DIALOGUE .*$', original)
        output_speech = re.findall(r'(?m)^DIALOGUE .*$', text)
        assert original_speech == output_speech, number
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
          'Hindi 16:9 preserved; original dialogue retained; final closure preserved; '
          'direct Seedance 2.5 image-and-text prompts with no skill dependency; '
          'all image links above the copy heading, no links or status notes below it; '
          'adult wardrobe rules and unchanged child costumes checked.')


if __name__ == '__main__':
    main()
