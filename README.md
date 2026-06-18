# Code-Grounded Vision (CGV) / Thị giác neo bằng mã (CGV)

English: CGV is a framework-agnostic routing rubric and minimal CPU toolset for AI agents that need reliable visual reasoning without local GPU dependencies. It prepares visual evidence with deterministic code first, then asks an image-capable VLM only for semantic judgment.

Tiếng Việt: CGV là bộ quy tắc định tuyến và công cụ CPU tối giản, không phụ thuộc framework, dành cho AI agent cần suy luận hình ảnh đáng tin cậy mà không cần GPU cục bộ. CGV chuẩn bị bằng chứng hình ảnh bằng mã tất định trước, rồi chỉ gọi VLM có khả năng đọc ảnh cho phần phán đoán ngữ nghĩa.

> English core thesis: Code is the best action interface for spatial and visual reasoning. Use local math and media tools to crop, diff, overlay, hash, and verify evidence before asking a VLM.
>
> Luận điểm cốt lõi tiếng Việt: Mã là giao diện hành động tốt nhất cho suy luận không gian và hình ảnh. Hãy dùng toán học và công cụ media cục bộ để crop, diff, vẽ overlay, băm hash, và xác minh bằng chứng trước khi hỏi VLM.

---

## Why CGV instead of Naive VLM? / Vì sao dùng CGV thay vì Naive VLM?

English: Start here. A standard multimodal model can describe an image, but it is a weak measuring instrument. CGV treats VLM output as a hypothesis, not as ground truth.

Tiếng Việt: Hãy bắt đầu từ đây. Mô hình đa phương thức tiêu chuẩn có thể mô tả ảnh, nhưng đo đạc rất yếu. CGV xem đầu ra của VLM là giả thuyết, không phải sự thật tuyệt đối.

| Decision point / Điểm so sánh | Naive VLM direct from the start / Dùng VLM trực tiếp từ đầu | Code-Grounded Vision (CGV) / Thị giác neo bằng mã |
| :--- | :--- | :--- |
| Bounding boxes and spatial coordinates / Bounding box và tọa độ không gian | English: VLMs often hallucinate pixel coordinates, box sizes, intersections, and overlap. Vietnamese: VLM thường bịa hoặc ước lượng sai tọa độ pixel, kích thước box, giao điểm, và vùng chồng lấp. | English: CGV uses local math with Pillow, OpenCV-style geometry, and IoU/intersection checks to compute exact overlaps and verify VLM box hypotheses. Vietnamese: CGV dùng toán học cục bộ với Pillow, hình học kiểu OpenCV, và kiểm tra IoU/giao điểm để tính vùng chồng lấp chính xác và xác minh giả thuyết box từ VLM. |
| Resolution and focus / Độ phân giải và vùng tập trung | English: VLM providers downscale large images, so small wires, tiny text, edge artifacts, or narrow occlusions may disappear. Vietnamese: Nhà cung cấp VLM thường giảm kích thước ảnh lớn, khiến dây nhỏ, chữ nhỏ, lỗi mép ảnh, hoặc vùng che khuất hẹp có thể biến mất. | English: CGV crops local zones losslessly on CPU first, then sends the focused crop so the VLM sees the fine detail. Vietnamese: CGV crop vùng cục bộ gần như không mất chi tiết trên CPU trước, rồi gửi crop tập trung để VLM nhìn được chi tiết nhỏ. |
| Cost and context / Chi phí và context | English: Re-sending full images bloats tokens and hides the relevant evidence inside a large context. Vietnamese: Gửi lại ảnh đầy đủ nhiều lần làm phình token và chôn bằng chứng cần xem trong context lớn. | English: CGV registers `local://` URIs, runs deterministic diffs first, and sends only small crops or overlays, saving more than 75% of visual-token/context cost in typical audit loops. Vietnamese: CGV đăng ký URI `local://`, chạy diff tất định trước, và chỉ gửi crop hoặc overlay nhỏ, thường tiết kiệm hơn 75% chi phí token/context hình ảnh trong các vòng audit. |
| Fail-closed verification / Xác minh fail-closed | English: Naive VLM has no built-in self-correction; a fluent answer can still be geometrically false. Vietnamese: Naive VLM không có cơ chế tự sửa đáng tin; câu trả lời trôi chảy vẫn có thể sai về hình học. | English: CGV runs code to verify VLM outputs and fails closed when the model cannot see images, the provider is unavailable, or geometry needs deterministic checking. Vietnamese: CGV chạy mã để xác minh đầu ra của VLM và fail-closed khi model không đọc được ảnh, provider không khả dụng, hoặc hình học cần kiểm tra tất định. |

