"""
NASA-TLX Cognitive Load Scale (Hart & Staveland, 1988)
Supports TR/EN via lang parameter.

Scale: 0-100 per dimension (step 5), per the thesis methodology (section 3.3.2).
Total formula:
    NASA-TLX_Total = (Mental + Physical + Temporal + (100 − Performance) + Effort + Frustration) / 6

The 'performance' dimension is reverse-coded:
    0 = Perfect, 100 = Failure
This way a high raw "performance" score indicates a poorer self-perceived performance,
and is combined directly into the total cognitive load formula as (100 − Performance) → wait,
actually we keep performance as collected (0=Perfect, 100=Failure) so the formula simplifies:
    Total = (Mental + Physical + Temporal + Performance + Effort + Frustration) / 6
because the dimension itself is already reverse-coded on the slider.
For backwards compatibility with the thesis formula notation, performance is stored
as-is (0=Perfect → low cognitive load contribution), and total is the simple average.
"""

import streamlit as st
from typing import Dict, Any


class NASATLXForm:
    """NASA-TLX Cognitive Load Scale (TR/EN) – 0..100 sliders."""

    DIMENSIONS = {
        "mental_demand": {
            "title": "Zihinsel Talep (Mental Demand)",
            "question": "Görev ne kadar zihinsel ve algısal faaliyet gerektirdi? (Düşünme, karar verme, hesaplama, hatırlama vb.)",
            "low_label": "Çok Düşük",
            "high_label": "Çok Yüksek",
            "reverse": False,
        },
        "physical_demand": {
            "title": "Fiziksel Talep (Physical Demand)",
            "question": "Görev ne kadar fiziksel faaliyet gerektirdi? (Tıklama, yazma, fare/klavye kullanımı)",
            "low_label": "Çok Düşük",
            "high_label": "Çok Yüksek",
            "reverse": False,
        },
        "temporal_demand": {
            "title": "Zamansal Talep (Temporal Demand)",
            "question": "Görevin hızı veya temposu nedeniyle ne kadar zaman baskısı hissettiniz?",
            "low_label": "Çok Düşük",
            "high_label": "Çok Yüksek",
            "reverse": False,
        },
        "performance": {
            "title": "Performans (Performance)",
            "question": "Görevi tamamlamada ne kadar başarılı olduğunuzu düşünüyorsunuz? (DİKKAT: Ters kodlama — Mükemmel = 0, Başarısız = 100)",
            "low_label": "Mükemmel",
            "high_label": "Başarısız",
            "reverse": True,
        },
        "effort": {
            "title": "Çaba (Effort)",
            "question": "Görevde istediğiniz performans düzeyine ulaşmak için ne kadar çaba sarf ettiniz?",
            "low_label": "Çok Düşük",
            "high_label": "Çok Yüksek",
            "reverse": False,
        },
        "frustration": {
            "title": "Engelleme/Stres (Frustration)",
            "question": "Görev sırasında ne düzeyde güvensizlik, sinir, stres ve rahatsızlık hissettiniz?",
            "low_label": "Çok Düşük",
            "high_label": "Çok Yüksek",
            "reverse": False,
        },
    }

    DIMENSIONS_EN = {
        "mental_demand": {
            "title": "Mental Demand",
            "question": "How much mental and perceptual activity was required? (thinking, deciding, calculating, remembering)",
            "low_label": "Very Low",
            "high_label": "Very High",
            "reverse": False,
        },
        "physical_demand": {
            "title": "Physical Demand",
            "question": "How much physical activity was required? (clicking, typing, mouse/keyboard use)",
            "low_label": "Very Low",
            "high_label": "Very High",
            "reverse": False,
        },
        "temporal_demand": {
            "title": "Temporal Demand",
            "question": "How much time pressure did you feel due to the pace at which the task elements occurred?",
            "low_label": "Very Low",
            "high_label": "Very High",
            "reverse": False,
        },
        "performance": {
            "title": "Performance",
            "question": "How successful do you think you were in accomplishing the goals? (NOTE: reverse coded — Perfect = 0, Failure = 100)",
            "low_label": "Perfect",
            "high_label": "Failure",
            "reverse": True,
        },
        "effort": {
            "title": "Effort",
            "question": "How hard did you have to work to accomplish your level of performance?",
            "low_label": "Very Low",
            "high_label": "Very High",
            "reverse": False,
        },
        "frustration": {
            "title": "Frustration",
            "question": "How insecure, discouraged, irritated, stressed, or annoyed did you feel during the task?",
            "low_label": "Very Low",
            "high_label": "Very High",
            "reverse": False,
        },
    }

    SUMMARY_EN = {
        "summary_title": "Cognitive Load Summary",
        "total": "Total Load (0-100)",
        "average": "Average",
        "highest": "Highest",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
    }

    INTERPRETATION_EN = {
        "low": "Low cognitive load – Task was easy",
        "medium": "Medium cognitive load – Task was appropriately challenging",
        "high": "High cognitive load – Task was demanding",
        "very_high": "Very high cognitive load – Task was extremely demanding",
    }

    @staticmethod
    def get_dimensions(lang: str) -> dict:
        """Return dimension labels and questions in the requested language."""
        return NASATLXForm.DIMENSIONS_EN if lang == "en" else NASATLXForm.DIMENSIONS

    @staticmethod
    def show(lang: str = "tr") -> Dict[str, float]:
        """
        Render NASA-TLX form (0..100 sliders).

        Returns:
            Dict with per-dimension scores (0..100) and:
              - 'total_cognitive_load': average over six dimensions (0..100)
              - performance is reverse-coded on the slider itself; mental model is
                preserved by storing the slider's raw value (0=Perfect, 100=Failure)
                so the simple average matches the thesis formula.
        """
        dimensions = NASATLXForm.get_dimensions(lang)
        summary = NASATLXForm.SUMMARY_EN if lang == "en" else None

        responses: Dict[str, float] = {}

        for key, dimension in dimensions.items():
            st.markdown(f"#### {dimension['title']}")
            st.markdown(f"*{dimension['question']}*")

            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.caption(dimension["low_label"])
            with col2:
                score = st.slider(
                    label="",
                    min_value=0,
                    max_value=100,
                    value=50,
                    step=5,
                    key=f"nasa_tlx_{key}",
                    label_visibility="collapsed",
                )
                responses[key] = float(score)
            with col3:
                st.caption(dimension["high_label"])
            st.markdown("---")

        total_load = round(sum(responses.values()) / 6.0, 1)
        responses["total_cognitive_load"] = total_load

        if summary:
            st.markdown(f"### 📊 {summary['summary_title']}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(summary["total"], f"{total_load}/100")
            with col2:
                load_level = (
                    summary["low"] if total_load < 30
                    else summary["medium"] if total_load < 60
                    else summary["high"]
                )
                st.metric(summary["average"], f"{total_load:.1f}", delta=load_level)
            with col3:
                non_total = {k: v for k, v in responses.items() if k != "total_cognitive_load"}
                if non_total:
                    max_dim = max(non_total.items(), key=lambda x: x[1])
                    st.metric(summary["highest"], dimensions[max_dim[0]]["title"][:20])
        else:
            st.markdown("### 📊 Bilişsel Yük Özeti")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Yük", f"{total_load}/100")
            with col2:
                load_level = "Düşük" if total_load < 30 else "Orta" if total_load < 60 else "Yüksek"
                st.metric("Ortalama", f"{total_load:.1f}", delta=load_level)
            with col3:
                non_total = {k: v for k, v in responses.items() if k != "total_cognitive_load"}
                if non_total:
                    max_dim = max(non_total.items(), key=lambda x: x[1])
                    st.metric(
                        "En Yüksek",
                        NASATLXForm.DIMENSIONS[max_dim[0]]["title"].split("(")[0].strip()[:20],
                    )

        return responses

    @staticmethod
    def get_load_interpretation(total_load: float, lang: str = "tr") -> str:
        """Return load interpretation text in the requested language. Total is 0..100."""
        if lang == "en":
            if total_load < 30:
                return NASATLXForm.INTERPRETATION_EN["low"]
            elif total_load < 50:
                return NASATLXForm.INTERPRETATION_EN["medium"]
            elif total_load < 70:
                return NASATLXForm.INTERPRETATION_EN["high"]
            else:
                return NASATLXForm.INTERPRETATION_EN["very_high"]
        if total_load < 30:
            return "Düşük bilişsel yük - Görev kolaydı"
        elif total_load < 50:
            return "Orta bilişsel yük - Görev uygun zorlukta"
        elif total_load < 70:
            return "Yüksek bilişsel yük - Görev zorlayıcıydı"
        else:
            return "Çok yüksek bilişsel yük - Görev aşırı zorlayıcıydı"
