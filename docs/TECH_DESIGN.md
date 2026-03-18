# tech-achievement-eval-system 技术设计文档（项目2）

> 版本：v1.0  
> 目标：将“相似行业大纲检索 + 模块提取 + AHP选择 + 大纲组装”落地为可执行系统。

---

## 1. 背景与目标

### 1.1 背景
新任务到来时，原始资料往往不完整或质量不一致。系统已有历史审核通过的大纲库，具备复用价值。

### 1.2 目标
构建一套“案例库驱动”的测试大纲生成系统，流程如下：
1. 新任务分类
2. 相似案例检索
3. 模块提取与候选池构建
4. AHP 决策选择最适配模块
5. 组装完整测试大纲
6. 一致性审计与缺口报告

---

## 2. 总体架构

```text
[任务输入]
   ↓
[任务分类器]
   ↓
[案例检索器] —— 从历史审核通过大纲库检索 TopN
   ↓
[模块抽取器] —— 抽取章节/指标/方法/阈值/条件
   ↓
[AHP 决策引擎] —— 选模块/选策略
   ↓
[大纲组装器]
   ↓
[一致性校验 + 缺口报告]
   ↓
[输出：完整大纲 / 待补清单]
```

---

## 3. 核心流程设计

## 3.1 任务分类（Task Classification）
输入任务描述，输出：
- 行业（industry）
- 任务类型（task_type）
- 测试对象（object_type）
- 约束条件（时间/成本/合规）

> 说明：分类不只看行业，必须包含任务属性与约束。

## 3.2 相似案例检索（Case Retrieval）
基于分类结果，从案例库检索 TopN 已审核大纲。

检索特征建议：
- 行业匹配（industry）
- 任务类型匹配（task_type）
- 指标集合相似度（metrics overlap）
- 文本语义相似度（可选向量）

## 3.3 模块提取（Module Extraction）
从每个候选大纲抽取标准模块：
- scope（范围）
- metrics（指标）
- methods（测试方法）
- thresholds（阈值）
- conditions（环境条件）
- evidence_rules（证据要求）
- acceptance_rules（验收规则）

## 3.4 AHP 决策（Module Selection）
对同类候选模块按多维度打分并选择。

推荐维度（可配置）：
- accuracy_fit（准确适配度）
- compliance_risk（合规风险，低风险高分）
- execution_cost（执行成本，低成本高分）
- interpretability（可解释性）
- maintainability（可维护性）

输出：
- best module（每一类模块一个最优）
- score breakdown（各维度得分）
- reason（选择理由）

## 3.5 大纲组装（Outline Assembly）
将选中的模块按模板拼装为完整大纲：
1. 测试目标
2. 测试范围
3. 指标与阈值
4. 测试方法
5. 环境与数据要求
6. 验收规则
7. 风险与限制
8. 证据与追溯说明

## 3.6 一致性校验（Consistency Check）
校验项：
- 指标-方法匹配
- 方法-阈值匹配
- 阈值冲突检测
- 必填章节完整性
- 证据链完整性

输出：
- pass/fail
- issue_list
- gap_report（缺失信息）

---

## 4. 数据结构定义（核心）

## 4.1 任务输入 TaskInput
```json
{
  "task_id": "task-20260318-001",
  "title": "某成果测试任务",
  "industry": "energy",
  "description": "需要产出可审计测试大纲",
  "constraints": {
    "deadline_days": 7,
    "budget_level": "medium",
    "compliance_level": "high"
  },
  "materials": [
    {"type": "report", "content": "..."},
    {"type": "spec", "content": "..."}
  ]
}
```

## 4.2 案例 CaseDocument
```json
{
  "case_id": "case-001",
  "industry": "energy",
  "task_type": "evaluation_outline",
  "approved": true,
  "version": "v1.2",
  "outline": {
    "sections": [...],
    "modules": [...]
  },
  "meta": {
    "created_at": "2025-12-10",
    "source": "internal_reviewed"
  }
}
```

## 4.3 模块 OutlineModule
```json
{
  "module_id": "mod-metrics-001",
  "module_type": "metrics",
  "content": {
    "items": [
      {"name": "准确率", "threshold": ">=95%"}
    ]
  },
  "applicability": {
    "industry": ["energy", "manufacturing"],
    "object_type": ["software"],
    "constraints": {"compliance_level": ["high"]}
  },
  "provenance": {
    "case_id": "case-001",
    "version": "v1.2"
  }
}
```