---

## What CGV includes / CGV gồm những gì

English:
- A declarative agent contract for deterministic-first visual reasoning.
- CPU media helpers for frame extraction, cropping, overlays, and pixel diffs.
- A manifest registry that maps artifacts to `local://` URIs with hashes, file sizes, and image dimensions.
- A strict Pydantic schema for VLM grounding responses.
- Routing helpers that fail closed for text-only models and verify bounding-box overlap mathematically.

Tiếng Việt:
- Bộ hợp đồng khai báo cho agent theo nguyên tắc suy luận hình ảnh tất định trước.
- Helper media chạy CPU để trích frame, crop, vẽ overlay, và so sánh diff theo pixel.
- Registry manifest ánh xạ artifact sang URI `local://` kèm hash, dung lượng file, và kích thước ảnh.
- Schema Pydantic nghiêm ngặt cho phản hồi grounding từ VLM.
- Helper định tuyến fail-closed với model chỉ hỗ trợ text và xác minh chồng lấp bounding box bằng toán học.

---

## Quickstart: deterministic local audit / Bắt đầu nhanh: audit cục bộ tất định

English: This path needs no GPU and no API key. It does need Python 3.9+ and FFmpeg on `PATH`.

Tiếng Việt: Luồng này không cần GPU và không cần API key. Bạn cần Python 3.9+ và FFmpeg có trong `PATH`.

### 1. Install system prerequisites / Cài điều kiện hệ thống

English:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg
```

Tiếng Việt:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### 2. Install the package / Cài package

English:
```bash
git clone https://github.com/your-username/agentic-visual-grounding-rubric.git
cd agentic-visual-grounding-rubric
python -m pip install -e .
```

Tiếng Việt:
```bash
git clone https://github.com/your-username/agentic-visual-grounding-rubric.git
cd agentic-visual-grounding-rubric
python -m pip install -e .
```

### 3. Run frame extraction, diffing, and manifest registration / Chạy trích frame, diff, và đăng ký manifest

English: Replace `/path/to/shot.mp4` with any local video file.

Tiếng Việt: Thay `/path/to/shot.mp4` bằng bất kỳ file video cục bộ nào.

```bash
python -m cgv.examples.frame_audit --input /path/to/shot.mp4 --out runs/demo
```

English output:
- `runs/demo/frames/`: extracted keyframes.
- `runs/demo/diffs/`: pixel-difference visualization.
- `runs/demo/manifest.json`: registered artifacts with `local://` URIs, hashes, sizes, and dimensions.
- A copy-paste VLM prompt that references the generated artifacts.

Đầu ra tiếng Việt:
- `runs/demo/frames/`: các keyframe đã trích xuất.
- `runs/demo/diffs/`: ảnh trực quan hóa khác biệt theo pixel.
- `runs/demo/manifest.json`: artifact đã đăng ký với URI `local://`, hash, dung lượng, và kích thước.
- Prompt có thể copy-paste cho VLM, tham chiếu đến các artifact đã tạo.

---

## Quickstart: remote VLM loop / Bắt đầu nhanh: vòng lặp VLM từ xa

