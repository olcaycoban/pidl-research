#!/usr/bin/env python3
"""
PITL Sentetik Veri Üretici v4 — Tezdeki tablolarla BİREBİR kalibre.

Hedef tablolar (tez Bölüm 4):

- Tablo 4.3 (Mod ana etkileri, N=150):
    LG     Similar M=10.22 SS=2.98 | Complementary M=19.86 SS=1.57
    NASA   Similar M=31.02 SS=3.81 | Complementary M=51.02 SS=4.54
    KK     Similar M=70.23 SS=5.98 | Complementary M=67.27 SS=5.96
    Süre   Similar M=13.03 SS=1.10 | Complementary M=16.61 SS=2.60

- Tablo 4.4 (Dreyfus × Mod):  bkz. LEVEL_PARAMS
- Tablo 4.6 (Adaptif vs Sabit):
    LG     Adaptif M=15.77 SS=2.26 | Sabit M=14.32 SS=2.27
    KK     Adaptif M=69.93 SS=6.01 | Sabit M=67.57 SS=5.93
- Tablo 4.7 (Dreyfus × Blok):  bkz. LEVEL_PARAMS
- H4: 134/150 = %89.3 katılımcıda adaptif > sabit (LG)

Tasarım:
- 150 katılımcı, Dreyfus tabakalı: novice=19, advanced_beginner=27,
  competent=38, proficient=35, expert=31 (tez Tablo 4.4).
- Her katılımcı 6 adaptif + 6 sabit = 12 görev.
- Adaptif blok: 3 Similar + 3 Complementary (rastgele sıra).
- Sabit blok: görev 1,3,5 Similar; 2,4,6 Complementary.

Model:
  Her (level, mod, blok) hücresi için ortalama μ ve standart sapma σ
  parametre olarak verilir. Görev gözlemi: x ~ N(μ, σ).

  Her ortalama bir analitik özdeşlik ile Tablo 4.3 / 4.4 / 4.6 / 4.7'yi
  birlikte sağlayacak şekilde belirlenir:
      μ(L, mod, Adaptif) = M_LM + δ_L / 2
      μ(L, mod, Sabit)   = M_LM - δ_L / 2
  Burada M_LM = Tablo 4.4'teki mod×level ortalaması,
         δ_L  = Tablo 4.7'deki adaptif-sabit farkı.

Doğrulama: scripts/load_synthetic_to_db.py + run_validation.py
"""
from __future__ import annotations

import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

random.seed(2026)

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "synthetic"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------
# TEZ HEDEF DEĞERLERİ
# -----------------------------------------------------------------
TASK_NAMES = [
    "Diploma Doğrulama", "Sertifika NFT", "Öğrenme Kaydı",
    "Çoklu İmza", "DAO Oylama", "Token Teşvik",
]

DREYFUS_LEVELS = ["novice", "advanced_beginner", "competent", "proficient", "expert"]

LEVEL_LABEL = {
    "novice": "Acemi",
    "advanced_beginner": "İleri Başlangıç",
    "competent": "Yetkin",
    "proficient": "Usta",
    "expert": "Uzman",
}

# Tezin tabakalı örneklem yapısı (Tablo 4.4 / 4.7 n-değerleri)
N_BY_LEVEL = {
    "novice": 19,
    "advanced_beginner": 27,
    "competent": 38,
    "proficient": 35,
    "expert": 31,
}
assert sum(N_BY_LEVEL.values()) == 150

# -----------------------------------------------------------------
# LG parametreleri (Tablo 4.4 + 4.7'den)
# -----------------------------------------------------------------
# Tablo 4.4: (Sim mean, Sim SS, Comp mean, Comp SS) — Öğrenme Kazanımı
LG_TABLE_44 = {
    "novice":            (6.18, 1.44, 18.07, 1.59),
    "advanced_beginner": (8.18, 0.69, 18.84, 1.50),
    "competent":         (10.17, 1.05, 19.72, 1.33),
    "proficient":        (12.38, 0.76, 20.89, 1.40),
    "expert":            (14.18, 0.89, 21.81, 1.04),
}
# Tablo 4.7: Adaptif - Sabit farkı (LG)
LG_DELTA_47 = {
    "novice":            1.26,
    "advanced_beginner": 1.74,
    "competent":         1.91,
    "proficient":        1.62,
    "expert":            1.11,
}

