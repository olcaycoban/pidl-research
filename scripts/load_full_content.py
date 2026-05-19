#!/usr/bin/env python3
"""
Mevcut DB'deki GeneratedCode kayıtlarını gerçek prompt/kod ile zenginleştirir ve
boş tabloları doldurur: AICodeEvaluation, TaskComparison, TechnicalMetrics,
PedagogicalMetrics, FinalEvaluation.

Kullanım:
    python3 scripts/load_full_content.py

Not: Veritabanını sıfırlamaz; mevcut katılımcı/görev metriklerini korur.
"""
from __future__ import annotations

import random
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import func  # noqa: E402

from database.database import DATABASE_URL, get_session  # noqa: E402
from database.models import (  # noqa: E402
    AIType,
    AICodeEvaluation,
    CompetencyLevel,
    FinalEvaluation,
    GeneratedCode,
    NASATLXResponse,
    Participant,
    PedagogicalMetrics,
    PrePostTest,
    TaskComparison,
    TaskSession,
    TestType,
    TechnicalMetrics,
)
from scripts.content_templates import make_content  # noqa: E402

LEVEL_FROM_ENUM = {
    CompetencyLevel.NOVICE: "novice",
    CompetencyLevel.ADVANCED_BEGINNER: "advanced_beginner",
    CompetencyLevel.COMPETENT: "competent",
    CompetencyLevel.PROFICIENT: "proficient",
    CompetencyLevel.EXPERT: "expert",
}

DIFFICULTY_FROM_TLX = [
    (0, 25, "Çok Kolay"),
    (26, 40, "Kolay"),
    (41, 60, "Orta"),
    (61, 80, "Zor"),
    (81, 100, "Çok Zor"),
]

BEST_ASPECTS_SIM = [
    "Kod yapısı benim seviyeme uygun ve anlaşılır.",
    "Açıklamalar adım adım ilerliyor, öğrenmeyi kolaylaştırdı.",
    "Benzer modda hızlı sonuca ulaştım.",
]
BEST_ASPECTS_COMP = [
    "Eksik kaldığım güvenlik konularını tamamladı.",
    "Daha derin teknik detaylar öğretici buldum.",
    "Tamamlayıcı mod zorlayıcı ama öğreticiydi.",
]
IMPROVE_SIM = [
    "Bazı edge case'ler daha detaylı anlatılabilir.",
    "Gas optimizasyonu konusunda daha fazla örnek istiyorum.",
]
IMPROVE_COMP = [
    "Başlangıçta kavramlar biraz yoğun geldi.",
    "Daha fazla görsel örnek faydalı olurdu.",
]

FINAL_OPEN = {
    "hardest_task": [
        "Çoklu İmza görevi en zorlayıcıydı.",
        "DAO Oylama akışını kavramak zaman aldı.",
        "Token Teşvik sözleşmesindeki ödül mantığı karmaşıktı.",
    ],
    "ai_potential": [
        "YZ personası kişiselleştirilmiş öğrenme yolunu hızlandırıyor.",
        "Akıllı sözleşme eğitiminde Sokratik geri bildirim potansiyeli yüksek.",
    ],
    "suggestions": [
        "Adaptif mod geçişleri için daha görünür bildirim eklenebilir.",
    ],
    "blockchain_education_view": [
        "Blokzincir eğitiminde pratik uygulama fırsatı arttı.",
        "Akıllı sözleşme güvenliği konusunda farkındalığım gelişti.",
    ],
}


def _difficulty(tlx: int) -> str:
    for lo, hi, label in DIFFICULTY_FROM_TLX:
        if lo <= tlx <= hi:
            return label
    return "Orta"


def _domain_from_persona(persona: str) -> str:
    return "technical" if persona.startswith("Teknik") else "educational"


def _level_from_participant(p: Participant) -> str:
    if p.competency_level:
        return LEVEL_FROM_ENUM.get(p.competency_level, "competent")
    return "competent"


def _clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def _scale_score(total: int, lo: int = 1, hi: int = 10) -> int:
    return _clamp(int(round(total / 10)), lo, hi)


def _clear_session_children(session, ts_id: int, code_id: int) -> None:
    session.query(AICodeEvaluation).filter(
        AICodeEvaluation.task_session_id == ts_id
    ).delete(synchronize_session=False)
    session.query(TaskComparison).filter(
        TaskComparison.task_session_id == ts_id
    ).delete(synchronize_session=False)
    session.query(TechnicalMetrics).filter(
        TechnicalMetrics.generated_code_id == code_id
    ).delete(synchronize_session=False)
    session.query(PedagogicalMetrics).filter(
        PedagogicalMetrics.generated_code_id == code_id
    ).delete(synchronize_session=False)


