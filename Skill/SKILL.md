---
name: zakariya-seedance-2-5-30s
description: "Seedance 2.5 video generation, hard-locked to one single 30-second 9:16 video per call, with full dialogue, sound effects and music. Use for Seedance 2.5, 30-second videos, cinematic animation, and especially for the Frost Son of the Wild Bigfoot movie parts (PART 01 to PART 180) that use character reference images. Never splits into multiple clips."
---

# Zakariya Seedance 2.5 — 30s Hard Lock (Movie Edition)

## Hard Lock (non-negotiable, overrides everything below)

- **Duration is locked at 30 seconds.** Always pass `duration: 30`.
- **One single continuous segment.** One tool call = one complete 30-second video.
- **Model is locked to Seedance 2.5.** Always pass `model_version: "seedance_2.5"`.
- **Ratio is locked to 9:16** (vertical reels) unless the user explicitly asks for another ratio. If a PART block contains `FORMAT: YOUTUBE 16:9`, it is the YouTube version: use ratio 16:9 and write "widescreen 16:9" instead of "vertical 9:16" in the GLOBAL RULES.
- **Audio is ON.** Every video must include spoken dialogue, sound effects and background music exactly as written in the prompt.

### Anti-spreading rules — never do any of these:

- Never split into two 15-second clips or any multi-part sequence inside one request.
- Never propose, offer or mention a two-segment / multi-clip / shorter-compressed delivery.
- Never present a "platform limitation", "tool cap", fallback, Plan B or workaround.
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
- **Ratio:** 9:16 default (also supports 21:9, 16:9, 4:3, 1:1, 3:4)
- **Input modes:** `text_to_video`, `image_to_video`
- **Audio:** native — dialogue (lip-synced), sound effects, music

---

## MOVIE MODE — "FROST: Son of the Wild"

Triggered when the user pastes a block that starts with `PART xx` (from the file `Bigfoot_Movie_Part_Prompts`) and/or attaches character images named like `C01_Lily_FACE.png`.

### Movie Mode workflow

1. **Read the PART block.** It already contains the full 30-second prompt, dialogue, SFX, music and the list of reference images. It is pre-approved by the user.
2. **Inspect every attached image with `Read`.** Match each file name to the character named in the prompt (C01 = Lily, C02 = King Magnus, C03 = Prince Damian, C04 = Bruno, C05 = Frost, C06 = Elder Orin, V = variant look, S = supporting, K = creature, L = location).
3. **Use public image URLs first.** If the PART prompt contains a section named `DIRECT IMAGE URLS FOR DOLA`, `REFERENCE IMAGE URLS`, or direct `https://raw.githubusercontent.com/.../*.png` / `.jpg` / `.webp` links, use those URLs directly in `image_reference_url_list`. Do not ask the user to upload those same images again.
4. **Upload only when URLs are missing.** If the PART prompt lists only local files or attached files, inspect every attached image with `Read`, upload with `FileBatchUpload`, and use only the returned URLs in `image_reference_url_list`. Never pass local Windows paths like `C:\...` to the video tool.
5. **Generate immediately** with `image_to_video` (or `text_to_video` only if no image references exist). Do not ask for confirmation again — a pasted PART block counts as "go". Only ask if a required character reference is missing; then say exactly which character/image is missing in one line.
6. **Pass the prompt exactly as written.** Do not shorten, summarize or remove any DIALOGUE, SFX or MUSIC line. Prepend the CHARACTER LOCK and append the GLOBAL RULES below.
   - If the video tool rejects or cuts the prompt because it is too long, shorten ONLY the visual description lines. Every DIALOGUE, SFX and MUSIC line stays word-for-word.
   - DIALOGUE time windows are a guide: every line must be spoken, in the given order, clearly, at a natural speed. Never drop a line to save time.
   - The "LOOK LOCK" line inside a PART is part of the prompt. Keep it.
6. Deliver the video via `NotifyHuman` with a renderable video asset, plus the Facebook caption from the PART block.

### CHARACTER LOCK (prepend to every movie prompt)

```
CHARACTER LOCK: Keep every character's face, body, hair, fur color, outfit and proportions exactly identical to the attached reference images for the full 30 seconds. Do not change age, face shape, eye color or fur color. Reference mapping: [list each attached file -> character name].
LILY LOOK LOCK (only if Lily is in the part): Lily always looks 22–24 years old — young, innocent, sweet and beautiful, soft fair face, big blue eyes, honey-blonde hair. She never looks older, tired or wrinkled, even in parts set years later.
```

### Voice Lock (same voice for a character in every part)

