from __future__ import annotations

from typing import Dict, List, Tuple

KEYWORDS = {
    "创新性": ["创新", "新方法", "突破"],
    "先进性": ["先进", "领先", "优化"],
    "实用性": ["实用", "落地", "应用"],
    "可推广性": ["推广", "复制", "复用"],
    "可追溯性": ["溯源", "来源", "证据"],
}

WEIGHTS = {
    "创新性": 0.30,
    "先进性": 0.25,
    "实用性": 0.20,
    "可推广性": 0.15,
    "可追溯性": 0.10,
}


def quick_extract_items(text: str) -> List[Dict]:
    out = []
    for k, kws in KEYWORDS.items():
        hits = [w for w in kws if w in text]
        if hits:
            out.append({"item": k, "evidence": f"命中关键词: {', '.join(hits)}"})
    return out


def build_edges(title: str, extracted_items: List[Dict]) -> List[Dict]:
    return [{"from": title, "rel": "具备", "to": x["item"]} for x in extracted_items]


def quick_score(extracted_items: List[Dict]) -> Tuple[float, str, str]:
    hit = {x["item"] for x in extracted_items}
    score = round(sum(w for item, w in WEIGHTS.items() if item in hit) * 100, 2)

    if score >= 80:
        level = "A"
    elif score >= 60:
        level = "B"
    elif score >= 40:
        level = "C"
    else:
        level = "D"

    reason = f"命中维度 {len(hit)}/{len(WEIGHTS)}，加权得分 {score}"
    return score, level, reason