## 4.4 AHP 评分结果 AHPResult
```json
{
  "module_id": "mod-metrics-001",
  "total_score": 0.83,
  "dimension_scores": {
    "accuracy_fit": 0.9,
    "compliance_risk": 0.8,
    "execution_cost": 0.7,
    "interpretability": 0.9,
    "maintainability": 0.8
  },
  "weights": {
    "accuracy_fit": 0.35,
    "compliance_risk": 0.25,
    "execution_cost": 0.15,
    "interpretability": 0.15,
    "maintainability": 0.10
  },
  "reason": "高合规场景下该模块在准确与可解释性上最优"
}
```

## 4.5 生成结果 GeneratedOutline
```json
{
  "task_id": "task-20260318-001",
  "outline_id": "outline-001",
  "sections": [
    {"name": "测试目标", "content": "..."},
    {"name": "测试范围", "content": "..."}
  ],
  "selected_modules": ["mod-scope-003", "mod-metrics-001"],
  "consistency_check": {
    "passed": false,
    "issues": ["缺少样本规模说明"]
  },
  "gap_report": [
    {"field": "sample_size", "severity": "high", "suggestion": "补充样本规模与分布说明"}
  ]
}
```

---

## 5. 接口定义（API Contract）

## 5.1 任务分类接口
### `POST /classify-task`
**请求**：TaskInput（可简化）  
**响应**：
```json
{
  "industry": "energy",
  "task_type": "evaluation_outline",
  "object_type": "software",
  "confidence": 0.87
}
```

## 5.2 相似案例检索接口
### `POST /retrieve-cases`
**请求**：
```json
{
  "industry": "energy",
  "task_type": "evaluation_outline",
  "top_n": 5
}
```
**响应**：
```json
{
  "cases": [
    {"case_id": "case-001", "score": 0.91},
    {"case_id": "case-004", "score": 0.83}
  ]
}
```

## 5.3 模块候选提取接口
### `POST /extract-modules`
**请求**：
```json
{
  "case_ids": ["case-001", "case-004"],
  "module_types": ["scope", "metrics", "methods", "thresholds"]
}
```
**响应**：
```json
{
  "candidates": {
    "metrics": [{"module_id": "mod-metrics-001"}],
    "methods": [{"module_id": "mod-method-002"}]
  }
}
```

## 5.4 AHP 模块选择接口
### `POST /select-modules`
**请求**：
```json
{
  "task_profile": {
    "compliance_level": "high",
    "deadline_days": 7
  },
  "candidates": {
    "metrics": [{"module_id": "mod-metrics-001"}, {"module_id": "mod-metrics-002"}]
  },
  "weights": {
    "accuracy_fit": 0.35,
    "compliance_risk": 0.25,
    "execution_cost": 0.15,
    "interpretability": 0.15,
    "maintainability": 0.10
  }
}
```
**响应**：
```json
{
  "selected": {
    "metrics": {"module_id": "mod-metrics-001", "score": 0.83}
  },
  "explanations": [
    "mod-metrics-001 在高合规场景合规风险最低"
  ]
}
```

## 5.5 大纲生成接口
### `POST /generate-outline`
**请求**：
```json
{
  "task_id": "task-20260318-001",
  "selected_modules": ["mod-scope-003", "mod-metrics-001", "mod-method-002"]
}
```
**响应**：GeneratedOutline

## 5.6 一致性校验接口
### `POST /validate-outline`
**请求**：GeneratedOutline  
**响应**：
```json
{
  "passed": false,
  "issues": ["阈值字段缺失"],
  "gap_report": [
    {"field": "threshold", "severity": "high", "suggestion": "补充阈值范围"}
  ]
}
```

---

## 6. 存储设计

### 6.1 案例库（Case Store）
- case_meta
- case_outline
- case_module_index

### 6.2 模块库（Module Store）
- module_base
- module_applicability
- module_provenance
- module_quality_stats

### 6.3 运行日志（Trace）
- task_trace（分类/检索/AHP/组装/校验每一步）

---

## 7. 风险与防线

## 7.1 风险
1. 行业相近但任务不匹配，造成错配模块
2. 模块组合后阈值冲突
3. 缺失高影响字段但仍误生成“完整稿”

## 7.2 防线
1. 检索增加任务属性约束（非纯行业）
2. 组装后强制一致性校验
3. 关键缺失字段触发阻断（不输出最终稿）

---

## 8. 里程碑实施建议

### P2（当前优先）
- 实现 `/select-modules`（AHP 选择器）
- 实现 `/generate-outline`（模板组装）
- 实现 `/validate-outline`（一致性 + 缺口报告）

### P3
- OCR + 文档结构化（页码/段落ID）
- 证据追溯字段贯通

### P4
- Neo4j 存储与路径查询
- 模块复用统计与质量反馈闭环

---

## 9. 面试表达（一句话）
该系统不是“直接生成文档”，而是“先检索审核通过案例，再做模块级AHP决策，最后在一致性与证据约束下组装大纲”的可审计工程系统。
