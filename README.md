# tech-achievement-eval-system

科技成果评价辅助系统（项目2）

## 目标
- 从文档中抽取评价要素（指标/方法/条件）
- 构建可追溯结构化结果（含来源位置）
- 输出评价打分建议（AHP 权重法，规则版）

## 当前里程碑（P1）
- [x] 项目骨架
- [x] 可运行 API（stub）
- [x] 抽取/图谱/评分最小闭环（规则版）
- [ ] OCR 与文档结构化增强
- [ ] 生产化图数据库接入

## 快速开始
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python -m uvicorn taes.api.app:app --reload --app-dir src
```

## API
- `GET /health`
- `POST /evaluate`

请求示例：
```json
{
  "title": "某科技成果",
  "text": "该成果具有创新性和实用性，测试方法明确，数据来源可追溯。"
}
```
