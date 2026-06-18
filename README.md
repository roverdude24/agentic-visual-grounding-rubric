# Code-Grounded Vision (CGV) / Thị giác neo bằng mã (CGV)

English: CGV is a framework-agnostic rubric and small CPU toolset for agents that need visual reasoning without a local GPU. It gathers visual evidence with deterministic code, then asks an image-capable VLM for semantic judgment.

Tiếng Việt: CGV là bộ hướng dẫn không phụ thuộc framework và bộ công cụ CPU nhỏ cho agent cần suy luận hình ảnh mà không có GPU cục bộ. CGV thu bằng chứng bằng mã tất định, rồi hỏi VLM đọc được ảnh về phần ngữ nghĩa.

> English: Use code as the action layer for spatial and visual reasoning. Crop, diff, overlay, hash, and verify evidence before asking a VLM.
>
> Tiếng Việt: Dùng mã làm lớp hành động cho suy luận không gian và hình ảnh. Crop, diff, vẽ overlay, hash, và kiểm chứng bằng chứng trước khi hỏi VLM.

---

## Why CGV instead of naive VLM? / Vì sao dùng CGV thay vì VLM trực tiếp?

English: A multimodal model can describe an image, but it cannot measure reliably. CGV treats VLM output as a hypothesis.

Tiếng Việt: Model đa phương thức có thể mô tả ảnh, nhưng đo đạc không ổn định. CGV xem đầu ra VLM là giả thuyết.

| Decision point / Điểm so sánh | Naive VLM / VLM trực tiếp | CGV |
| :--- | :--- | :--- |
| Boxes and coordinates / Box và tọa độ | English: VLMs often invent pixel coordinates, box sizes, intersections, or overlap. Vietnamese: VLM thường bịa tọa độ pixel, kích thước box, giao điểm, hoặc vùng chồng lấp. | English: CGV uses local math, Pillow, OpenCV-style geometry, and IoU/intersection checks to verify box hypotheses. Vietnamese: CGV dùng toán cục bộ, Pillow, hình học kiểu OpenCV, và kiểm tra IoU/giao điểm để xác minh giả thuyết box. |
| Resolution and focus / Độ phân giải và vùng nhìn | English: Providers may downscale large images, hiding small wires, tiny text, edge artifacts, or narrow occlusions. Vietnamese: Provider có thể giảm kích thước ảnh lớn, làm mất dây nhỏ, chữ nhỏ, lỗi mép, hoặc vùng che hẹp. | English: CGV crops the target zone locally, then sends the focused crop to the VLM. Vietnamese: CGV crop vùng cần xem trên máy, rồi gửi crop tập trung cho VLM. |
| Cost and context / Chi phí và context | English: Re-sending full images wastes tokens and buries evidence. Vietnamese: Gửi lại ảnh đầy đủ tốn token và chôn bằng chứng. | English: CGV registers `local://` URIs, runs diffs first, and sends only crops or overlays. Typical audit loops cut visual-token cost by more than 75%. Vietnamese: CGV đăng ký URI `local://`, chạy diff trước, và chỉ gửi crop hoặc overlay. Vòng audit thường giảm hơn 75% token hình ảnh. |
| Fail-closed checks / Kiểm tra fail-closed | English: A fluent answer can still be wrong about geometry. Vietnamese: Câu trả lời trôi chảy vẫn có thể sai hình học. | English: CGV verifies VLM output with code and stops when the model cannot read images, the provider is unavailable, or geometry needs deterministic checks. Vietnamese: CGV kiểm chứng đầu ra VLM bằng mã và dừng khi model không đọc được ảnh, provider lỗi, hoặc hình học cần kiểm tra tất định. |

---

## What CGV includes / CGV gồm những gì

English:
- A declarative agent contract for deterministic-first visual reasoning.
- CPU helpers for frame extraction, crops, overlays, and pixel diffs.
- A manifest that maps artifacts to `local://` URIs with hashes, file sizes, and image dimensions.
- A Pydantic schema for VLM grounding responses.
- Routing helpers that reject text-only models and verify bounding-box overlap with math.

Tiếng Việt:
- Hợp đồng khai báo cho agent suy luận hình ảnh theo hướng tất định trước.
- Helper CPU để trích frame, crop, vẽ overlay, và so sánh diff theo pixel.
- Manifest ánh xạ artifact sang URI `local://` kèm hash, dung lượng, và kích thước ảnh.
- Schema Pydantic cho phản hồi grounding từ VLM.
- Helper định tuyến chặn model chỉ có text và kiểm tra chồng lấp bounding box bằng toán.

