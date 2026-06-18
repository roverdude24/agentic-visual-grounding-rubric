# .windsurfrules

Use Code-Grounded Vision (CGV) whenever a task depends on pixels, coordinates, frames, screenshots, overlays, layout, generated media, or visual continuity.

## Required workflow

1. Gather deterministic evidence first.
   - Use FFmpeg, Pillow, OCR, hashes, dimensions, crops, overlays, diffs, and box math.

2. Reduce the visual context.
   - Send a crop, overlay, or short extracted frame set instead of full raw media.
   - Keep artifact paths and dimensions in the working notes.

3. Call only image-capable models for visual judgment.
   - Use VLMs for semantic questions.
   - Do not use VLMs for frame counts, measurements, overlap, or bounds that code can verify.

4. Validate and verify.
   - Require structured output.
   - Verify VLM coordinates with deterministic checks.
   - Mark unverified visual regions as hypotheses.

5. Fail closed.
   - Stop when no image-capable provider is configured.
   - Stop when auth, registry lookup, or image upload fails.
   - Never answer a visual question with a text-only fallback.

## Output discipline

When answering, state:

- The local evidence produced.
- The artifact sent to the VLM, if any.
- The VLM judgment, if any.
- The deterministic checks that passed or still remain.
- Any caveat from occlusion, compression, crop limits, or low resolution.

Skip this workflow for text-only work.
