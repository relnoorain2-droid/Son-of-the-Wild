"""Build labelled reference sheets and independent Hindi 30-second prompts.

Input is the committed Hindi package, so rebuilding never stacks prompt additions.
Only this Hindi YouTube folder is written. Original image pixels remain unchanged.
"""

import csv
import hashlib
import io
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, unquote

from PIL import Image, ImageDraw, ImageFont, ImageOps

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
BASE = '885eb6afd26a0cd528f8592db8dc7fb18a4e4aeb'
RAW = 'https://raw.githubusercontent.com/relnoorain2-droid/Son-of-the-Wild/main/'
FOLDER = PACKAGE / 'Prompts_16x9_Hindi'
SHEETS = PACKAGE / 'Reference_Sheets'
TITLE = re.compile(r'PART (\d{3}) - "([^"]+)"')
SHOT = re.compile(r'(?m)^(\d+)[-\u2013](\d+)s:\s*(.+)$')
URL = re.compile(r'https://raw\.githubusercontent\.com/[^\s]+')

NAMES = {
    'C01': 'Lily Carter - everyday clothes', 'C02': 'King Magnus Thorne',
    'C03': 'Prince Damian Thorne', 'C04': 'Bruno - living',
    'C05': 'Frost - adult, before full power', 'C06': 'Elder Orin - ancestor',
    'S01': 'Grace Carter - Lily\'s mother', 'S02': 'Martha Hayes',
    'S03': 'Hank Miller', 'S04': 'Old Joe Whitaker', 'S05': 'Tommy Miller - child',
    'S06': 'Sarah Miller - child', 'S07': 'Captain Vex',
    'S08': 'Kingdom guards', 'S09': 'Previous brides - adult women',
    'S10': 'Cedar Hollow villagers', 'S11': 'Rose - castle maid',
    'V01': 'Lily - wedding outfit', 'V02': 'Lily - forest outfit',
    'V03': 'Lily - pregnant', 'V04': 'Lily - young mother',
    'V05': 'Frost - baby', 'V06': 'Frost - child', 'V07': 'Frost - teenager',
    'V08': 'Frost - powered adult', 'V09': 'Bruno - spirit only',
    'V10': 'Damian - battle armor', 'V11': 'Magnus - battle armor',
    'V12': 'Tommy Miller - adult', 'V13': 'Sarah Miller - adult',
    'V14': 'Grace Carter - older',
}