---

## Quickstart: deterministic local audit / Bắt đầu nhanh: audit cục bộ tất định

English: This path needs no GPU or API key. It needs Python 3.9+ and FFmpeg on `PATH`.

Tiếng Việt: Luồng này không cần GPU hay API key. Cần Python 3.9+ và FFmpeg trong `PATH`.

### 1. Install system prerequisites / Cài điều kiện hệ thống

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### 2. Install the package / Cài package

```bash
git clone https://github.com/your-username/agentic-visual-grounding-rubric.git
cd agentic-visual-grounding-rubric
python3 -m pip install -e .
```

### 3. Run the audit / Chạy audit

English: Replace `/path/to/shot.mp4` with a local video file.

Tiếng Việt: Thay `/path/to/shot.mp4` bằng file video cục bộ.

```bash
python3 -m cgv.examples.frame_audit --input /path/to/shot.mp4 --out runs/demo
```

English output:
- `runs/demo/frames/`: extracted keyframes.
- `runs/demo/diffs/`: pixel-difference images.
- `runs/demo/manifest.json`: artifacts with `local://` URIs, hashes, sizes, and dimensions.
- A VLM prompt that references the artifacts.

Đầu ra tiếng Việt:
- `runs/demo/frames/`: keyframe đã trích.
- `runs/demo/diffs/`: ảnh diff theo pixel.
- `runs/demo/manifest.json`: artifact kèm URI `local://`, hash, dung lượng, và kích thước.
- Prompt VLM tham chiếu các artifact đã tạo.

---

## Quickstart: remote VLM loop / Bắt đầu nhanh: vòng lặp VLM từ xa

English: This example checks provider configuration and validates a grounding response against the schema. In production, connect it to your agent runtime or provider client. CGV requires image input support; text-only fallback is not allowed.

Tiếng Việt: Ví dụ này kiểm tra cấu hình provider và xác thực phản hồi grounding theo schema. Khi dùng thật, nối bước này với agent runtime hoặc provider client. CGV cần model hỗ trợ input hình ảnh; không fallback sang text-only.

### 1. Set environment variables / Thiết lập biến môi trường

```bash
export CGV_VLM_PROVIDER="openai"   # options: openai, anthropic, google
export OPENAI_API_KEY="your-api-key"
```

### 2. Run the VLM-gated audit / Chạy audit qua cổng VLM

```bash
python3 -m cgv.examples.frame_audit --input /path/to/shot.mp4 --out runs/demo --ask-vlm
```

English flow:
1. Extract keyframes locally with FFmpeg.
2. Compute visual diffs and register artifact metadata.
3. Validate the VLM grounding response against the schema.
4. Stop with a configuration error if provider config is missing or the selected model cannot handle images.

Luồng tiếng Việt:
1. Trích keyframe cục bộ bằng FFmpeg.
2. Tính diff hình ảnh và đăng ký metadata artifact.
3. Xác thực phản hồi grounding của VLM theo schema.
4. Dừng với lỗi cấu hình nếu thiếu cấu hình provider hoặc model không xử lý được ảnh.

---

## When to use or skip CGV / Khi nào dùng hoặc bỏ qua CGV

| Use case / Trường hợp | Route to CGV? / Dùng CGV? | Action / Cách làm |
| :--- | :--- | :--- |
| Visual or spatial audits: continuity, frame QC, scene boundaries / Audit hình ảnh hoặc không gian: continuity, QC frame, ranh giới cảnh | Yes / Có | Extract frame → crop zone → ask VLM / Trích frame → crop vùng cần xem → hỏi VLM |
| UI screenshot debugging: clipped text, overlapping boxes, z-index / Debug screenshot UI: chữ bị cắt, box chồng nhau, z-index | Yes / Có | OCR or geometry checks → overlap math → VLM overlay review / OCR hoặc kiểm tra hình học → tính chồng lấp → VLM xem overlay |
| Generation QC: watermark placement, constraint checks / QC ảnh hoặc video sinh ra: vị trí watermark, kiểm tra ràng buộc | Yes / Có | Edge or contrast check → crop/overlay → VLM check / Kiểm tra cạnh hoặc tương phản → crop/overlay → VLM kiểm tra |
| Text-only coding or refactoring / Code hoặc refactor chỉ có text | No / Không | Use the normal edit-test loop / Dùng vòng edit-test bình thường |
| Web research or docs / Nghiên cứu web hoặc tài liệu | No / Không | Use a text agent; skip media handlers / Dùng agent text; bỏ qua media handler |

