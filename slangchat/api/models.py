from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from slangchat.detection.models import DetectionResult


class DetectRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, description="은어 탐지를 수행할 원문 텍스트")


class DetectResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    matches: list[DetectionResult]