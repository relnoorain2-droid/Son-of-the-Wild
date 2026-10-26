---
name: zakariya-seedance-2-5-30s-hindi-youtube-16x9
description: "Separate 30-second Hindi 16:9 YouTube movie generation for FROST Parts 001-312. One named reference board per part, at most three image inputs, Hindi voices and explicit opening/ending handoffs."
---

# Zakariya Seedance 2.5 — 30s Hard Lock (Hindi YouTube 16x9 Movie Edition)

## Current Reference And Handoff Workflow - 2026-10-26

This section replaces legacy public-URL/image-upload guidance below wherever
it conflicts. It applies to every one of the 312 Hindi YouTube parts.

- Each part is a fresh, separate request for one 30-second landscape 16:9 video.
  Choose 30 seconds in an available supported duration control. Instructions in
  text cannot extend a tool's duration cap. Inspect actual duration before calling
  a render complete. Do not generate anything just to edit/review a prompt package.
- Use the single JPG listed in `Production_Docs/REFERENCE_IMAGE_INDEX.csv` as image
  1. It already combines this part's character, variant, creature and location
  references. The names are printed ABOVE the panels. Match the panel map in the
  part prompt. Do not attach the separate source portraits as extra images.
- The entire request has a maximum of THREE images: image 1 is the board, image 2
  may be the previous part's actual approved end frame, and image 3 may be one
  approved face/prop/detail crop or combined detail board. Part 001 has no previous
  frame. Never fabricate a previous rendered frame or claim a future frame exists.
- Load/import the board into the actual reference-image input. A raw image URL in
  text alone is not proof of image conditioning. Inspect the attachment mapping.
- Use faces, body, age stage, fur, outfit, props and style from the panels while
  creating the scene fresh. Never render the board, labels or grid in the movie,
  merge identities, add every pictured person, or take incidental figures in a
  location reference as cast. Show only the written shot-plan subjects.
- Read `OPENING HANDOFF IN` and `ENDING HANDOFF OUT` on each request. A boundary
  CUT_NNN_NNN has the same completed event and next opening on both sides.
  Previous actions are setup context and must not be repeated as new action.
- For same-scene joins use the approved end frame to preserve staging, camera
  side, motion, eyelines, lighting, clothing, wetness/damage, held props and hands.
  If the written edit changes location/time or enters a memory, follow that
  explicit scene and historical age/outfit; the preceding background is context.
- Use only local dialogue in natural Hindi/Hindustani. Reuse the same approved
  voice preset when available, otherwise the same Hindi voice description.
  Finish speech before the edit and keep compatible background sound/music.
- Preserve meaningful action across the whole local 0-30 second timeline. Keep
  a naturally moving, readable last second for the next edit. No repeated intro,
  new end card or unrequested black tail. Part 312 closes the story emotionally.
- Read `Production_Docs/REFERENCE_ATTACHMENT_AND_HANDOFF_RULES.md` for the image
  workflow and record the actual render in `HANDOFF_LOG_TEMPLATE.csv`.

## Hard Lock (non-negotiable, overrides everything below)

- **Duration is locked at 30 seconds.** Always pass `duration: 30`.
- **Never deliver a 15-second result.** If the generated file is shorter than 29 seconds, it is not complete. Do not repeat the same capped route. Switch to the Seedance 2.5 30s composer route, or use text_to_video with the raw GitHub image URLs kept inside the prompt as references.
- **One single continuous segment.** One tool call = one complete 30-second video.
- **Model is locked to Seedance 2.5.** Always pass `model_version: "seedance_2.5"`.
- **Ratio is locked to 16:9 YouTube widescreen.** Always use ratio 16:9 and write "widescreen 16:9 cinematic movie frame" in GLOBAL RULES. Do not use vertical/reels framing for this YouTube movie skill.
- **Audio is ON.** Every video must include spoken dialogue, sound effects and background music exactly as written in the prompt.
- **Suspense hook is ON.** Every normal movie part must end with a final 3-second hook that pulls viewers into the next part. The final movie part must close emotionally instead of adding a new cliffhanger.

### Anti-spreading rules — never do any of these:

- Never split into two 15-second clips or any multi-part sequence inside one request.
- Never propose, offer or mention a two-segment / multi-clip / shorter-compressed delivery.
- Never claim Seedance 2.5 cannot do 30 seconds just because one route returned 15 seconds. If image_to_video returns 15 seconds, treat that as the wrong route and switch route.
- Never use the words "split", "segments", "clips", "chapters", "15s", "fallback" or "Plan B" in a confirmation summary.
- Note: "PART 01, PART 02 ..." are separate movie episodes the user posts one by one. Each PART is its own complete 30-second video and its own request. This is not splitting.

