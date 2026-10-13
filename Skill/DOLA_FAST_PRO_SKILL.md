---
name: frost-dola-fast-pro
description: "Fast Dola AI production workflow for FROST: Son of the Wild using Seedance 2.5 30s. Use for creating one complete 30-second vertical cinematic movie part at a time from approved character references."
---

# FROST Dola Fast Pro Skill

Use this skill for the movie project **FROST: Son of the Wild** when generating a Dola AI video.

## Hard Locks

- Model: Seedance 2.5
- Duration: 30 seconds
- Ratio: 9:16 vertical
- Output: one complete 30-second video per prompt
- Dialogue: natural American English
- Setting: fully American / Western, no Asian elements
- Style: hyper-realistic cinematic 3D animation, Unreal Engine 5 quality
- No subtitles, no watermark, no logo, no on-screen captions

## Character Reference Rule

Use the approved character images from:

`C:\Users\user\Desktop\Bigfoot_Movie\Characters`

Lock every attached character for the full video:

- same face
- same age
- same hair / fur
- same outfit logic
- same body proportions
- no character drift

If Lily appears, always include:

`LILY LOOK LOCK: Lily is always a young adult woman, 22-24 years old, innocent, beautiful, American, and never aged or wrinkled.`

If Frost appears, always include:

`FROST LOCK: Frost is an American Pacific Northwest white Bigfoot / Sasquatch, not Hanuman, not a deity, not Asian mythology.`

## Fast Prompt Template

Paste this structure into Dola:

```text
Seedance 2.5 30s

TITLE:
PART:
FORMAT: vertical 9:16, one complete 30-second cinematic video

CHARACTER LOCK:
[List attached character image names and who they are.]

SETTING RULE:
Setting and people are fully American / Western, no Asian elements.

STYLE:
Hyper-realistic cinematic 3D animation, Unreal Engine 5 quality, photorealistic skin, hair and fur, cinematic lighting, shallow depth of field, smooth handheld camera, vertical 9:16.

SCENE:
[Where the scene happens.]

0-3s HOOK:
[Immediate shocking action or emotion.]

3-22s STORY:
[Main action and dialogue.]

22-30s PUNCH / CLIFFHANGER:
[Final twist/action/wow moment.]

DIALOGUE:
[Character name] ([voice lock]) says: "[exact line]"

SFX:
[Sound effects with timing.]

MUSIC:
[Background score.]

NEGATIVE:
No subtitles, no captions, no watermark, no logo, no Asian elements, no anime, no cartoon, no face morphing, no character drift, no extra limbs, no gore, no nudity.
```

## Fast Generation Order

1. Generate Part 01 as the first test.
2. If the result is usable, continue Part 02 to Part 10.
3. Use only individual character references first.
4. Avoid group people references unless the user later asks for them.

## First Test Prompt: Part 01

Use the Part 01 prompt from:

`C:\Users\user\Desktop\Bigfoot_Movie\Prompts\Parts_001-010.txt`

If the exact variant/creature images are missing, use text-only or the closest available individual references first, then regenerate later after variants/creatures are complete.
