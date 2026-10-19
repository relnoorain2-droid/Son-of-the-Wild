# Ready Videos and Missing Prompts

English vertical 9:16 only. Checked the ready folder recursively, including its `File 1` subfolder, on 2026-10-19. Story identity comes from `part-XXX` with an optional A/B suffix, not the leading generation queue number. Actual duration and dimensions were read from each video's container metadata. This is a coverage audit, not a visual or audio quality review.

| Item | Count |
| --- | ---: |
| Video files | 127 |
| Complete original parts available as 30-second videos | 55 |
| Individual 15-second clips | 72 |
| Complete original parts available as A/B pairs | 14 |
| Original parts with only one half available | 44 |
| Original parts with neither half available | 199 |
| Missing 15-second prompts | 442 |

312 original parts = 55 full videos + 14 complete pairs + 44 partial parts + 199 entirely missing parts. Remaining generation work is 199 x 2 + 44 = 442 clips. The TXT contains 441 `-------` separators with blank lines.

Use `ZDola_Combined_Prompts/English_9x16_MISSING_442_15SEC_2026-10-19_CLEAN.txt`. Keep its original story numbers and A/B labels. A ready full 30-second video covers both halves. A ready A or B video covers only its own half. Missing partners preserve the existing 502-prompt file's exact text, avoiding changes to the split that generated their ready partners. Previously excluded parts that are no longer in the folder are restored as two 15-second prompts generated from the full master.

All 127 filenames were normalized with their actual story number, full master title, duration and A/B label where applicable. Example: `028B_part-028B---the-private-room_15s.mp4`. Videos remain in their original parent directories. No video was deleted, overwritten or transcoded. The full master and historical pending TXT files are unchanged.

The JSON inventory records original and corrected filenames, measured metadata, complete and partial parts, and every missing clip identifier. Original byte sizes were checked after rename. Ready coverage plus missing prompts was checked to include all 624 possible story half-slots without overlap.

Prompt conversion preserves reference links, image-loading requirements, half-specific dialogue and written A/B handoffs. These instructions do not guarantee identical generated faces or perfect visual joins; use each ready partner's final frame as a starting reference where supported.
