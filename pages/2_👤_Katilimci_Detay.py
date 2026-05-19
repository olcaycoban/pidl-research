"""
PITL Katılımcı Detay Sayfası
Her katılımcının 6 görevi, kodları, değerlendirmeleri
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Working directory'yi düzelt
if os.path.basename(os.getcwd()) == "pages":
    os.chdir("..")
sys.path.insert(0, os.getcwd())

from database.database import DatabaseSession
from database.models import (
    Participant, TaskSession, PrePostTest, GeneratedCode,
    NASATLXResponse, AICodeEvaluation, FinalEvaluation,
    TaskStatus, AIType, TechnicalMetrics, PedagogicalMetrics
)
from i18n import t, get_lang

PREPOST_QUESTION_COUNT = 5
PREPOST_POINTS_PER_Q = 5
PREPOST_MAX_POINTS = 25


def _prepost_from_percent(score_100: int | None) -> tuple[int, int]:
    """Veritabanındaki 0–100 skor → (toplam/25, doğru soru/5)."""
    if score_100 is None:
        return 0, 0
    pct = max(0, min(100, int(score_100)))
    correct = max(0, min(PREPOST_QUESTION_COUNT, round(pct * PREPOST_QUESTION_COUNT / 100)))
    return correct * PREPOST_POINTS_PER_Q, correct


def _render_prepost_test(test, *, is_post: bool) -> None:
    points, correct = _prepost_from_percent(test.score)
    pct = int(test.score) if test.score is not None else 0
    st.markdown(f"**Toplam Skor:** {points}/{PREPOST_MAX_POINTS} ({correct}/{PREPOST_QUESTION_COUNT} soru doğru, %{pct})")
    active_q = PREPOST_QUESTION_COUNT if is_post else 3
    for i in range(1, PREPOST_QUESTION_COUNT + 1):
        answer = getattr(test, f"q{i}_answer", None)
        if not is_post and i > active_q:
            st.write(f"Soru {i}: — (ön testte uygulanmadı)")
            continue
        q_pts = PREPOST_POINTS_PER_Q if i <= correct else 0
        label = answer if answer else "—"
        st.write(f"Soru {i}: {label} · **{q_pts}/{PREPOST_POINTS_PER_Q}** puan")

# Dil session state
if "lang" not in st.session_state:
    st.session_state.lang = "tr"

# Sayfa yapılandırması
st.set_page_config(
    page_title="Katılımcı Detay",
    page_icon="👤",
    layout="wide"
)

st.markdown("""
<style>
    .participant-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .session-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .code-container {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        max-height: 500px;
        overflow-y: auto;
    }
    .metric-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: dil seçimi
with st.sidebar:
    st.markdown("### 🌐 Language / Dil")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(t("lang.turkish"), key="pg2_lang_tr", use_container_width=True):
            st.session_state.lang = "tr"
            st.rerun()
    with c2:
        if st.button(t("lang.english"), key="pg2_lang_en", use_container_width=True):
            st.session_state.lang = "en"
            st.rerun()
    st.markdown("---")

# Header
st.markdown("# 👤 " + t("participant_detail.title"))
st.markdown("---")

# Katılımcı listesini yükle
@st.cache_data(ttl=10)
def load_participants():
    with DatabaseSession() as session:
        participants = session.query(Participant).all()
        return [{
            "uuid": p.uuid,
            "display_name": f"{p.uuid} - {p.gender}, {p.age} yaş, {p.competency_level.value}",
            "age": p.age,
            "gender": p.gender,
            "education": p.education,
            "work_field": p.work_field,
            "technical_score": p.technical_score,
            "pedagogical_score": p.pedagogical_score,
            "competency_level": p.competency_level.value,
            "completed": p.completed
        } for p in participants]

participants = load_participants()

if len(participants) == 0:
    st.error("❌ " + t("participant_detail.no_data"))
    st.stop()

# Katılımcı seçici
st.sidebar.markdown("## 🔍 " + t("participant_detail.select"))

# Filtreler
filter_gender = st.sidebar.multiselect(
    t("participant_detail.gender"),
    options=list(set([p["gender"] for p in participants])),
    default=None
)

filter_level = st.sidebar.multiselect(
    t("participant_detail.dreyfus"),
    options=list(set([p["competency_level"] for p in participants])),
    default=None
)

# Filtreleme
filtered_participants = participants
if filter_gender:
    filtered_participants = [p for p in filtered_participants if p["gender"] in filter_gender]
if filter_level:
    filtered_participants = [p for p in filtered_participants if p["competency_level"] in filter_level]

