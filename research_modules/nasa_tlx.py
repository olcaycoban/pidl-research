"""
NASA-TLX Cognitive Load Scale
Supports TR/EN via lang parameter.
"""

import streamlit as st
from typing import Dict, Any


class NASATLXForm:
    """NASA-TLX Cognitive Load Scale (TR/EN)"""

    DIMENSIONS = {
        "mental_demand": {
            "title": "Zihinsel Talep (Mental Demand)",
            "question": "Bu görevi yapmak ne kadar zihinsel çaba gerektirdi?",
            "low_label": "Çok Az",
            "high_label": "Çok Fazla"
        },
        "physical_demand": {
            "title": "Fiziksel Talep (Physical Demand)",
            "question": "Bu görev ne kadar fiziksel aktivite gerektirdi?",
            "low_label": "Çok Az",
            "high_label": "Çok Fazla"
        },
        "temporal_demand": {
            "title": "Zamansal Talep (Temporal Demand)",
            "question": "Zaman baskısı ne kadar hissettiniz?",
            "low_label": "Çok Az",
            "high_label": "Çok Fazla"
        },
        "performance": {
            "title": "Performans (Performance)",
            "question": "Görevi ne kadar başarılı tamamladığınızı düşünüyorsunuz?",
            "low_label": "Başarısız",
            "high_label": "Mükemmel"
        },
        "effort": {
            "title": "Çaba (Effort)",
            "question": "Bu görevi başarmak için ne kadar çaba harcadınız?",
            "low_label": "Çok Az",
            "high_label": "Çok Fazla"
        },
        "frustration": {
            "title": "Hayal Kırıklığı (Frustration)",
            "question": "Görev sırasında ne kadar sinirli, stresli veya hayal kırıklığı yaşadınız?",
            "low_label": "Çok Az",
            "high_label": "Çok Fazla"
        }
    }

    DIMENSIONS_EN = {
        "mental_demand": {
            "title": "Mental Demand",
            "question": "How much mental effort did it take to complete this task?",
            "low_label": "Very Little",
            "high_label": "Very Much"
        },
        "physical_demand": {
            "title": "Physical Demand",
            "question": "How much physical activity did this task require?",
            "low_label": "Very Little",
            "high_label": "Very Much"
        },
        "temporal_demand": {
            "title": "Temporal Demand",
            "question": "How much time pressure did you feel?",
            "low_label": "Very Little",
            "high_label": "Very Much"
        },
        "performance": {
            "title": "Performance",
            "question": "How successfully do you feel you completed the task?",
            "low_label": "Failure",
            "high_label": "Perfect"
        },
        "effort": {
            "title": "Effort",
            "question": "How much effort did you put into accomplishing this task?",
            "low_label": "Very Little",
            "high_label": "Very Much"
        },
        "frustration": {
            "title": "Frustration",
            "question": "How stressed, irritated, or frustrated did you feel during the task?",
            "low_label": "Very Little",
            "high_label": "Very Much"
        }
    }

    SUMMARY_EN = {
        "summary_title": "Cognitive Load Summary",
        "total": "Total Load",
        "average": "Average",
        "highest": "Highest",
        "low": "Low",
        "medium": "Medium",
        "high": "High"
    }

    INTERPRETATION_EN = {
        "low": "Low cognitive load – Task was easy",
        "medium": "Medium cognitive load – Task was appropriately challenging",
        "high": "High cognitive load – Task was demanding",
        "very_high": "Very high cognitive load – Task was extremely demanding"
    }

    @staticmethod
    def get_dimensions(lang: str) -> dict:
        """Return dimension labels and questions in the requested language."""
        return NASATLXForm.DIMENSIONS_EN if lang == "en" else NASATLXForm.DIMENSIONS

    @staticmethod
    def show(lang: str = "tr") -> Dict[str, int]:
        """
        Render NASA-TLX form. Title and intro are shown by the caller (research_app) via i18n.

        Returns:
            Dimension scores {dimension: score (1-10)} plus total_cognitive_load.
        """
        dimensions = NASATLXForm.get_dimensions(lang)
        summary = NASATLXForm.SUMMARY_EN if lang == "en" else None

        responses = {}

        for key, dimension in dimensions.items():
            st.markdown(f"#### {dimension['title']}")
            st.markdown(f"*{dimension['question']}*")

            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.caption(dimension['low_label'])
            with col2:
                score = st.slider(
                    label="",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key=f"nasa_tlx_{key}",
                    label_visibility="collapsed"
                )
                responses[key] = score
            with col3:
                st.caption(dimension['high_label'])
            st.markdown("---")

        total_load = sum(responses.values())
        responses['total_cognitive_load'] = total_load

        if summary:
            st.markdown(f"### 📊 {summary['summary_title']}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(summary['total'], f"{total_load}/60")
            with col2:
                avg_load = total_load / 6
                load_level = summary['low'] if avg_load < 4 else summary['medium'] if avg_load < 7 else summary['high']
                st.metric(summary['average'], f"{avg_load:.1f}/10", delta=load_level)
            with col3:
                max_dim = max(responses.items(), key=lambda x: x[1] if x[0] != 'total_cognitive_load' else 0)
                if max_dim[0] != 'total_cognitive_load':
                    st.metric(summary['highest'], dimensions[max_dim[0]]['title'][:20])
        else:
            st.markdown("### 📊 Bilişsel Yük Özeti")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Yük", f"{total_load}/60")
            with col2:
                avg_load = total_load / 6
                load_level = "Düşük" if avg_load < 4 else "Orta" if avg_load < 7 else "Yüksek"
                st.metric("Ortalama", f"{avg_load:.1f}/10", delta=load_level)
            with col3:
                max_dim = max(responses.items(), key=lambda x: x[1] if x[0] != 'total_cognitive_load' else 0)
                if max_dim[0] != 'total_cognitive_load':
                    st.metric("En Yüksek", NASATLXForm.DIMENSIONS[max_dim[0]]['title'].split('(')[0].strip()[:20])

        return responses

    @staticmethod
    def get_load_interpretation(total_load: int, lang: str = "tr") -> str:
        """Return load interpretation text in the requested language."""
        if lang == "en":
            if total_load < 20:
                return NASATLXForm.INTERPRETATION_EN["low"]
            elif total_load < 35:
                return NASATLXForm.INTERPRETATION_EN["medium"]
            elif total_load < 50:
                return NASATLXForm.INTERPRETATION_EN["high"]
            else:
                return NASATLXForm.INTERPRETATION_EN["very_high"]
        if total_load < 20:
            return "Düşük bilişsel yük - Görev kolaydı"
        elif total_load < 35:
            return "Orta bilişsel yük - Görev uygun zorlukta"
        elif total_load < 50:
            return "Yüksek bilişsel yük - Görev zorlayıcıydı"
        else:
            return "Çok yüksek bilişsel yük - Görev aşırı zorlayıcıydı"
