import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'ZDola_Combined_Prompts/English_9x16_PENDING_251_CLEAN.txt'
TARGET = ROOT / 'ZDola_Combined_Prompts/English_9x16_PENDING_502_15SEC_CLEAN.txt'
REPORT = ROOT / '06_Production_Docs/ENGLISH_9X16_15SEC_SPLIT_MANIFEST.json'
SEPARATOR = '\n\n-------\n\n'
HEADING = re.compile(r'(?m)^([A-Z][A-Z /0-9():-]*):\s*\n')


def sections(text):
    matches = list(HEADING.finditer(text))
    return [(m.group(1), text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)].strip())
            for i, m in enumerate(matches)]


def timeline(shots):
    duration = sum(b - a for a, b, _ in shots)
    cursor = 0
    result = []
    for i, (a, b, action) in enumerate(shots):
        end = 15 if i == len(shots) - 1 else round(cursor + 15 * (b - a) / duration, 2)
        result.append(f'{cursor:g}-{end:g}s: {action}')
        cursor = end
    return '\n'.join(result)


def dialogue_lines(body):
    # Only extract authored speech, excluding the following delivery instructions.
    result = []
    for match in re.finditer(r'([^\n".]*?):\s*"([^"\n]+)"', body):
        speaker = re.sub(r'^DIALOGUE\s*\d+[^:]*:\s*', '', match.group(1).strip(), flags=re.I)
        result.append((speaker, match.group(2)))
    return result