English: The example checks provider configuration and validates a grounding response against the schema. In production, connect this step to your agent runtime or provider client. CGV still requires the model to support image inputs; text-only fallback is prohibited.

Tiếng Việt: Ví dụ này kiểm tra cấu hình provider và xác thực phản hồi grounding theo schema. Khi dùng thật, hãy nối bước này với runtime agent hoặc client của provider. CGV vẫn yêu cầu model hỗ trợ input hình ảnh; fallback sang text-only bị cấm.

### 1. Set environment variables / Thiết lập biến môi trường

English:
```bash
export CGV_VLM_PROVIDER="openai"   # options: openai, anthropic, google
export OPENAI_API_KEY="your-api-key"
```

Tiếng Việt:
```bash
export CGV_VLM_PROVIDER="openai"   # tùy chọn: openai, anthropic, google
export OPENAI_API_KEY="your-api-key"
```

### 2. Run the VLM-gated audit / Chạy audit có cổng VLM

```bash
python -m cgv.examples.frame_audit --input /path/to/shot.mp4 --out runs/demo --ask-vlm
```

English: The agent flow is:
1. Extract keyframes locally through FFmpeg.
2. Compute visual diffs and register artifact metadata.
3. Validate the VLM grounding response against the canonical schema.
4. Fail closed if provider configuration is missing or the selected model cannot handle images.

Tiếng Việt: Luồng agent là:
1. Trích keyframe cục bộ bằng FFmpeg.
2. Tính diff hình ảnh và đăng ký metadata của artifact.
3. Xác thực phản hồi grounding của VLM theo schema chuẩn.
4. Fail-closed nếu thiếu cấu hình provider hoặc model được chọn không xử lý được ảnh.

---

## When to use or skip CGV / Khi nào dùng hoặc bỏ qua CGV

| Use case / Trường hợp | Route to CGV? / Có đưa qua CGV không? | Action protocol / Giao thức hành động |
| :--- | :--- | :--- |
| Visual or spatial audits: continuity, frame QC, scene boundaries / Audit hình ảnh hoặc không gian: continuity, QC frame, ranh giới cảnh | Yes / Có | Deterministic frame extract → crop interest zone → ask VLM / Trích frame tất định → crop vùng quan tâm → hỏi VLM |
| UI screenshot debugging: clipped text, overlapping boxes, z-index / Debug screenshot UI: chữ bị cắt, box chồng nhau, z-index | Yes / Có | Local OCR or geometry checks → bounding-box overlap math → highlighted VLM review / OCR cục bộ hoặc kiểm tra hình học → tính chồng lấp bounding box → VLM xem overlay |
| Visual prompt or generation QC: watermark placement, constraint checks / QC prompt hoặc ảnh/video sinh ra: vị trí watermark, kiểm tra ràng buộc | Yes / Có | Edge or contrast analysis on placement zone → crop/overlay → VLM check / Phân tích cạnh hoặc tương phản trong vùng đặt → crop/overlay → VLM kiểm tra |
| Text-only coding or refactoring / Code hoặc refactor chỉ có text | No / Không | Use the normal edit-test loop; keep CGV out of context / Dùng vòng edit-test bình thường; không đưa CGV vào context |
| General web research or documentation / Nghiên cứu web hoặc tài liệu thông thường | No / Không | Use a standard text agent; do not load media handlers / Dùng agent text tiêu chuẩn; không tải handler media |

---

## Core agent contract / Hợp đồng cốt lõi cho agent

English: Agents that consume this skill must follow these rules.

Tiếng Việt: Agent dùng skill này phải tuân thủ các quy tắc sau.

1. **Deterministic-first / Tất định trước**  
   English: Never ask a VLM “Where is object X?” directly on a raw high-resolution image. Use local code to crop, diff, measure, or draw overlays first.  
   Tiếng Việt: Không hỏi VLM “vật thể X ở đâu?” trực tiếp trên ảnh thô độ phân giải cao. Hãy dùng mã cục bộ để crop, diff, đo đạc, hoặc vẽ overlay trước.