st.sidebar.markdown(f"**{len(filtered_participants)} {t('participant_detail.found')}**")

# Katılımcı seçimi
participant_options = {p["display_name"]: p["uuid"] for p in filtered_participants}
selected_display = st.sidebar.selectbox(
    t("participant_detail.participant"),
    options=list(participant_options.keys()),
    index=0
)

selected_uuid = participant_options[selected_display]

# Seçilen katılımcının tam verilerini yükle
@st.cache_data(ttl=10)
def load_participant_full_data(uuid):
    with DatabaseSession() as session:
        # Participant
        participant = session.query(Participant).filter_by(uuid=uuid).first()

        # Task sessions
        task_sessions = session.query(TaskSession).filter_by(participant_uuid=uuid).all()

        # Her session için detayları al
        sessions_data = []
        for ts in task_sessions:
            # Pre/Post tests
            pre_test = session.query(PrePostTest).filter_by(
                task_session_id=ts.id,
                test_type="PRE"
            ).first()
            post_test = session.query(PrePostTest).filter_by(
                task_session_id=ts.id,
                test_type="POST"
            ).first()

            # Generated code
            code = session.query(GeneratedCode).filter_by(task_session_id=ts.id).first()

            # NASA-TLX
            nasa = session.query(NASATLXResponse).filter_by(task_session_id=ts.id).first()

            # AI Evaluation
            ai_eval = session.query(AICodeEvaluation).filter_by(task_session_id=ts.id).first()

            # Technical & Pedagogical metrics
            tech_metrics = None
            ped_metrics = None
            if code:
                tech_metrics = session.query(TechnicalMetrics).filter_by(generated_code_id=code.id).first()
                ped_metrics = session.query(PedagogicalMetrics).filter_by(generated_code_id=code.id).first()

            sessions_data.append({
                "task_session": ts,
                "pre_test": pre_test,
                "post_test": post_test,
                "code": code,
                "nasa_tlx": nasa,
                "ai_eval": ai_eval,
                "tech_metrics": tech_metrics,
                "ped_metrics": ped_metrics
            })

        # Final evaluation
        final_eval = session.query(FinalEvaluation).filter_by(participant_uuid=uuid).first()

        return {
            "participant": participant,
            "sessions": sessions_data,
            "final_eval": final_eval
        }

data = load_participant_full_data(selected_uuid)