| Character | Voice |
|---|---|
| NARRATOR | deep, cinematic American male movie-trailer voice, slow and dramatic |
| Lily (C01) | young American woman, 22, soft gentle warm voice, slight small-town accent, trembles when scared |
| King Magnus (C02) | deep, rough, commanding American male, 55, slow and menacing, booming when angry |
| Prince Damian (C03) | smooth charming American male, 27, arrogant, cold smirking tone |
| Bruno (C04) | very deep slow warm gentle-giant voice, gravelly, short simple English sentences |
| Frost (C05) | deep powerful young male voice, early 20s, calm and strong, thunderous roar when angry |
| Tommy grown up (V12) | friendly young American man, about 22, a little nervous, joking |
| Sarah grown up (V13) | warm, brave young American woman, about 19 |
| Grace years later (V14) | old, trembling, caring American woman's voice |
| Kid Frost (V06) | cheerful young boy voice, about 8 years old, slightly deep for a kid, American accent |
| Teen Frost (V07) | energetic teenage boy voice, about 15, voice cracking sometimes, American accent |
| Elder Orin (C06) | ancient very deep echoing wise voice, reverberating like it comes from the sky |
| Grace (S01) | soft tired caring older American woman |
| Martha (S02) | warm grandmotherly voice, slight Southern drawl |
| Hank (S03) | deep friendly rural American male |
| Old Joe (S04) | slow raspy wise old man |
| Tommy (S05) | excited young boy |
| Sarah (S06) | small cute girl |
| Captain Vex (S07) | harsh loud threatening male |
| Rose (S11) | old kind British-accented castle maid, whispering, nervous |

### GLOBAL RULES (append to every movie prompt)

```
AUDIO: Generate all spoken dialogue clearly with accurate lip-sync, in natural American English, using the exact lines and voices given, at the given timings. No line may be skipped. Every part must include at least 4 spoken lines whenever possible, with active character conversation across the full 30 seconds. Prefer 5-7 short, clear lines when the action allows. Include all listed sound effects and background music. Dialogue must stay louder and clearer than music and effects.
STYLE: Hyper-realistic cinematic 3D animation, Unreal Engine 5 quality, photorealistic skin, hair and fur, cinematic lighting, shallow depth of field, smooth camera movement, vertical 9:16.
SETTING: Fully American / Western. Pacific Northwest USA forests, Western dark-fantasy castle, American people and clothing. No Asian elements, no Asian architecture, no Asian dragons.
TEXT RULE: On-screen text is allowed only for intentional short cinematic title/location/time cards when the PART asks for it, for 2-3 seconds, such as "CEDAR HOLLOW, OREGON" or "THREE DAYS EARLIER". No subtitles for dialogue. NEGATIVE: no random text, no watermark, no logo, no extra limbs, no face morphing, no character drift, no gore, no blood spray, no nudity.
```

### Movie content rules

- **Punch rule:** every part has a 0–3 s hook, a 3–22 s story beat with dialogue, and a 22–30 s punch or cliffhanger (action, fun, emotion, twist or wow).
- **Standalone rule:** every part makes sense on its own; at least 3 spoken dialogue lines, preferably 4-6 short lines; character voices + SFX + music in every part.
- **Safety:** Lily is always an adult (22+). Romance is shown only by looks, hand-holding, hugging, then fade to black. Deaths and violence are shown emotionally (slow motion, silhouettes, impact cuts), never graphic.

---

## Standard (non-movie) workflow

### 1. Planning
Design one 30-second arc: Opening 0–5 s, Development 5–20 s, Resolution 20–30 s. Include subjects, wardrobe, props, action beats, environment, style, lighting, camera, mood, pacing, dialogue, SFX and music.

### 2. Confirmation
Present: Duration 30 s, Model Seedance 2.5, Ratio, Style, Scene/characters, Lighting, Content, Dialogue/SFX/Music, Negative constraints. No fallback or split language. Wait for "go / yes / generate".

### 3. Generation
Call `text_to_video` or `image_to_video` with `model_version: "seedance_2.5"`, `duration: 30`, `ratio`, full `prompt`, and `image_reference_url_list` (URLs from `FileBatchUpload` only). Deliver via `NotifyHuman`.

---

## Image-to-Video

1. Inspect every local image with `Read` first.
2. Upload with `FileBatchUpload` to get public URLs.
3. Use only those URLs in `image_reference_url_list`.
4. State in the prompt which characteristics must be preserved (face, fur, outfit, style).

### Public GitHub URL Mode

When a prompt includes raw GitHub image links, use them directly:

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
image_to_video(
  model_version: "seedance_2.5",
  duration: 30,
  ratio: "9:16",
  prompt: "<CHARACTER LOCK> + <PART prompt exactly as written> + <GLOBAL RULES>",
  image_reference_url_list: ["<url-from-FileBatchUpload>", ...]
)
```

```
text_to_video(
  model_version: "seedance_2.5",
  duration: 30,
  ratio: "9:16",
  prompt: "<full 30-second prompt with dialogue, SFX, music> + <GLOBAL RULES>"
)
```


### TEXT OVERLAY RULE

Use short cinematic title/location/time cards when the PART asks for them. Especially show "CEDAR HOLLOW, OREGON" for 2-3 seconds when Lily reaches the village area. Do not create dialogue subtitles or random text.

### MANDATORY DIALOGUE RULE

Every movie PART must include clear spoken audio. Never generate a silent scene. Use at least 3 spoken lines per 30-second part, preferably 4-6 short lines when possible. Use character voices first and narrator only for context. Dialogue must be natural American English, timed with `DIALOGUE 1-3s:` style labels, and must fit inside the 30-second video. Dialogue must be louder and clearer than music and SFX. Do not create dialogue subtitles unless a PART specifically asks for a short title/location card.