# These are explicit shot changes in the authored story. All other changes still
# follow their written opening; a previous screenshot must never override it.
TRANSITIONS = {
    18: 'ONE MONTH LATER', 37: 'CUTAWAY TO THE CASTLE TRACKERS',
    42: 'EARLIER FOREST ENCOUNTER - MEMORY INSERT',
    48: 'LATER, IN THE SAME FOREST REFUGE',
    56: 'CUTAWAY TO DAMIAN AND THE HUNT',
    57: 'EARLIER HAPPY FOREST MEMORY - BEFORE THE APPROACHING HUNT',
    60: 'LATER, AFTER THE WATERFALL ENCOUNTER',
    67: 'ANOTHER DAY IN THE FOREST', 69: 'ANOTHER MORNING IN THE FOREST',
    74: 'LATER, UNDER THE STARS', 75: 'WEEKS LATER',
    76: 'EARLIER MOONLIT MEMORY - BEFORE THE PREGNANCY REVEAL',
    79: 'RETURN TO THE PREGNANCY TIMELINE',
    81: 'EARLIER PREGNANCY REVEAL - MEMORY INSERT',
    84: 'CUTAWAY TO THE KING\'S SCOUT',
    87: 'EARLIER: THE KING LOCATES THE CAVE - LEAD-UP TO THE SAME ATTACK',
    95: 'A SEPARATE MOMENT DURING THE SAME FOREST BATTLE',
    105: 'LATER, FAR DOWNRIVER NEAR CEDAR HOLLOW',
    111: 'CUTAWAY TO THE TAX WAGON', 112: 'MONTHS PASS - WINTER',
    113: 'LILY\'S DREAM OF GRACE',
    114: 'EARLIER RIVERBANK MEMORY - BEFORE THE CABIN WAS REPAIRED',
    115: 'CONTINUATION OF THE EARLIER ARRIVAL MEMORY',
    116: 'CONTINUATION OF THE EARLIER SURVIVAL MEMORY',
    117: 'CONTINUATION OF THE EARLIER CABIN MEMORY',
    118: 'CONTINUATION OF THE EARLIER FIRST-VISIT MEMORY',
    119: 'CONTINUATION OF THE EARLIER VILLAGE-ARRIVAL MEMORY',
    120: 'NEXT MORNING IN THE ARRIVAL MEMORY',
    121: 'CONTINUATION OF THE EARLIER VILLAGE MEMORY',
    122: 'RETURN TO THE LATER PREGNANCY TIMELINE',
    124: 'LATER, BEFORE LABOR', 130: 'NEXT MORNING, INSIDE THE CABIN',
    133: 'LATER, BABY BATH TIME', 134: 'ANOTHER MORNING IN THE CABIN',
    138: 'ANOTHER VISIT TO THE CABIN', 142: 'LATER, FROST\'S CHILDHOOD',
    149: 'ANOTHER DAY IN FROST\'S CHILDHOOD',
    157: 'THANKSGIVING', 158: 'WINTER', 165: 'HALLOWEEN',
    169: 'FOURTH OF JULY', 170: 'LATER, FROST\'S TEEN YEARS',
    180: 'A LATER BIRTHDAY', 184: 'LATER, FROST\'S ADULT YEARS',
    196: 'EARLIER, BEFORE THE RAID - RIVER OUTING',
    197: 'CUTAWAY TO THE RAID WHILE LILY AND FROST ARE AWAY',
    200: 'CONTINUATION OF THE SAME RETURN TO THE RUINED VILLAGE',
    202: 'LATER, LILY TELLS THE TRUTH',
    211: 'LATER THAT NIGHT, THE TOWN MEETING IN THE CHURCH',
    212: 'PREPARATIONS BEFORE THE NEXT FULL MOON',
    213: 'THE NEXT FULL MOON', 221: 'CUTAWAY TO VEX\'S REPORT',
    222: 'RETURN TO LILY\'S SEARCH FOR FROST',
    224: 'MEMORY OF THE RECENT DEFEAT',
    225: 'RETURN TO FROST\'S RECOVERY',
    230: 'SPIRIT VISION DURING THE QUEST',
    233: 'VISION OF THE POWER PATH - FULL PHYSICAL TRANSFER IS IN PART 254',
    234: 'RETURN TO OLD JOE\'S TRIALS MAP - BEFORE THE FULL POWER RITUAL',
    236: 'TRAINING OVER SUCCESSIVE DAYS', 243: 'LATER, AT THUNDER PEAK',
    247: 'LATER, AT MIRROR LAKE',
    249: 'UNDERWATER VISION - NOT A SECOND PHYSICAL FROST',
    255: 'LATER, POWER TRAINING', 263: 'LATER, ALLIED PLANNING WITH ROSE',
    264: 'LATER, LILY\'S OLD TOWN', 269: 'LATER, BEFORE THE MARCH',
    271: 'THE MARCH TO THORNE CASTLE', 272: 'MORNING, OUTSIDE THE CASTLE',
    274: 'CUTAWAY TO THE CASTLE STABLE DRAGONS',
    275: 'RETURN TO THE MAIN BATTLEFIELD',
    278: 'CUTAWAY TO ROSE\'S SECRET TUNNEL',
    279: 'RETURN TO FROST ON THE BATTLEFIELD',
    282: 'RETURN TO THE SAME TUNNEL RESCUE',
    283: 'RETURN TO THE MAMMOTH BATTLE',
    286: 'CUTAWAY TO DAMIAN AND LILY INSIDE THE CASTLE',
    288: 'RETURN TO THE FROST AND DRAGON BATTLE',
    289: 'EARLIER RUBBLE-ROOM DISCOVERY - MEMORY INSERT',
    290: 'RETURN TO THE TUNNEL TEAM FREEING DRAGONS',
    291: 'RETURN TO LILY AND DAMIAN', 294: 'RETURN TO THE AERIAL BATTLE',
    300: 'FROST\'S MEMORY DURING HIS FALL',
    301: 'EARLIER AERIAL BATTLE - MEMORY INSERT BEFORE THE CRYSTAL BROKE',
    302: 'EARLIER KING\'S ISOLATION - MEMORY INSERT',
    303: 'RETURN TO THE PRESENT FALL AND RESCUE',
    306: 'LATER, AFTER THE KING\'S FALL',
    307: 'RETURN TO THE FREED COURTYARD IN DAYLIGHT',
    308: 'LATER, GRACE\'S HOME', 310: 'LATER, THE VICTORY CELEBRATION',
    312: 'LATER THAT NIGHT, THE HILL ABOVE THE CELEBRATION',
}