2. **VLM boxes are hypotheses / Box từ VLM là giả thuyết**  
   English: Never treat coordinates returned by a VLM as physical truth. Verify them with crop-and-re-ask, overlay review, or kernel math.  
   Tiếng Việt: Không xem tọa độ VLM trả về là sự thật vật lý. Hãy xác minh bằng crop-and-re-ask, xem overlay, hoặc tính toán trong kernel.

3. **No automatic raw-image injection / Không tự động nhét ảnh thô vào context**  
   English: Do not inject raw base64 images into the main orchestrator context. Register artifacts as `local://` URIs and inspect them through isolated VLM calls.  
   Tiếng Việt: Không nhét ảnh base64 thô vào context của orchestrator chính. Hãy đăng ký artifact dưới dạng URI `local://` và kiểm tra bằng các lệnh gọi VLM tách biệt.

4. **Fail closed / Fail-closed**  
   English: If the model is text-only, missing from the registry, or offline, raise a configuration error. Never simulate vision with text-only completion.  
   Tiếng Việt: Nếu model chỉ hỗ trợ text, không có trong registry, hoặc offline, hãy báo lỗi cấu hình. Không bao giờ giả lập thị giác bằng completion chỉ có text.

---

## Portable grounding schema / Schema grounding có thể mang đi

English: VLM grounding responses must follow this shape to prevent conversational drift. The Python implementation lives in `cgv/schemas.py`.

