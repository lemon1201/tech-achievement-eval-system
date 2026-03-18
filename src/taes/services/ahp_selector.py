from __future__ import annotations

from typing import Any, Dict, List, Tuple

from taes.models.schemas import ModuleCandidate

DIMENSIONS = ["accuracy_fit", "compliance_risk", "execution_cost", "interpretability", "maintainability"]


def _normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    vals = {k: max(float(v), 0.0) for k, v in weights.items() if k in DIMENSIONS}
    for d in DIMENSIONS:
        vals.setdefault(d, 0.0)
    s = sum(vals.values())
    if s <= 0:
        return {"accuracy_fit": 0.35, "compliance_risk": 0.25, "execution_cost": 0.15, "interpretability": 0.15, "maintainability": 0.10}
    return {k: v / s for k, v in vals.items()}


def _score_candidate(task_profile: Dict[str, Any], candidate: ModuleCandidate) -> Tuple[float, Dict[str, float]]:
    # 规则版打分，可替换模型评估
    compliance = str(task_profile.get("compliance_level", "medium")).lower()
    budget = str(task_profile.get("budget_level", "medium")).lower()

    content_text = str(candidate.content)
    has_threshold = "threshold" in content_text or "阈值" in content_text
    has_evidence = "evidence" in content_text or "证据" in content_text

    dim = {
        "accuracy_fit": 0.9 if has_threshold else 0.7,
        "compliance_risk": 0.9 if (compliance == "high" and has_evidence) else 0.75,
        "execution_cost": 0.85 if budget == "low" else 0.7,
        "interpretability": 0.88,
        "maintainability": 0.8,
    }
    return 0.0, dim


def select_modules(task_profile: Dict[str, Any], candidates: Dict[str, List[ModuleCandidate]], weights: Dict[str, float]) -> Dict[str, Any]:
    w = _normalize_weights(weights)
    selected = {}
    explanations = []

    for m_type, options in candidates.items():
        best = None
        best_score = -1.0
        best_dim = {}

        for c in options:
            _, dim = _score_candidate(task_profile, c)
            score = sum(dim[d] * w[d] for d in DIMENSIONS)
            if score > best_score:
                best_score = score
                best = c
                best_dim = dim

        if best is not None:
            selected[m_type] = {
                "module_id": best.module_id,
                "score": round(best_score, 4),
                "dimension_scores": {k: round(v, 4) for k, v in best_dim.items()},
                "weights": {k: round(v, 4) for k, v in w.items()},
            }
            explanations.append(f"{m_type}: 选择 {best.module_id}，加权得分 {round(best_score, 4)}")

    return {"selected": selected, "explanations": explanations}