for first, last, note in (
    (43, 47, 'CONTINUATION OF THE EARLIER FOREST ENCOUNTER MEMORY'),
    (77, 78, 'CONTINUATION OF THE EARLIER MOONLIT COURTSHIP MEMORY'),
    (82, 83, 'CONTINUATION OF THE EARLIER PREGNANCY MEMORY'),
    (88, 89, 'CONTINUATION OF THE LEAD-UP TO THE SAME FOREST ATTACK'),
):
    for number in range(first, last + 1):
        TRANSITIONS.setdefault(number, note)


def git_text(path):
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(['git', 'show', f'{BASE}:{relative}'], cwd=ROOT).decode('utf-8-sig')


def clean_action(value):
    return re.sub(r'^Build into the hook:\s*', '', value).strip()


def parse(path):
    text = git_text(path)
    match = TITLE.search(text)
    shots = [(int(m[1]), int(m[2]), clean_action(m[3])) for m in SHOT.finditer(text)]
    if int(match[1]) == 227:
        shots.insert(1, (3, 8, 'Old Joe holds Lily\'s gaze as she listens; Frost turns toward him '
                        'and the blue light begins to gather for the legend vision.'))
    assert shots and shots[0][0] == 0 and shots[-1][1] == 30, path.name
    scene = re.search(r'(?m)^Scene:\s*(.+)$', text)
    # Older prompts place their scene description immediately below LOOK LOCK.
    if scene:
        context = scene[1]
    else:
        preamble = text[:SHOT.search(text).start()]
        look = re.search(r'(?m)^LOOK LOCK:.*\n', preamble)
        context = preamble[look.end():].strip() if look else ''
    first = shots[0][2]
    if first.startswith('Start with a strong immediate visual hook'):
        first = context
    last_frame = re.search(r'(?m)^Final frame:\s*(.+)$', text)
    ending = last_frame[1] if last_frame else shots[-1][2]
    refs = list(dict.fromkeys(URL.findall(text)))
    local_refs = []
    for url in refs:
        relative = unquote(url.split('/main/', 1)[1])
        image = ROOT / relative
        assert image.is_file(), image
        local_refs.append(relative)
    # A foreground character in a handoff needs an identity panel as well.
    additions = {'Captain Vex': 'S07_CaptainVex_FULL.png',
                 'Martha': 'S02_MarthaHayes_FULL.png', 'Hank': 'S03_HankMiller_FULL.png',
                 'Old Joe': 'S04_OldJoeWhitaker_FULL.png', 'Rose': 'S11_Rose_FULL.png'}
    action = ' '.join([context, *[s[2] for s in shots], ending])
    for name, filename in additions.items():
        if name in action and not any(Path(r).name == filename for r in local_refs):
            candidates = list((ROOT / 'Characters_Dola_1024').rglob(filename))
            assert len(candidates) == 1
            local_refs.append(candidates[0].relative_to(ROOT).as_posix())
    return {'number': int(match[1]), 'title': match[2], 'path': path, 'source': text,
            'source_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'shots': shots, 'first': first, 'ending': ending, 'context': context,
            'references': local_refs}


