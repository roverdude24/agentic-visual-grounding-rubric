# Code-Grounded Vision (CGV)

CGV is an agent rubric for visual work. It makes the agent inspect pixels with code before it asks a vision model for judgment.

Use CGV when an agent must reason about images, video frames, screenshots, overlays, layout, continuity, or generated media.

---

## 1-minute setup

1. Copy the matching rule file into your agent workspace:

| Agent | Copy from this repo | Place in your project |
| :--- | :--- | :--- |
| Cursor | `agent-rules/cursor-rules.md` | `.cursorrules` |
| Claude Code | `agent-rules/claude-code.md` | `CLAUDE.md` |
| Windsurf | `agent-rules/windsurf-rules.md` | `.windsurfrules` |
| GitHub Copilot | `agent-rules/copilot-instructions.md` | `.github/copilot-instructions.md` |

2. Add the skill file if your agent supports reusable skills:

```text
skill/visual_grounding_rubric.md
```

3. Tell the agent:

```text
Use CGV for any visual or spatial task. Inspect with code first. Ask a vision model only for semantic judgment. Fail closed if no image-capable model is configured.
```

That is enough for most teams. The Python package is optional; it gives agents small CPU helpers for frames, crops, overlays, diffs, artifact manifests, schemas, and model checks.

---

## What CGV changes

A plain VLM can describe an image, but it cannot measure reliably. CGV splits the job:

1. Code extracts evidence: frames, crops, diffs, hashes, dimensions, OCR, bounding boxes, and overlays.
2. A VLM judges only the focused artifact it receives.
3. Code verifies coordinates, overlap, bounds, and structured output.

This keeps visual claims tied to pixels and stops text-only fallbacks from pretending to see.

---

## When to use CGV

Use CGV for:

- Video QC, scene boundaries, keyframes, and continuity audits.
- UI screenshots, clipped text, overlap, z-index, and alignment.
- Generated image or video checks against prompt constraints.
- Logo, watermark, object, face, pose, depth, or segmentation checks.
- Any answer that depends on pixels, coordinates, or visual evidence.

Skip CGV for:

- Text-only coding, refactoring, package config, or documentation.
- Web research with no image or layout question.
- Questions that a normal unit test or type check can answer.

---

## The CGV contract for agents

Use these rules in Cursor, Claude Code, Windsurf, Copilot, or any agent runner.

1. **Inspect with code first.** Use local CPU tools before a VLM: FFmpeg, Pillow, OpenCV-style geometry, OCR, hashes, and diffs.
2. **Send focused artifacts.** Crop or overlay the relevant region. Do not inject raw full-resolution images into the main context.
3. **Treat VLM boxes as hypotheses.** Verify coordinates with crop-and-re-ask, overlay review, IoU, bounds checks, or pixel math.
4. **Fail closed.** If the model cannot accept images, the provider is missing, or auth fails, stop with a configuration error. Never use a text-only answer as visual evidence.
5. **Return structured evidence.** Require a schema with answer, evidence, confidence, caveats, regions, and whether deterministic verification remains.

---

## Install the optional CPU helpers

Requirements: Python 3.9+ and FFmpeg on `PATH`.

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg
```

```bash
git clone https://github.com/your-username/agentic-visual-grounding-rubric.git
cd agentic-visual-grounding-rubric
python3 -m pip install -e .
```

Run a deterministic local audit:

```bash
python3 -m cgv.examples.frame_audit --input /path/to/shot.mp4 --out runs/demo
```

Outputs:

- `runs/demo/frames/`: extracted keyframes.
- `runs/demo/diffs/`: pixel-difference images.
- `runs/demo/manifest.json`: `local://` artifacts with hashes, sizes, paths, and dimensions.
- A VLM-ready prompt that references focused artifacts instead of raw media.

---

## Optional VLM configuration

CGV does not require a local GPU. Use your agent platform's image-capable model or provider.

```bash
export CGV_VLM_PROVIDER="openai"   # openai, anthropic, google, or your runtime name
export OPENAI_API_KEY="your-api-key"
```

Then run the VLM-gated example:

```bash
python3 -m cgv.examples.frame_audit --input /path/to/shot.mp4 --out runs/demo --ask-vlm
```

The routing layer must reject text-only models. See [`docs/vlm-configuration.md`](docs/vlm-configuration.md).

---

## Portable grounding schema

Agents should ask the VLM for this JSON shape, then validate it before using the answer.

```json
{
  "answer": true,
  "evidence": "The red box encloses the visible logo in the lower-right corner; no other logo appears in the crop.",
  "confidence": 0.86,
  "caveats": "The crop is slightly compressed.",
  "regions": [
    { "x": 812, "y": 438, "w": 96, "h": 42, "label": "logo", "frame_id": "frame_03" }
  ],
  "needs_deterministic_check": true
}
```

The Python model lives in `cgv/schemas.py` as `VisualGroundingResult`.

---

## Agent rule templates

- [`agent-rules/cursor-rules.md`](agent-rules/cursor-rules.md)
- [`agent-rules/claude-code.md`](agent-rules/claude-code.md)
- [`agent-rules/windsurf-rules.md`](agent-rules/windsurf-rules.md)
- [`agent-rules/copilot-instructions.md`](agent-rules/copilot-instructions.md)

Each file contains the same CGV contract, adapted to the target agent's project-rule format.

---

## Documentation

- [`docs/human-agent-loop.md`](docs/human-agent-loop.md): how a human and agent cooperate with CGV.
- [`docs/vlm-configuration.md`](docs/vlm-configuration.md): provider setup and fail-closed behavior.
- [`docs/evaluation.md`](docs/evaluation.md): before/after metrics and JSONL labels.

---

## Repository guide

```text
agentic-visual-grounding-rubric/
├── README.md
├── agent-rules/
│   ├── claude-code.md
│   ├── copilot-instructions.md
│   ├── cursor-rules.md
│   └── windsurf-rules.md
├── cgv/
│   ├── manifest.py
│   ├── media.py
│   ├── routing.py
│   └── schemas.py
├── docs/
│   ├── evaluation.md
│   ├── human-agent-loop.md
│   └── vlm-configuration.md
├── skill/
│   ├── system_prompt_template.txt
│   └── visual_grounding_rubric.md
└── tests/
```

---

## Development

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest
```

Tests cover media helpers, artifact registration, model capability checks, and box-overlap math.

---

## License

Apache License 2.0. See [LICENSE](LICENSE).
