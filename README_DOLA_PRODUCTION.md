# FROST: Son of the Wild - Dola Production Package

Use this repo for Dola AI generation.

## Fast Workflow

1. For the current English 9:16 restart, use only the manual clean files marked `MANUAL`.
2. Paste one part at a time into Dola. Each part is separated only by `-------`.
3. The prompt already includes direct GitHub raw image URLs, so Dola should not need local image uploads.
4. Use Seedance 2.5, 30 seconds, vertical 9:16.
5. The final all-312 combined file will be recreated only after every batch has been manually rewritten.

## Important Rules

- Use the `_URL.txt` prompts, not the local-path prompt versions.
- The clean restart prompts must contain video instructions only. Do not include Facebook/Reels captions, Dola status checklists, notes, or upload reminders inside the prompt text.
- Do not paste local Windows paths into Dola.
- Character reference images are in `Characters_Dola_1024`.
- Each part must be self-contained because Dola does not remember the previous render. Repeat the needed image URLs, character locks, setting, action, dialogue, and final frame inside every part.
- Dialogue must be fresh for that part. Do not reuse the same line across nearby videos, and do not add filler speech during action/fight scenes.
- Short place/time title cards are allowed when the prompt asks, for example `CEDAR HOLLOW, OREGON`.

## Main Files

- `Skill/SKILL.md` - Dola skill instructions.
- `09_Dola_Ready_Prompts_URL/` - prompts ready with public image URLs.
- `ZDola_Combined_Prompts/English_9x16_MANUAL_001_030_CLEAN.txt` - current manually rewritten English 9:16 progress file.
- `ZDola_Combined_Prompts/English_9x16_Batches/` - manual clean restart batch files for English 9:16 reels.
- `Characters_Dola_1024/` - production image references.
- `Story_Plan_DETAILED_ENGLISH_CANON.txt` - final English story canon.
- `00_PUBLIC_IMAGE_URLS_VERIFIED.csv` - direct image URL tracker.
