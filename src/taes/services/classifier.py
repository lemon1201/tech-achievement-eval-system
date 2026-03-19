from __future__ import annotations

from typing import List

from taes.models.schemas import ClassifiedTask, TaskInput

RELATED_INDUSTRIES = {
    "energy": ["manufacturing"],
    "manufacturing": ["energy"],
    "medical": ["manufacturing"],
}


def classify_task(task: TaskInput) -> ClassifiedTask:
    text = f"{task.title} {task.description}".lower()

    industry = task.industry or "unknown"
    if industry == "unknown":
        if "电力" in text or "能源" in text:
            industry = "energy"
        elif "医疗" in text:
            industry = "medical"
        elif "制造" in text:
            industry = "manufacturing"

    task_type = "evaluation_outline"
    object_type = "software"
    if any(k in text for k in ["硬件", "设备", "传感器"]):
        object_type = "hardware"
    elif any(k in text for k in ["系统", "平台"]):
        object_type = "system"

    confidence = 0.78 if industry != "unknown" else 0.55

    return ClassifiedTask(
        industry=industry,
        task_type=task_type,
        object_type=object_type,
        confidence=confidence,
    )


def recommend_industries(industry: str) -> List[str]:
    """返回主行业 + 相关行业（用于相近案例召回）。"""
    if not industry or industry == "unknown":
        return ["energy", "manufacturing", "medical"]

    related = RELATED_INDUSTRIES.get(industry, [])
    return [industry, *[x for x in related if x != industry]]
