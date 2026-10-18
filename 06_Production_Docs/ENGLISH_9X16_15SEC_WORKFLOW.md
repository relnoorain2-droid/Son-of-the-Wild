# Pending English 9:16 - 15-second version

Use `ZDola_Combined_Prompts/English_9x16_PENDING_502_15SEC_CLEAN.txt` for this run. It converts the existing 251-part pending list into 502 standalone prompts. The original pending selection and full 312-part master are unchanged. Already-ready parts are not included.

Each original story part keeps its number, with A then B: for example 001A, 001B, 009A, 009B. Gaps are intentional because the intervening parts are already ready. Every prompt produces 15 seconds; join A and B to restore its original 30-second story duration. Do not renumber clips by queue position.

The conversion partitions complete shots at the closest shot boundary to the original midpoint, then retimes each half to 0-15 seconds. It does not split a shot in the middle of an action. Speech is assigned to one half with a word-count budget; all 233 explicitly authored dialogue lines extracted from the source speech sections are preserved once per original part. Shared identity, camera and sound instructions and the original reference lists repeat in both halves so independent generations have their guides.

A ends on a written handoff state. B restates the completed action as context and explicitly starts from its result without replaying it. If the generator supports an initial image, supply A's actual final frame to B in addition to the required identity references. That frame is not included automatically by the TXT file.

This is a programmatic shot-boundary conversion with continuity instructions, not a fresh manual creative rewrite or a verified render. Matching prompts alone cannot guarantee matching generated frames. Test one A/B pair before queuing all 502, checking faces, clothing, age and the visual join. Existing content restrictions and reference-input limitations still apply; a shorter duration does not remove them.

The accompanying JSON manifest records every split boundary, number of shots, speech budget and reference count. `scripts/split_pending_15s.py` reproduces the output from the preserved 251-part source.
