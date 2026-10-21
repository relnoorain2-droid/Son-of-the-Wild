"""Exclude measured, uniquely identified ready halves from a pending TXT."""

import argparse
import concurrent.futures
import json
import re
from datetime import date
from pathlib import Path

from reconcile_ready_videos import ROOT, probe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--date', default=date.today().isoformat())
    args = parser.parse_args()
    source = args.source.read_text(encoding='utf-8')
    blocks = [b.strip() for b in re.split(r'(?m)^-------\s*$', source) if b.strip()]
    keyed = {}
    for block in blocks:
        match = re.match(r'PART (\d{3})([AB]) ', block)
        if not match:
            raise ValueError('Pending prompt lacks original A/B identifier')
        key = (int(match[1]), match[2])
        if key in keyed:
            raise ValueError(f'Duplicate source key: {key}')
        keyed[key] = block
    paths = sorted(args.folder.rglob('*.mp4'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        videos = list(pool.map(probe, paths))
    ready = {(v['part'], v['half']) for v in videos}
    if any(not h for _, h in ready):
        raise ValueError('This command expects labeled 15-second halves')
    unknown = ready - keyed.keys()
    if unknown:
        raise ValueError(f'Ready clips not in source: {sorted(unknown)}')
    remaining = [block for key, block in keyed.items() if key not in ready]
    text = '\n\n-------\n\n'.join(remaining) + '\n'
    assert len(remaining) == len(blocks) - len(ready)
    assert len(re.findall(r'(?m)^-------$', text)) == max(0, len(remaining) - 1)
    assert all('https://raw.githubusercontent.com/' in b and 'DOWNLOAD AND LOAD REFERENCES' in b
               and 'SPOKEN DIALOGUE FOR THIS HALF ONLY:' in b for b in remaining)
    args.output.write_text(text, encoding='utf-8')
    assert args.source.read_text(encoding='utf-8') == source
    report = {
        'date': args.date, 'scope': 'English 9:16, 15-second A/B clips',
        'verification': 'Actual container duration and dimensions plus original part/half filename; no visual or audio quality review.',
        'source': str(args.source), 'output': str(args.output),
        'previous_pending': len(blocks), 'video_files': len(videos),
        'unique_ready': len(ready), 'duplicate_files': len(videos) - len(ready),
        'remaining_prompts': len(remaining),
        'excluded': [f'{n:03}{h}' for n, h in sorted(ready)],
        'remaining': [f'{n:03}{h}' for n, h in keyed if (n, h) not in ready],
        'videos': [{'filename': Path(v['original_path']).name, 'part': v['part'],
                    'half': v['half'], 'seconds': v['seconds'], 'width': v['width'],
                    'height': v['height']} for v in videos],
    }
    args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('previous_pending', 'video_files', 'unique_ready',
                                           'duplicate_files', 'remaining_prompts')}, indent=2))


if __name__ == '__main__':
    main()
