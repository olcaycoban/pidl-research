#!/usr/bin/env python3
"""Tez 4.5 ile görüşme transkriptlerinin birebir uyum kontrolü."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.interview_content import K_TO_PARTICIPANT_ID, THESIS_K_PROFILES

FILLED = PROJECT_ROOT / "data/interviews/filled"
SYNTHETIC = PROJECT_ROOT / "data/synthetic"

REQUIRED_QUOTES = {
    2: "parçalar birleşince çok şey öğrendiğimi fark ettim",
    3: "temel kavramları anlatarak başladı",
    5: "bilmediğim şeyleri tamamlıyordu",
    7: "Benzer modda işler daha akıcı gitti",
    8: "insan uzmanla konuşuyormuş gibi",
    11: "çift yönlü bir süreçti",
    12: "daha çok öğrendiğimi hissettim",
    14: "Benzer modda daha verimli çalıştım",
    17: "uygun derinlikte yanıtlar verebildi",
}


def main() -> None:
    errors = []
    tech = edu = 0
    by_level: dict[str, int] = {}

    for k, pid in K_TO_PARTICIPANT_ID.items():
        f = list(FILLED.glob(f"INT-{k:03d}_K{k}_*.md"))
        if not f:
            errors.append(f"K{k}: transkript yok")
            continue
        text = f[0].read_text(encoding="utf-8")
        if k in REQUIRED_QUOTES and REQUIRED_QUOTES[k] not in text:
            errors.append(f"K{k}: tez alıntısı eksik — {REQUIRED_QUOTES[k][:40]}...")

        p = json.loads(list(SYNTHETIC.glob(f"participant_{pid:03d}_*.json"))[0].read_text())
        cp = p["competency_profile"]
        dom = cp["dominant_domain"]
        lv = cp.get("stratum_level") or cp["technical_level"]
        if dom == "technical":
            tech += 1
        else:
            edu += 1
        by_level[lv] = by_level.get(lv, 0) + 1

        # typo check: common humanize artifacts
        for bad in ("alıştm", "Teşekkr", "deişti", "gorev", "öğrendğimi"):
            if bad in text:
                errors.append(f"K{k}: yazım hatası kalıntısı '{bad}'")

    if tech != 10 or edu != 10:
        errors.append(f"Alan dengesi: teknik={tech}, pedagojik={edu} (hedef 10+10)")

    if errors:
        print("❌ UYUM SORUNLARI:")
        for e in errors:
            print(" ", e)
        sys.exit(1)
    print("✅ Tez uyumu: 20 transkript, 10+10 alan, zorunlu alıntılar, yazım hatası yok")
    print(f"   Dreyfus dağılımı: {by_level}")


if __name__ == "__main__":
    main()