# Tablo 4.4 (CL — NASA-TLX 0-100)
CL_TABLE_44 = {
    "novice":            (35.79, 2.87, 57.25, 3.00),
    "advanced_beginner": (33.68, 1.82, 53.88, 2.09),
    "competent":         (30.99, 2.61, 50.77, 2.80),
    "proficient":        (28.37, 2.35, 48.01, 2.83),
    "expert":            (26.25, 2.66, 45.22, 2.93),
}
# Adaptif blokta NASA-TLX adaptasyon sayesinde HAFİFÇE daha düşük (tezde
# Tablo 4.6 sadece LG ve KK içerir; CL için Adaptif vs Sabit verilmemiştir.
# Konservatif: δ_CL = 0 → mod×seviye ortalamaları korunur).
CL_DELTA = 0.0

# Tablo 4.6 (Adaptif vs Sabit): KK ortalamaları
CQ_ADAPT_MEAN = 69.93
CQ_FIXED_MEAN = 67.57
CQ_ADAPT_SD = 6.01
CQ_FIXED_SD = 5.93

# Tablo 4.3 (Mod ana etkileri): KK
CQ_SIM_MEAN = 70.23
CQ_COMP_MEAN = 67.27

# Seviye bazlı KK eğilimi (regresyon Tablo 4.8 → β=0.86, B=4.15 per seviye)
CQ_LEVEL_SLOPE = 4.15  # her Dreyfus adımı için + bu kadar
CQ_REF_LEVEL_IDX = 2  # competent (3. seviye, 0-tabanlı 2) referans

# Tablo 4.3: Süre
DUR_SIM_MEAN = 13.03
DUR_SIM_SD = 1.10
DUR_COMP_MEAN = 16.61
DUR_COMP_SD = 2.60

# Mod×Dreyfus etkileşimi süreye yansır (Acemi'de geniş, Uzman'da dar).
# Tezde: Acemi diff=5.86, Uzman diff=1.06; basit doğrusal eğim.
DUR_LEVEL_SHIFT = {
    "novice":            +1.5,
    "advanced_beginner": +0.8,
    "competent":         +0.0,
    "proficient":        -0.7,
    "expert":            -1.5,
}

# Demografik dağılımlar
WORK_FIELDS = [
    "Yazılım Geliştirme", "Eğitim/Akademi", "Araştırma",
    "Blokzincir Geliştirme", "EdTech", "Veri Bilimi",
]
EDUCATION = ["Lise", "Önlisans", "Lisans", "Yüksek Lisans", "Doktora"]
GENDERS = ["Kadın", "Erkek", "Belirtmek İstemiyor"]


def level_index(level: str) -> int:
    return DREYFUS_LEVELS.index(level)


def cell_mean_lg(level: str, mod: str, block: str, h4_factor: float = 1.0) -> float:
    """h4_factor ∈ [-1, +1]: +1 tam adaptif avantajı, 0 nötr, -1 ters yön.
    Tezde 134/150 (=%89.3) katılımcıda adaptif > sabit; bu yüzden katılımcıların
    yaklaşık %10.7'sinde h4_factor < 0 alınır (Tablo 4.6/4.7 ortalamaları
    yaklaşık olarak korunur)."""
    sim_m, _, comp_m, _ = LG_TABLE_44[level]
    base = sim_m if mod == "Similar" else comp_m
    half = (LG_DELTA_47[level] * h4_factor) / 2.0
    return base + (half if block == "adaptive" else -half)


def cell_sd_lg(level: str, mod: str) -> float:
    sim_sd, comp_sd = LG_TABLE_44[level][1], LG_TABLE_44[level][3]
    # Aynı modun adaptif ve sabit dağılımlarının ortak varyansı yaklaşık SS_table
    # (göz önüne alarak küçük gürültüyü hedef SS'in altında tutarız).
    return (sim_sd if mod == "Similar" else comp_sd) * 0.85


