# Visual Grounding Rubric

Use this skill for visual or spatial tasks: video frames, screenshots, layouts, overlays, generated images, and generated video. Inspect with code before asking a VLM for judgment.

---

## Trigger conditions

Load this rubric for:

- Video QC, keyframes, scene boundaries, and continuity audits.
- UI layout inspection, screenshot debugging, clipped text, overlap, and alignment.
- Contrast checks, logo placement, watermark placement, and visual constraints.
- Generated image or video QC against a prompt or storyboard.

Skip it for text-only code, research, documentation, or package config.

---

## Protocol

1. **Start with deterministic evidence.** Use CPU code to extract frames, crop regions, compute diffs, draw overlays, check dimensions, hash files, or measure boxes.
2. **Register artifacts.** Store generated images or clips as paths or `local://` URIs with labels, purpose, dimensions, and hashes.
3. **Ask a VLM only for semantics.** Send the exact crop or overlay. Do not send full raw media when a focused artifact answers the question.
4. **Validate the VLM response.** Require structured output and reject malformed answers.
5. **Verify geometry with code.** Treat VLM coordinates as proposals. Check bounds, overlap, IoU, and intersections locally.
6. **Fail closed.** If no image-capable model is configured, stop with a configuration error. Never use a text-only model as a visual fallback.

---

## Routing rubric

Ask these questions in order:

1. **Can code answer it?**
   - Frame count, resolution, file type, crop bounds, duplicate frames, histograms, pixel diffs, OCR text, and box overlap should run locally.
   - If code can answer, do not call a VLM.

2. **Does the task need semantic judgment?**
   - Identity, style, expression, obstruction, scene meaning, or prompt adherence may need a VLM.
   - Send the smallest useful crop or overlay.

3. **Does the task need segmentation, depth, or pose?**
   - Route to a configured vision adapter or remote GPU service.
   - If none exists, report the missing capability. Do not emulate large vision models on CPU.

---

## VLM response schema

Require this shape or a stricter equivalent:

```json
{
  "answer": true,
  "evidence": "Concrete visual cues tied to the crop or overlay.",
  "confidence": 0.0,
  "caveats": "Ambiguity, occlusion, compression, or resolution limits.",
  "regions": [
    { "x": 0, "y": 0, "w": 1, "h": 1, "label": "object", "frame_id": "optional" }
  ],
  "needs_deterministic_check": true
}
```

Use `needs_deterministic_check: true` when any coordinate, boundary, count, or overlap claim still needs code verification.

---

## Agent checklist

Before answering a visual question:

- Name the local evidence you produced.
- Name each artifact you sent to the VLM.
- State whether the VLM had image input.
- Separate observed pixels from model judgment.
- Mark unverified VLM boxes as hypotheses.
- Stop if the provider, model, or image input path fails.
