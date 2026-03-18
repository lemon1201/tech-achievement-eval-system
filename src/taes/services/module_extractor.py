from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from taes.models.schemas import ModuleCandidate
from taes.storage.case_store import case_store
from taes.services.applicability import is_module_applicable


def extract_module_candidates(case_ids: List[str], module_types: List[str], task_profile: Dict | None = None) -> Dict[str, List[ModuleCandidate]]:
    task_profile = task_profile or {}
    cases = case_store.get_cases_by_ids(case_ids)
    out: Dict[str, List[ModuleCandidate]] = defaultdict(list)

    for case in cases:
        modules = case.get("modules", [])
        for m in modules:
            m_type = m.get("module_type")
            if m_type not in module_types:
                continue

            applicability = m.get("applicability", {})
            if not is_module_applicable(applicability, task_profile):
                continue

            out[m_type].append(
                ModuleCandidate(
                    module_id=m["module_id"],
                    module_type=m_type,
                    content=m.get("content", {}),
                    applicability=applicability,
                    provenance={
                        "case_id": case.get("case_id"),
                        "version": case.get("version", "v1"),
                    },
                )
            )

    return dict(out)