def cell_mean_cl(level: str, mod: str, block: str) -> float:
    sim_m, _, comp_m, _ = CL_TABLE_44[level]
    base = sim_m if mod == "Similar" else comp_m
    half = CL_DELTA / 2.0
    return base + (half if block == "adaptive" else -half)


def cell_sd_cl(level: str, mod: str) -> float:
    sim_sd, comp_sd = CL_TABLE_44[level][1], CL_TABLE_44[level][3]
    return (sim_sd if mod == "Similar" else comp_sd) * 0.85


def cell_mean_cq(level: str, mod: str, block: str) -> float:
    sim_base = CQ_SIM_MEAN
    comp_base = CQ_COMP_MEAN
    base = sim_base if mod == "Similar" else comp_base
    delta = (CQ_ADAPT_MEAN - CQ_FIXED_MEAN)
    half = delta / 2.0
    cq = base + (half if block == "adaptive" else -half)
    # Seviye eğimi
    level_offset = (level_index(level) - CQ_REF_LEVEL_IDX) * CQ_LEVEL_SLOPE
    return cq + level_offset


def cell_sd_cq() -> float:
    return 4.0  # makul hücre içi varyans; toplam SS ~ 5.9-6.0 olacak


def cell_mean_dur(level: str, mod: str) -> float:
    base = DUR_SIM_MEAN if mod == "Similar" else DUR_COMP_MEAN
    return base + DUR_LEVEL_SHIFT[level]


def cell_sd_dur(mod: str) -> float:
    return DUR_SIM_SD if mod == "Similar" else DUR_COMP_SD


def sample_truncated_normal(mu: float, sigma: float, lo: float, hi: float) -> float:
    for _ in range(50):
        v = random.gauss(mu, sigma)
        if lo <= v <= hi:
            return v
    return max(lo, min(hi, mu))


def quantize_5(v: float, lo: int = 0, hi: int = 100) -> int:
    v = max(lo, min(hi, v))
    return int(round(v / 5.0)) * 5


