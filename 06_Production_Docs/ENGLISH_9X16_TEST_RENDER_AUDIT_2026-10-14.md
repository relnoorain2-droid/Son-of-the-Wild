# English 9:16 Test Render Audit - 2026-10-14

Audit source: `C:\Users\relno\Desktop\dola video\2026-10-14 02-52 - 312 videos`

Scope: 78 random test renders, not a sequential export. Missing part numbers are expected because the renders were made for spot testing.

## Main Problems Found

- Face drift: Lily, Rose, village children, and some crowd faces change between shots when the prompt does not force exact reference-image identity.
- Creature drift: Bruno and Frost sometimes become cartoon, toy-like, dog-like, wolf-like, or too human instead of locked to the required Bigfoot/Frost reference.
- Wrong character placement: Rose appears too centrally or in rooms where she should only be hidden at the side.
- Camera problem: King Magnus and several emotional reaction shots are too close to the camera, making faces distorted or uncomfortable.
- Dialogue problem: many prompts repeat generic lines and allow unnecessary speech during action, chase, fight, or visual suspense moments.
- Prompt contamination: older prompts include Facebook/Reels captions, Dola status checklists, notes, `Punch/Status` labels, and malformed dialogue such as `this time."...`.
- Self-contained problem: many parts depend on previous memory, but Dola treats each prompt separately. Every part must restate its image URLs, character locks, setting, action, dialogue, and final hook.

## Prompt Rules For Restart

- Work only on English 9:16 reel prompts until this restart is clean.
- Create prompts in 10-part batches.
- Each prompt starts with the part number and title.
- Each prompt includes the exact direct GitHub raw image URLs needed for that part.
- Each prompt is self-contained; no part should depend on Dola remembering a previous render.
- Use only `-------` as the separator in batch files.
- Keep prompt text pure for video creation only: no captions, no checklists, no notes, no upload reminders.
- Dialogue must be unique to the scene. Use silence, reaction, music, breathing, footsteps, and camera movement instead of filler dialogue where action is stronger.
- Keep Rose hidden at the side unless the story beat explicitly requires her to warn someone.
- Use medium and wide shots for King Magnus; no extreme close-up.
- Lock style to hyper-realistic cinematic 3D. Explicitly reject cartoon, anime, toy, plastic, dog-like, wolf-like, white-dog Frost, human-looking Bigfoot, melted face, face swap, and character drift.
- Frost age must be restated every time he appears: baby, child, teen, young adult, or powered form. His fast growth is because of his mixed wild/royal genes.

## Current Clean Batches

- Manual clean English 9:16 batch files now live in `ZDola_Combined_Prompts/English_9x16_Batches/`.
- Final combined file: `ZDola_Combined_Prompts/English_9x16_ALL_312_CLEAN.txt`.
- Individually authored scene rewrites cover Parts 001-312. Shared formatting is assembled programmatically; generated video quality still requires visual review. Earlier partial combined progress files have been retired to avoid import confusion.
- The prior controller-generated all-312 combined file was removed to avoid risk.
- The final all-312 combined file should be recreated only after every batch has been manually rewritten.
