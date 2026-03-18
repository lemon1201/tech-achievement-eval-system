from __future__ import annotations

from typing import Any, Dict, List

from taes.models.schemas import CaseHit
from taes.storage.case_store import case_store


def _case_score(case: Dict[str, Any], industry: str, task_type: str) -> float:
    score = 0.0
    if case.get("approved"):
        score += 0.25
    if case.get("industry") == industry:
        score += 0.45
    if case.get("task_type") == task_type:
        score += 0.2
    score += min(float(case.get("quality_score", 0.0)), 1.0) * 0.1
    return round(score, 4)


def retrieve_cases(industry: str, task_type: str, top_n: int) -> List[CaseHit]:
    cases = case_store.list_cases()
    scored = []
    for c in cases:
        s = _case_score(c, industry, task_type)
        if s > 0:
            scored.append(CaseHit(case_id=c["case_id"], score=s, title=c.get("title", c["case_id"])))

    scored.sort(key=lambda x: x.score, reverse=True)
    return scored[:top_n]