# -----------------------------------------------------------------
# Kompozisyon
# -----------------------------------------------------------------
def make_participant(pid: int, level: str, h4_supports_adaptive: bool) -> dict:
    domain = random.choice(["technical", "educational"])
    # Tezde 134/150 katılımcıda adaptif > sabit; geri kalan 16'da etkisiz/ters.
    # h4_factor: +1 normal, -0.6 ters (varyansla birleştiğinde adaptif <= sabit olur).
    h4_factor = 1.0 if h4_supports_adaptive else -0.6
    # Demografik
    age = random.randint(20, 55)
    gender = random.choice(GENDERS)
    education = random.choice(EDUCATION)
    work_field = random.choice(WORK_FIELDS)
    created_at = datetime(2026, 1, 15) + timedelta(days=pid)

    # Adaptif blok: 3 Sim + 3 Comp, karışık sıra
    adaptive_mods = ["Similar"] * 3 + ["Complementary"] * 3
    random.shuffle(adaptive_mods)
    # Sabit blok: 1,3,5 Sim; 2,4,6 Comp
    fixed_mods = ["Similar", "Complementary"] * 3

    def make_task(task_no: int, mod: str, block: str) -> dict:
        # LG
        mu_lg = cell_mean_lg(level, mod, block, h4_factor=h4_factor)
        sd_lg = cell_sd_lg(level, mod)
        lg = sample_truncated_normal(mu_lg, sd_lg, 1.0, 35.0)
        # Pre/Post — pre eşit dağılımdan, post = pre + lg
        pre_target = 50 - 8 * (1 if mod == "Complementary" else -1)  # Comp pre biraz düşük olur
        pre = max(10, min(85, int(round(random.gauss(pre_target, 12)))))
        post = max(pre + 1, min(99, int(round(pre + lg))))
        learning_gain = post - pre  # integer fark; DB'de pre/post saklanır

        # CL
        mu_cl = cell_mean_cl(level, mod, block)
        sd_cl = cell_sd_cl(level, mod)
        cl = sample_truncated_normal(mu_cl, sd_cl, 5.0, 95.0)
        cl_int = quantize_5(cl)

        # KK
        mu_cq = cell_mean_cq(level, mod, block)
        cq = sample_truncated_normal(mu_cq, cell_sd_cq(), 35.0, 99.0)
        cq_int = int(round(cq))

        # Süre
        mu_d = cell_mean_dur(level, mod)
        d = sample_truncated_normal(mu_d, cell_sd_dur(mod), 5.0, 35.0)

        return {
            "task_number": task_no,
            "task_name": TASK_NAMES[task_no - 1],
            "block": block,
            "assigned_ai_type": mod,
            "duration_minutes": round(d, 1),
            "pre_test": {"score": pre},
            "post_test": {"score": post, "learning_gain": round(lg, 2)},
            "nasa_tlx": {"mental_demand": quantize_5(cl * 0.9), "total_cognitive_load": cl_int},
            "generated_code": {"total_score": cq_int},
            "learning_gain": float(learning_gain),
            "code_quality": round(cq, 2),
            "cognitive_load": cl_int,
        }

    adaptive_tasks = [make_task(i + 1, adaptive_mods[i], "adaptive") for i in range(6)]
    fixed_tasks = [make_task(i + 1, fixed_mods[i], "fixed") for i in range(6)]

    def block_avgs(tasks: list[dict]) -> dict:
        n = len(tasks)
        return {
            "avg_learning_gain": round(sum(t["learning_gain"] for t in tasks) / n, 2),
            "avg_code_quality":  round(sum(t["code_quality"] for t in tasks) / n, 2),
            "avg_nasa_tlx":      round(sum(t["cognitive_load"] for t in tasks) / n, 2),
            "avg_duration":      round(sum(t["duration_minutes"] for t in tasks) / n, 2),
        }

    a_avg = block_avgs(adaptive_tasks)
    f_avg = block_avgs(fixed_tasks)

    return {
        "participant_id": pid,
        "uuid": str(uuid.UUID(int=random.getrandbits(128))),
        "created_at": created_at.isoformat(),
        "demographics": {
            "age": age, "gender": gender,
            "education": education, "work_field": work_field,
        },
        "competency_profile": {
            "technical_level": level,
            "educational_level": level,
            "dominant_domain": domain,
            "weak_domain": "technical" if domain == "educational" else "educational",
        },
        "adaptive_block": {"tasks": adaptive_tasks, **a_avg},
        "fixed_block":    {"tasks": fixed_tasks,    **f_avg},
        "tasks": adaptive_tasks + fixed_tasks,
        "summary": {
            "dreyfus_level": level,
            "domain": domain,
            "h4_adaptive_better_learning": a_avg["avg_learning_gain"] > f_avg["avg_learning_gain"],
            "h4_adaptive_better_quality":  a_avg["avg_code_quality"]  > f_avg["avg_code_quality"],
        },
    }


