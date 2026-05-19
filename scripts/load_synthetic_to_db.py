"""
Sentetik veriyi (data/synthetic/) Streamlit veritabanına (SQLite/PostgreSQL) yükler.

Akış:
  1. reset_database() → tüm tabloları drop + create_all
  2. Her participant_XXX_*.json dosyasını okur
  3. Participant + 12 TaskSession + PrePostTest (pre/post) + NASATLXResponse + GeneratedCode kayıtları oluşturur

Kullanım:
    python3 scripts/load_synthetic_to_db.py

Notlar:
  - Sentetik veri tez Tablo 4.4'teki tabakalı örneklem (N=150) ile birebir uyumludur.
  - DB seçimi `database/database.py` tarafından (DATABASE_URL env / st.secrets) yapılır.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Proje kök dizinini PYTHONPATH'e ekle
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from database.database import DATABASE_URL, get_session, reset_database  # noqa: E402
from database.models import (  # noqa: E402
    AIType,
    CompetencyLevel,
    GeneratedCode,
    NASATLXResponse,
    Participant,
    PrePostTest,
    TaskSession,
    TaskStatus,
    TestType,
)
from scripts.content_templates import make_content  # noqa: E402

SYNTHETIC_DIR = PROJECT_ROOT / "data" / "synthetic"

LEVEL_MAP = {
    "novice": CompetencyLevel.NOVICE,
    "advanced_beginner": CompetencyLevel.ADVANCED_BEGINNER,
    "competent": CompetencyLevel.COMPETENT,
    "proficient": CompetencyLevel.PROFICIENT,
    "expert": CompetencyLevel.EXPERT,
}

AI_TYPE_MAP = {
    "Similar": AIType.SIMILAR,
    "Complementary": AIType.COMPLEMENTARY,
}


def _caq_sum_to_percent(caq_total: int) -> int:
    """12 maddelik CAQ toplamı (12–60) → 0–100."""
    total = max(12, min(60, int(caq_total)))
    return int(round((total - 12) / 48 * 100))


def _level_to_score(level: str) -> int:
    """Dreyfus seviyesini 0–100 CAQ skoruna çevir."""
    midpoints = {
        "novice": 18,
        "advanced_beginner": 28,
        "competent": 38,
        "proficient": 48,
        "expert": 56,
    }
    return _caq_sum_to_percent(midpoints.get(level, 36))


def _normalize_caq_score(score: int) -> int:
    """Eski kayıtlar (12–60) ve yeni kayıtlar (0–100) için tek ölçek."""
    if score <= 60:
        return _caq_sum_to_percent(score)
    return max(0, min(100, int(score)))


def _make_persona_name(level_enum: CompetencyLevel, ai_type: AIType, domain: str) -> str:
    """Tez personaları için kısa etiket."""
    level_label = level_enum.value
    mod_label = "Similar" if ai_type == AIType.SIMILAR else "Complementary"
    dom_label = "Teknik" if domain == "technical" else "Pedagojik"
    return f"{dom_label} {level_label} ({mod_label})"


def load_participant(session, p: dict[str, Any]) -> None:
    """Tek bir katılımcı için tüm DB kayıtlarını oluştur."""
    uuid_ = p["uuid"]
    created_at = datetime.fromisoformat(p["created_at"])
    demo = p["demographics"]
    profile = p["competency_profile"]
    # Tabakalı örnekleme seviyesi (30/level); CAQ skorları alanlara göre ayrışır
    level_str = profile.get("stratum_level") or profile["technical_level"]
    level_enum = LEVEL_MAP[level_str]
    if "technical_score" in profile and "pedagogical_score" in profile:
        tech_score = _normalize_caq_score(int(profile["technical_score"]))
        ped_score = _normalize_caq_score(int(profile["pedagogical_score"]))
    else:
        tech_score = _level_to_score(profile["technical_level"])
        ped_score = _level_to_score(
            profile.get("educational_level", profile["technical_level"])
        )

    participant = Participant(
        uuid=uuid_,
        created_at=created_at,
        age=demo.get("age"),
        gender=demo.get("gender"),
        education=demo.get("education"),
        work_field=demo.get("work_field"),
        technical_score=tech_score,
        pedagogical_score=ped_score,
        competency_level=level_enum,
        condition="dual",  # 6 adaptif + 6 sabit
        consent_given=True,
        completed=True,
        total_duration_minutes=int(
            round(
                p["adaptive_block"]["avg_duration"] * 6
                + p["fixed_block"]["avg_duration"] * 6
            )
        ),
    )
    session.add(participant)
    session.flush()  # uuid kullanılabilir

    domain = profile.get("dominant_domain", "technical")

    # `tasks` listesi adaptif 6 + sabit 6 görevi sırayla içerir (toplam 12).
    for idx, t in enumerate(p["tasks"], start=1):
        block = t["block"]  # "adaptive" | "fixed"
        ai_type = AI_TYPE_MAP[t["assigned_ai_type"]]
        persona_name = _make_persona_name(level_enum, ai_type, domain)
        duration_min = float(t["duration_minutes"])
        # Görevler arasında 5 dakikalık boşluk varsayımı
        started_at = created_at + timedelta(minutes=(idx - 1) * (duration_min + 5))
        completed_at = started_at + timedelta(minutes=duration_min)

        ts = TaskSession(
            participant_uuid=uuid_,
            task_number=idx,  # 1..12
            block_type=block,
            assigned_ai_type=ai_type,
            assigned_persona=persona_name,
            started_at=started_at,
            completed_at=completed_at,
            duration_minutes=int(round(duration_min)),
            status=TaskStatus.COMPLETED,
        )
        session.add(ts)
        session.flush()  # ts.id

        # Pre-test
        pre_score = int(t["pre_test"]["score"])
        session.add(
            PrePostTest(
                task_session_id=ts.id,
                test_type=TestType.PRE,
                q1_answer="A",
                q2_answer="B",
                q3_answer="C",
                q4_answer=None,
                q5_answer=None,
                score=pre_score,
                completed_at=started_at,
            )
        )

        # Post-test
        post_score = int(t["post_test"]["score"])
        session.add(
            PrePostTest(
                task_session_id=ts.id,
                test_type=TestType.POST,
                q1_answer="A",
                q2_answer="B",
                q3_answer="C",
                q4_answer="D",
                q5_answer="E",
                score=post_score,
                completed_at=completed_at,
            )
        )

        # NASA-TLX (tez 3.3.2: 0-100; total_cognitive_load 1-puan hassasiyetinde)
        tlx_total = int(round(float(t["cognitive_load"])))
        def _clamp(v: int) -> int:
            return max(0, min(100, int(v)))

        mental = _clamp(t["nasa_tlx"].get("mental_demand", tlx_total))
        physical = _clamp(max(0, tlx_total - 20))
        temporal = _clamp(tlx_total)
        performance = _clamp(100 - post_score)  # Ters kodlu
        effort = _clamp(tlx_total + 5)
        frustration = _clamp(max(0, tlx_total - 10))
        session.add(
            NASATLXResponse(
                task_session_id=ts.id,
                mental_demand=mental,
                physical_demand=physical,
                temporal_demand=temporal,
                performance=performance,
                effort=effort,
                frustration=frustration,
                total_cognitive_load=tlx_total,
                completed_at=completed_at,
            )
        )

        # Üretilen kod skoru (kalite) + prompt/kod metni
        quality = float(t.get("code_quality", t["generated_code"]["total_score"]))
        total = int(round(quality))
        mod_str = "Similar" if ai_type == AIType.SIMILAR else "Complementary"
        prompt_text, code_text, gen_sec = make_content(
            idx, level_str, mod_str, domain, quality, duration_min
        )
        functionality = int(round(total * 0.30))
        security = int(round(total * 0.25))
        gas_opt = int(round(total * 0.25))
        code_q = total - functionality - security - gas_opt
        session.add(
            GeneratedCode(
                code_text=code_text,
                language="Solidity",
                prompt_used=prompt_text,
                ai_persona=persona_name,
                generation_time_seconds=gen_sec,
                task_session_id=ts.id,
                functionality_score=functionality,
                security_score=security,
                gas_optimization_score=gas_opt,
                code_quality_score=code_q,
                total_score=total,
                created_at=completed_at,
            )
        )


def main() -> None:
    print(f"📦 Database URL: {DATABASE_URL}")
    print(f"📂 Synthetic dir: {SYNTHETIC_DIR}")

    if not SYNTHETIC_DIR.exists():
        raise SystemExit(f"❌ Sentetik veri klasörü bulunamadı: {SYNTHETIC_DIR}")

    print("\n⚠️  Veritabanı sıfırlanıyor (drop + create_all)...")
    reset_database()

    files = sorted(SYNTHETIC_DIR.glob("participant_*.json"))
    print(f"\n👥 {len(files)} katılımcı dosyası bulundu. Yükleniyor...")

    session = get_session()
    try:
        for i, fp in enumerate(files, 1):
            data = json.loads(fp.read_text(encoding="utf-8"))
            load_participant(session, data)
            if i % 25 == 0:
                session.commit()
                print(f"   • {i}/{len(files)} yüklendi (commit)")
        session.commit()
        print(f"\n✅ Tüm {len(files)} katılımcı kayıtları yazıldı.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    # Doğrulama
    from sqlalchemy import func

    s = get_session()
    try:
        n_part = s.query(func.count(Participant.uuid)).scalar()
        n_ts = s.query(func.count(TaskSession.id)).scalar()
        n_test = s.query(func.count(PrePostTest.id)).scalar()
        n_tlx = s.query(func.count(NASATLXResponse.id)).scalar()
        n_code = s.query(func.count(GeneratedCode.id)).scalar()
        print("\n📊 Doğrulama:")
        print(f"   participants       : {n_part}     (beklenen 150)")
        print(f"   task_sessions      : {n_ts}    (beklenen 1800 = 150×12)")
        print(f"   pre_post_tests     : {n_test}    (beklenen 3600 = 1800×2)")
        print(f"   nasa_tlx_responses : {n_tlx}    (beklenen 1800)")
        print(f"   generated_codes    : {n_code}    (beklenen 1800)")
    finally:
        s.close()


if __name__ == "__main__":
    main()
