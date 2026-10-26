# Hindi Output Rules

Only audible words are Hindi. Production instructions and non-spoken text remain English.

Required:
- Spoken dialogue in natural Hindi / Hindustani.
- Narrator in Hindi movie-trailer style.
- Accurate Hindi lip-sync.
- Singing and any audible words in Hindi.
- Scene, action, camera, timing, reference and continuity instructions in English.
- Character names and voice descriptions in English, matching the reference board.
- Requested visible cards and written props remain English, not spoken dialogue.
- Opening title: "FROST: SON OF THE WILD".
- Director card: "Directed by Noorul Ain".
- No added dialogue subtitles.

## Literal Hindi, Not Automatic Translation

Dialogue-bearing parts supply actual Devanagari dialogue; silent parts stay
silent. Narration is used only where explicitly authored. Only `SPOKEN HINDI`
authorizes speech; quotations in handoff/action text are not extra lines.
English production directions are not dialogue and must never
be read aloud. Only explicitly requested English title/location/time cards or
written story props may appear; do not display production instructions or board labels.

Names retain their identity and Hindi pronunciation. English speaker labels
such as Lily, Bruno and Frost match the reference board directly. Their English
voice descriptions request natural Hindi delivery, not American-English speech.

Do not ask the video tool to translate English dialogue at generation time.
Do not translate the supplied Hindi back into English. This removes a source
of mixed-language results; it cannot guarantee a generator will follow every
instruction. Listen to each rendered part before approving its end frame.

The corrected English Reels scenes are adapted into short natural Hindi without
reading the chapter title as dialogue. Repeated filler and unnecessary Rose
warnings are removed. No minimum dialogue count is imposed. No videos were
generated or auditioned by this update.

The authored adaptation is in `revised_hindi_dialogue.py`. Build and validate
with `merge_reel_corrections.py`; the old entry points delegate to it. Validation
covers all 312 prompts, Hindi-only unique spoken payloads, timelines, adjacent
handoff text, combined reference boards and their dimensions.

Not allowed:
- English spoken dialogue.
- English subtitles/captions in the video.
- Random extra text.

## Reference Boards And Independent Parts

Use the part-specific combined JPG as one attachment. Its English character names
are reference labels only and must not appear in the video. Follow
`REFERENCE_ATTACHMENT_AND_HANDOFF_RULES.md` and the per-part image index.
The normal request has one reference board plus, when supplied, the preceding
approved end frame. Reserve image 3 for an optional detail reference; never
exceed three attachments. A named panel locks identity and does not automatically
put that subject on screen.

All 312 parts remain separate 30-second requests. Each contains its local scene,
full timeline and paired opening/ending handoffs. Same-scene joins preserve
staging, props, wardrobe, camera side and ambient audio. Explicit location/time
cuts and memories use their own local context. Part 312 closes the movie.
