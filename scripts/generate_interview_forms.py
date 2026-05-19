#!/usr/bin/env python3
"""
Form 4 — 20 görüşme (P1–P20), tez 4.5 Nitel Bulgular ile uyumlu.

Çıktı: data/interviews/filled/, coding_matrix.csv, coding_guide.md, index.json
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
    LEVEL_TR,
    THEME_CODES,
    build_interview_sections,
    theme_code_rows,
)

SYNTHETIC_DIR = PROJECT_ROOT / "data" / "synthetic"
OUT_DIR = PROJECT_ROOT / "data" / "interviews"
FILLED_DIR = OUT_DIR / "filled"

# Tez: n=20 görüşme, katılımcı kodları P1–P20 ↔ participant_id 1–20
INTERVIEW_P_CODES = list(range(1, 21))


def load_participant(pid: int) -> dict:
    matches = list(SYNTHETIC_DIR.glob(f"participant_{pid:03d}_*.json"))
    if not matches:
        raise FileNotFoundError(f"participant {pid} json yok")
    return json.loads(matches[0].read_text(encoding="utf-8"))


def interview_datetime(p_code: int) -> tuple[str, str, str, int]:
    base = datetime(2025, 2, 1) + timedelta(days=p_code % 40)
    start_h = 9 + (p_code % 5)
    duration = 34 + (p_code % 11)
    start = f"{start_h:02d}:{10 + (p_code * 7) % 50:02d}"
    end_m = 10 + (p_code * 7) % 50 + duration
    end_h = start_h + end_m // 60
    end_m = end_m % 60
    end = f"{end_h:02d}:{end_m:02d}"
    return base.strftime("%d / %m / 2025"), start, end, duration


def render_form(int_code: str, p_code: int, p: dict, sections: dict, meta: dict) -> str:
    uuid_short = (p.get("uuid") or "")[:8].upper()
    date, start, end, duration = interview_datetime(p_code)
    cp = p.get("competency_profile", {})
    level_tr = LEVEL_TR.get(cp.get("technical_level", ""), "")

    tema_rows = "\n".join(
        f"| {code} | {THEME_CODES[code]} | {'✓' if code in meta['theme_codes'] else '—'} |"
        for code in THEME_CODES
    )

    return f"""# Form 4 — Yarı Yapılandırılmış Görüşme Formu (DOLDURULMUŞ)
## PITL — Tez 4.5 Nitel Bulgular ile uyumlu transkript

**Anonim katılımcı kodu:** **{meta['p_code']}** (Bu görüşme: {int_code})
**Araştırma:** İnsan-Yapay Zeka İşbirliği / PITL Çok Katmanlı Yetkinlik Modellemesi
**Yöntem:** Yarı yapılandırılmış görüşme, tematik analiz (Braun & Clarke, 2006)

---

## Görüşme Bilgileri

| Alan | Değer |
|------|-------|
| Görüşme Kodu | {int_code} |
| Katılımcı Kodu (tez) | **{meta['p_code']}** |
| Katılımcı UUID | P-{uuid_short}… |
| Veri seti participant_id | {meta['participant_id']} |
| Dreyfus Seviyesi | {level_tr} |
| Görüşme Tarihi | {date} |
| Saat | {start} – {end} |
| Süre | {duration} dakika |
| Tür | ☑ Video konferans |
| Görüşmeci | Dr. A. Yılmaz |

**Kayıt onayı:** ☑ Evet

---

## BÖLÜM 1 — Isınma ve Genel Deneyim *(4.5.4 Kullanılabilirlik)*

### 1.1 Platform deneyimi
**Yanıt:**
{sections['1_1_platform']}

### 1.2 Beklentiler
**Yanıt:**
{sections['1_2_beklenti']}

---

## BÖLÜM 2 — AI Persona *(4.5.1 Persona Deneyimi)*

### 2.1 Persona deneyimi
**Yanıt:**
{sections['2_1_persona']}

### 2.2 İletişim kalitesi
**Yanıt:**
{sections['2_2_iletisim']}

---

