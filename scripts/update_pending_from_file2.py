"""Filter the previous missing list against measured ready-video coverage."""

import concurrent.futures
import json
import re
from pathlib import Path

from reconcile_ready_videos import FOLDER, ROOT, probe


def blocks(path):
    return [b.strip() for b in re.split(r'(?m)^-------\s*$', path.read_text(encoding='utf-8')) if b.strip()]


def key(block):
    match = re.match(r'PART (\d{3})([AB]) ', block)
    assert match, block[:100]
    return int(match[1]), match[2]


def main():
    directory = ROOT / 'ZDola_Combined_Prompts'
    source = directory / 'English_9x16_MISSING_442_15SEC_2026-10-19_CLEAN.txt'
    original = blocks(source)
    original_keys = [key(b) for b in original]
    assert len(original_keys) == len(set(original_keys)) == 442
    paths = sorted(FOLDER.rglob('*.mp4'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        videos = list(pool.map(probe, paths))
    new = [v for v in videos if (FOLDER / 'file2') in Path(v['original_path']).parents]
    new_keys = [(v['part'], v['half']) for v in new]
    assert len(new) == len(set(new_keys)) == 66
    assert set(new_keys).issubset(original_keys)
    full = {v['part'] for v in videos if not v['half']}
    ready_halves = {(v['part'], v['half']) for v in videos if v['half']}
    ready = ready_halves | {(n, h) for n in full for h in 'AB'}
    missing = {(n, h) for n in range(1, 313) for h in 'AB'} - ready
    remaining = [b for b in original if key(b) not in ready]
    assert {key(b) for b in remaining} == missing
    assert len(remaining) == 376
    outputs = [
        ('English_9x16_MISSING_376_15SEC_CLEAN.txt', remaining),
        ('English_9x16_MISSING_15SEC_BATCH1_300_CLEAN.txt', remaining[:300]),
        ('English_9x16_MISSING_15SEC_BATCH2_76_CLEAN.txt', remaining[300:]),
    ]
    for name, items in outputs:
        text = '\n\n-------\n\n'.join(items) + '\n'
        assert len(re.findall(r'(?m)^-------$', text)) == len(items) - 1
        assert all('DOWNLOAD AND LOAD REFERENCES' in b and 'https://raw.githubusercontent.com/' in b for b in items)
        target = directory / name
        target.write_text(text, encoding='utf-8')
        assert blocks(target) == items
    assert blocks(directory / outputs[1][0]) + blocks(directory / outputs[2][0]) == remaining
    report = {
        'date': '2026-10-19', 'scope': 'English 9:16 only',
        'method': 'Recursive ready-folder inventory, story part suffix, container duration and resolution; not visual quality review.',
        'previous_missing': 442, 'new_file2_videos': len(new), 'new_unique_clips': len(set(new_keys)),
        'removed_from_previous': [f'{n:03}{h}' for n, h in sorted(set(new_keys))],
        'remaining_count': len(remaining), 'remaining': [f'{n:03}{h}' for n, h in sorted(missing)],
        'all_ready_video_files': len(videos), 'full_30s_parts': len(full),
        'complete_15s_pairs': sum(n not in full and all((n, h) in ready_halves for h in 'AB') for n in range(1, 313)),
        'partial_parts': sum(n not in full and sum((n, h) in ready_halves for h in 'AB') == 1 for n in range(1, 313)),
        'outputs': [name for name, _ in outputs],
        'new_files': [{'filename': Path(v['original_path']).name,
                       'part': v['part'], 'half': v['half'], 'duration': v['seconds'],
                       'width': v['width'], 'height': v['height']} for v in new],
    }
    (ROOT / '06_Production_Docs/FILE2_PENDING_RECONCILIATION_2026-10-19.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Verified: 442 minus 66 unique new ready halves = 376 missing prompts.')
    print('Created combined 376, batch 300, batch 76. Prompt text unchanged; no videos renamed or modified.')


if __name__ == '__main__':
    main()
