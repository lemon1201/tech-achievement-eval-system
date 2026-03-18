from typing import List, Dict, Tuple

WEIGHTS = {
    "创新性": 0.30,
    "先进性": 0.25,
    "实用性": 0.20,
    "可推广性": 0.15,
    "可追溯性": 0.10,
}


def score_items(extracted_items: List[Dict]) -> Tuple[float, str, str]:
    hit = {x["item"] for x in extracted_items}
    score = 0.0
    for item, w in WEIGHTS.items():
        if item in hit:
            score += w
    score = round(score * 100, 2)

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