### Duration exceptions

- User explicitly asks for shorter than 30 s → one single call with that duration (5–30 s).
- User asks for longer than 30 s → one single 30 s call compressing the arc.

### Maximum videos per reply: **2 (hard cap)**

---

## Model Specification

- **Model:** Seedance 2.5 (`seedance_2.5`)
- **Duration:** 30 seconds, single continuous segment
- **Ratio:** 16:9 YouTube widescreen default (1920x1080 landscape target)
- **Input modes:** prefer the visible/composer "Seedance 2.5 30s" route or `text_to_video` with raw GitHub image URLs inside the prompt. Use `image_to_video` only after it is verified to return 29-31 seconds in the current account/session.
- **Audio:** native — dialogue (lip-synced), sound effects, music

---

## MOVIE MODE — "FROST: Son of the Wild" HINDI YOUTUBE 16:9
### Hindi Output Lock

- This skill is only for the Hindi YouTube 16:9 package.
- The prompt instructions may be in English, but the generated video output must be 100% Hindi.
- Translate all dialogue, narrator lines, songs, title cards, place cards, time cards, visible on-screen text, and final titles/descriptions into natural Hindi / Hindustani in Devanagari.
- Use Hindi dubbing voices with accurate lip-sync. Do not speak English except proper names.
- For the opening title, use: "फ्रॉस्ट: जंगल का बेटा" and "निर्देशन: नूरुल ऐन".
### YouTube 16:9 Framing Lock

- This skill is only for the YouTube movie package.
- Generate landscape 16:9 video, target 1920x1080 composition.
- Keep faces, bodies, title cards, castle, forest, action, and important props inside safe widescreen margins.
- Show more left/right environment than the Reels version.
- Never crop like vertical shorts/reels.

Triggered when the user pastes a block that starts with `PART xx` (from the file `Bigfoot_Movie_Part_Prompts`) and/or attaches character images named like `C01_Lily_FACE.png`.

### Movie Mode workflow

1. **Read the PART block.** It already contains the full 30-second prompt, dialogue, SFX, music and the list of reference images. It is pre-approved by the user.
2. **Inspect every attached image with `Read`.** Match each file name to the character named in the prompt (C01 = Lily, C02 = King Magnus, C03 = Prince Damian, C04 = Bruno, C05 = Frost, C06 = Elder Orin, V = variant look, S = supporting, K = creature, L = location).
3. **Attach the single labelled board.** Use image 1 named in the part prompt and panel map. Its raw URL is a download source; the board must reach the generator's image input. Keep the complete request within three images.
4. **Attach a real handoff frame when supplied.** Image 2 is the previous part's approved end frame. For a same-scene edit it fixes the opening state; for an explicit scene/time/memory cut it provides context only. Reserve image 3 for optional detail. Never pass local Windows paths as remote URLs.
5. **Generate immediately using the 30-second Seedance route.** Prefer the visible/composer route named "Seedance 2.5 30s" when available. If a callable backend must be chosen, use `text_to_video` with all raw GitHub image URLs kept inside the prompt as character-reference URLs. Use `image_to_video` only if this exact route is already verified to return a real 29-31 second video in the current account/session; if it returns about 15 seconds once, do not use that route again for this movie.
6. **Pass the prompt exactly as written.** Do not shorten, summarize or remove any DIALOGUE, SFX or MUSIC line. Prepend the CHARACTER LOCK and append the GLOBAL RULES below.
   - If the video tool rejects or cuts the prompt because it is too long, shorten ONLY the visual description lines. Every DIALOGUE, SFX and MUSIC line stays word-for-word.
   - DIALOGUE time windows are a guide: every line must be spoken, in the given order, clearly, at a natural speed. Never drop a line to save time.
   - The "LOOK LOCK" line inside a PART is part of the prompt. Keep it.
   - Keep the paired `OPENING HANDOFF IN` and `ENDING HANDOFF OUT` sections for Parts 001-312. Parts 001-311 pass to the next part. Part 312 ends emotionally without a new cliffhanger.
