"""Verify complete numbered coverage, reference preservation and written joins."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'YouTube movie'


def main():
    report = json.loads((PACKAGE / 'Production_Docs/YOUTUBE_624_CONTINUITY_MANIFEST.json').read_text())
    master = ROOT / report['source']
    assert hashlib.sha256(master.read_bytes()).hexdigest() == report['source_sha256']
    sources = [b.strip() for b in re.split(r'(?m)^-------\s*$', master.read_text(encoding='utf-8')) if b.strip()]
    imported = []
    for first, last in ((1, 312), (313, 624)):
        file = PACKAGE / f'English_YouTube_16x9_15SEC_PARTS_{first:03}_{last:03}_CLEAN.txt'
        text = file.read_text(encoding='utf-8')
        items = [b.strip() for b in re.split(r'(?m)^-------\s*$', text) if b.strip()]
        assert len(items) == 312
        assert len(re.findall(r'(?m)^-------$', text)) == 311
        for number, block in enumerate(items, first):
            assert block.startswith(f'PART {number:03} - ')
            individual = PACKAGE / f'Prompts_16x9_15sec/Part_{number:03}_YouTube_15sec.txt'
            assert individual.read_text(encoding='utf-8').strip() == block
        imported.extend(items)
    assert len(imported) == 624
    for number, block in enumerate(imported, 1):
        source = sources[(number - 1) // 2]
        urls = set(re.findall(r'https://raw\.githubusercontent\.com/\S+', block))
        assert urls == set(re.findall(r'https://raw\.githubusercontent\.com/\S+', source))
        for url in urls:
            relative = url.split('/Son-of-the-Wild/main/', 1)[1]
            assert (ROOT / relative).is_file(), (number, relative)
        assert all(s in block for s in ('FRESH-CHAT GENERATION CONTRACT:', 'OPENING STATE FOR THIS FRESH CHAT:',
                                       'ENDING STATE FOR THE FOLLOWING EDIT:', 'DOWNLOAD AND LOAD REFERENCES',
                                       'SPOKEN DIALOGUE FOR THIS PART ONLY:', 'landscape 16:9'))
        assert not re.search(r'9:16|\bvertical\b|\bPART \d{3}[AB]\b|\bA/B\b|30 seconds|30-second', block, re.I)
        timeline = re.search(r'SHOT PLAN - LOCAL 0-15 SECOND TIMELINE:\s*(.*?)(?=\n\nSPOKEN DIALOGUE)', block, re.S)[1]
        shots = list(re.finditer(r'(?m)^(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s:\s*(.+)$', timeline))
        assert float(shots[0][1]) == 0 and float(shots[-1][2]) == 15
        assert all(float(s[2]) > float(s[1]) for s in shots)
        assert all(a[2] == b[1] for a, b in zip(shots, shots[1:]))
        entry = report['parts'][number - 1]
        assert entry['first_action'] == shots[0][3] and entry['final_action'] == shots[-1][3]
        if number > 1:
            preceding = report['parts'][number - 2]['final_action']
            assert entry['previous_final_action'] == preceding
            assert f'The previous cut has already completed this event: {preceding}' in block
        if number < 624:
            assert f'The next numbered clip is PART {number + 1:03}' in block
    assert 'This is the completed movie ending.' in imported[-1]
    skill = (PACKAGE / 'Skill/SKILL.md').read_text(encoding='utf-8')
    assert re.match(r'\A---\nname: [a-z0-9-]+\ndescription: [^\n]+\n---', skill)
    print('PASS: 624 sequential standalone prompts; 2 x 312 imports, 311 separators each; 624 local timelines;')
    print('all source reference sets preserved and present locally; 623 exact written joins including 312/313;')
    print('source master unchanged; final closure at 624; skill frontmatter structure checked.')


if __name__ == '__main__':
    main()
