from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI

from slangchat.api.models import DetectRequest, DetectResponse
from slangchat.data.loader import load_entries
from slangchat.detection.hybrid import HybridSlangDetector

DATA_PATH = "data/slang.json"


@lru_cache(maxsize=1)
def get_detector() -> HybridSlangDetector:
    return HybridSlangDetector(load_entries(DATA_PATH))


app = FastAPI(title="SlangChat API")


@app.post("/detect", response_model=DetectResponse)
def detect(request: DetectRequest) -> DetectResponse:
    detector = get_detector()
    matches = detector.detect(request.text)
    return DetectResponse(text=request.text, matches=matches)