---

## Agent contract / Hợp đồng cho agent

English: Agents that use this skill follow these rules.

Tiếng Việt: Agent dùng skill này theo các quy tắc sau.

1. **Deterministic-first / Tất định trước**  
   English: Do not ask a VLM “Where is object X?” on a raw high-resolution image. Crop, diff, measure, or draw overlays first.  
   Tiếng Việt: Không hỏi VLM “vật thể X ở đâu?” trên ảnh thô độ phân giải cao. Crop, diff, đo, hoặc vẽ overlay trước.

2. **VLM boxes are hypotheses / Box từ VLM là giả thuyết**  
   English: Treat VLM coordinates as proposed regions. Verify them with crop-and-re-ask, overlay review, or math.  
   Tiếng Việt: Xem tọa độ VLM là vùng đề xuất. Kiểm chứng bằng crop-and-re-ask, xem overlay, hoặc tính toán.

3. **No automatic raw-image injection / Không tự động đưa ảnh thô vào context**  
   English: Do not inject raw base64 images into the main orchestrator context. Register artifacts as `local://` URIs and inspect them through isolated VLM calls.  
   Tiếng Việt: Không đưa ảnh base64 thô vào context của orchestrator chính. Đăng ký artifact dưới dạng URI `local://` và kiểm tra bằng lệnh gọi VLM riêng.

4. **Fail closed / Fail-closed**  
   English: If the model is text-only, missing from the registry, or offline, raise a configuration error. Do not simulate vision with text-only completion.  
   Tiếng Việt: Nếu model chỉ hỗ trợ text, không có trong registry, hoặc offline, báo lỗi cấu hình. Không giả lập thị giác bằng completion chỉ có text.

---

## Portable grounding schema / Schema grounding dùng được ở nhiều nơi

English: VLM grounding responses use this shape to stay structured. The Python implementation lives in `cgv/schemas.py`.

