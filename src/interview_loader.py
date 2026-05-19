"""Yarı yapılandırılmış görüşme verilerini yükle (data/interviews)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INTERVIEWS_DIR = PROJECT_ROOT / "data" / "interviews"
FILLED_DIR = INTERVIEWS_DIR / "filled"


def load_interview_index() -> Dict[str, Any]:
    path = INTERVIEWS_DIR / "index.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_coding_matrix() -> pd.DataFrame:
    path = INTERVIEWS_DIR / "coding_matrix.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_transcript(k_code: str) -> Optional[str]:
    """k_code: 'K1' veya '1'"""
    k = k_code.upper().strip()
    if not k.startswith("K"):
        k = f"K{int(k)}"
    num = int(k[1:])
    matches = list(FILLED_DIR.glob(f"INT-{num:03d}_{k}_*.md"))
    if not matches:
        matches = list(FILLED_DIR.glob(f"INT-{num:03d}_*.md"))
    if not matches:
        return None
    return matches[0].read_text(encoding="utf-8")


def list_interviews() -> List[Dict[str, Any]]:
    idx = load_interview_index()
    return idx.get("interviews", [])
