from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

SEED_CASES = Path("data") / "seed" / "cases.json"


class CaseStore:
    def __init__(self) -> None:
        self._cases: List[Dict[str, Any]] = []
        self._loaded = False

    def _load_if_needed(self) -> None:
        if self._loaded:
            return
        if not SEED_CASES.exists():
            self._cases = []
            self._loaded = True
            return
        self._cases = json.loads(SEED_CASES.read_text(encoding="utf-8"))
        self._loaded = True

    def list_cases(self) -> List[Dict[str, Any]]:
        self._load_if_needed()
        return self._cases

    def get_cases_by_ids(self, case_ids: List[str]) -> List[Dict[str, Any]]:
        self._load_if_needed()
        id_set = set(case_ids)
        return [c for c in self._cases if c.get("case_id") in id_set]


case_store = CaseStore()