Tiếng Việt: Phản hồi grounding của VLM dùng cấu trúc này để giữ định dạng. Bản Python nằm ở `cgv/schemas.py`.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VisualGroundingResult",
  "type": "object",
  "properties": {
    "answer": {
      "type": "boolean",
      "description": "English: final yes/no judgment on the visual question. Vietnamese: phán đoán có/không cho câu hỏi hình ảnh."
    },
    "evidence": {
      "type": "string",
      "description": "English: concrete visual cues, such as color, position, overlap, or contrast. Vietnamese: tín hiệu hình ảnh cụ thể như màu sắc, vị trí, chồng lấp, hoặc tương phản."
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "English: self-rated confidence. Vietnamese: độ tin cậy tự đánh giá."
    },
    "caveats": {
      "type": "string",
      "description": "English: ambiguity, low resolution, occlusion, or other limits. Vietnamese: điểm mơ hồ, độ phân giải thấp, che khuất, hoặc giới hạn khác."
    },
    "regions": {
      "type": "array",
      "description": "English: optional regions of interest proposed by the VLM. Vietnamese: vùng quan tâm tùy chọn do VLM đề xuất.",
      "items": {
        "type": "object",
        "properties": {
          "x": { "type": "number", "description": "English: top-left x coordinate. Vietnamese: tọa độ x góc trên trái." },
          "y": { "type": "number", "description": "English: top-left y coordinate. Vietnamese: tọa độ y góc trên trái." },
          "w": { "type": "number", "description": "English: box width. Vietnamese: chiều rộng box." },
          "h": { "type": "number", "description": "English: box height. Vietnamese: chiều cao box." },
          "label": { "type": "string", "description": "English: semantic label. Vietnamese: nhãn ngữ nghĩa." },
          "frame_id": { "type": "string", "description": "English: frame identifier for multi-frame tasks. Vietnamese: định danh frame cho tác vụ nhiều frame." }
        },
        "required": ["x", "y", "w", "h", "label"]
      }
    },
    "needs_deterministic_check": {
      "type": "boolean",
      "description": "English: true when geometry or bounds need code/math verification. Vietnamese: true khi hình học hoặc biên cần xác minh bằng mã/toán."
    }
  },
  "required": ["answer", "evidence", "confidence", "needs_deterministic_check"]
}
```

---

## Evaluation metrics / Chỉ số đánh giá

English: Use these metrics to compare direct VLM calls with CGV-routed calls.

Tiếng Việt: Dùng các chỉ số này để so sánh lệnh gọi VLM trực tiếp với lệnh gọi qua CGV.

| Metric / Chỉ số | Measures / Đo | Direction / Hướng |
| :--- | :--- | :--- |
| `continuity_true_positive_rate` | English: accuracy on visual continuity breaks. Vietnamese: độ chính xác khi phát hiện lỗi continuity hình ảnh. | Higher / Cao hơn |
| `hallucinated_visual_claim_rate` | English: visual claims not grounded in pixels. Vietnamese: tỷ lệ khẳng định hình ảnh không neo vào pixel. | Lower / Thấp hơn |
| `unnecessary_vlm_call_count` | English: remote VLM calls avoidable after deterministic checks. Vietnamese: số lần gọi VLM từ xa có thể tránh sau kiểm tra tất định. | Lower / Thấp hơn |
| `fail_closed_rate_for_missing_vlm` | English: compliance with the no-text-fallback rule. Vietnamese: mức tuân thủ quy tắc không fallback sang text-only. | Higher / Cao hơn |
| `visual_token_cost` | English: visual context sent to the VLM. Vietnamese: context hình ảnh gửi đến VLM. | Lower, often >75% reduction / Thấp hơn, thường giảm >75% |

English expectation:
- Naive VLM: lower continuity accuracy, more hallucinated coordinate claims, higher visual-token cost.
- CGV-routed agent: higher continuity accuracy, fewer unverified visual claims, lower token cost through crops and overlays.

Kỳ vọng tiếng Việt:
- VLM trực tiếp: độ chính xác continuity thấp hơn, nhiều tọa độ hallucinate hơn, chi phí token hình ảnh cao hơn.
- Agent qua CGV: độ chính xác continuity cao hơn, ít khẳng định hình ảnh chưa xác minh hơn, chi phí token thấp hơn nhờ crop và overlay.

---

## Directory guide / Hướng dẫn thư mục

```text
agentic-visual-grounding-rubric/
├── README.md                         # Bilingual project guide / Hướng dẫn dự án song ngữ
├── LICENSE                           # Apache-2.0 license / Giấy phép Apache-2.0
├── pyproject.toml                    # Python package metadata and dependencies / Metadata và dependency Python
├── setup.py                          # Setuptools entry point / Điểm vào setuptools
├── .gitignore                        # Ignored local files / File cục bộ bị bỏ qua
├── cgv/
│   ├── __init__.py                   # Package marker / Đánh dấu package
│   ├── media.py                      # FFmpeg/Pillow frame, crop, overlay, diff helpers / Helper frame, crop, overlay, diff
│   ├── manifest.py                   # local:// registry with hashes and metadata / Registry local:// kèm hash và metadata
│   ├── schemas.py                    # Pydantic grounding models / Model grounding Pydantic
│   ├── routing.py                    # Model checks and box math / Kiểm tra model và toán box
│   └── examples/
│       ├── __init__.py               # Example package marker / Đánh dấu package ví dụ
│       └── frame_audit.py            # Deterministic frame audit CLI / CLI audit frame tất định
├── skill/
│   ├── visual_grounding_rubric.md    # Declarative skill file / File skill khai báo
│   └── system_prompt_template.txt    # Agent integration prompt / Prompt tích hợp agent
└── tests/
    ├── test_media.py                 # Media helper tests / Test helper media
    ├── test_manifest.py              # Manifest tests / Test manifest
    └── test_routing.py               # Routing and geometry tests / Test định tuyến và hình học
```

---

## Development and tests / Phát triển và kiểm thử

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest
```

English: Tests cover media helpers, artifact registration, model capability checks, and bounding-box overlap math.

Tiếng Việt: Test bao phủ helper media, đăng ký artifact, kiểm tra năng lực model, và toán chồng lấp bounding box.

---

## License / Giấy phép

English: Apache License 2.0. See [LICENSE](LICENSE).

Tiếng Việt: Giấy phép Apache License 2.0. Xem [LICENSE](LICENSE).