from __future__ import annotations

from typing import Any, Dict, List, Sequence

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


def retrieve_cases_multi(industry_candidates: Sequence[str], task_type: str, top_n: int) -> List[CaseHit]:
    """
    多行业召回：
    - 主行业优先（候选列表前面的行业权重更高）
    - 兼顾相关行业，降低分类误差带来的漏召回
    """
    cases = case_store.list_cases()
    ranked: Dict[str, CaseHit] = {}

    for rank, industry in enumerate(industry_candidates):
        rank_bonus = max(0.0, 0.08 - rank * 0.02)  # 主行业有更高加成
        for c in cases:
            s = _case_score(c, industry, task_type) + rank_bonus
            if s <= 0:
                continue

            case_id = c["case_id"]
            prev = ranked.get(case_id)
            hit = CaseHit(case_id=case_id, score=round(s, 4), title=c.get("title", case_id))
            if prev is None or hit.score > prev.score:
                ranked[case_id] = hit

    result = sorted(ranked.values(), key=lambda x: x.score, reverse=True)
    return result[:top_n]
