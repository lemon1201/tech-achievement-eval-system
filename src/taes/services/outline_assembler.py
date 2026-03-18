from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from taes.models.schemas import GeneratedOutline, ModuleCandidate, OutlineSection, ValidateIssue

SECTION_ORDER = [
    ("测试目标", "scope"),
    ("测试范围", "scope"),
    ("指标与阈值", "metrics"),
    ("测试方法", "methods"),
    ("环境与数据要求", "conditions"),
    ("验收规则", "acceptance_rules"),
    ("证据与追溯说明", "evidence_rules"),
]


def _find_module(modules: List[ModuleCandidate], module_type: str) -> ModuleCandidate | None:
    for m in modules:
        if m.module_type == module_type:
            return m
    return None


def _collect_metric_thresholds(selected_modules: List[ModuleCandidate]) -> Dict[str, set]:
    metric_map: Dict[str, set] = {}
    for m in selected_modules:
        items = m.content.get("items", []) if isinstance(m.content, dict) else []
        for it in items:
            name = str(it.get("name", "")).strip()
            threshold = str(it.get("threshold", "")).strip()
            if not name or not threshold:
                continue
            metric_map.setdefault(name, set()).add(threshold)
    return metric_map


def assemble_outline(task_id: str, title: str, selected_modules: List[ModuleCandidate]) -> GeneratedOutline:
    sections = []

    for sec_name, sec_type in SECTION_ORDER:
        m = _find_module(selected_modules, sec_type)
        if m is None:
            sections.append(OutlineSection(name=sec_name, content=f"[缺失模块] {sec_type}"))
        else:
            sections.append(OutlineSection(name=sec_name, content=str(m.content)))

    outline_id = f"outline-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    gap_report: List[ValidateIssue] = []
    issues: List[str] = []

    if any("[缺失模块]" in s.content for s in sections):
        issues.append("module_completeness")
        gap_report.append(ValidateIssue(field="module_completeness", severity="high", suggestion="补齐缺失模块后再生成正式大纲"))

    metric_map = _collect_metric_thresholds(selected_modules)
    for metric, th_set in metric_map.items():
        if len(th_set) > 1:
            issues.append(f"threshold_conflict:{metric}")
            gap_report.append(
                ValidateIssue(
                    field=f"threshold_conflict:{metric}",
                    severity="high",
                    suggestion=f"同一指标出现多个阈值 {sorted(list(th_set))}，请统一阈值定义",
                )
            )

    return GeneratedOutline(
        task_id=task_id,
        outline_id=outline_id,
        title=title,
        sections=sections,
        selected_modules=[m.module_id for m in selected_modules],
        consistency_check={"passed": len(issues) == 0, "issues": issues},
        gap_report=gap_report,
    )