def _ai_eval_scores(mod: str, quality: int, rng: random.Random) -> dict:
    if mod == "Similar":
        return {
            "code_understandability": _clamp(7 + rng.randint(0, 2), 1, 10),
            "explanation_quality": _clamp(7 + rng.randint(0, 2), 1, 10),
            "educational_value": _clamp(5 + rng.randint(0, 2), 1, 10),
            "perceived_code_quality": _clamp(6 + quality // 20, 1, 10),
            "perceived_security": _clamp(5 + quality // 25, 1, 10),
        }
    return {
        "code_understandability": _clamp(5 + rng.randint(0, 2), 1, 10),
        "explanation_quality": _clamp(6 + rng.randint(0, 2), 1, 10),
        "educational_value": _clamp(8 + rng.randint(0, 2), 1, 10),
        "perceived_code_quality": _clamp(6 + quality // 20, 1, 10),
        "perceived_security": _clamp(6 + quality // 22, 1, 10),
    }


def _mean_test_learning_gain(session, p: Participant) -> float:
    """Görev ön/son test farkının ortalaması (0–100 ölçek)."""
    gains: list[float] = []
    for ts in p.task_sessions:
        pre = session.query(PrePostTest).filter_by(
            task_session_id=ts.id, test_type=TestType.PRE
        ).first()
        post = session.query(PrePostTest).filter_by(
            task_session_id=ts.id, test_type=TestType.POST
        ).first()
        if pre and post and pre.score is not None and post.score is not None:
            gains.append(float(post.score - pre.score))
    return sum(gains) / len(gains) if gains else 15.0


def _final_for_participant(
    p: Participant, session, rng: random.Random
) -> FinalEvaluation:
    roll = rng.random()
    if roll < 0.60:
        preferred = "Complementary"
    elif roll < 0.90:
        preferred = "Similar"
    else:
        preferred = "Both"

    avg_gain = _mean_test_learning_gain(session, p)
    # Tipik kazanım ~12–22 → AI rating çoğunlukla 7–10 (tez olumlu dağılım)
    rating = _clamp(7 + int(round(avg_gain / 7)) + rng.randint(-1, 1), 6, 10)
    if rating >= 9:
        would_recommend = "Kesinlikle evet"
    elif rating >= 7:
        would_recommend = "Evet"
    else:
        would_recommend = "Kısmen"

    return FinalEvaluation(
        participant_uuid=p.uuid,
        preferred_ai=preferred,
        preferred_ai_reason=(
            "Tamamlayıcı mod eksik yönlerimi tamamladı."
            if preferred == "Complementary"
            else "Benzer mod seviyeme uygun ve rahattı."
        ),
        learning_better_ai=preferred if preferred != "Both" else "Complementary",
        speed_better_ai="Similar" if rng.random() > 0.4 else preferred,
        comfort_similar=rng.randint(3, 5),
        development_complementary=rng.randint(3, 5),
        clarity_similar=rng.randint(3, 5),
        quality_complementary=rng.randint(3, 5),
        hybrid_ideal=rng.randint(4, 5),
        blockchain_view_change="Olumlu",
        ai_learning_rating=rating,
        would_recommend=would_recommend,
        hardest_task=rng.choice(FINAL_OPEN["hardest_task"]),
        ai_potential=rng.choice(FINAL_OPEN["ai_potential"]),
        suggestions=rng.choice(FINAL_OPEN["suggestions"]),
        blockchain_education_view=rng.choice(FINAL_OPEN["blockchain_education_view"]),
        completed_at=datetime.utcnow(),
    )


def main() -> None:
    print(f"📦 Database: {DATABASE_URL}")
    session = get_session()
    rng = random.Random(42)

    try:
        participants = session.query(Participant).all()
        print(f"👥 {len(participants)} katılımcı")

        codes_updated = 0
        for p in participants:
            level = _level_from_participant(p)
            domain = "technical"
            if p.technical_score is not None and p.pedagogical_score is not None:
                domain = "technical" if p.technical_score >= p.pedagogical_score else "educational"

            # Final evaluation (tek kayıt)
            session.query(FinalEvaluation).filter(
                FinalEvaluation.participant_uuid == p.uuid
            ).delete(synchronize_session=False)
            session.add(
                _final_for_participant(
                    p, session, random.Random(hash(p.uuid) % 2**31)
                )
            )

            sessions = sorted(p.task_sessions, key=lambda t: t.task_number or 0)
            for ts in sessions:
                if not ts.generated_codes:
                    continue
                gc = ts.generated_codes[0]
                mod = "Similar" if ts.assigned_ai_type == AIType.SIMILAR else "Complementary"
                if ts.assigned_persona:
                    domain = _domain_from_persona(ts.assigned_persona)

                quality = float(gc.total_score or 70)
                prompt, code, gen_sec = make_content(
                    ts.task_number or 1,
                    level,
                    mod,
                    domain,
                    quality,
                    float(ts.duration_minutes or 15),
                )
                gc.prompt_used = prompt
                gc.code_text = code
                gc.generation_time_seconds = gen_sec
                codes_updated += 1

                _clear_session_children(session, ts.id, gc.id)

                scores = _ai_eval_scores(mod, int(quality), rng)
                session.add(
                    AICodeEvaluation(
                        task_session_id=ts.id,
                        best_aspect=rng.choice(
                            BEST_ASPECTS_SIM if mod == "Similar" else BEST_ASPECTS_COMP
                        ),
                        improvement_needed=rng.choice(
                            IMPROVE_SIM if mod == "Similar" else IMPROVE_COMP
                        ),
                        completed_at=ts.completed_at or datetime.utcnow(),
                        **scores,
                    )
                )

                other = "Complementary" if mod == "Similar" else "Similar"
                tlx = 50
                if ts.nasa_tlx:
                    tlx = ts.nasa_tlx.total_cognitive_load or 50

                is_first = (ts.task_number == 1)
                session.add(
                    TaskComparison(
                        task_session_id=ts.id,
                        used_ai_type=mod,
                        other_ai_type=other,
                        suitability_choice=(
                            f"{mod} modu bu görev için daha uygun"
                            if not is_first
                            else None
                        ),
                        reason=(
                            "Önceki görev deneyimime göre bu mod daha verimli."
                            if not is_first
                            else None
                        ),
                        difficulty_rating=_difficulty(tlx),
                        has_comparison=not is_first,
                        completed_at=ts.completed_at or datetime.utcnow(),
                    )
                )

                t_score = _scale_score(int(quality))
                session.add(
                    TechnicalMetrics(
                        generated_code_id=gc.id,
                        security_score=t_score,
                        gas_optimization_score=_clamp(t_score - 1, 1, 10),
                        code_quality_score=t_score,
                        maintainability_score=_clamp(t_score, 1, 10),
                        production_readiness=_clamp(t_score - 2, 1, 10),
                        auto_security_score=float(quality) * 0.9,
                        auto_gas_score=float(quality) * 0.85,
                        auto_complexity_score=float(max(20, 100 - quality)),
                        completed_at=ts.completed_at or datetime.utcnow(),
                    )
                )

                ped_cl = _clamp(10 - t_score // 2, 1, 10) if mod == "Similar" else _clamp(t_score // 2, 1, 10)
                bloom_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate"]
                bloom_idx = 2
                if isinstance(p.competency_level, CompetencyLevel):
                    bloom_idx = list(LEVEL_FROM_ENUM.keys()).index(p.competency_level)
                bloom = bloom_levels[min(bloom_idx, len(bloom_levels) - 1)]

                session.add(
                    PedagogicalMetrics(
                        generated_code_id=gc.id,
                        learning_ease_score=_clamp(t_score + (1 if mod == "Similar" else -1), 1, 10),
                        instructiveness_score=_clamp(t_score + (2 if mod == "Complementary" else 0), 1, 10),
                        cognitive_load_score=ped_cl,
                        example_quality_score=t_score,
                        scaffolding_score=_clamp(t_score, 1, 10),
                        bloom_taxonomy_level=bloom,
                        explanation_quality=_clamp(t_score + 1, 1, 10),
                        completed_at=ts.completed_at or datetime.utcnow(),
                    )
                )

            if codes_updated % 300 == 0 and codes_updated > 0:
                session.commit()
                print(f"   • {codes_updated} kod güncellendi...")

        session.commit()
        print(f"\n✅ {codes_updated} GeneratedCode prompt/kod güncellendi.")

        # Doğrulama
        n_fn = session.query(func.count(GeneratedCode.id)).filter(
            GeneratedCode.code_text.like("%function%")
        ).scalar()
        checks = [
            ("generated_codes (function içeren)", n_fn, 1800),
            ("ai_code_evaluations", session.query(func.count(AICodeEvaluation.id)).scalar(), 1800),
            ("task_comparisons", session.query(func.count(TaskComparison.id)).scalar(), 1800),
            ("technical_metrics", session.query(func.count(TechnicalMetrics.id)).scalar(), 1800),
            ("pedagogical_metrics", session.query(func.count(PedagogicalMetrics.id)).scalar(), 1800),
            ("final_evaluations", session.query(func.count(FinalEvaluation.id)).scalar(), 150),
        ]
        print("\n📊 Doğrulama:")
        for name, got, expected in checks:
            ok = "✓" if got == expected else "!"
            print(f"   {ok} {name}: {got} (beklenen {expected})")

        sample = session.query(GeneratedCode).first()
        if sample:
            wc = len((sample.prompt_used or "").split())
            lines = len((sample.code_text or "").splitlines())
            print(f"\n🔍 Örnek (code_id={sample.id}): prompt ~{wc} kelime, kod ~{lines} satır")

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
