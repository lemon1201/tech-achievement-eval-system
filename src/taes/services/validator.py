from __future__ import annotations

from taes.models.schemas import GeneratedOutline, ValidateIssue, ValidateOutlineResponse


def validate_outline(outline: GeneratedOutline) -> ValidateOutlineResponse:
    issues = []
    gap_report = []

    names = {s.name for s in outline.sections}
    required = {"测试目标", "测试范围", "指标与阈值", "测试方法", "环境与数据要求", "验收规则", "证据与追溯说明"}

    missing = required - names
    for m in sorted(missing):
        issues.append(f"缺少章节: {m}")
        gap_report.append(ValidateIssue(field=m, severity="high", suggestion="补充该章节"))

    for s in outline.sections:
        if "[缺失模块]" in s.content:
            issues.append(f"章节内容缺失: {s.name}")
            gap_report.append(ValidateIssue(field=s.name, severity="high", suggestion="补充对应模块并重新生成"))

    return ValidateOutlineResponse(
        passed=len(issues) == 0,
        issues=issues,
        gap_report=gap_report,
    )
