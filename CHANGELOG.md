# Changelog

All notable changes to the Code-Grounded Vision (CGV) repository are documented in this file.

---

## [1.1.0] - 2026-06-18

### Added
- **OMP URI Mapping Rule**: Created the `prepare_prompt_for_vlm(prompt_str)` helper in `cgv/routing.py` to intercept and resolve `local://` URIs by copying them to a temporary workspace directory (`.omp_vlm_temp/`). This prevents OMP's `read()` tool from dumping raw binary bytes into the LLM context, which previously caused VLM models (like Gemini) to hang.
- **Unit Tests for URI Resolver**: Added `test_prepare_prompt_for_vlm` to `tests/test_routing.py` to guarantee correct path resolution.
- **Bilingual Documentation**: Documented the new OMP-specific path mapping rules in `docs/vlm-configuration.md`.
- **Non-Technical Presentation**: Added a "CGV in 30 Seconds" explanation and a satellite-photo/local-drone analogy at the top of the README.md to make the repository friendly to project managers and non-technical stakeholders.

---

## [1.0.0] - 2026-06-18

### Added
- **Core CPU Toolset**: Implemented `cgv.media` with Pillow and FFmpeg support for extracting frames, cropping, drawing overlays, and computing pixel diffs.
- **Artifact Registry**: Implemented `cgv.manifest` to track files, labels, sizes, dimensions, and SHA256 hashes to prevent context pollution.
- **Structured Schemas**: Added `cgv.schemas` using Pydantic to enforce the canonical `VisualGroundingResult` model with strict validation (`extra="forbid"`).
- **Geometry & Capability Checks**: Added `cgv.routing` to compute Intersection over Union (IoU) bounding box overlaps and verify model capabilities (fail-closed).
- **Rule Templates**: Created rule files for Cursor (`.cursorrules`), Claude Code (`CLAUDE.md`), Windsurf (`.windsurfrules`), and GitHub Copilot (`copilot-instructions.md`).
- **Declarative Skill**: Added `skill/visual_grounding_rubric.md` for OMP-native visual task routing.
- **Unit Test Suite**: Created tests under `tests/` covering routing, media helpers, and manifest lifecycle (100% test pass verified).

### Changed
- **License**: Switched copyright from Apache-2.0 to MIT License across the codebase.
- **Bilingual Support**: Translated the README and core files into bilingual English-Vietnamese, then simplified to pure English for cleaner context windows.
- **Generalization**: Expanded target audience description from IDE-only agents to any AI agent, framework, or harness (OMP, LangChain, AutoGPT, CrewAI, AutoGen, Cursor, Claude Code).
