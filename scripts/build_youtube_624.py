"""Build sequential, standalone English widescreen clips from the revised story."""

import hashlib
import json
import re
import tempfile
from collections import Counter
from pathlib import Path

from split_pending_15s import ROOT, SEPARATOR, main as split_story

MASTER = ROOT / 'ZDola_Combined_Prompts/English_9x16_ALL_312_CLEAN.txt'
YOUTUBE = ROOT / 'YouTube movie'


def original_numbering(text):
    # Translate old story-number references before assigning the new public numbering.
    text = re.sub(r'\bParts?\s+(\d{3})[-\u2013](\d{3})',
                  lambda m: f'Parts {2 * int(m[1]) - 1:03}-{2 * int(m[2]):03}', text)
    text = re.sub(r'\bPart\s+(\d{3})(?!\d)',
                  lambda m: f'the story sequence in clips {2 * int(m[1]) - 1:03}-{2 * int(m[1]):03}', text)
    return text


def widescreen(text):
    text = text.replace('9:16', '16:9').replace('VERTICAL', 'LANDSCAPE')
    text = re.sub(r'\bvertical\b', 'landscape', text, flags=re.I)
    text = text.replace('vertical/reels', 'widescreen')
    return original_numbering(text)


def local_shots(block):
    match = re.search(r'SHOT PLAN - LOCAL 0-15 SECOND TIMELINE:\s*(.*?)(?=\n\nSPOKEN DIALOGUE)', block, re.S)
    assert match
    return list(re.finditer(r'(?m)^(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s:\s*(.+)$', match[1]))


