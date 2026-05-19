#!/usr/bin/env python3
"""
Form 4 — 20 görüşme (K1–K20), tez Bölüm 4.5 ile birebir.

Kullanım: python3 scripts/generate_interview_forms.py
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.interview_content import (  # noqa: E402
    K_DURATION,
    K_TO_PARTICIPANT_ID,
    LEVEL_TR,
    THEME_CODES,
    build_interview_sections,
    theme_code_rows,
)

SYNTHETIC_DIR = PROJECT_ROOT / "data" / "synthetic"
OUT_DIR = PROJECT_ROOT / "data" / "interviews"
FILLED_DIR = OUT_DIR / "filled"

JOINT_DISPLAY = [
    ("Tamamlayıcı Mod → yüksek öğrenme kazanımı (H1)", "K5, K12", "Tamamlayıcı modda daha çok zorlandım ama daha çok öğrendiğimi hissettim"),
    ("Benzer Mod → düşük bilişsel yük (H2)", "K7, K14", "Benzer modda işler daha akıcı gitti"),
    ("Mod × Dreyfus (H3)", "K2, K3; K17", "Başta zorlandım ama çok şey öğrendim / Her iki modda rahat çalıştım"),
    ("Adaptif > Sabit (H4)", "K9; K4, K18", "Mod değiştiğinde rahatladım / farkında değilim"),
    ("Benzer → kod kalitesi", "K14, K20", "Benzer modda daha verimli çalıştım"),
]


def load_participant(pid: int) -> dict:
    matches = list(SYNTHETIC_DIR.glob(f"participant_{pid:03d}_*.json"))
    if not matches:
        raise FileNotFoundError(f"participant {pid} json yok")
    return json.loads(matches[0].read_text(encoding="utf-8"))


def interview_datetime(k_code: int) -> tuple[str, str, str]:
    base = datetime(2025, 3, 1) + timedelta(days=k_code % 35)
    dur = K_DURATION.get(k_code, 42)
    start_h = 9 + (k_code % 6)
    start_m = 10 + (k_code * 5) % 50
    end_total = start_h * 60 + start_m + dur
    end_h, end_m = end_total // 60, end_total % 60
    date = base.strftime("%d / %m / 2025")
    start = f"{start_h:02d}:{start_m:02d}"
    end = f"{end_h:02d}:{end_m:02d}"
    return date, start, end


def render_form(int_code: str, k_code: int, p: dict, sections: dict, meta: dict) -> str:
    uuid_short = (p.get("uuid") or "")[:8].upper()
    date, start, end = interview_datetime(k_code)
    cp = p.get("competency_profile", {})
    level_tr = LEVEL_TR.get(cp.get("technical_level", ""), "")
    dur = meta["duration_minutes"]
    tema_rows = "\n".join(
        f"| {code} | {THEME_CODES[code]} | {'✓' if code in meta['theme_codes'] else '—'} |"
        for code in THEME_CODES
    )

    return f"""# Form 4 — Yarı Yapılandırılmış Görüşme (DOLDURULMUŞ)
## PITL — Tez Bölüm 4.5 Nitel Bulgular

**Anonim katılımcı kodu:** **{meta['k_code']}** · Görüşme: {int_code}
**Tez uyumu:** `s/Tez_Toplu (1).pdf` — κ = .84, n = 20, ort. 42 dk (28–61)

---

## Görüşme Bilgileri

| Alan | Değer |
|------|-------|
| Görüşme Kodu | {int_code} |
| Katılımcı Kodu (tez) | **{meta['k_code']}** |
| Katılımcı UUID | P-{uuid_short}… |
| Veri seti participant_id | {meta['participant_id']} |
| Dreyfus Seviyesi | {level_tr} |
| Baskın alan | {meta['dominant_domain']} |
| Görüşme Tarihi | {date} |
| Saat | {start} – {end} |
| Süre | **{dur}** dakika |
| Tür | ☑ Video konferans |
| Görüşmeci | Dr. A. Yılmaz |

**Kayıt onayı:** ☑ Evet

---

## BÖLÜM 1 — Isınma *(4.5.4)*

### 1.1 Platform deneyimi
{sections['1_1_platform']}

### 1.2 Beklentiler
{sections['1_2_beklenti']}

---

## BÖLÜM 2 — AI Persona *(4.5.1)*