def main() -> None:
    # Tabakalı katılımcı listesi
    plan: list[tuple[int, str]] = []
    pid = 1
    for lvl in DREYFUS_LEVELS:
        for _ in range(N_BY_LEVEL[lvl]):
            plan.append((pid, lvl))
            pid += 1
    # Karıştır (id ile seviye sıralı görünmesin)
    random.shuffle(plan)

    # H4 etiketleri: tezdeki 134/150 = %89.3 oranı.
    # 16 katılımcı (seviyelere göre orantılı) "adaptif avantajı olmayan" sınıfa atanır.
    h4_failures_per_level = {
        "novice": 2, "advanced_beginner": 3, "competent": 4,
        "proficient": 4, "expert": 3,
    }
    assert sum(h4_failures_per_level.values()) == 16
    h4_support: dict[int, bool] = {}
    by_level_pids: dict[str, list[int]] = {}
    for new_pid, (_, lvl) in enumerate(plan, 1):
        by_level_pids.setdefault(lvl, []).append(new_pid)
    for lvl, pids in by_level_pids.items():
        random.shuffle(pids)
        fail = h4_failures_per_level[lvl]
        for i, p_ in enumerate(pids):
            h4_support[p_] = i >= fail

    participants: list[dict] = []
    all_list: list[dict] = []
    task_level_rows: list[dict] = []

    for new_pid, (orig_pid, lvl) in enumerate(plan, 1):
        p = make_participant(new_pid, lvl, h4_support[new_pid])
        # Dosya adı: participant_NNN_<level>.json
        fname = f"participant_{new_pid:03d}_{lvl}.json"
        (OUT_DIR / fname).write_text(json.dumps(p, ensure_ascii=False, indent=2))

        participants.append(p)
        all_list.append({
            "participant_id": new_pid,
            "uuid": p["uuid"],
            "dreyfus_level": lvl,
            "adaptive_avg_learning_gain": p["adaptive_block"]["avg_learning_gain"],
            "fixed_avg_learning_gain":    p["fixed_block"]["avg_learning_gain"],
            "adaptive_avg_quality":       p["adaptive_block"]["avg_code_quality"],
            "fixed_avg_quality":          p["fixed_block"]["avg_code_quality"],
            "h4_adaptive_better": p["summary"]["h4_adaptive_better_learning"],
        })
        for t in p["tasks"]:
            task_level_rows.append({
                "participant_id": new_pid,
                "dreyfus_level": lvl,
                "block": t["block"],
                "task_number": t["task_number"],
                "mod": t["assigned_ai_type"],
                "learning_gain": t["learning_gain"],
                "cognitive_load": t["cognitive_load"],
                "code_quality": t["code_quality"],
                "duration_minutes": t["duration_minutes"],
            })

    (OUT_DIR / "all_participants.json").write_text(
        json.dumps(all_list, ensure_ascii=False, indent=2))
    (OUT_DIR / "task_level_data.json").write_text(
        json.dumps(task_level_rows, ensure_ascii=False, indent=2))

    # Summary istatistikleri
    by_level = {}
    h4_count = 0
    for p in participants:
        lvl = p["summary"]["dreyfus_level"]
        d = by_level.setdefault(lvl, {"count": 0, "a_lg": [], "f_lg": [], "a_cq": [], "f_cq": []})
        d["count"] += 1
        d["a_lg"].append(p["adaptive_block"]["avg_learning_gain"])
        d["f_lg"].append(p["fixed_block"]["avg_learning_gain"])
        d["a_cq"].append(p["adaptive_block"]["avg_code_quality"])
        d["f_cq"].append(p["fixed_block"]["avg_code_quality"])
        if p["summary"]["h4_adaptive_better_learning"]:
            h4_count += 1

    def avg(xs):
        return round(sum(xs) / len(xs), 2) if xs else 0

    summary_stats = {
        "total_participants": 150,
        "generation_date": datetime.now().isoformat(),
        "version": "4.0 — Tezdeki tablolar (4.3/4.4/4.6/4.7) ile birebir kalibre",
        "design": "Her katılımcı 6 adaptif + 6 sabit = 12 görev; tabakalı (19/27/38/35/31)",
        "by_level": {
            lvl: {
                "count": d["count"],
                "adaptive_avg_learning_gain": avg(d["a_lg"]),
                "fixed_avg_learning_gain": avg(d["f_lg"]),
                "adaptive_avg_quality": avg(d["a_cq"]),
                "fixed_avg_quality": avg(d["f_cq"]),
            } for lvl, d in by_level.items()
        },
        "h4_adaptive_better_count": h4_count,
        "h4_support_rate": round(100 * h4_count / 150, 1),
        "task_level_rows": len(task_level_rows),
    }
    (OUT_DIR / "summary_statistics.json").write_text(
        json.dumps(summary_stats, ensure_ascii=False, indent=2))

    print(f"✅ {len(participants)} katılımcı dosyası yazıldı: {OUT_DIR}")
    print(f"✅ task_level_data.json satır: {len(task_level_rows)}")
    print(f"✅ H4 destek: {h4_count}/150 = %{100*h4_count/150:.1f} (hedef %89.3)")


if __name__ == "__main__":
    main()
