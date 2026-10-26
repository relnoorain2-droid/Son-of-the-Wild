# English YouTube Movie - 30-Second Edition

## Current Matching Edition

The current English YouTube movie matches the Hindi YouTube story and its
combined reference boards: **312 numbered parts of 30 seconds each, plus the
optional Part 004Aextra**, in landscape 16:9. All speech is written in English.
No skill file is needed.

- `Prompts_16x9/` contains the 312 current individual prompts and
  `Part_004Aextra_The_Wedding_Night.txt`.
- `English_YouTube_16x9_30SEC_312_PLUS_004Aextra.txt` contains 313 independent
  prompts, with `-------` on a separate line between them. The optional extra
  is placed after Part 004. Do not render the extra if it is not wanted.
- Each prompt links the same combined reference board used by its Hindi
  counterpart. Download that board and attach it as image 1. An approved prior
  final frame and a detail image can be added when supported.
- Part 004 includes the bride's brief, willing wedding kiss. The extra uses the
  same separate wedding-night board as Hindi and is a flash-forward that returns
  to the wedding hall before Part 005. Its specified time cards are silent.
- Keep Lily's and the first bride's distinct faces and costumes, with flattering
  tailoring and cinematic light. Speak only the listed English lines; silent
  action remains silent. Frost's voice and reference change with his growth stage.

The older 624-part, 15-second files remain available in this folder for anyone
who needs that previous edit. Do not mix their numbering with this 312-part
30-second edition. To rebuild and validate the current edition, run:

```text
python "YouTube movie/Production_Docs/build_english_30sec.py"
python "YouTube movie/Production_Docs/build_english_30sec.py" --validate
```

The validator checks all 313 combined blocks, references, timelines and English
speech, and confirms that the Hindi and 15-second source packages are unchanged.
The prompts are prepared for generation; actual video, lip-sync and visual
continuity still need review after rendering.

## Previous 15-Second Edition

Use this package for the English landscape 16:9 movie, exactly 15 seconds per generated clip.

## Import Files

1. `English_YouTube_16x9_15SEC_PARTS_001_312_CLEAN.txt` - Parts 001-312.
2. `English_YouTube_16x9_15SEC_PARTS_313_624_CLEAN.txt` - Parts 313-624.

Each file contains 312 prompts with 311 `-------` separators and blank lines. Import each once. Do not combine them with older English reel pending lists. All 624 individual prompts are also in `Prompts_16x9_15sec/`.

## Generation

- Use a supported model/route with duration exactly 15 seconds and ratio 16:9; 1920x1080 is the composition target when supported, not a claim of native output resolution.
- Upload the updated `Skill/SKILL.md` if your Dola workflow requires a skill. Do not use the old hard-locked 30-second skill.
- Every prompt is independent and can be sent in a different chat. It repeats references, loading requirements, identity rules, timing, local dialogue and opening/ending states.
- Download, inspect and attach the listed reference images to the actual reference input. Text URLs alone do not prove attachment. Report unavailable reference input rather than inventing a match.
- Use written speech only; quiet scenes do not need added dialogue. Keep faces, age stages and voices matched to their references.
- Render and assemble strictly by the displayed part numbers. The leading queue number from a batch tool is not the story number.
- If supported, use the actual previous final frame as an opening reference alongside identity images. A fresh chat cannot access that frame merely because the prompt describes it.

## Story and Numbering

The source is the updated full 312-part English reel master, including the later reference-loading, identity, growth, dialogue and story fixes. No ready or pending reel parts are excluded from this YouTube version. Old story part N becomes new Parts 2N-1 and 2N; all displayed YouTube headers are plain numeric Parts 001-624, without letter suffixes. The two imports meet between Parts 312 and 313, and the movie ends in Part 624.

This package is a programmatic shot-boundary conversion and landscape adaptation, not a fresh manual rewrite or a guarantee of rendered continuity. Each original action and speech line is retained while timing and framing adapt. The written join states are checked; actual character faces and generated motion still need visual review. Test adjoining clips before bulk generation.

## Files

- `Prompts_16x9_15sec/`: current 624 individual prompts.
- `Production_Docs/YOUTUBE_624_CONTINUITY_MANIFEST.json`: source-to-new-part mapping and every join state.
- `Production_Docs/YOUTUBE_16X9_RULES.md`: current framing and assembly rules.
- `Prompts_16x9/`: the newer 312-part 30-second edition described above; do not use it with the 624-part numbering.

English reel masters, ready videos and Hindi versions remain unchanged.
