import argparse
import concurrent.futures
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from split_pending_15s import main as split_prompts

ROOT = Path(__file__).resolve().parents[1]
FOLDER = Path(r'C:\Users\relno\Desktop\reel movie all ready parts')
FFMPEG = ROOT.parent / 'video_tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
MASTER = ROOT / 'ZDola_Combined_Prompts/English_9x16_ALL_312_CLEAN.txt'
AUDIT = ROOT / '06_Production_Docs/READY_INVENTORY_2026-10-19.json'


def probe(path):
    # Read container metadata only; do not decode, transcode or modify the video.
    result = subprocess.run([str(FFMPEG), '-hide_banner', '-i', str(path)],
                            capture_output=True, text=True, errors='replace', timeout=30)
    duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', result.stderr)
    size = re.search(r'Video:.*?\b(\d{3,5})x(\d{3,5})\b', result.stderr)
    if not duration or not size:
        raise ValueError(f'Cannot read video metadata: {path}')
    seconds = int(duration[1]) * 3600 + int(duration[2]) * 60 + float(duration[3])
    match = re.search(r'(?:^|_)part[-_](\d{3})([ab])?(?:---|_)', path.name, re.I)
    if not match:
        raise ValueError(f'Cannot identify story part: {path.name}')
    part, half = int(match[1]), (match[2] or '').upper()
    if not 1 <= part <= 312:
        raise ValueError(f'Invalid part: {path.name}')
    if half and not 14 <= seconds <= 16.5:
        raise ValueError(f'A/B label but duration {seconds}: {path.name}')
    if not half and not 29 <= seconds <= 32:
        raise ValueError(f'Unlabelled or incomplete half, duration {seconds}: {path.name}')
    width, height = int(size[1]), int(size[2])
    if abs(width / height - 9 / 16) > .02:
        raise ValueError(f'Not English reel portrait dimensions: {path.name}: {width}x{height}')
    return {'original_path': str(path), 'part': part, 'half': half,
            'seconds': seconds, 'width': width, 'height': height, 'bytes': path.stat().st_size}


def main(apply=False):
    before_hash = hashlib.sha256(MASTER.read_bytes()).hexdigest()
    source = MASTER.read_text(encoding='utf-8')
    titles = {int(m[1]): m[2] for m in re.finditer(r'(?m)^PART (\d{3}) - "([^"]+)"', source)}
    assert len(titles) == 312
    paths = sorted(FOLDER.rglob('*.mp4'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        videos = list(pool.map(probe, paths))
    full = {v['part'] for v in videos if not v['half']}
    halves = {(v['part'], v['half']) for v in videos if v['half']}
    missing = [(n, h) for n in range(1, 313) for h in 'AB'
               if n not in full and (n, h) not in halves]
    entirely_missing = [n for n in range(1, 313) if n not in full
                        and all((n, h) not in halves for h in 'AB')]
    partial = [n for n in range(1, 313) if n not in full
               and sum((n, h) in halves for h in 'AB') == 1]
    paired = [n for n in range(1, 313) if n not in full
              and all((n, h) in halves for h in 'AB')]
    reserved = set()
    for v in videos:
        slug = re.sub(r'[^a-z0-9]+', '-', titles[v['part']].lower()).strip('-')
        stem = f"{v['part']:03}{v['half']}_part-{v['part']:03}{v['half']}---{slug}_{'15s' if v['half'] else '30s'}"
        old = Path(v['original_path'])
        target = old.with_name(stem + '.mp4')
        take = 2
        while str(target).lower() in reserved or (target.exists() and target != old):
            target = old.with_name(f'{stem}_take-{take:02}.mp4')
            take += 1
        assert target.parent == old.parent and target.resolve().is_relative_to(FOLDER.resolve())
        reserved.add(str(target).lower())
        v['renamed_path'] = str(target)
    summary = {'video_files': len(videos), 'full_30s_parts': len(full),
               'half_15s_files': sum(bool(v['half']) for v in videos),
               'paired_15s_parts': len(paired), 'partial_parts': len(partial),
               'entirely_missing_parts': len(entirely_missing), 'missing_15s_prompts': len(missing),
               'filenames_to_change': sum(v['original_path'] != v['renamed_path'] for v in videos)}
    print(json.dumps({'summary': summary, 'partial_parts': partial,
                      'full_parts': sorted(full)}, indent=2))
    if not apply:
        return
    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        split_prompts(MASTER, temp / 'all.txt', temp / 'manifest.json')
        all_blocks = [b.strip() for b in re.split(r'(?m)^-------\s*$', (temp / 'all.txt').read_text()) if b.strip()]
        keyed = {}
        for b in all_blocks:
            m = re.match(r'PART (\d{3})([AB]) ', b)
            keyed[(int(m[1]), m[2])] = b
        # Existing A/B prompt text takes precedence so a missing half still matches its generated partner.
        existing = ROOT / 'ZDola_Combined_Prompts/English_9x16_PENDING_502_15SEC_CLEAN.txt'
        for b in re.split(r'(?m)^-------\s*$', existing.read_text(encoding='utf-8')):
            m = re.match(r'PART (\d{3})([AB]) ', b.strip())
            if m:
                keyed[(int(m[1]), m[2])] = b.strip()
        pending_text = '\n\n-------\n\n'.join(keyed[key] for key in missing) + '\n'
    target = ROOT / f'ZDola_Combined_Prompts/English_9x16_MISSING_{len(missing)}_15SEC_2026-10-19_CLEAN.txt'
    target.write_text(pending_text, encoding='utf-8')
    for v in videos:
        old, new = Path(v['original_path']), Path(v['renamed_path'])
        if old != new:
            old.rename(new)
        assert new.stat().st_size == v['bytes']
    data = {'date': '2026-10-19', 'folder': str(FOLDER), 'scope': 'English vertical 9:16 only',
            'verification': 'Filename identity, container duration and resolution; no visual or audio quality review.',
            'summary': summary, 'full_parts': sorted(full), 'paired_parts': paired,
            'partial_parts': partial, 'entirely_missing_parts': entirely_missing,
            'missing_clips': [f'{n:03}{h}' for n, h in missing], 'videos': videos,
            'output_file': str(target.relative_to(ROOT))}
    AUDIT.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    assert hashlib.sha256(MASTER.read_bytes()).hexdigest() == before_hash
    assert len(re.findall(r'(?m)^PART \d{3}[AB] ', pending_text)) == len(missing)
    assert len(re.findall(r'(?m)^-------$', pending_text)) == len(missing) - 1
    print(f'Created {target.name}; filenames normalized; master unchanged.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    main(parser.parse_args().apply)
