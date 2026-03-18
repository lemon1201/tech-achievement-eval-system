from typing import List, Dict


def build_edges(title: str, extracted_items: List[Dict]) -> List[Dict]:
    edges = []
    for x in extracted_items:
        edges.append({"from": title, "rel": "具备", "to": x["item"]})
    return edges