7. **Verify duration before final delivery.** The output must be 29-31 seconds. If the first render is about 15 seconds, do not call it complete and do not retry the same backend path. Switch to the Seedance 2.5 30s composer/text route and prepend: `EXACT 30 SECOND OUTPUT REQUIRED. Use Seedance 2.5 30s route. Do not use any route that returns 15 seconds. Use the full 0-30s timeline.`
8. Deliver the video via `NotifyHuman` with a renderable video asset, plus the Facebook caption from the PART block.

### CHARACTER LOCK (prepend to every movie prompt)

```
CHARACTER LOCK: Keep every character's face, body, hair, fur color, outfit and proportions exactly identical to the attached reference images for the full 30 seconds. Do not change age, face shape, eye color or fur color. Reference mapping: [list each attached file -> character name].
LILY LOOK LOCK (only if Lily is in the part): Lily always looks 22–24 years old — young, innocent, sweet and beautiful, soft fair face, big blue eyes, honey-blonde hair. She never looks older, tired or wrinkled, even in parts set years later.
```

### Voice Lock (same voice for a character in every part)

| Character | Voice |
|---|---|
| NARRATOR | deep cinematic male Hindi storyteller, measured and dramatic |
| Lily (C01/V01-V04) | young adult female Hindi voice, soft, gentle and warm; trembles when scared |
| King Magnus (C02/V11) | mature deep rough commanding male Hindi voice, controlled and menacing |
| Prince Damian (C03/V10) | smooth young adult male Hindi voice, charming with cold arrogance |
| Bruno (C04/V09) | very deep slow warm gravelly Hindi voice; gentle, short simple sentences |
| Frost adult (C05/V08) | powerful young adult male Hindi voice, calm and strong |
| Frost baby (V05) | baby vocalizations; no adult male voice from an infant |
| Frost child (V06) | cheerful Hindi boy voice, same age stage as the image |
| Frost teen (V07) | energetic Hindi teenage boy voice, occasionally cracking |
| Tommy adult (V12) | friendly young adult male Hindi voice, nervous humor |
| Sarah adult (V13) | warm brave young adult female Hindi voice |
| Grace (S01/V14) | older caring Hindi female voice, more fragile in the older variant |
| Elder Orin (C06) | ancient very deep wise Hindi voice, restrained spiritual reverberation |
| Martha (S02) | warm grandmotherly Hindi voice |
| Hank (S03) | deep friendly practical Hindi male voice |
| Old Joe (S04) | slow raspy wise older Hindi male voice |
| Tommy/Sarah children (S05/S06) | distinct age-appropriate Hindi boy/girl voices |
| Captain Vex (S07) | harsh loud commanding Hindi male voice |
| Rose (S11) | older kind nervous Hindi female voice, usually whispering |

### GLOBAL RULES (append to every movie prompt)

```
AUDIO/VIDEO DURATION LOCK: Generate exactly one complete 30-second video. Use the full 0-30s timeline. Do not generate 5s, 10s, 15s, or any shorter version. If the model has a duration control, it must be set to 30 seconds, not auto/default.
AUDIO: Generate all spoken dialogue clearly with accurate lip-sync, in natural Hindi / Hindustani, using the exact lines and voices given, at the given timings. No line may be skipped. Every part must include at least 4 spoken lines whenever possible, with active character conversation across the full 30 seconds. Prefer 5-7 short, clear lines when the action allows. Include all listed sound effects and background music. Dialogue must stay louder and clearer than music and effects.
STYLE: Hyper-realistic cinematic 3D animation, Unreal Engine 5 quality, photorealistic skin, hair and fur, cinematic lighting, shallow depth of field, smooth camera movement, widescreen 16:9 cinematic movie frame.
SETTING: Fully American / Western. Pacific Northwest USA forests, Western dark-fantasy castle, American people and clothing. No Asian elements, no Asian architecture, no Asian dragons.
TEXT RULE: On-screen text is allowed only for intentional short cinematic title/location/time cards when the PART asks for it, for 2-3 seconds, such as "CEDAR HOLLOW, OREGON" or "THREE DAYS EARLIER". No subtitles for dialogue. NEGATIVE: no random text, no watermark, no logo, no extra limbs, no face morphing, no character drift, no gore, no blood spray, no nudity.
```

### Movie content rules

