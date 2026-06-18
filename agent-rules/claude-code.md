# CLAUDE.md

## Code-Grounded Vision

Use Code-Grounded Vision (CGV) for visual or spatial tasks: video frames, screenshots, UI layouts, overlays, generated images, generated video, continuity checks, logo placement, watermark placement, and visual prompt adherence.

## Rules

1. Inspect with code first.
   - Extract frames, crop regions, compute pixel diffs, draw overlays, check dimensions, hash files, run OCR, or measure boxes before asking a VLM.

2. Send focused artifacts.
   - Use the smallest crop or overlay that can answer the question.
   - Keep raw base64 images and full-resolution media out of the main context unless the task truly needs them.

3. Use a VLM only for semantic judgment.
   - Ask the VLM about identity, style, expression, obstruction, scene meaning, or prompt adherence.
   - Do not ask it to do math that code can do.

4. Treat VLM boxes as hypotheses.
   - Verify coordinates with bounds checks, IoU, intersection math, crop-and-re-ask, or overlay review.

5. Fail closed.
   - If no image-capable model is configured, or the provider fails, stop with a configuration error.
   - Never substitute a text-only completion for vision.

6. Return structured evidence.
   - Separate observed pixels from VLM judgment.
   - Include answer, evidence, confidence, caveats, regions, and whether deterministic checks remain.

## Non-visual work

Do not invoke CGV for text-only coding, refactoring, documentation, dependency updates, or research with no visual artifact.
