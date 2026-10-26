# Hindi Version YouTube Movie - FROST: Son of the Wild

## Final Reels Correction Merge - 2026-10-26

### Review From Part 031 - 2026-10-27

Parts 001-030 have already been rendered. This revision preserves those prompt
files and their reference boards byte for byte; it does not rewrite the user's
completed wedding edit. Continue production at Part 031 using the updated files.

Parts 031-312 received a Hindi grammar and meaning review, clearer local costume
instructions, and specific character/age voice guidance. Lily retains the approved
clothes and elegant film styling. Unrelated royal wedding-night instructions are
removed from these later scenes. The combined all-312 file is refreshed with the
same first 30 blocks and updated later blocks; no additional import file is needed.
The builder now preserves Parts 001-030 by default and validates their file hashes.

The corrected English Reels scenes now drive all 312 Hindi prompts, with literal
scene-specific Hindi dialogue. Repeated warnings and filler are removed; action
scenes can be silent. Rose, Grace and Martha are distinct and only appear where
the local scene requires them. Parts 002/006/011 exclude Rose. Parts 006/011
include Damian's face detail on the combined board. Frost's growth, counts,
anatomy and later spirit/power continuity follow the corrected Reels story.

Use the combined board linked in each UPDATED prompt. New boards combine the
existing images in the same labelled layout. Original office boards are retained.
The established reference outfit takes priority over styling descriptions;
adult styling refines fit, natural proportions and fabric. Lily's royal first
night leads to her escape before consummation; existing gentle affection remains
in its story context. This update does not verify generated video quality.

This folder is separate from the English YouTube package and the Hindi Reels package.

Use this folder for Hindi YouTube movie videos in widescreen 16:9.

## Separate 30-Second Generation With Reference Images

All 312 parts have a named reference board and paired opening/ending handoffs.
Each part is a separate request; the generator must not be assumed to remember
another video. Use the complete local 0-30 second timeline and choose 30 seconds
and landscape 16:9 in the generator controls.

Use the reference image attachments and prompt text directly in your video tool.
No skill file, skill upload or Dola-specific command is required. Select
Seedance 2.5 in your new tool, with 30 seconds and landscape 16:9.

## Literal Hindi Dialogue

All dialogue-bearing prompts include actual Devanagari speech and English voice
descriptions. Narration is used only where authored; silent parts stay silent.
Songs are written in Hindi too. Everything non-spoken remains
English: scene/camera directions, character names, voice descriptions, reference
labels, and explicitly requested visible cards or written story props. English
speaker labels match the reference boards. Only the actual words inside spoken
or sung lines are Hindi, as requested.

Use the newly updated prompts, not an older downloaded copy. Listen to the
rendered audio before accepting each part. These text corrections reduce language
ambiguity but do not guarantee generator compliance or identical voices.

All combined reference sheets are limited to 8,000,000 pixels (8.0 MP) and
4096 pixels on the longest side, leaving room below the tool's 8.3 MP limit.
Labels and panel layout are preserved. Reference links include a version suffix
so a freshly downloaded sheet is not confused with a cached oversized copy.

## Wardrobe Update

Each prompt includes adult costume guidance: flattering tailoring, opaque rich
fabrics, distinct hairstyles and accessories. Lily has a glamorous ivory wedding
gown, a refined blue forest dress, practical maternity/mother outfits and a teal
celebration gown. Private-room scenes retain the wedding dress. Continuous
scenes retain the same outfit and its existing damage; romantic moments retain
their existing gentle actions. Older women retain their age and character, and
children's outfits are unchanged.

The combined boards supply identity, age and setting. Costume guidance refines
the established clothing without replacing it. Updated boards reuse existing
image pixels; characters have not been redesigned. No video has been generated.

1. Find the part in `Production_Docs/REFERENCE_IMAGE_INDEX.csv`.
2. Attach its single JPG from `Reference_Sheets/`. Every panel has the character,
   creature or location name printed above it. These boards combine the existing
   repository images without redesigning the characters. Several parts can share
   the same board when they use the same reference set.
3. For Part 002 onward, optionally attach the approved final frame of the previous
   generated video as image 2. Export it after approval and name it, for example,
   `Part_001_EndFrame.png`. These future frame files are not included in this repo.
4. Open the part in `Prompts_16x9_Hindi/`. Its image link and attachment instructions
   are ABOVE `PROMPT TO COPY AND PASTE (SEEDANCE 2.5)`. Attach the images first,
   then copy everything BELOW that heading to the end of that part. The copy area
   has no image links, post descriptions, status checklists or trailing notes.
   Its reference-panel map and both handoffs are included. Image 3 is reserved for an optional approved detail crop.
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

- `Prompts_16x9_Hindi/` - all 312 Seedance 2.5 prompts for Hindi YouTube 16:9 output.
- `Production_Docs/` - Hindi YouTube output rules.
- `Reference_Sheets/` - combined, labelled JPG reference boards; attach one per part.
- `Hindi_YouTube_16x9_ALL_312_REFERENCE_HANDOFF_CLEAN.txt` - all 312 generation-only
  part blocks, separated by `-------`. Each block has its image link above the
  copy heading and its complete paste-ready prompt below. Stop copying at that
  part's separator. Each block is still a separate request.
- `Production_Docs/REFERENCE_HANDOFF_MANIFEST.json` - every part's source image
  mapping, local action timeline and paired boundary states.
- `Production_Docs/REFERENCE_ATTACHMENT_AND_HANDOFF_RULES.md` - reference and edit rules.

## Rebuilding And Validation

From the repository root, run:

```text
python "Hindi version youtube movie/Production_Docs/merge_reel_corrections.py"
python "Hindi version youtube movie/Production_Docs/merge_reel_corrections.py" --validate
```

The builder reads the corrected English Reels all-312 script and the authored
Hindi adaptation in `revised_hindi_dialogue.py`. It writes only this Hindi folder.
It validates complete timelines, unique Hindi dialogue, matching adjacent handoff
text, board mappings and dimensions. The older builder/validator entry points now
delegate to this workflow so they cannot restore the repeated template dialogue.
Requested title/credit cards stay English; voices alone are Hindi. The English
source remains unchanged. Generated faces, audio and continuity still need review.

## Hindi Output Rule

The prompt instructions can stay in English, but the video tool must use the supplied Hindi output:

- Hindi spoken dialogue
- Hindi narrator voice
- Hindi song lyrics
- Hindi lip-sync
- English production instructions and requested screen text

Character and place names retain their identities with Hindi pronunciation.
