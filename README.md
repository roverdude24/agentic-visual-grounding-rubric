# Code-Grounded Vision (CGV)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](pyproject.toml)
[![Agents & Harnesses Compatibility](https://img.shields.io/badge/compatibility-OMP%20%7C%20LangChain%20%7C%20Cursor%20%7C%20Claude%20Code-orange.svg)](#1-minute-setup)

CGV is a visual reasoning rubric and CPU toolset for AI agents. It makes the agent inspect pixels with code before it asks a vision model for judgment.

Use CGV when an agent must reason about images, video frames, screenshots, overlays, layout, continuity, or generated media.

────────────────────────────────────────

## CGV in 30 Seconds (For Non-Technical Managers)

| The problem | The CGV answer |
| :--- | :--- |
| Vision models can describe an image, but they often guess at exact locations, sizes, and small defects. | CGV makes the agent measure and crop with local code before asking the vision model to judge. |
| Full-resolution images and videos are expensive to send to remote models. | CGV sends focused crops, overlays, and frame evidence instead of raw media. |
| A text-only fallback can sound confident without seeing the image. | CGV fails closed when no image-capable model is configured. |
| Project reviews need proof, not impressions. | CGV returns structured evidence: coordinates, crops, hashes, caveats, and verification status. |

**Plain analogy:** Sending a raw high-res image to a VLM is like sending a satellite photo to a remote inspector to verify a tiny scratch on a building's roof. It is expensive, slow, and the inspector may guess. CGV is like using a local drone to crop the scratch first, then sending only the high-res close-up. It is 10x faster and mathematically accurate because code supplies the crop and coordinates.

**Outcome:** CGV turns visual QA from "the model thinks so" into "the pixels show this, and here is the crop."

────────────────────────────────────────

## At a Glance

| Question | Short answer |
| :--- | :--- |
| Who is it for? | Product teams, project managers, QA reviewers, designers, researchers, and agent builders. |
| What does it add? | A simple contract for visual tasks: inspect locally, ask narrowly, verify deterministically. |
| Do I need a GPU? | No. CGV uses CPU helpers and your existing image-capable model provider. |
| Do I need to install the Python package? | No for the rule files. Yes if you want frame, crop, diff, manifest, and schema helpers. |
| What does success look like? | Smaller model calls, clearer artifacts, fewer visual guesses, and evidence that reviewers can inspect. |

────────────────────────────────────────

## 1-minute setup

### 1. Add the rule file for your agent

| Agent | Copy from this repo | Place in your project |
| :--- | :--- | :--- |
| Cursor | `agent-rules/cursor-rules.md` | `.cursorrules` |
| Claude Code | `agent-rules/claude-code.md` | `CLAUDE.md` |
| Windsurf | `agent-rules/windsurf-rules.md` | `.windsurfrules` |
| GitHub Copilot | `agent-rules/copilot-instructions.md` | `.github/copilot-instructions.md` |

### 2. Add the reusable skill, if your agent supports skills

```text
skill/visual_grounding_rubric.md
```

### 3. Tell the agent how to route visual work

```text
Use CGV for any visual or spatial task. Inspect with code first. Ask a vision model only for semantic judgment. Fail closed if no image-capable model is configured.
```

That is enough for most teams. The Python package is optional. It gives agents small CPU helpers for frames, crops, overlays, diffs, artifact manifests, schemas, and model checks.

────────────────────────────────────────

## What CGV Changes

A plain VLM can describe an image, but it cannot measure reliably. CGV splits the work into three parts.

| Step | Owner | Evidence produced |
| :--- | :--- | :--- |
| 1. Inspect | Local code | Frames, crops, dimensions, hashes, OCR, diffs, boxes, and overlays. |
| 2. Judge | Image-capable model | A narrow answer about the focused artifact. |
| 3. Verify | Local code | Bounds checks, overlap math, coordinate checks, and schema validation. |

This keeps visual claims tied to pixels. It also stops text-only fallbacks from pretending to see.

────────────────────────────────────────

## When to Use CGV

| Use CGV for | Skip CGV for |
| :--- | :--- |
| Video QC, scene boundaries, keyframes, and continuity audits. | Text-only coding, refactoring, package config, or documentation. |
| UI screenshots, clipped text, overlap, z-index, and alignment. | Web research with no image or layout question. |
| Generated image or video checks against prompt constraints. | Questions that a normal unit test or type check can answer. |
| Logo, watermark, object, face, pose, depth, or segmentation checks. | Pure copyediting, summarization, or planning. |
| Any answer that depends on pixels, coordinates, or visual evidence. | Anything that does not require visual proof. |

────────────────────────────────────────

## The CGV Contract for Agents

Use these rules in Cursor, Claude Code, Windsurf, Copilot, OMP, LangChain, AutoGPT, CrewAI, AutoGen, or any agent runner/framework.

| Rule | What it means |
| :--- | :--- |
| **Inspect with code first.** | Use local CPU tools before a VLM: FFmpeg, Pillow, OpenCV-style geometry, OCR, hashes, and diffs. |
| **Send focused artifacts.** | Crop or overlay the relevant region. Do not inject raw full-resolution images into the main context. |
| **Treat VLM boxes as hypotheses.** | Verify coordinates with crop-and-re-ask, overlay review, IoU, bounds checks, or pixel math. |
| **Fail closed.** | If the model cannot accept images, the provider is missing, or auth fails, stop with a configuration error. Never use a text-only answer as visual evidence. |
| **Return structured evidence.** | Require a schema with answer, evidence, confidence, caveats, regions, and whether deterministic verification remains. |

────────────────────────────────────────

## Install the Optional CPU Helpers

Requirements: Python 3.9+ and FFmpeg on `PATH`.

### FFmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### Python package

```bash
git clone https://github.com/your-username/agentic-visual-grounding-rubric.git
cd agentic-visual-grounding-rubric
python3 -m pip install -e .
```

### Deterministic local audit

```bash
python3 -m cgv.examples.frame_audit --input /path/to/shot.mp4 --out runs/demo
```

Outputs:

| Output | Purpose |
| :--- | :--- |
| `runs/demo/frames/` | Extracted keyframes. |
| `runs/demo/diffs/` | Pixel-difference images. |
| `runs/demo/manifest.json` | `local://` artifacts with hashes, sizes, paths, and dimensions. |
| VLM-ready prompt | References focused artifacts instead of raw media. |

────────────────────────────────────────

## Optional VLM Configuration

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

────────────────────────────────────────

## Portable Grounding Schema

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

────────────────────────────────────────

## Agent and Harness Rule Templates

| Template | Use it for |
| :--- | :--- |
| [`agent-rules/cursor-rules.md`](agent-rules/cursor-rules.md) | IDE agents. |
| [`agent-rules/claude-code.md`](agent-rules/claude-code.md) | CLI agents. |
| [`agent-rules/windsurf-rules.md`](agent-rules/windsurf-rules.md) | IDE agents. |
| [`agent-rules/copilot-instructions.md`](agent-rules/copilot-instructions.md) | GitHub Copilot. |
| [`skill/visual_grounding_rubric.md`](skill/visual_grounding_rubric.md) | Declarative skill for OMP and agent harnesses. |

Each file contains the same CGV contract, adapted to the target agent or harness integration format.

────────────────────────────────────────

## Documentation

| Document | What it covers |
| :--- | :--- |
| [`docs/human-agent-loop.md`](docs/human-agent-loop.md) | How a human and agent cooperate with CGV. |
| [`docs/vlm-configuration.md`](docs/vlm-configuration.md) | Provider setup and fail-closed behavior. |
| [`docs/evaluation.md`](docs/evaluation.md) | Before/after metrics and JSONL labels. |

────────────────────────────────────────

## Repository Guide

```text
agentic-visual-grounding-rubric/
├── README.md
├── CHANGELOG.md                     # Commit history and updates
├── LICENSE
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

────────────────────────────────────────

## Development

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest
```

Tests cover media helpers, artifact registration, model capability checks, and box-overlap math.

────────────────────────────────────────

## License and Changelog

MIT License. See [LICENSE](LICENSE) and [CHANGELOG.md](CHANGELOG.md).