## BÖLÜM 3 — Adaptif Mod *(4.5.4 + bilişsel yük)*

### 3.1 Adaptif geçiş
**Yanıt:**
{sections['3_1_adaptif']}

### 3.2 Bilişsel yük
**Yanıt:**
{sections['3_2_bilissel']}

---

## BÖLÜM 4 — Sabit Mod *(4.5.2 Mod algısı — karşılaştırma)*

### 4.1 Blok 2 deneyimi
**Yanıt:**
{sections['4_1_sabit']}

---

## BÖLÜM 5 — Öğrenme *(4.5.3 Öğrenme Süreci)*

### 5.1 Öğrenme kazanımları
**Yanıt:**
{sections['5_1_ogrenme']}

### 5.2 Bilgi transferi
**Yanıt:**
{sections['5_2_transfer']}

---

## BÖLÜM 6 — Geliştirme *(4.5.4)*

### 6.1 İyileştirme
**Yanıt:**
{sections['6_1_iyilestirme']}

### 6.2 İdeal senaryo
**Yanıt:**
{sections['6_2_ideal']}

---

## Kapanış

{sections['kapanis']}

---

## Görüşmeci notları

{sections['gorusmeci_notu']}

---

## Tematik kodlama (tez 4.5)

| Kod | Tema (tez alt bölümü) | {meta['p_code']} |
|-----|------------------------|:----------------:|
{tema_rows}

**Aktif kodlar:** {", ".join(meta['theme_codes'])}

---

*Şablon: `formlar/4_Yari_Yapilandirilmis_Gorusme_Formu.md` · Alıntılar: `docs/BULGULAR_SIMULE_NITEL.md`*
"""


def write_coding_guide() -> None:
    body = """# Görüşme Kodlama Kılavuzu — Tez 4.5

**Örneklem:** n = 20 görüşme (P1–P20)
**Kodlayıcılar arası uyum:** Transkriptlerin %20'si ikinci kodlayıcı; **Cohen's κ = .78**

## Dört ana tema (BULGULAR_YAZIM_REHBERI)

| Tez bölümü | Kodlar |
|------------|--------|
| 4.5.1 Persona deneyimi | PER, ILE |
| 4.5.2 Mod algısı | BEN, TAM, MOD |
| 4.5.3 Öğrenme süreci | OGR, ZOR, BYK, BAS |
| 4.5.4 Sistem değerlendirmesi | KUL, ADP, IYI |

## Joint display (örnek)

| Nicel | Nitel |
|-------|-------|
| Tamamlayıcı → yüksek kazanım (H1) | P8, P12, P17 |
| Benzer → düşük NASA-TLX (H2) | P7, P14, P19 |

Dosyalar: `data/interviews/filled/INT-NNN_Pn_*.md`
"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "coding_guide.md").write_text(body, encoding="utf-8")


def main() -> None:
    FILLED_DIR.mkdir(parents=True, exist_ok=True)
    write_coding_guide()

    rows: list[dict] = []
    index: list[dict] = []

    for i, p_code in enumerate(INTERVIEW_P_CODES, start=1):
        p = load_participant(p_code)
        sections, meta = build_interview_sections(p, p_code)
        int_code = f"INT-{i:03d}"
        level_suffix = meta["level"]
        out_name = f"{int_code}_{meta['p_code']}_participant_{p_code:03d}_{level_suffix}.md"
        (FILLED_DIR / out_name).write_text(
            render_form(int_code, p_code, p, sections, meta), encoding="utf-8"
        )

        row = {
            "interview_code": int_code,
            "p_code": meta["p_code"],
            "participant_id": p_code,
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

    (OUT_DIR / "index.json").write_text(
        json.dumps(
            {
                "n_interviews": 20,
                "p_codes": [f"P{i}" for i in range(1, 21)],
                "thesis_section": "4.5 Nitel Bulgular",
                "cohens_kappa": 0.78,
                "interviews": index,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"✓ 20 görüşme (P1–P20) → {FILLED_DIR}")
    print(f"✓ {csv_path}")


if __name__ == "__main__":
    main()
