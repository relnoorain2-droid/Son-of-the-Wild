# Hindi Version YouTube Movie - FROST: Son of the Wild

This folder is separate from the English YouTube package and the Hindi Reels package.

Use this folder for Hindi YouTube movie videos in widescreen 16:9.

## Separate 30-Second Generation With Reference Images

All 312 parts have a named reference board and paired opening/ending handoffs.
Each part is a separate request; the generator must not be assumed to remember
another video. Use the complete local 0-30 second timeline and choose 30 seconds
and landscape 16:9 in the generator controls.

1. Find the part in `Production_Docs/REFERENCE_IMAGE_INDEX.csv`.
2. Attach its single JPG from `Reference_Sheets/`. Every panel has the character,
   creature or location name printed above it. These boards combine the existing
   repository images without redesigning the characters. Several parts can share
   the same board when they use the same reference set.
3. For Part 002 onward, optionally attach the approved final frame of the previous
   generated video as image 2. Export it after approval and name it, for example,
   `Part_001_EndFrame.png`. These future frame files are not included in this repo.
4. Paste the part prompt from `Prompts_16x9_Hindi/`, including its attachment map
   and both handoffs. Image 3 is reserved for an optional approved detail crop.
   Never attach more than three images; do not also attach every source portrait.
5. Create the scene fresh. Reference-board names and grid must never appear in the
   final movie. Only show the cast called for in that part's shots.
6. Check the actual rendered duration, Hindi audio, 16:9 frame, face identities,
   age stages, wardrobe, props, camera direction and ending. Record the accepted
   state in `Production_Docs/HANDOFF_LOG_TEMPLATE.csv`, then generate the next part.

For a same-scene join, image 2 anchors the previous pose and screen positions.
For an authored scene/time change or memory, follow the local setting and age
stage. The handoff identifies that edit so a previous background is not forced
into a different scene. Written context is included if image 2 is unavailable;
rendered continuity still needs visual review.

The prompt cannot force a tool to exceed its duration limit or guarantee exactly
the same voice. Select an available 30-second mode and reuse a voice preset when
supported. No videos have been rendered as part of this prompt/reference update.

## Folder Contents

- `Prompts_16x9_Hindi/` - all 312 Dola-ready prompts for Hindi YouTube 16:9 output.
- `Skill/SKILL.md` - Hindi YouTube skill file to upload in Dola.
- `Production_Docs/` - Hindi YouTube output rules.
- `Reference_Sheets/` - combined, labelled JPG reference boards; attach one per part.
- `Hindi_YouTube_16x9_ALL_312_REFERENCE_HANDOFF_CLEAN.txt` - all 312 generation-only
  prompt blocks, separated by `--------`; post descriptions and status checklists
  are excluded from this combined file. Each block is still a separate request.
- `Production_Docs/REFERENCE_HANDOFF_MANIFEST.json` - every part's source image
  mapping, local action timeline and paired boundary states.
- `Production_Docs/REFERENCE_ATTACHMENT_AND_HANDOFF_RULES.md` - reference and edit rules.

## Rebuilding And Validation

From the repository root, run:

```text
python "Hindi version youtube movie/Production_Docs/build_reference_handoffs.py"
python "Hindi version youtube movie/Production_Docs/validate_reference_handoffs.py"
```

The builder uses the committed Hindi package at the source SHA recorded in the
manifest. It only updates this Hindi YouTube folder. Its source dialogue and
scene actions are retained; new handoff context marks existing insertions as
memories or cutaways where they otherwise replay earlier events. This update is
not a new dialogue rewrite. The Cedar Hollow location-card typo is corrected to
Oregon and the opening title/credit examples are in Hindi. Part 227's missing
3-8 second visual range now shows the listeners reacting before the legend vision.
Pass `--refresh-sheets` to the builder after replacing an approved source image;
otherwise existing reference JPGs are reused.

## Hindi Output Rule

The prompt instructions can stay in English, but Dola must generate the video output in Hindi:

- Hindi spoken dialogue
- Hindi narrator voice
- Hindi lip-sync
- Hindi title cards and location/time cards in Devanagari
- Hindi YouTube title/description after download

Character names and place names can remain as names.
