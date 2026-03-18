from pydantic import BaseModel
from typing import List, Dict


class EvalRequest(BaseModel):
    title: str
    text: str


class EvalResponse(BaseModel):
    title: str
    extracted_items: List[Dict]
    graph_edges: List[Dict]
    score: float
    level: str
    reason: str
