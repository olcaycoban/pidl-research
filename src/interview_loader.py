"""Yarı yapılandırılmış görüşme verilerini yükle (data/interviews)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INTERVIEWS_DIR = PROJECT_ROOT / "data" / "interviews"
FILLED_DIR = INTERVIEWS_DIR / "filled"

THEME_LABELS: Dict[str, str] = {
    "UZM": "4.5.1 Personanın uzmanlık algısı",
    "ILE": "4.5.1 İletişim stili",
    "ESL": "4.5.1 Eşleştirme süreci",
    "TAM": "4.5.2 Tamamlayıcı mod",
    "BEN": "4.5.2 Benzer mod",
    "MDF": "4.5.2 Modlar arası deneyim farkı",
    "BDG": "4.5.3 Bilgi değişimi",
    "ZOR": "4.5.3 Zorlayıcı noktalar",
    "KUL": "4.5.4 Kullanılabilirlik",
    "ADP": "4.5.4 Adaptif mod algısı",
    "IYI": "4.5.4 İyileştirme önerisi",
    "BAS": "Zaman / bilişsel baskı",
}


def format_theme_codes(codes_pipe: str) -> str:
    """IYI|KUL → okunabilir tema adları."""
    if not codes_pipe or not isinstance(codes_pipe, str):
        return ""
    parts = [c.strip() for c in codes_pipe.split("|") if c.strip()]
    return "; ".join(THEME_LABELS.get(c, c) for c in parts)


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