def label(relative):
    stem = Path(relative).stem
    code = stem.split('_')[0]
    name = NAMES.get(code)
    if not name:
        name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', stem.split('_', 1)[1])
    if stem.endswith('_FACE'):
        name += ' - face detail'
    return name


def font(size):
    for candidate in ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/segoeui.ttf'):
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)


def sheet(references, target, refresh=False):
    panels = [{'panel': index + 1, 'name': label(relative), 'source': relative}
              for index, relative in enumerate(references)]
    if target.is_file() and not refresh and '--refresh-sheets' not in sys.argv:
        return panels
    cell, header, gap, top = 1024, 116, 16, 118
    cols = min(4, max(1, math.ceil(math.sqrt(len(references)))))
    rows = math.ceil(len(references) / cols)
    canvas = Image.new('RGB', (gap + cols * (cell + gap), top + rows * (cell + header + gap)), '#e5e7eb')
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 18), 'FROST: SON OF THE WILD - REFERENCE BOARD', font=font(34), fill='#111827')
    draw.text((24, 65), 'Read names above each panel. Use identities and designs; create the movie scene fresh.', font=font(26), fill='#111827')
    panels = []
    for index, relative in enumerate(references):
        col, row = index % cols, index // cols
        x, y = gap + col * (cell + gap), top + row * (cell + header + gap)
        draw.rectangle((x, y, x + cell, y + header + cell), fill='white')
        title = f'{index + 1}. {label(relative)}'
        size = 39
        while draw.textbbox((0, 0), title, font=font(size))[2] > cell - 40 and size > 20:
            size -= 1
        draw.text((x + 20, y + 14), title, font=font(size), fill='#111827')
        draw.text((x + 20, y + 69), Path(relative).name, font=font(25), fill='#374151')
        with Image.open(ROOT / relative) as original:
            original.load()
            image = original.convert('RGBA')
            background = Image.new('RGBA', image.size, 'white')
            image = Image.alpha_composite(background, image).convert('RGB')
            image = ImageOps.contain(image, (cell, cell), method=Image.Resampling.LANCZOS)
            canvas.paste(image, (x + (cell - image.width) // 2,
                                 y + header + (cell - image.height) // 2))
        panels.append({'panel': index + 1, 'name': label(relative), 'source': relative})
    canvas.save(target, quality=92, subsampling=0, optimize=True)
    return panels


def boundary(previous, current):
    if previous is None:
        return {'id': 'MOVIE_OPENING', 'mode': 'opening', 'previous': None,
                'next': current['number'], 'completed_event': None,
                'next_action': current['first']}
    number = current['number']
    mode = TRANSITIONS.get(number, 'CONTINUING STORY - FOLLOW THE LOCAL SCENE AND SHOT PLAN')
    return {'id': f"CUT_{previous['number']:03}_{number:03}", 'mode': mode,
            'previous': previous['number'], 'next': number,
            'completed_event': previous['ending'], 'next_action': current['first']}


def opening_text(part, incoming):
    if not incoming['previous']:
        return ('This is the opening of the movie. No previous video or handoff image exists. '
                f"First action: {part['first']} Only this part may show the opening movie title and director card.")
    return (f"Boundary {incoming['id']}; previous video: PART {incoming['previous']:03}.\n"
            f"Completed previous ending (context, not a scene to replay): {incoming['completed_event']}\n"
            f"Edit instruction: {incoming['mode']}.\n"
            f"First action in this video: {part['first']}\n"
            'For a same-scene join, continue the resulting pose and action immediately after the supplied end frame. '
            'Preserve camera side, left/right positions, eyelines, movement direction, held objects, wetness, dirt, '
            'wounds, clothes, weather and light; do not reset them to a clean reference portrait. '
            'When the local scene or the edit instruction changes time, location, viewpoint or enters a memory, '
            'make that deliberate cut and establish the local setting. Carry identities and story consequences, '
            'not the previous background or absent cast. A memory returns to its stated age/outfit; it does not '
            'resurrect a character in the present. Speak only this part\'s dialogue.')


def ending_text(part, outgoing):
    if outgoing is None:
        return (f"Final movie image: {part['ending']}\n"
                'Finish the emotional ending within 30 seconds. No next-part hook or new threat. '
                'Let the written final chord resolve; preserve the final starlight image and allow its written fade.')
    return (f"Boundary {outgoing['id']}; following video: PART {outgoing['next']:03}.\n"
            f"Complete this ending by 30 seconds: {outgoing['completed_event']}\n"
            f"Next opening is setup context only: {outgoing['next_action']}\n"
            f"Next edit: {outgoing['mode']}. Do not start the next part's action or dialogue in this video. "
            'During the final 1 second keep the chosen end composition readable while breathing, cloth, hair '
            'and ambience continue naturally. This is an edit handle, not a freeze frame. '
            'End with stable identity, props, screen direction and lighting. Avoid a new title, recap, '
            'unrequested fade, black tail or music outro at this join.')


def update(part, incoming, outgoing, sheet_path, panels):
    text = part['source']
    number = part['number']
    raw_url = RAW + quote(sheet_path.relative_to(ROOT).as_posix(), safe='/')
    mapping = '\n'.join(f"Panel {p['panel']}: {p['name']} ({Path(p['source']).name})." for p in panels)
    attached_frame = ('No previous final-frame attachment for the movie opening.' if number == 1 else
                      f"Optional attachment 2: the actual approved end frame exported from PART {number - 1:03}, "
                      f"named Part_{number - 1:03}_EndFrame.png. This is created after rendering that part; "
                      'it is not a supplied repository asset or a URL. For a same-scene cut it anchors the opening pose. '
                      'For a stated time/location/memory cut it is continuity context only.')
    # Replace the legacy reference inventory, including lists that exceeded the UI cap.
    start = text.index('FROST: Son of the Wild')
    text = text[start:]
    begin = text.index('REFERENCE IMAGES FOR THIS PART')
    end = text.index('PROMPT TO PASTE IN DOLA')
    text = text[:begin] + text[end:]
    text = text.replace('Status: ready - EXPANDED CANON PACKAGE', 'Status: reference and handoff update - render pending')
    text = re.sub(r'(?m)^Mode:.*$',
                  'Mode: Generate this part as one separate 30-second video. Load the attached reference board into '
                  'the actual reference-image input. Select 30 seconds and 16:9 in the available generator controls.', text)
    text = re.sub(r'(?m)^CHARACTER LOCK:.*$',
                  'CHARACTER LOCK: Match each named panel in attachment 1 for face, age stage, body, hair/fur, eyes, '
                  'clothes and armor. Use the correct variant shown for this part. Each panel is reference material, '
                  'not another character to add. Show only the cast requested by the shots. For same-scene continuity '
                  'retain the approved end frame\'s dirt, wetness, damage and carried objects.', text)
    text = re.sub(r'(?m)^OPENING CONTINUITY LOCK:.*\n?', '', text)
    text = text.replace('0-3s: Start with a strong immediate visual hook connected to the previous part.',
                        f"0-3s: {part['first']}")
    text = re.sub(r'\nSUSPENSE HOOK LOCK:\n.*?(?=\nGLOBAL RULES:)', '', text, flags=re.S)
    text = re.sub(r'\nFINAL EMOTIONAL CLOSURE LOCK:\n.*?(?=\nGLOBAL RULES:)', '', text, flags=re.S)
    text = text.replace('[ ] Images loaded by raw URLs', '[ ] Reference board attached (1 image)')
    text = text.replace('[ ] Images uploaded', '[ ] Reference board attached (1 image)')
    # Correct the geographic inconsistency in the Hindi folder only.
    text = text.replace('CEDAR HOLLOW, WASHINGTON', 'CEDAR HOLLOW, OREGON')
    if number == 227:
        visual_bridge = next(s[2] for s in part['shots'] if s[:2] == (3, 8))
        text = re.sub(r'(?m)^(8[-\u2013]24s:)', f'3-8s: {visual_bridge}\n\\1', text, count=1)
    # The Hindi output instruction overrides English control-text examples.
    text = text.replace('"FROST: SON OF THE WILD" and below it "Directed by Noorul Ain"',
                        '"फ्रॉस्ट: जंगल का बेटा" and below it "निर्देशन: नूरुल ऐन"')
    contract = (
        '\nSEPARATE GENERATION + ATTACHMENT CONTRACT:\n'
        'Generate this numbered part from a fresh request. There is no memory of an earlier video. '
        'Create a new moving scene using the identities, products/props where relevant, and style in the references. '
        'The combined board occupies ONE image slot. The entire request may contain at most THREE images.\n'
        f'Attachment 1 (required): {sheet_path.name}\n{raw_url}\n'
        f'{mapping}\n{attached_frame}\n'
        'Attachment 3 is optional: one approved face/prop/detail crop or one additional combined detail board '
        'only when needed. Do not also attach all the separate source portraits.\n'
        'Read the names printed ABOVE each panel. Keep people, age variants, creatures and locations separate. '
        'Board text is identification only and must not appear in the movie. Create the scene fresh: never animate '
        'the board as a collage, show its grid, merge faces, copy reference backgrounds indiscriminately or make '
        'all panels appear together. A location panel defines place design, not its background figures as cast. '
        'URLs alone are not image conditioning; the board must be attached/imported into the actual image input.\n\n'
        'FULL 30-SECOND PERFORMANCE:\n'
        'Use the existing complete 0-30s action and dialogue timeline below. Every time range must have meaningful '
        'movement, reaction or consequence; progress through the written beats instead of finishing early and '
        'holding, looping, recapping or padding. Voices, effects and score follow the action. Confirm 30 seconds '
        'in the UI before rendering; prompt wording cannot override a tool duration cap.\n\n'
        f'OPENING HANDOFF IN:\n{opening_text(part, incoming)}\n\n'
        f'ENDING HANDOFF OUT:\n{ending_text(part, outgoing)}\n\n'
        'VOICE AND AUDIO CONTINUITY:\n'
        'All audible output is natural Hindi/Hindustani with Hindi lip-sync. Keep the same approved voice preset '
        'or reference per character when supported. Otherwise repeat the same Hindi voice description, tone and '
        'speaking pace in every separate request; text alone cannot guarantee an identical generated voice. '
        'Carry compatible ambience and score across a same-scene cut, with no repeated intro. Finish a line '
        'before the edit, leave a natural breath, and do not repeat dialogue from the handoff context.\n'
    )
    text = text.replace('PROMPT TO PASTE IN DOLA\n', 'PROMPT TO PASTE IN DOLA\n' + contract + '\n', 1)
    # The package's pre-existing scene actions and dialogue are preserved, except
    # explicit scene-transition context above and the Oregon/title correction.
    text = re.sub(r'(?m)^Expanded 312-part canon\..*$',
                  '312-part Hindi 16:9 package. Each part is generated separately; follow its paired handoffs.', text)
    return text.strip() + '\n'


def main():
    parts = [parse(p) for p in sorted(FOLDER.glob('Part_*_Dola_URL.txt'))]
    assert [p['number'] for p in parts] == list(range(1, 313))
    opening_set = set(parts[0]['references'])
    lily_identity = 'Characters_Dola_1024/Main/C01_Lily/C01_Lily_FULL.png'
    for part in parts:
        part['opening_board_lily'] = set(part['references']) == opening_set
        if part['opening_board_lily']:
            part['references'].append(lily_identity)
    SHEETS.mkdir(exist_ok=True)
    boundaries = [boundary(parts[i - 1] if i else None, p) for i, p in enumerate(parts)]
    assets, reports, prompts = {}, [], []
    for i, part in enumerate(parts):
        references = tuple(sorted(part['references']))
        if part['opening_board_lily']:
            references = tuple(r for r in references if r != lily_identity) + (lily_identity,)
        if references not in assets:
            name = f"References_{part['number']:03}.jpg"
            target = SHEETS / name
            panels = sheet(references, target, refresh=part['opening_board_lily'])
            assets[references] = (target, panels)
        target, panels = assets[references]
        outgoing = boundaries[i + 1] if i < 311 else None
        text = update(part, boundaries[i], outgoing, target, panels)
        part['path'].write_text(text, encoding='utf-8')
        prompt = text.split('PROMPT TO PASTE IN DOLA\n', 1)[1]
        prompt = prompt.split('\nHINDI YOUTUBE TITLE / DESCRIPTION AFTER DOWNLOAD', 1)[0].strip()
        prompt = f"PART {part['number']:03} - \"{part['title']}\"\n\n{prompt}"
        prompts.append(prompt)
        reports.append({'part': part['number'], 'title': part['title'],
                        'source_sha256': part['source_sha256'],
                        'reference_board': target.relative_to(PACKAGE).as_posix(),
                        'image_input_count_required': 1,
                        'image_input_count_with_handoff': 1 if i == 0 else 2,
                        'max_image_inputs': 3, 'panels': panels,
                        'local_scene': part['context'], 'local_shots': part['shots'],
                        'incoming': boundaries[i], 'outgoing': outgoing})
        if (i + 1) % 30 == 0:
            print(f'Updated {i + 1}/312 parts; {len(assets)} labelled sheets', flush=True)
    combined = PACKAGE / 'Hindi_YouTube_16x9_ALL_312_REFERENCE_HANDOFF_CLEAN.txt'
    combined.write_text('\n\n--------\n\n'.join(prompts) + '\n', encoding='utf-8')
    report = {'source_commit': BASE, 'date': '2026-10-26', 'parts': 312,
              'duration_seconds_per_part': 30, 'aspect_ratio': '16:9',
              'required_images_per_part': 1, 'maximum_images_per_request': 3,
              'unique_labelled_reference_sheets': len(assets),
              'continuous_boundaries': 311,
              'method': 'Preserve Hindi scene actions and dialogue; replace unlimited URL sets with one labelled '
                        'board per unique set and explicit shared incoming/outgoing states. Scene changes and '
                        'memory inserts are identified to avoid resetting the present timeline. No video rendered.',
              'records': reports}
    (PACKAGE / 'Production_Docs/REFERENCE_HANDOFF_MANIFEST.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (PACKAGE / 'Production_Docs/REFERENCE_IMAGE_INDEX.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['part', 'title', 'attach_image_1', 'optional_attach_image_2_after_render', 'max_images'])
        for p in reports:
            writer.writerow([f"{p['part']:03}", p['title'], p['reference_board'],
                             '' if p['part'] == 1 else f"Part_{p['part'] - 1:03}_EndFrame.png", 3])
    with (PACKAGE / 'Production_Docs/HANDOFF_LOG_TEMPLATE.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['part', 'video_file', 'duration_seconds', 'aspect_ratio', 'approved_end_frame',
                         'cast_screen_positions', 'wardrobe_damage_wetness', 'held_props_and_hands',
                         'lighting_weather_camera_side', 'voice_presets', 'continuity_approved'])
        writer.writerows([[f'{i:03}', *[''] * 10] for i in range(1, 313)])
    print(f'Finished: 312 prompts, {len(assets)} sheets, 311 paired boundaries, one combined TXT.', flush=True)


if __name__ == '__main__':
    main()
