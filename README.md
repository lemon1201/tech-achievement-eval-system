# tech-achievement-eval-system

科技成果评价辅助系统（项目2）

## 功能概览
- 任务分类：`/classify-task`
- 相似案例检索：`/retrieve-cases`
- 模块提取（含适用边界过滤）：`/extract-modules`
- AHP 模块选择：`/select-modules`
- 大纲生成（含阈值冲突标记）：`/generate-outline`
- 一致性校验（含冲突阈值检测）：`/validate-outline`
- 大纲导出 Word/PDF：`/export-outline`
- 端到端流水线：`/pipeline/run`
- 快速评价（兼容旧接口）：`/evaluate`

## 快速开始
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python -m uvicorn taes.api.app:app --reload --app-dir src --port 8010
```

## 示例：端到端流水线
`POST /pipeline/run`

```json
{
  "task_id": "task-001",
  "title": "新能源调度成果评测",
  "industry": "energy",
  "description": "需要生成可审计测试大纲，强调合规与证据链",
  "constraints": {
    "deadline_days": 7,
    "budget_level": "medium",
    "compliance_level": "high"
  },
  "materials": [
    {"type": "report", "content": "包含创新性、实用性、测试方法和证据来源"}
  ]
}
```

## 导出接口说明
`POST /export-outline`

- 输入：`GeneratedOutline`
- 输出：`word_path`、`pdf_path`
- 默认导出目录：`data/processed/exports`

> 说明：当前 PDF 为轻量文本版，复杂中文排版可后续接入专业渲染引擎。

## 数据说明
- 案例库种子数据：`data/seed/cases.json`
- 可按行业持续追加已审核通过的大纲模块
