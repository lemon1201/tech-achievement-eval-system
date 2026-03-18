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

    # 冲突阈值检测（来自组装阶段的一致性标记）
    for marker in outline.consistency_check.get("issues", []):
        if str(marker).startswith("threshold_conflict:"):
            metric = str(marker).split(":", 1)[1]
            issues.append(f"阈值冲突: {metric}")
            gap_report.append(ValidateIssue(field=f"threshold:{metric}", severity="high", suggestion="统一该指标阈值后再发布"))

    return ValidateOutlineResponse(
        passed=len(issues) == 0,
        issues=issues,
        gap_report=gap_report,
    )
