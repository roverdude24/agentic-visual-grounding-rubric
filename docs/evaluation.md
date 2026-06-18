# Evaluation

Evaluate CGV against a naive VLM baseline. The baseline receives the original image or video frame and answers directly. The CGV agent must extract evidence first, route only focused artifacts to a VLM, and verify geometry with code.

---

## Test suite

Use paired before/after runs.

### Before: naive VLM

- Prompt the VLM with the raw image, screenshot, or representative frame.
- Ask the same visual question.
- Record the answer, evidence, coordinates, confidence, and cost.

### After: CGV-routed agent

- Extract frames, crops, overlays, diffs, OCR, or box measurements first.
- Send only needed crops or overlays to an image-capable VLM.
- Validate structured output.
- Verify coordinates and overlap with code.
- Record the same fields plus deterministic artifacts.

---

## Metrics

| Metric | Measures | Better direction |
| :--- | :--- | :--- |
| `continuity_true_positive_rate` | Correct detection of real visual continuity breaks. | Higher |
| `continuity_false_positive_rate` | Reported continuity breaks that are not present. | Lower |
| `hallucinated_visual_claim_rate` | Claims not supported by pixels, artifacts, or verified metadata. | Lower |
| `unverified_coordinate_rate` | Coordinate or box claims used without deterministic verification. | Lower |
| `unnecessary_vlm_call_count` | VLM calls that local code could have avoided. | Lower |
| `fail_closed_rate_for_missing_vlm` | Missing or text-only VLM cases that stop with configuration errors. | Higher |
| `visual_token_cost` | Image or visual context sent to the VLM. | Lower |
| `artifact_reproducibility_rate` | Answers with enough artifact paths, dimensions, and steps to reproduce. | Higher |

---

## JSONL label format

Store one case per line. Keep labels simple and auditable.

```json
{"case_id":"ui_001","asset":"fixtures/ui/menu_overlap.png","question":"Does the dropdown overlap the button?","expected_answer":true,"task_type":"ui_overlap","requires_vlm":false,"requires_geometry":true,"regions":[{"x":310,"y":140,"w":220,"h":90,"label":"dropdown"}],"notes":"Overlap is measurable from bounding boxes."}
```

Recommended fields:

| Field | Type | Meaning |
| :--- | :--- | :--- |
| `case_id` | string | Stable test identifier. |
| `asset` | string | Image, screenshot, or video path. |
| `question` | string | The visual question asked in both runs. |
| `expected_answer` | boolean or string | Human-labeled answer. |
| `task_type` | string | Category such as `continuity`, `ui_overlap`, `watermark`, or `prompt_adherence`. |
| `requires_vlm` | boolean | Whether semantic judgment is needed. |
| `requires_geometry` | boolean | Whether bounds, coordinates, or overlap matter. |
| `regions` | array | Optional human-labeled boxes in `x`, `y`, `w`, `h`, `label` form. |
| `notes` | string | Short label rationale or edge condition. |

---

## Result record format

Record each agent run separately.

```json
{"case_id":"ui_001","runner":"cgv","answer":true,"correct":true,"vlm_calls":0,"visual_token_cost":0,"hallucinated_claims":0,"unverified_coordinates":0,"artifacts":["runs/ui_001/overlay.png"],"fail_closed":false,"caveats":"None"}
```

Recommended result fields:

| Field | Type | Meaning |
| :--- | :--- | :--- |
| `runner` | string | `naive_vlm` or `cgv`. |
| `answer` | boolean or string | Agent answer. |
| `correct` | boolean | Match against label. |
| `vlm_calls` | integer | Number of VLM calls. |
| `visual_token_cost` | number | Provider-reported visual tokens or a normalized proxy. |
| `hallucinated_claims` | integer | Unsupported visual claims. |
| `unverified_coordinates` | integer | Geometry claims not checked by code. |
| `artifacts` | array | Paths or `local://` URIs used as evidence. |
| `fail_closed` | boolean | Whether the run stopped because vision was unavailable. |
| `caveats` | string | Any visible ambiguity or provider limit. |

---

## Scoring rules

- Count a visual claim as hallucinated when no artifact, pixel evidence, metadata, or deterministic check supports it.
- Count a coordinate as unverified when the agent uses it in the final answer without bounds, crop, overlay, IoU, or intersection checks.
- Count a VLM call as unnecessary when local code could answer the question with no semantic judgment.
- Count fail-closed as correct only when the configured model or provider truly cannot process images.
- Require reproducibility: another reviewer should be able to open the artifacts and rerun the checks.

---

## Expected outcome

CGV should reduce hallucinated visual claims, unverified coordinates, unnecessary VLM calls, and visual token cost. It should increase continuity accuracy, fail-closed behavior, and reproducibility.