Tiếng Việt: Phản hồi grounding của VLM phải theo cấu trúc này để tránh trôi sang hội thoại tự do. Bản cài đặt Python nằm ở `cgv/schemas.py`.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VisualGroundingResult",
  "type": "object",
  "properties": {
    "answer": {
      "type": "boolean",
      "description": "English: final binary judgment on the visual question. Vietnamese: phán đoán nhị phân cuối cùng cho câu hỏi hình ảnh."
    },
    "evidence": {
      "type": "string",
      "description": "English: concrete visual cues observed, such as color, position, overlap, or contrast. Vietnamese: tín hiệu hình ảnh cụ thể quan sát được, như màu sắc, vị trí, chồng lấp, hoặc tương phản."
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "English: self-rated confidence score. Vietnamese: điểm tự đánh giá độ tin cậy."
    },
    "caveats": {
      "type": "string",
      "description": "English: visual ambiguities, low resolution, occlusion, or other limits. Vietnamese: điểm mơ hồ hình ảnh, độ phân giải thấp, che khuất, hoặc giới hạn khác."
    },
    "regions": {
      "type": "array",
      "description": "English: optional regions of interest proposed by the VLM. Vietnamese: các vùng quan tâm tùy chọn do VLM đề xuất.",
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
      "description": "English: true when geometry or bounds need code/math verification. Vietnamese: true khi hình học hoặc biên cần được xác minh bằng mã/toán."
    }
  },
  "required": ["answer", "evidence", "confidence", "needs_deterministic_check"]
}
```

---

## Evaluation metrics / Chỉ số đánh giá

English: Use these metrics to compare a direct VLM workflow against a CGV-routed workflow.

Tiếng Việt: Dùng các chỉ số này để so sánh luồng gọi VLM trực tiếp với luồng được định tuyến qua CGV.

| Metric / Chỉ số | What it measures / Đo điều gì | Target direction / Hướng mục tiêu |
| :--- | :--- | :--- |
| `continuity_true_positive_rate` | English: accuracy when detecting visual continuity breaks. Vietnamese: độ chính xác khi phát hiện lỗi continuity hình ảnh. | Higher / Cao hơn |
| `hallucinated_visual_claim_rate` | English: rate of visual claims not grounded in pixels. Vietnamese: tỷ lệ khẳng định hình ảnh không được neo vào pixel. | Lower / Thấp hơn |
| `unnecessary_vlm_call_count` | English: avoidable remote VLM calls after deterministic checks. Vietnamese: số lần gọi VLM từ xa có thể tránh sau kiểm tra tất định. | Lower / Thấp hơn |
| `fail_closed_rate_for_missing_vlm` | English: compliance with the no-text-fallback rule. Vietnamese: mức tuân thủ quy tắc không fallback sang text-only. | Higher / Cao hơn |
| `visual_token_cost` | English: visual context sent to the VLM. Vietnamese: lượng context hình ảnh gửi đến VLM. | Lower, typically >75% reduction / Thấp hơn, thường giảm >75% |

English heuristic expectation:
- Naive VLM: lower continuity accuracy, higher hallucinated coordinate claims, higher visual-token cost.
- CGV-routed agent: higher continuity accuracy, fewer unverified visual claims, lower token cost through crops and overlays.

Kỳ vọng heuristic tiếng Việt:
- Naive VLM: độ chính xác continuity thấp hơn, nhiều khẳng định tọa độ bị hallucinate hơn, chi phí token hình ảnh cao hơn.
- Agent định tuyến qua CGV: độ chính xác continuity cao hơn, ít khẳng định hình ảnh chưa xác minh hơn, chi phí token thấp hơn nhờ crop và overlay.

---

## Directory guide / Hướng dẫn thư mục

```text
agentic-visual-grounding-rubric/
├── README.md                         # English/Vietnamese project guide / Hướng dẫn dự án song ngữ Anh/Việt
├── LICENSE                           # Apache-2.0 license / Giấy phép Apache-2.0
├── pyproject.toml                    # Python package metadata and dependencies / Metadata package Python và dependency
├── setup.py                          # Setuptools entry point / Điểm vào setuptools
├── .gitignore                        # Ignored local files / File cục bộ bị bỏ qua
├── cgv/
│   ├── __init__.py                   # Package marker / Đánh dấu package
│   ├── media.py                      # FFmpeg and Pillow frame, crop, overlay, diff helpers / Helper FFmpeg và Pillow cho frame, crop, overlay, diff
│   ├── manifest.py                   # local:// artifact registry with hashes and metadata / Registry artifact local:// kèm hash và metadata
│   ├── schemas.py                    # Pydantic grounding models / Model grounding bằng Pydantic
│   ├── routing.py                    # Fail-closed model checks and bounding-box math / Kiểm tra model fail-closed và toán bounding box
│   └── examples/
│       ├── __init__.py               # Example package marker / Đánh dấu package ví dụ
│       └── frame_audit.py            # Deterministic frame audit CLI / CLI audit frame tất định
├── skill/
│   ├── visual_grounding_rubric.md    # Core declarative skill file / File skill khai báo cốt lõi
│   └── system_prompt_template.txt    # Prompt template for agent integration / Mẫu prompt để tích hợp agent
└── tests/
    ├── test_media.py                 # Media helper tests / Test helper media
    ├── test_manifest.py              # Manifest registry tests / Test registry manifest
    └── test_routing.py               # Routing and geometry tests / Test định tuyến và hình học
```

---

## Development and tests / Phát triển và kiểm thử

English:
```bash
python -m pip install -e ".[dev]"
pytest
```

Tiếng Việt:
```bash
python -m pip install -e ".[dev]"
pytest
```

English: The tests cover media helpers, artifact registration, fail-closed model capability checks, and bounding-box overlap math.

Tiếng Việt: Bộ test bao phủ helper media, đăng ký artifact, kiểm tra năng lực model theo fail-closed, và toán chồng lấp bounding box.

---

## License / Giấy phép

English: Apache License 2.0. See [LICENSE](LICENSE) for details.

Tiếng Việt: Giấy phép Apache License 2.0. Xem [LICENSE](LICENSE) để biết chi tiết.