- **Punch rule:** every part has a 0–3 s hook, a 3–22 s story beat with dialogue, and a 22–30 s punch or cliffhanger (action, fun, emotion, twist or wow).
- **Duration verification rule:** after generation, check that the delivered file is 29-31 seconds. If it is around 15 seconds, regenerate immediately with exact 30-second wording and the same references.
- **Standalone rule:** every part makes sense on its own; at least 3 spoken dialogue lines, preferably 4-6 short lines; character voices + SFX + music in every part.
- **Safety:** Lily is always an adult (22+). Romance is shown only by looks, hand-holding, hugging, then fade to black. Deaths and violence are shown emotionally (slow motion, silhouettes, impact cuts), never graphic.

---

## Standard (non-movie) workflow

### 1. Planning
Design one 30-second arc: Opening 0–5 s, Development 5–20 s, Resolution 20–30 s. Include subjects, wardrobe, props, action beats, environment, style, lighting, camera, mood, pacing, dialogue, SFX and music.

### 2. Confirmation
Present: Duration 30 s, Model Seedance 2.5, Ratio, Style, Scene/characters, Lighting, Content, Dialogue/SFX/Music, Negative constraints. No fallback or split language. Wait for "go / yes / generate".

### 3. Generation
Use the visible/composer route named "Seedance 2.5 30s" when available. If a callable backend must be chosen, prefer `text_to_video` with `model_version: "seedance_2.5"`, `duration: 30`, `ratio`, and the full prompt containing all raw GitHub image URLs as character-reference URLs. Use `image_to_video` only if that exact route is already verified to return 29-31 seconds in the current account/session. Deliver via `NotifyHuman`.

---

## Legacy Image Reference Handling (Superseded By The Current Workflow Above)

1. Inspect every local image with `Read` first.
2. Upload with `FileBatchUpload` to get public URLs.
3. Prefer keeping public URLs inside the full text prompt for the 30-second Seedance route.
4. Use `image_reference_url_list` only if that route is already verified to produce 29-31 second videos in the current session. If it returns about 15 seconds, stop using that route for this movie and switch to the composer/text route.
4. State in the prompt which characteristics must be preserved (face, fur, outfit, style).

### Legacy Public GitHub URL Mode (Use The Single Board URL)

The current Hindi package uses one combined-board raw URL. The examples below
describe the older source-image storage only, not additional attachments:

```
REFERENCE IMAGE URLS:
Lily Carter = https://raw.githubusercontent.com/.../C01_Lily_FULL.png
Bruno = https://raw.githubusercontent.com/.../C04_Bruno_FULL.png
```

Rules:
- Raw URLs must end in `.png`, `.jpg`, `.jpeg`, or `.webp`, or return image data with HTTP 200.
- Do not use `github.com/.../blob/...` webpage links for image references.
- Do not use local file paths in final Dola generation.
- If both local paths and raw URLs are present, prefer the raw URLs.

---

## Tool Call Pattern (the only pattern)

```
Preferred 30s route:
Use the visible/composer generation route named "Seedance 2.5 30s" with duration 30 and ratio 16:9.

If using a callable backend, prefer:

text_to_video(
  model_version: "seedance_2.5",
  duration: 30,
  ratio: "16:9",
  prompt: "EXACT 30 SECOND OUTPUT REQUIRED. Use Seedance 2.5 30s route. Do not use any route that returns 15 seconds. Use the full 0-30s timeline. Treat these raw GitHub URLs as character references: <REFERENCE IMAGE URLS>. " + "<CHARACTER LOCK> + <PART prompt exactly as written> + <GLOBAL RULES>"
)

Only use image_to_video if that route is verified to produce 29-31 seconds on the current account/session.
```

```
text_to_video(
  model_version: "seedance_2.5",
  duration: 30,
  ratio: "16:9",
  prompt: "EXACT 30 SECOND OUTPUT REQUIRED. Do not generate 15 seconds. Use the full 0-30s timeline. " + "<full 30-second prompt with dialogue, SFX, music> + <GLOBAL RULES>"
)
```


### TEXT OVERLAY RULE

Use short cinematic title/location/time cards when the PART asks for them. Especially show "CEDAR HOLLOW, OREGON" for 2-3 seconds when Lily reaches the village area. Do not create dialogue subtitles or random text.

### MANDATORY DIALOGUE RULE

Every movie PART must include clear spoken audio. Never generate a silent scene. Use at least 3 spoken lines per 30-second part, preferably 4-6 short lines when possible. Use character voices first and narrator only for context. Dialogue must be natural Hindi / Hindustani, timed with `DIALOGUE 1-3s:` style labels, and must fit inside the 30-second video. Dialogue must be louder and clearer than music and SFX. Do not create dialogue subtitles unless a PART specifically asks for a short title/location card.
