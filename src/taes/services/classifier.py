from __future__ import annotations

from taes.models.schemas import ClassifiedTask, TaskInput


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
