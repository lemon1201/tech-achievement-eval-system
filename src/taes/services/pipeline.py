from __future__ import annotations

from typing import Any, Dict, List

from taes.models.schemas import ModuleCandidate, TaskInput
from taes.services.ahp_selector import select_modules
from taes.services.classifier import classify_task, recommend_industries
from taes.services.module_extractor import extract_module_candidates
from taes.services.outline_assembler import assemble_outline
from taes.services.retriever import retrieve_cases_multi
from taes.services.validator import validate_outline


DEFAULT_MODULE_TYPES = [
    "scope",
    "metrics",
    "methods",
    "thresholds",
    "conditions",
    "acceptance_rules",
    "evidence_rules",
]

DEFAULT_WEIGHTS = {
    "accuracy_fit": 0.35,
    "compliance_risk": 0.25,
    "execution_cost": 0.15,
    "interpretability": 0.15,
    "maintainability": 0.10,
}


def run_evaluation_pipeline(req: TaskInput) -> Dict[str, Any]:
    """
    按“分类 -> 相关案例召回 -> 模块提取 -> AHP筛选 -> 大纲组装 -> 校验”执行完整流水线。
    """
    classified = classify_task(req)

    # 不只查一个行业：主行业 + 相关行业，增强鲁棒性
    industry_candidates = recommend_industries(classified.industry)
    hits = retrieve_cases_multi(industry_candidates, classified.task_type, top_n=5)
    case_ids = [h.case_id for h in hits]

    task_profile = {
        "industry": classified.industry,
        "object_type": classified.object_type,
        **req.constraints.model_dump(),
    }

    candidates = extract_module_candidates(case_ids, DEFAULT_MODULE_TYPES, task_profile)

    selected_result = select_modules(req.constraints.model_dump(), candidates, DEFAULT_WEIGHTS)

    selected_candidates: List[ModuleCandidate] = []
    selected_ids = {v["module_id"] for v in selected_result["selected"].values()}
    for _, mods in candidates.items():
        for m in mods:
            if m.module_id in selected_ids:
                selected_candidates.append(m)

    outline = assemble_outline(req.task_id, req.title, selected_candidates)
    validation = validate_outline(outline)

    return {
        "classified": classified,
        "industry_candidates": industry_candidates,
        "retrieved_case_ids": case_ids,
        "selected": selected_result,
        "outline": outline,
        "validation": validation,
    }
