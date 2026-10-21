# FROST: Son of the Wild - Dola Production Package

Use this repo for Dola AI generation.

## Fast Workflow

Current retry file after the 2026-10-21 14-29 batch: `ZDola_Combined_Prompts/English_9x16_MISSING_94_15SEC_CLEAN.txt`. The 14 unique ready clips have been excluded from the prior 108-prompt list. Use this 94-prompt file for the next English 9:16 run; the older counts below are historical snapshots.

Part 001B in that current file was simplified on 2026-10-21: five scene-specific references instead of seven, a concise standalone shot plan, and the original spoken line and sealed-scroll ending. The other 93 prompts are unchanged. Test just this clip with `ZDola_Combined_Prompts/English_9x16_PART_001B_15SEC_REVISED.txt` before another batch. The cause of the reported generation failure is unconfirmed; this rewrite has not been rendered or confirmed accepted by Dola. If a content-policy rejection appears, follow the provider's guidance rather than retrying to bypass it. Older pending snapshots and the 30-second master retain the original version.

1. After the `file2` update checked on 2026-10-19, use `ZDola_Combined_Prompts/English_9x16_MISSING_376_15SEC_CLEAN.txt`. Its smaller import alternatives are `English_9x16_MISSING_15SEC_BATCH1_300_CLEAN.txt` then `English_9x16_MISSING_15SEC_BATCH2_76_CLEAN.txt`. Use either the combined file or the two batches, not both. The 66 unique new clips have been excluded from the former 442-prompt list. Older pending files are historical snapshots. The unchanged `English_9x16_ALL_312_CLEAN.txt` remains the complete story master.
2. Paste one part at a time into Dola. Each part is separated only by `-------`.
3. Dola must first download and inspect every listed image, then attach/import it into the generator's actual reference-image inputs. URLs in text alone do not prove image conditioning. Stop if the route cannot load references; do not silently generate text-only substitutes.
4. For the current split file, select an available supported video model, exactly 15 seconds, vertical 9:16. Render A then B and join in that order. The original master is a separate 30-second version.
5. All 312 English 9:16 prompts have individual scene rewrites. The final combined file is assembled from those part files; generated videos still require visual review.

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
- `ZDola_Combined_Prompts/English_9x16_ALL_312_CLEAN.txt` - final English 9:16 combined file, Parts 001-312, separated only by `-------` with blank lines.
- `Characters_Dola_1024/` - production image references.
- `Story_Plan_DETAILED_ENGLISH_CANON.txt` - final English story canon.
- `00_PUBLIC_IMAGE_URLS_VERIFIED.csv` - direct image URL tracker.
