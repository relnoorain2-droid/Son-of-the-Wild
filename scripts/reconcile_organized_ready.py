"""Reconcile organized original clips, excluding assembled multi-part exports."""

import argparse
import concurrent.futures
import json
import re
from pathlib import Path

from reconcile_ready_videos import probe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--date', required=True)
    parser.add_argument('--pending-ids', required=True)
    args = parser.parse_args()
    requested = args.pending_ids.split()
    if len(requested) != len(set(requested)):
        raise ValueError('Duplicate requested pending IDs')
    source_bytes = args.source.read_bytes()
    source_text = args.source.read_text(encoding='utf-8')
    blocks = [b.strip() for b in re.split(r'(?m)^-------\s*$', source_text) if b.strip()]
    keyed = {}
    for block in blocks:
        match = re.match(r'PART (\d{3}[AB]) ', block)
        if not match or match[1] in keyed:
            raise ValueError('Missing or duplicate source identifier')
        keyed[match[1]] = block
    if set(requested) - keyed.keys():
        raise ValueError('Requested IDs are not a subset of the pending source')

    originals, assemblies = [], []
    for path in sorted(args.folder.rglob('*.mp4')):
        if re.search(r'(?:^|_)part[-_](\d{3})([ab])?(?:---|_)', path.name, re.I):
            originals.append(path)
        elif re.fullmatch(r'part-\d+ two min FULL\.mp4', path.name, re.I):
            assemblies.append(path)
        else:
            raise ValueError(f'Unrecognized video filename: {path}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        videos = list(pool.map(probe, originals))
    covered = set()
    for video in videos:
        for half in video['half'] or 'AB':
            covered.add(f"{video['part']:03}{half}")
    missing = {f'{n:03}{h}' for n in range(1, 313) for h in 'AB'} - covered
    if missing != set(requested):
        raise ValueError(f'Folder differs from requested pending list: '
                         f'extra missing={sorted(missing - set(requested))}, '
                         f'already present={sorted(set(requested) - missing)}')
    remaining = [block for key, block in keyed.items() if key in missing]
    removed = set(keyed) - missing
    if not removed <= covered:
        raise ValueError('An excluded prompt has no ready original clip')
    output = '\n\n-------\n\n'.join(remaining) + '\n'
    assert len(remaining) == len(requested)
    assert len(re.findall(r'(?m)^-------$', output)) == len(remaining) - 1
    assert all('https://raw.githubusercontent.com/' in b
               and 'DOWNLOAD AND LOAD REFERENCES' in b
               and 'SPOKEN DIALOGUE FOR THIS HALF ONLY:' in b for b in remaining)
    report = {
        'date': args.date,
        'scope': 'English 9:16, original story parts 001-312, 15-second A/B prompts',
        'verification': 'Original clip filenames, container durations and dimensions; '
                        'user pending list matches global folder coverage. '
                        'No visual, audio or assembled-edit quality review.',
        'folder': str(args.folder), 'source': str(args.source),
        'output': str(args.output), 'previous_pending': len(blocks),
        'original_video_files': len(videos),
        'full_30s_files': sum(not v['half'] for v in videos),
        'half_15s_files': sum(bool(v['half']) for v in videos),
        'unique_ready_half_equivalents': len(covered),
        'excluded_from_previous_pending': sorted(removed),
        'newly_ready_count': len(removed), 'remaining_prompts': len(remaining),
        'remaining': [key for key in keyed if key in missing],
        'user_pending_list_matches_folder': True,
        'ignored_assembled_exports': [str(p.relative_to(args.folder)) for p in assemblies],
        'videos': videos,
    }
    assert args.source.read_bytes() == source_bytes
    args.output.write_text(output, encoding='utf-8')
    args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in (
        'previous_pending', 'original_video_files', 'full_30s_files',
        'half_15s_files', 'newly_ready_count', 'remaining_prompts',
        'user_pending_list_matches_folder')}, indent=2))


if __name__ == '__main__':
    main()
