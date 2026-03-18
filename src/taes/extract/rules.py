from typing import List, Dict

KEYWORDS = {
    "创新性": ["创新", "新方法", "突破"],
    "先进性": ["先进", "领先", "优化"],
    "实用性": ["实用", "落地", "应用"],
    "可推广性": ["推广", "复制", "复用"],
    "可追溯性": ["溯源", "来源", "证据"],
}


def extract_items(text: str) -> List[Dict]:
    out = []
    for k, kws in KEYWORDS.items():
        hit = any(w in text for w in kws)
        if hit:
            out.append({"item": k, "evidence": f"命中关键词: {', '.join([w for w in kws if w in text])}"})
    return out
