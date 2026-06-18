# GitHub Copilot instructions

Apply Code-Grounded Vision (CGV) to visual and spatial work.

## Use CGV for

- Video frames, scene boundaries, continuity, and QC.
- Screenshots, UI layout, clipped text, overlap, and alignment.
- Generated images or videos checked against prompts.
- Logo, watermark, object, pose, segmentation, depth, or crop questions.

## Do not use CGV for

- Text-only code changes.
- Documentation edits with no visual artifact.
- Dependency, package, or configuration work.
- Research that does not inspect an image or layout.

## Required behavior

- Inspect with code first: frames, crops, overlays, diffs, OCR, dimensions, hashes, and box math.
- Prefer the smallest useful artifact over full raw media.
- Use VLMs only for semantic judgment.
- Treat VLM boxes and coordinates as hypotheses.
- Verify bounds, IoU, intersections, and measurements in code.
- Fail closed if no image-capable model is available or the provider fails.
- Never replace vision with a text-only fallback.
- Return structured evidence: answer, evidence, confidence, caveats, regions, and pending deterministic checks.

## Review standard

Reject visual answers that lack pixel evidence, cite unverified coordinates, omit crop or artifact provenance, or rely on a text-only model for an image question.
