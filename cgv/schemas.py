from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class Region(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: float = Field(..., ge=0, description="X coordinate of top-left corner")
    y: float = Field(..., ge=0, description="Y coordinate of top-left corner")
    w: float = Field(..., gt=0, description="Width of bounding box")
    h: float = Field(..., gt=0, description="Height of bounding box")
    label: str = Field(..., min_length=1, description="Semantic label for the bounded region")
    frame_id: Optional[str] = Field(None, description="Identifier for the frame if multi-frame task")

class VisualGroundingResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: bool = Field(..., description="Final binary judgment on the visual question")
    evidence: str = Field(..., min_length=1, description="Concrete visual cues observed (color, position, overlap, contrast)")
    confidence: float = Field(..., description="Self-rated confidence score between 0.0 and 1.0", ge=0.0, le=1.0)
    caveats: Optional[str] = Field(None, description="Visual ambiguities, occlusions, or resolution issues")
    regions: List[Region] = Field(default_factory=list, description="Associated bounding boxes/regions of interest")
    needs_deterministic_check: bool = Field(..., description="True if geometry needs code/math verification")
