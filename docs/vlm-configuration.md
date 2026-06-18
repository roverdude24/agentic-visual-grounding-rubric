# VLM Configuration

CGV can run deterministic checks with no VLM. Configure an image-capable model only when the task needs semantic judgment.

---

## Required capability

The selected model must accept image input. A registry record should expose that capability explicitly:

```json
{
  "id": "example-vision-model",
  "input": ["text", "image"]
}
```

A text-only model must fail before the agent answers the visual question.

---

## Environment variables

Use the provider names and keys from your own agent runtime. This repo uses simple examples:

```bash
export CGV_VLM_PROVIDER="openai"
export OPENAI_API_KEY="your-api-key"
```

Other valid setups may use Anthropic, Google, an internal gateway, or a hosted agent platform. The rule is the same: the model must accept images, and the agent must verify that before using it.

---

## Fail-closed logic

The router must stop when any condition is true:

- The model is missing from the registry.
- The model exists but lacks image input.
- The provider key is missing.
- Authentication fails.
- Image upload fails.
- The VLM returns malformed JSON.
- The visual task requires segmentation, depth, pose, or OCR and no configured adapter exists.

Do not continue with a text-only completion. Do not ask the model to imagine the image from a filename or caption.

---

## Minimal routing pseudocode

```python
def require_image_model(model_id, registry):
    model = next((m for m in registry if m["id"] == model_id), None)
    if model is None:
        raise ValueError(f"FAIL-CLOSED: model {model_id!r} is not registered")
    if "image" not in model.get("input", []):
        raise ValueError(f"FAIL-CLOSED: model {model_id!r} cannot read images")
    return model
```

The package implementation lives in `cgv/routing.py` as `check_model_capabilities`.

---

## Recommended request shape

Send the VLM the smallest useful artifact and a strict schema:

```json
{
  "question": "Is the logo fully visible in this crop?",
  "artifact_path": ".omp_vlm_temp/abc123-logo-crop.jpg",
  "artifact_dimensions": [420, 180],
  "schema": "VisualGroundingResult"
}
```

---

## URI mapping & local file resolution

When using agents in environments (like OMP) where image loading is sensitive to file locations:
- **The Out-of-Workspace image hang:** The agent's `read()` tool may only auto-detect image formats for files located inside the active workspace. If you reference out-of-workspace URIs (like `local://` paths pointing to the session root folder), the tool might read the raw binary file as UTF-8 text, flooding the context with binary garbage and causing the model to hang or error.
- **The Workspace resolution fix:** Always copy the visual artifacts from `local://` to a temporary directory in your active workspace (e.g., `.omp_vlm_temp/`) and rewrite the prompt's URIs to relative workspace paths before executing the VLM call.
- **The Helper:** Use `cgv.routing.prepare_prompt_for_vlm(prompt_str)` to automatically parse, copy, and replace all `local://` URIs in a prompt with safe workspace paths before calling the VLM subtask.

```python
from cgv.routing import prepare_prompt_for_vlm

prompt_safe = prepare_prompt_for_vlm(prompt_with_local_uris)
response = agent(prompt_safe, model="your-vision-model")
```

Ask for concrete cues. Reject answers that do not cite pixels in the crop or overlay.

---

## Verification after VLM response

After the VLM returns:

1. Validate the JSON schema.
2. Check all boxes have positive width and height.
3. Check boxes stay inside image bounds.
4. Compute overlap or IoU when the answer depends on geometry.
5. Re-crop disputed regions and ask again only if semantics remain unclear.

The VLM supplies judgment. Code supplies measurement.