def main():
    source_bytes = MASTER.read_bytes()
    originals = [b.strip() for b in re.split(r'(?m)^-------\s*$', source_bytes.decode('utf-8')) if b.strip()]
    assert len(originals) == 312
    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        split_story(MASTER, temp / 'split.txt', temp / 'split.json')
        split = [b.strip() for b in re.split(r'(?m)^-------\s*$', (temp / 'split.txt').read_text()) if b.strip()]
        mapping = json.loads((temp / 'split.json').read_text())
    assert len(split) == 624
    converted, report = [], []
    for index, block in enumerate(split):
        number = index + 1
        source_number = index // 2 + 1
        source_block = originals[source_number - 1]
        title = re.match(r'PART \d{3}[AB] - "([^"]+)"', block)[1]
        block = re.sub(r'\APART \d{3}[AB] - "[^"]+"', f'PART {number:03} - "{title}"', block)
        block = widescreen(block)
        # Replace the old within-pair handoff; provide a join for every sequential cut.
        block = re.sub(r'\n\nA/B CONTINUITY PRIORITY:.*?(?=\n\nSHOT PLAN - LOCAL)', '', block, flags=re.S)
        block = block.replace('Generate only this half.', 'Generate only this numbered part.')
        block = block.replace('SPOKEN DIALOGUE FOR THIS HALF ONLY:', 'SPOKEN DIALOGUE FOR THIS PART ONLY:')
        block = block.replace('No spoken dialogue or narration in this half.', 'No spoken dialogue or narration in this part.')
        block = block.replace('Do not borrow speech from the other half.', 'Do not add speech from any other part.')
        shots = local_shots(block.replace('SPOKEN DIALOGUE FOR THIS PART ONLY:', 'SPOKEN DIALOGUE'))
        first_action = shots[0][3]
        final_action = shots[-1][3]
        previous_action = widescreen(local_shots(split[index - 1])[-1][3]) if index else None
        urls = re.findall(r'https://raw\.githubusercontent\.com/\S+', block)
        mapping_lines = '\n'.join(f'- {url.rsplit("/", 1)[-1]}: {url.split("/")[-2]}' for url in dict.fromkeys(urls))
        scene = re.search(r'(?s)\nSCENE:\s*(.*?)(?=\n\n[A-Z][A-Z /-]+:)', source_block)
        context = widescreen(scene[1].strip()) if scene else ''
        opening = (f'The previous cut has already completed this event: {previous_action}\n'
                   'This is setup context only. Do not replay the completed action, dialogue or arrival. '
                   'If the first shot remains in that scene, reconstruct its resulting pose, costume, wetness, '
                   'injuries, props, lighting and screen positions, then continue the next action. '
                   'If the written first shot explicitly cuts location, time, memory or viewpoint, make that motivated cut; '
                   'do not force the previous scene or its offscreen characters into the new shot.'
                   if previous_action else
                   'This is the movie opening. Establish the castle and title exactly as the first shot specifies; no recap.')
        closing = (f'Complete this event by the end of this part: {final_action}\n'
                   f'The next numbered clip is PART {number + 1:03}. Leave a clean edit point with stable faces, '
                   'character positions and props. No extra cliffhanger, end card, flash, silent black tail or unrelated fade. '
                   'Allow a fade only when the written shot explicitly changes time or enters a memory. '
                   'Finish the listed speech before the cut; do not begin the next part\'s line.'
                   if number < 624 else
                   f'Final event: {final_action}\nThis is the completed movie ending. Preserve the peaceful fade to black; '
                   'no new threat, next-part hook, recap or promotional card.')
        fresh = ('FRESH-CHAT GENERATION CONTRACT:\n'
                 'This request is complete by itself. The generator has no memory of another chat, video or project. '
                 'Do not ask for the previous prompt and do not invent missing continuity. Download, inspect and attach '
                 'the images listed below before rendering. Use only this part\'s local shot plan and spoken lines; '
                 'the context and reference mappings explain identity and setup, not additional scenes to render. '
                 'If reference-image attachment is unavailable, report it and stop instead of silently generating text-only.\n\n'
                 'WIDESCREEN COMPOSITION:\n'
                 'English YouTube movie, exactly 15 seconds, landscape 16:9. Compose for a 1920x1080 canvas when supported; '
                 'otherwise use the selected native 16:9 resolution without cropping a portrait video. '
                 'Use left/right space to establish geography, with balanced medium two-shots and readable action. '
                 'Keep heads, hands, feet and important props inside widescreen safe margins. No portrait framing or letterboxed phone footage.\n\n'
                 f'LOCAL CAST AND LOCATION REFERENCE MAPPING:\n{mapping_lines}\n\n'
                 + (f'SCENE SETUP CONTEXT:\n{context}\n\n' if context else '')
                 + f'OPENING STATE FOR THIS FRESH CHAT:\n{opening}\n'
                 + f'First render action for this part: {first_action}\n\n'
                 + 'IDENTITY AT THE EDIT:\n'
                 'Match the same reference face, age stage, hair, fur pattern, clothes, scale and established voice throughout '
                 'this numbered part. Reference roles listed here include continuity guides: only show the characters requested '
                 'by the local shot plan. Location-reference background figures are not the cast. Do not duplicate a child, '
                 'swap Lily with the earlier red-haired bride, turn Frost into a dog or human, change his growth stage, or '
                 'change creature counts between cuts. No unmotivated camera-side reversal. '
                 'For same-scene joins retain the last established screen direction and eyelines. '
                 'If an actual previous final-frame image is supplied and the selected route supports it, use it as the '
                 'opening-frame reference alongside the identity references. This prompt itself does not attach that frame, '
                 'so never claim it has been loaded when it has not.\n\n'
                 f'ENDING STATE FOR THE FOLLOWING EDIT:\n{closing}\n\n'
                 'AUDIO AT THE EDIT:\n'
                 'Same-scene ambience and score remain restrained and compatible across adjoining clips; no fresh music intro '
                 'or outro sting on every part. An intentional location/time change may change ambience. '
                 'Only the local dialogue section authorizes speech. Keep natural pauses and do not repeat a spoken line '
                 'because it appears in the setup context. Action scenes remain quiet when no line is written.\n\n')
        # Put all fresh-chat setup immediately after the visible part name.
        header, rest = block.split('\n\n', 1)
        result = f'{header}\n\n{fresh}{rest}'
        forbidden = re.search(r'\bPART \d{3}[AB]\b|\bA/B\b|9:16|\bvertical\b|30-second|30 seconds', result, re.I)
        assert not forbidden, (number, forbidden[0] if forbidden else '')
        assert set(urls) == set(re.findall(r'https://raw\.githubusercontent\.com/\S+', result))
        converted.append(result)
        report.append({'youtube_part': number, 'source_story_part': source_number,
                       'source_half': 'first' if index % 2 == 0 else 'second',
                       'title': title, 'first_action': first_action, 'final_action': final_action,
                       'previous_final_action': previous_action, 'references': len(set(urls))})
    target_dir = YOUTUBE / 'Prompts_16x9_15sec'
    target_dir.mkdir(exist_ok=True)
    for number, prompt in enumerate(converted, 1):
        (target_dir / f'Part_{number:03}_YouTube_15sec.txt').write_text(prompt + '\n', encoding='utf-8')
    for first, last in ((1, 312), (313, 624)):
        (YOUTUBE / f'English_YouTube_16x9_15SEC_PARTS_{first:03}_{last:03}_CLEAN.txt').write_text(
            SEPARATOR.join(converted[first - 1:last]) + '\n', encoding='utf-8')
    source_speech = Counter(re.findall(r'(?m)^[^\n:]+:\s*"([^"\n]+)"', '\n'.join(
        re.search(r'SPOKEN DIALOGUE FOR THIS HALF ONLY:\n(.*?)(?=\nDeliver)', b, re.S)[1] for b in split)))
    output_speech = Counter(re.findall(r'(?m)^[^\n:]+:\s*"([^"\n]+)"', '\n'.join(
        re.search(r'SPOKEN DIALOGUE FOR THIS PART ONLY:\n(.*?)(?=\nDeliver)', b, re.S)[1] for b in converted)))
    assert source_speech == output_speech
    assert MASTER.read_bytes() == source_bytes
    data = {'source': str(MASTER.relative_to(ROOT)), 'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
            'date': '2026-10-20', 'format': 'English landscape 16:9, 15 seconds',
            'source_parts': 312, 'youtube_parts': 624, 'combined_files': 2, 'prompts_per_file': 312,
            'source_dialogue_lines_preserved': mapping['dialogue_lines_preserved'],
            'method': 'Revised-story shot-boundary conversion, sequential renumbering, explicit every-cut handoffs and fresh-chat setup; not a new manual story rewrite or rendered-video verification.',
            'parts': report}
    (YOUTUBE / 'Production_Docs/YOUTUBE_624_CONTINUITY_MANIFEST.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(f'Built 624 individual landscape prompts and two 312-prompt files; {mapping["dialogue_lines_preserved"]} speech lines preserved.')


if __name__ == '__main__':
    main()