# 1. KATILIMCI BİLGİLERİ
st.markdown(f"""
<div class="participant-card">
    <h2>👤 {data['participant'].uuid}</h2>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
        <div>
            <strong>{t('participant_detail.age')}:</strong> {data['participant'].age}<br>
            <strong>{t('participant_detail.gender')}:</strong> {data['participant'].gender}<br>
            <strong>Eğitim:</strong> {data['participant'].education}
        </div>
        <div>
            <strong>{t('participant_detail.work_field')}:</strong> {data['participant'].work_field}<br>
            <strong>{t('participant_detail.technical_score')}:</strong> {data['participant'].technical_score}/60 (CAQ)<br>
            <strong>{t('participant_detail.pedagogical_score')}:</strong> {data['participant'].pedagogical_score}/60 (CAQ)
        </div>
        <div>
            <strong>{t('participant_detail.dreyfus')}:</strong> {data['participant'].competency_level.value}<br>
            <strong>{t('participant_detail.completed_q')}:</strong> {'✅ ' + t('participant_detail.yes') if data['participant'].completed else '❌ ' + t('participant_detail.no')}<br>
            <strong>{t('participant_detail.total_duration')}:</strong> {data['participant'].total_duration_minutes or 0} dk
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. ÖZET İSTATİSTİKLER
st.markdown("## 📊 " + t("participant_detail.summary_stats"))

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_tasks = len(data["sessions"])
    st.metric(t("participant_detail.total_tasks"), total_tasks)

with col2:
    similar_count = sum(1 for s in data["sessions"]
                       if s["task_session"].assigned_ai_type == AIType.SIMILAR)
    st.metric("Similar Mod", similar_count)

with col3:
    comp_count = sum(1 for s in data["sessions"]
                    if s["task_session"].assigned_ai_type == AIType.COMPLEMENTARY)
    st.metric("Complementary Mod", comp_count)

with col4:
    if data["sessions"]:
        avg_duration = sum(s["task_session"].duration_minutes or 0 for s in data["sessions"]) / len(data["sessions"])
        st.metric(t("participant_detail.avg_duration"), f"{avg_duration:.1f} dk")
    else:
        st.metric(t("participant_detail.avg_duration"), "N/A")

with col5:
    # Learning gain
    learning_gains = []
    for s in data["sessions"]:
        if s["pre_test"] and s["post_test"]:
            post_pts, _ = _prepost_from_percent(s["post_test"].score)
            pre_pts, _ = _prepost_from_percent(s["pre_test"].score)
            learning_gains.append(post_pts - pre_pts)

    if learning_gains:
        avg_gain = sum(learning_gains) / len(learning_gains)
        st.metric("Ort. Learning Gain", f"+{avg_gain:.1f}", help="Görev ön/son test farkı (0–25 puan)")
    else:
        st.metric("Ort. Learning Gain", "N/A")

st.markdown("---")

# 3. GÖREV DETAYLARI
st.markdown("## 📝 " + t("participant_detail.task_details"))

for idx, session_data in enumerate(data["sessions"], 1):
    ts = session_data["task_session"]

    # AI type display
    ai_mode_display = "Similar" if ts.assigned_ai_type == AIType.SIMILAR else "Complementary"
    status_display = t("participant_detail.completed") if ts.status == TaskStatus.COMPLETED else t("participant_detail.in_progress")

    with st.expander(f"🎯 {t('task.title')} {ts.task_number} - {ai_mode_display} Mod - {ts.assigned_persona}", expanded=(idx == 1)):

        # Görev başlığı
        st.markdown(f"""
        <div class="session-card">
            <h3>{t('task.title')} {ts.task_number}</h3>
            <strong>AI Mod:</strong> {ai_mode_display}<br>
            <strong>Persona:</strong> {ts.assigned_persona}<br>
            <strong>Status:</strong> {status_display}<br>
            <strong>{t('participant_detail.total_duration')}:</strong> {ts.duration_minutes} dk
        </div>
        """, unsafe_allow_html=True)

        # Tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📝 " + t("participant_detail.prompt_code"),
            "📊 " + t("participant_detail.pre_post"),
            "🧠 NASA-TLX",
            "⭐ " + t("participant_detail.ai_eval"),
            "🔧 " + t("participant_detail.tech_metrics"),
            "📚 " + t("participant_detail.ped_metrics")
        ])

        # TAB 1: PROMPT & KOD
        with tab1:
            if session_data["code"]:
                st.markdown("### 💬 " + t("participant_detail.used_prompt"))
                st.info(session_data["code"].prompt_used)

                st.markdown("### 💻 " + t("participant_detail.generated_code"))
                st.markdown(f"**{t('participant_detail.language')}:** {session_data['code'].language} | **{t('participant_detail.gen_time')}:** {session_data['code'].generation_time_seconds:.1f}s")

                st.markdown(f"""
                <div class="code-container">
{session_data['code'].code_text}
                </div>
                """, unsafe_allow_html=True)

                # Download button
                st.download_button(
                    "📥 " + t("participant_detail.download_code"),
                    session_data["code"].code_text,
                    file_name=f"task_{ts.task_number}_code.sol",
                    mime="text/plain"
                )
            else:
                st.warning(t("participant_detail.code_not_found"))

        # TAB 2: PRE/POST TEST
        with tab2:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📝 Pre-Test")
                if session_data["pre_test"]:
                    _render_prepost_test(session_data["pre_test"], is_post=False)
                else:
                    st.warning("Pre-test verisi yok")

            with col2:
                st.markdown("### 📝 Post-Test")
                if session_data["post_test"]:
                    _render_prepost_test(session_data["post_test"], is_post=True)

                    if session_data["pre_test"]:
                        post_pts, _ = _prepost_from_percent(session_data["post_test"].score)
                        pre_pts, _ = _prepost_from_percent(session_data["pre_test"].score)
                        gain = post_pts - pre_pts
                        sign = "+" if gain >= 0 else ""
                        st.success(f"**Learning Gain:** {sign}{gain} puan (/25)")
                else:
                    st.warning("Post-test verisi yok")

        # TAB 3: NASA-TLX
        with tab3:
            if session_data["nasa_tlx"]:
                nasa = session_data["nasa_tlx"]

                st.markdown("### 🧠 Bilişsel Yük (NASA-TLX)")

                # Radar chart
                categories = ['Mental Demand', 'Physical Demand', 'Temporal Demand',
                            'Performance', 'Effort', 'Frustration']
                values = [
                    nasa.mental_demand,
                    nasa.physical_demand,
                    nasa.temporal_demand,
                    10 - nasa.performance,  # Inverse
                    nasa.effort,
                    nasa.frustration
                ]

                fig = go.Figure(data=go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                    showlegend=False,
                    title="NASA-TLX Dimensions"
                )
                st.plotly_chart(fig, use_container_width=True)

                st.metric("Toplam Bilişsel Yük", f"{nasa.total_cognitive_load}/60")
            else:
                st.warning("NASA-TLX verisi yok")

        # TAB 4: AI DEĞERLENDIRME
        with tab4:
            if session_data["ai_eval"]:
                ai = session_data["ai_eval"]

                st.markdown("### ⭐ AI Kod Değerlendirmesi")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Code Understandability", f"{ai.code_understandability}/10")
                    st.metric("Explanation Quality", f"{ai.explanation_quality}/10")

                with col2:
                    st.metric("Educational Value", f"{ai.educational_value}/10")
                    st.metric("Perceived Quality", f"{ai.perceived_code_quality}/10")

                with col3:
                    st.metric("Perceived Security", f"{ai.perceived_security}/10")
                    avg = (ai.code_understandability + ai.explanation_quality +
                          ai.educational_value + ai.perceived_code_quality +
                          ai.perceived_security) / 5
                    st.metric("Ortalama", f"{avg:.1f}/10")

                if ai.best_aspect:
                    st.success(f"**En iyi yönü:** {ai.best_aspect}")
                if ai.improvement_needed:
                    st.warning(f"**Geliştirilebilir:** {ai.improvement_needed}")
            else:
                st.warning("AI değerlendirme verisi yok")

        # TAB 5: TECHNICAL METRICS
        with tab5:
            if session_data["tech_metrics"]:
                tech = session_data["tech_metrics"]

                st.markdown("### 🔧 Technical Metrics (Yazılımcı Bakışı)")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Manuel Değerlendirme (1-10)**")
                    st.metric("Security", f"{tech.security_score}/10")
                    st.metric("Gas Optimization", f"{tech.gas_optimization_score}/10")
                    st.metric("Code Quality", f"{tech.code_quality_score}/10")
                    st.metric("Maintainability", f"{tech.maintainability_score}/10")
                    st.metric("Production Readiness", f"{tech.production_readiness}/10")

                with col2:
                    st.markdown("**Otomatik Analiz (0-100)**")
                    if tech.auto_security_score:
                        st.metric("Auto Security", f"{tech.auto_security_score:.1f}/100")
                    if tech.auto_gas_score:
                        st.metric("Auto Gas", f"{tech.auto_gas_score:.1f}/100")
                    if tech.auto_complexity_score:
                        st.metric("Auto Complexity", f"{tech.auto_complexity_score:.1f}/100")
            else:
                st.warning("Technical metrics verisi yok")

        # TAB 6: PEDAGOGICAL METRICS
        with tab6:
            if session_data["ped_metrics"]:
                ped = session_data["ped_metrics"]

                st.markdown("### 📚 Pedagogical Metrics (Eğitimci Bakışı)")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Learning Ease", f"{ped.learning_ease_score}/10")
                    st.metric("Instructiveness", f"{ped.instructiveness_score}/10")
                    st.metric("Cognitive Load", f"{ped.cognitive_load_score}/10",
                            help="Düşük=iyi")
                    st.metric("Example Quality", f"{ped.example_quality_score}/10")

                with col2:
                    st.metric("Scaffolding", f"{ped.scaffolding_score}/10")
                    if ped.explanation_quality:
                        st.metric("Explanation Quality", f"{ped.explanation_quality}/10")
                    if ped.bloom_taxonomy_level:
                        st.info(f"**Bloom Taxonomy:** {ped.bloom_taxonomy_level}")
            else:
                st.warning("Pedagogical metrics verisi yok")

st.markdown("---")

# 4. FINAL EVALUATION
if data["final_eval"]:
    st.markdown("## 🎓 Final Değerlendirme")

    final = data["final_eval"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🤖 AI Tercihleri")
        st.write(f"**Tercih Edilen AI:** {final.preferred_ai}")
        st.write(f"**Sebep:** {final.preferred_ai_reason}")
        st.write(f"**Öğrenme için Daha İyi:** {final.learning_better_ai}")
        st.write(f"**Hız için Daha İyi:** {final.speed_better_ai}")

    with col2:
        st.markdown("### ⭐ Genel Değerlendirme")
        st.metric("AI Learning Rating", f"{final.ai_learning_rating}/10")
        st.write(f"**Tavsiye Eder mi:** {final.would_recommend}")
        st.write(f"**En Zor Görev:** {final.hardest_task}")

    if final.suggestions:
        st.info(f"**Öneriler:** {final.suggestions}")

