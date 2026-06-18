# .cursorrules

Use Code-Grounded Vision (CGV) for every visual or spatial task.

## CGV contract

- Inspect with deterministic code before asking a VLM.
- Use local CPU tools for frames, crops, overlays, diffs, OCR, dimensions, hashes, and box math.
- Send only focused crops or overlays to a VLM. Do not inject raw full-resolution images into the main context.
- Treat VLM coordinates and boxes as hypotheses. Verify them with bounds checks, IoU, intersection math, crop-and-re-ask, or overlay review.
- Fail closed when no image-capable model is configured, the provider is unavailable, auth fails, or the model is text-only.
- Never use a text-only model response as visual evidence.
- Return structured evidence with answer, evidence, confidence, caveats, regions, and whether deterministic verification remains.

## Cursor workflow

When the user asks about an image, screenshot, video, layout, generated frame, or visual defect:

1. Locate the asset path.
2. Extract or crop the smallest useful visual artifact.
3. Register or name the artifact path and include dimensions when available.
4. Ask an image-capable model only for semantic judgment.
5. Validate the response schema.
6. Verify all geometry claims in code.
7. Answer with observed evidence, model judgment, caveats, and remaining uncertainty.

Skip CGV for text-only coding, refactoring, docs, and package configuration.
