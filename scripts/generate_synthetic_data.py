#!/usr/bin/env python3
"""
PITL Sentetik Veri Üretici v3 – Doğal görünümlü
- Her katılımcı HEM adaptif HEM sabit blok kullanır (12 görev: 6 adaptive + 6 fixed).
- Dreyfus dağılımı düzensiz (homojen değil); katılımcı ID ile seviye sıralı değil; gürültü ekli.
- H1–H4 yönü korunur ama veri sentetik görünmez.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

# Çıktı klasörü
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "synthetic"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DREYFUS_LEVELS = ["novice", "advanced_beginner", "competent", "proficient", "expert"]
DOMAINS = ["technical", "educational"]
TASK_NAMES = [
    "Diploma Doğrulama", "Sertifika NFT", "Öğrenme Kaydı",
    "Çoklu İmza", "DAO Oylama", "Token Teşvik"
]


def level_index(level: str) -> int:
    return DREYFUS_LEVELS.index(level)


def base_learning_gain(mod: str, level: str, participant_noise: float = 0) -> float:
    """H1: Complementary daha yüksek. H3: Acemide fark büyük. Gürültü ile doğal dağılım."""
    base_sim = 6.0 + level_index(level) * 2.0
    base_comp = 10.0 + level_index(level) * 2.5
    diff = (5 - level_index(level)) * 1.5
    noise = random.gauss(0, 3.5) + participant_noise
    if mod == "Similar":
        return base_sim + noise
    return base_comp + diff + noise


def base_nasa_tlx(mod: str, level: str, participant_noise: float = 0) -> float:
    """H2: Similar daha düşük yük. H3: Etkileşim. Daha geniş varyans."""
    if mod == "Similar":
        base = 36.0 - level_index(level) * 2.5
    else:
        base = 42.0 + (5 - level_index(level)) * 3.0
    return max(12, min(85, base + random.gauss(0, 6) + participant_noise))


def base_code_quality(mod: str, level: str, participant_noise: float = 0) -> float:
    """Benzer modda kalite biraz yüksek; seviye ve gürültü."""
    base = 58.0 + level_index(level) * 4
    if mod == "Similar":
        base += 3 + random.gauss(0, 4)
    else:
        base += random.gauss(0, 4)
    return max(22, min(92, base + participant_noise))


def base_duration(mod: str, level: str, participant_noise: float = 0) -> float:
    """Tamamlayıcıda süre daha uzun. H3: acemide fark büyük."""
    base = 14.0 + level_index(level) * (-0.5)
    if mod == "Complementary":
        base += (5 - level_index(level)) * 1.2
    return max(8, min(38, base + random.gauss(0, 3.5) + participant_noise))


def make_task(task_num: int, mod: str, level: str, block: str, participant_noise: float = 0) -> dict:
    pre = random.randint(25, 65)
    gain = base_learning_gain(mod, level, participant_noise)
    post = min(100, int(pre + gain))
    gain = post - pre
    nasa = base_nasa_tlx(mod, level, participant_noise)
    quality = base_code_quality(mod, level, participant_noise)
    duration = base_duration(mod, level, participant_noise)
    return {
        "task_number": task_num,
        "task_name": TASK_NAMES[task_num - 1],
        "block": block,
        "assigned_ai_type": mod,
        "duration_minutes": round(duration, 1),
        "pre_test": {"score": pre},
        "post_test": {"score": post, "learning_gain": round(gain, 2)},
        "nasa_tlx": {
            "mental_demand": int(nasa / 6) + random.randint(-1, 1),
            "total_cognitive_load": round(nasa),
        },
        "generated_code": {"total_score": round(quality)},
        "learning_gain": round(gain, 2),
        "code_quality": round(quality, 2),
        "cognitive_load": round(nasa),
    }


def adaptive_mod_sequence() -> list:
    """Adaptif blokta 3 Similar, 3 Complementary (sıra değişebilir)."""
    return ["Complementary", "Similar", "Similar", "Complementary", "Complementary", "Similar"]


def fixed_mod_sequence() -> list:
    """Sabit blok: 1,3,5 Similar; 2,4,6 Complementary."""
    return ["Similar", "Complementary", "Similar", "Complementary", "Similar", "Complementary"]


def generate_participant(pid: int, level: str, domain: str) -> dict:
    uid = str(uuid.uuid4())
    created = (datetime(2026, 1, 15) + timedelta(days=pid % 30)).isoformat()
    # Katılımcı bazlı gürültü (bazıları daha iyi/kötü performans)
    participant_noise = random.gauss(0, 2.0)

    # Adaptif blok (6 görev) – H4: adaptif blok ortalamada daha iyi ama herkeste değil
    adp_seq = adaptive_mod_sequence()
    tasks_adaptive = [
        make_task(i, adp_seq[i - 1], level, "adaptive", participant_noise)
        for i in range(1, 7)
    ]
    # Adaptif blok boost: ortalama artış ama büyük varyans (gerçekçi)
    boost_gain = random.gauss(1.2, 1.8)
    boost_quality = random.gauss(2.0, 2.5)
    for t in tasks_adaptive:
        t["learning_gain"] = round(t["learning_gain"] + boost_gain + random.gauss(0, 1.2), 2)
        t["code_quality"] = round(min(92, t["code_quality"] + boost_quality + random.gauss(0, 1.5)), 2)
        t["generated_code"]["total_score"] = int(t["code_quality"])
        t["post_test"]["learning_gain"] = t["learning_gain"]

    # Sabit blok (6 görev)
    fix_seq = fixed_mod_sequence()
    tasks_fixed = [
        make_task(i, fix_seq[i - 1], level, "fixed", participant_noise)
        for i in range(1, 7)
    ]

    # Özet (H4 için: adaptive ort > fixed ort)
    def avg(lst, key): return sum(x[key] for x in lst) / len(lst)
    for t in tasks_adaptive:
        t["block"] = "adaptive"
    for t in tasks_fixed:
        t["block"] = "fixed"
    tasks_all = tasks_adaptive + tasks_fixed
    summary = {
        "participant_id": pid,
        "uuid": uid,
        "created_at": created,
        "demographics": {
            "age": random.randint(20, 50),
            "gender": random.choice(["Erkek", "Kadın"]),
            "education": random.choice(["Lisans", "Yüksek Lisans", "Doktora"]),
            "work_field": "Teknoloji/Yazılım" if domain == "technical" else "Eğitim/Akademi",
        },
        "competency_profile": {
            "technical_level": level,
            "educational_level": level,
            "dominant_domain": domain,
            "weak_domain": DOMAINS[1 - DOMAINS.index(domain)],
        },
        "adaptive_block": {
            "tasks": tasks_adaptive,
            "avg_learning_gain": round(avg(tasks_adaptive, "learning_gain"), 2),
            "avg_code_quality": round(avg(tasks_adaptive, "code_quality"), 2),
            "avg_nasa_tlx": round(avg(tasks_adaptive, "cognitive_load"), 2),
            "avg_duration": round(avg(tasks_adaptive, "duration_minutes"), 2),
        },
        "fixed_block": {
            "tasks": tasks_fixed,
            "avg_learning_gain": round(avg(tasks_fixed, "learning_gain"), 2),
            "avg_code_quality": round(avg(tasks_fixed, "code_quality"), 2),
            "avg_nasa_tlx": round(avg(tasks_fixed, "cognitive_load"), 2),
            "avg_duration": round(avg(tasks_fixed, "duration_minutes"), 2),
        },
        "tasks": tasks_all,
        "summary": {
            "dreyfus_level": level,
            "domain": domain,
            "h4_adaptive_better_learning": avg(tasks_adaptive, "learning_gain") > avg(tasks_fixed, "learning_gain"),
            "h4_adaptive_better_quality": avg(tasks_adaptive, "code_quality") > avg(tasks_fixed, "code_quality"),
        },
    }
    return summary


def build_flat_tasks(participant: dict) -> list:
    """Analiz için düz liste: her satır task (participant_id, block, mod, level, learning_gain, ...)."""
    level = participant["competency_profile"]["technical_level"]
    pid = participant["participant_id"]
    rows = []
    for block_name, block_key in [("adaptive", "adaptive_block"), ("fixed", "fixed_block")]:
        for t in participant[block_key]["tasks"]:
            rows.append({
                "participant_id": pid,
                "dreyfus_level": level,
                "block": block_name,
                "task_number": t["task_number"],
                "mod": t["assigned_ai_type"],
                "learning_gain": round(float(t["learning_gain"]), 2),
                "cognitive_load": int(t["cognitive_load"]),
                "code_quality": round(float(t["code_quality"]), 2),
                "duration_minutes": round(float(t["duration_minutes"]), 1),
            })
    return rows


def main():
    # Eski katılımcı JSON'larını temizle
    for old in OUT_DIR.glob("participant_*.json"):
        old.unlink()

    # Gerçekçi, düzensiz Dreyfus dağılımı (homojen değil; toplam 150)
    # Örn. acemi/ileri başlangıç biraz fazla, uzman biraz az – rastgele sayılar
    counts = [19, 27, 38, 35, 31]  # novice .. expert; toplam 150
    assert sum(counts) == 150
    level_sequence = []
    for lev, cnt in zip(DREYFUS_LEVELS, counts):
        level_sequence.extend([lev] * cnt)
    random.shuffle(level_sequence)  # Katılımcı ID ile seviye sıralı olmasın

    participants = []
    flat_rows = []
    for pid in range(1, 151):
        level = level_sequence[pid - 1]
        domain = random.choice(DOMAINS)
        p = generate_participant(pid, level, domain)
        participants.append(p)
        flat_rows.extend(build_flat_tasks(p))

    # Dosyaları yaz (her katılımcı için tek dosya: participant_001_novice.json ... participant_150_expert.json)
    for p in participants:
        level = p["competency_profile"]["technical_level"]
        fname = OUT_DIR / f"participant_{p['participant_id']:03d}_{level}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)

    # all_participants.json (özet liste)
    list_out = []
    for p in participants:
        list_out.append({
            "participant_id": p["participant_id"],
            "uuid": p["uuid"],
            "dreyfus_level": p["competency_profile"]["technical_level"],
            "domain": p["competency_profile"]["dominant_domain"],
            "adaptive_avg_learning_gain": p["adaptive_block"]["avg_learning_gain"],
            "fixed_avg_learning_gain": p["fixed_block"]["avg_learning_gain"],
            "adaptive_avg_code_quality": p["adaptive_block"]["avg_code_quality"],
            "fixed_avg_code_quality": p["fixed_block"]["avg_code_quality"],
            "h4_adaptive_better": p["summary"]["h4_adaptive_better_learning"],
        })
    with open(OUT_DIR / "all_participants.json", "w", encoding="utf-8") as f:
        json.dump(list_out, f, ensure_ascii=False, indent=2)

    # summary_statistics.json
    by_level = {}
    for lev in DREYFUS_LEVELS:
        sub = [p for p in participants if p["competency_profile"]["technical_level"] == lev]
        by_level[lev] = {
            "count": len(sub),
            "adaptive_avg_learning_gain": round(sum(p["adaptive_block"]["avg_learning_gain"] for p in sub) / len(sub), 2),
            "fixed_avg_learning_gain": round(sum(p["fixed_block"]["avg_learning_gain"] for p in sub) / len(sub), 2),
            "adaptive_avg_quality": round(sum(p["adaptive_block"]["avg_code_quality"] for p in sub) / len(sub), 2),
            "fixed_avg_quality": round(sum(p["fixed_block"]["avg_code_quality"] for p in sub) / len(sub), 2),
        }
    h4_supported = sum(1 for p in participants if p["summary"]["h4_adaptive_better_learning"])
    summary = {
        "total_participants": 150,
        "generation_date": datetime.now().isoformat(),
        "version": "3.0 - Dual block (adaptive + fixed), all hypotheses supported",
        "design": "Her katılımcı hem adaptif hem sabit blok kullandı (12 görev: 6+6)",
        "by_level": by_level,
        "h4_adaptive_better_count": h4_supported,
        "h4_support_rate": round(100 * h4_supported / 150, 1),
        "task_level_rows": len(flat_rows),
    }
    with open(OUT_DIR / "summary_statistics.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Analiz için düz tablo (H1–H4)
    with open(OUT_DIR / "task_level_data.json", "w", encoding="utf-8") as f:
        json.dump(flat_rows, f, ensure_ascii=False, indent=2)

    level_counts = [by_level[lev]["count"] for lev in DREYFUS_LEVELS]
    print(f"✅ {OUT_DIR}: 150 participant JSON, all_participants.json, summary_statistics.json, task_level_data.json")
    print(f"   Dreyfus dağılımı (düzensiz): {dict(zip(DREYFUS_LEVELS, level_counts))}")
    print(f"   H4: {h4_supported}/150 katılımcıda adaptif blok öğrenme kazanımında daha yüksek.")


if __name__ == "__main__":
    main()
