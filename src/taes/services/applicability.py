from __future__ import annotations

from typing import Any, Dict


LEVEL_RANK = {"low": 1, "medium": 2, "high": 3}


def _as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def is_module_applicable(applicability: Dict[str, Any], task_profile: Dict[str, Any]) -> bool:
    if not applicability:
        return True

    industry = str(task_profile.get("industry", "")).lower()
    object_type = str(task_profile.get("object_type", "")).lower()
    compliance_level = str(task_profile.get("compliance_level", "medium")).lower()

    industries = [str(x).lower() for x in _as_list(applicability.get("industry"))]
    if industries and industry and industry not in industries:
        return False

    object_types = [str(x).lower() for x in _as_list(applicability.get("object_type"))]
    if object_types and object_type and object_type not in object_types:
        return False

    constraints = applicability.get("constraints", {})
    comp_allowed = [str(x).lower() for x in _as_list(constraints.get("compliance_level"))]
    if comp_allowed:
        req_rank = LEVEL_RANK.get(compliance_level, 2)
        max_allowed_rank = max(LEVEL_RANK.get(c, 2) for c in comp_allowed)
        # 任务要求高于模块声明能力时拒绝
        if req_rank > max_allowed_rank:
            return False

    return True