def main():
    blocks = [b.strip() for b in re.split(r'(?m)^-------\s*$', SOURCE.read_text(encoding='utf-8')) if b.strip()]
    assert len(blocks) == 251
    output, manifest = [], []
    total_lines = 0
    for block in blocks:
        header = re.match(r'PART (\d{3}) - "([^"]+)"', block)
        assert header, block[:100]
        number, title = header.groups()
        parsed = sections(block[header.end():])
        shot_body = next(body for name, body in parsed if name == 'SHOT PLAN')
        shots = [(float(m[1]), float(m[2]), m[3]) for m in
                 re.finditer(r'(?m)^(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s:\s*(.+)$', shot_body)]
        assert 4 <= len(shots) <= 7, number
        cut = min(range(1, len(shots)), key=lambda i: abs(shots[i - 1][1] - 15))
        halves = [shots[:cut], shots[cut:]]
        speech = '\n'.join(body for name, body in parsed if name in ('SPOKEN AUDIO', 'SPOKEN DIALOGUE'))
        lines = dialogue_lines(speech)
        assigned = [[], []]
        for speaker, words in lines:
            key = re.sub(r'\([^)]*\)', '', speaker).strip().lower()
            key = re.sub(r'^(king|prince|captain)\s+', '', key).split()[0]
            scores = []
            for group in halves:
                action = ' '.join(s[2] for s in group).lower()
                scores.append(len(re.findall(r'\b' + re.escape(key) + r'\b', action)))
            selected = 0 if key == 'narrator' or scores[0] > scores[1] else 1
            assigned[selected].append((speaker, words))
        # Keep speech feasible at a measured pace, while retaining every authored line.
        count = lambda group: sum(len(re.findall(r"\b[\w']+\b", words)) for _, words in group)
        for i in (0, 1):
            while count(assigned[i]) > 34 and len(assigned[i]) > 1:
                candidate = assigned[i][-1]
                if count(assigned[1 - i]) + len(candidate[1].split()) > 34:
                    break
                assigned[i].pop()
                assigned[1 - i].append(candidate)
        assert max(map(count, assigned)) <= 40, f'Speech too long: {number}'
        assert sorted(x for group in assigned for x in group) == sorted(lines)
        total_lines += len(lines)
        common = []
        for name, body in parsed:
            if name in ('SHOT PLAN', 'SPOKEN AUDIO', 'SPOKEN DIALOGUE', 'SCENE', 'VIDEO LENGTH', 'FORMAT'):
                continue
            if name == 'VIDEO':
                continue
            body = re.sub(r'[^\n]*Seedance[^\n]*', '', body)
            body = re.sub(r'\b30-second\b', '15-second', body)
            body = re.sub(r'\b30 seconds\b', '15 seconds', body)
            if body.strip():
                common.append(f'{name}:\n{body.strip()}')
        shared = '\n\n'.join(common)
        urls = set(re.findall(r'https://raw\.githubusercontent\.com/\S+', block))
        for i, letter in enumerate('AB'):
            handoff = halves[0][-1][2]
            join = (f'END STATE FOR THE NEXT CLIP:\nComplete this last action before the cut: {handoff}\n'
                    'End on its settled result, without fade, recap or a new event. The next clip begins from that result.'
                    if i == 0 else
                    f'OPENING STATE - DO NOT REPLAY THE ACTION:\nThe preceding clip has ALREADY completed: {handoff}\n'
                    'Begin from the resulting pose, object positions, setting and emotion, then move directly into the shot plan below. '
                    'Do not repeat that action, its dialogue, a title card or an earlier arrival.')
            spoken = '\n'.join(f'{speaker}: "{words}"' for speaker, words in assigned[i]) or 'No spoken dialogue or narration in this half.'
            prompt = (f'PART {number}{letter} - "{title}"\n\n'
                      'VIDEO: Exactly one 15-second English video, vertical 9:16. Use the available supported 15-second video route. '
                      'Do not request a longer duration. Generate only this half.\n\n'
                      f'{shared}\n\n'
                      'A/B CONTINUITY PRIORITY:\nEach half is an independent generation. Download and attach the listed references again. '
                      'Use the same reference face, age stage, fur, hair, costume, damage, lighting and voice across both halves. '
                      'Show only the characters called for by this half\'s shot plan; the repeated reference list also contains continuity guides. '
                      'Do not show an offscreen reference character merely because its URL is included. '
                      'No camera-side reversal, new costume, changed child count, sudden age shift or duplicated character at the join. '
                      'If the tool supports a starting-frame reference and the actual final frame of A is supplied, use it for B; '
                      'otherwise reconstruct the written handoff, without claiming the final frame was loaded.\n\n'
                      f'{join}\n\nSHOT PLAN - LOCAL 0-15 SECOND TIMELINE:\n{timeline(halves[i])}\n\n'
                      f'SPOKEN DIALOGUE FOR THIS HALF ONLY:\n{spoken}\n'
                      'Deliver each listed line once at a natural pause with its speaker visible when lip sync is needed. '
                      'Do not borrow speech from the other half. Text quoted in actions is staging, not permission to add another spoken line. '
                      'Keep action scenes quiet apart from breath and motivated effects.\n')
            if number == '312' and i == 1:
                prompt += '\nThis is the final movie ending: retain the peaceful final fade and complete closure.\n'
            assert urls == set(re.findall(r'https://raw\.githubusercontent\.com/\S+', prompt)), number
            assert not re.search(r'(?m)^\d+(?:\.\d+)?-(?:1[6-9]|[2-9]\d)s:', prompt)
            output.append(prompt.strip())
        manifest.append({'part': number, 'split_after_original_second': halves[0][-1][1],
                         'a_shots': len(halves[0]), 'b_shots': len(halves[1]),
                         'a_dialogue_words': count(assigned[0]), 'b_dialogue_words': count(assigned[1]),
                         'dialogue_lines_preserved': len(lines), 'reference_count': len(urls)})
    assert len(output) == 502
    TARGET.write_text(SEPARATOR.join(output) + '\n', encoding='utf-8')
    REPORT.write_text(json.dumps({'source': SOURCE.name, 'original_parts': 251, 'output_clips': 502,
                                  'duration_per_clip': 15, 'dialogue_lines_preserved': total_lines,
                                  'method': 'Shot-boundary conversion with repeated identity rules and explicit A/B handoff; not a fresh manual rewrite.',
                                  'parts': manifest}, indent=2) + '\n', encoding='utf-8')
    print(f'Created {len(output)} prompts; {total_lines} speech lines preserved; 501 separators.')


if __name__ == '__main__':
    main()