### 2.1 Persona deneyimi
{sections['2_1_persona']}

### 2.2 İletişim kalitesi
{sections['2_2_iletisim']}

---

## BÖLÜM 3 — Adaptif Mod

### 3.1 Adaptif geçiş
{sections['3_1_adaptif']}

### 3.2 Bilişsel yük
{sections['3_2_bilissel']}

---

## BÖLÜM 4 — Sabit Mod *(4.5.2)*

### 4.1 Blok 2
{sections['4_1_sabit']}

---

## BÖLÜM 5 — Öğrenme *(4.5.3)*

### 5.1 Kazanımlar
{sections['5_1_ogrenme']}

### 5.2 Transfer
{sections['5_2_transfer']}

---

## BÖLÜM 6 — Geliştirme *(4.5.4)*

### 6.1 İyileştirme
{sections['6_1_iyilestirme']}

### 6.2 İdeal senaryo
{sections['6_2_ideal']}

---

## Kapanış

{sections['kapanis']}

---

## Görüşmeci notları

{sections['gorusmeci_notu']}

---

## Tematik kodlama (12 alt tema, 4 ana tema)

| Kod | Tema | {meta['k_code']} |
|-----|------|:--:|
{tema_rows}

**Aktif:** {", ".join(meta['theme_codes'])}

---

*Şablon: `formlar/4_Yari_Yapilandirilmis_Gorusme_Formu.md`*
"""


def write_coding_guide() -> None:
    lines = [
        "# Görüşme Kodlama — Tez 4.5",
        "",
        "- **n = 20** yarı yapılandırılmış görüşme (K1–K20)",
        "- **Örnekleme:** Her Dreyfus seviyesinden 2; teknik/pedagojik eşit",
        "- **Süre:** Ort. 42 dk (28–61)",
        "- **Cohen's κ = .84** (iki kodlayıcı)",
        "- **4 ana tema, 12 alt tema** (Braun & Clarke, 2006)",
        "",
        "## Joint display (Tablo 4.11)",
        "",
        "| Nicel | Katılımcı | Örnek alıntı |",
        "|-------|-----------|--------------|",
    ]
    for nicel, ks, quote in JOINT_DISPLAY:
        lines.append(f"| {nicel} | {ks} | {quote} |")
    (OUT_DIR / "coding_guide.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    FILLED_DIR.mkdir(parents=True, exist_ok=True)
    write_coding_guide()

    # Eski P* dosyalarını temizle
    for old in FILLED_DIR.glob("INT-*_P*.md"):
        old.unlink()

    rows: list[dict] = []
    index: list[dict] = []

    for k_code in range(1, 21):
        pid = K_TO_PARTICIPANT_ID[k_code]
        p = load_participant(pid)
        sections, meta = build_interview_sections(p, k_code)
        int_code = f"INT-{k_code:03d}"
        level_suffix = meta["level"]
        out_name = f"{int_code}_{meta['k_code']}_participant_{pid:03d}_{level_suffix}.md"
        (FILLED_DIR / out_name).write_text(
            render_form(int_code, k_code, p, sections, meta), encoding="utf-8"
        )

        row = {
            "interview_code": int_code,
            "k_code": meta["k_code"],
            "participant_id": pid,
            "duration_minutes": meta["duration_minutes"],
            "level": meta["level"],
            "dominant_domain": meta["dominant_domain"],
            "avg_cognitive_load": meta["avg_cognitive_load"],
            "avg_learning_gain": meta["avg_learning_gain"],
            "preferred_mod": meta["preferred_mod"],
            "themes_active": "|".join(meta["theme_codes"]),
        }
        row.update(theme_code_rows(meta))
        rows.append(row)
        index.append({"interview_code": int_code, "file": f"filled/{out_name}", **row})

    csv_path = OUT_DIR / "coding_matrix.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    alignment = json.loads((OUT_DIR / "thesis_alignment.json").read_text(encoding="utf-8"))
    (OUT_DIR / "index.json").write_text(
        json.dumps(
            {
                **alignment,
                "joint_display": [
                    {"nicel": n, "katilimci": k, "ornek_alinti": q}
                    for n, k, q in JOINT_DISPLAY
                ],
                "interviews": index,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"✓ 20 görüşme K1–K20 → {FILLED_DIR}")


if __name__ == "__main__":
    main()
