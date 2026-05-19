"""
Bilgilendirilmiş Onam Formu
KVKK/GDPR uyumlu katılımcı onay formu
"""

import streamlit as st
from typing import Dict, Any

try:
    from i18n import t
except ImportError:
    def t(key: str, **kwargs) -> str:
        return key


class ConsentForm:
    """Bilgilendirilmiş onam formu"""

    @staticmethod
    def show() -> bool:
        """
        Onam formunu göster

        Returns:
            True if consent given, False otherwise
        """
        st.markdown("# 📋 " + t("consent.form_title"))

        st.markdown(f"""
        ### {t("consent.research_name")}
        **{t("consent.research_name_value")}**

        ---

        ### 🎯 {t("consent.research_objective")}
        {t("consent.research_objective_value")}

        ### ⏱️ {t("consent.participation_process")}
        {t("consent.participation_intro")}
        - **{t("consent.session1")}**
        - **{t("consent.session2")}**
        - **{t("consent.total_duration")}**

        ### 📝 {t("consent.what_you_will_do")}
        1. {t("consent.what_1")}
        2. {t("consent.what_2")}
        3. {t("consent.what_3")}
        4. {t("consent.what_4")}

        ### ⚠️ {t("consent.risks")}
        - {t("consent.risk_1")}
        - {t("consent.risk_2")}
        - {t("consent.risk_3")}

        ### ✅ {t("consent.benefits")}
        - {t("consent.benefit_1")}
        - {t("consent.benefit_2")}
        - {t("consent.benefit_3")}
        - {t("consent.benefit_4")}
        - {t("consent.benefit_5")}

        ### 🔒 {t("consent.privacy")}
        - {t("consent.privacy_1")}
        - {t("consent.privacy_2")}
        - {t("consent.privacy_3")}
        - {t("consent.privacy_4")}

        ### 🤝 {t("consent.your_rights")}
        - ✓ {t("consent.right_1")}
        - ✓ {t("consent.right_2")}
        - ✓ {t("consent.right_3")}
        - ✓ {t("consent.right_4")}
        - ✓ {t("consent.right_5")}

        ### 📧 {t("consent.contact_heading")}
        {t("consent.contact_questions")}
        {t("consent.contact_ethics")}

        ---
        """)

        st.markdown("### 📋 " + t("consent.consent_heading"))

        col1, col2 = st.columns([1, 10])

        consents = []

        with col1:
            c1 = st.checkbox("", key="consent1")
        with col2:
            st.markdown(t("consent.check_1"))
        consents.append(c1)

        with col1:
            c2 = st.checkbox("", key="consent2")
        with col2:
            st.markdown(t("consent.check_2"))
        consents.append(c2)

        with col1:
            c3 = st.checkbox("", key="consent3")
        with col2:
            st.markdown(t("consent.check_3"))
        consents.append(c3)

        with col1:
            c4 = st.checkbox("", key="consent4")
        with col2:
            st.markdown(t("consent.check_4"))
        consents.append(c4)

        with col1:
            c5 = st.checkbox("", key="consent5")
        with col2:
            st.markdown(t("consent.check_5"))
        consents.append(c5)

        st.markdown("---")

        # Tüm onaylar verildi mi?
        all_consents_given = all(consents)

        if all_consents_given:
            st.success("✅ " + t("consent.success_all"))
        else:
            st.warning("⚠️ " + t("consent.warning_check_all"))

        return all_consents_given

    @staticmethod
    def get_consent_data() -> Dict[str, Any]:
        """Onam verilerini döndür"""
        return {
            "consent_given": True,
            "consent_timestamp": st.session_state.get('consent_timestamp'),
            "participant_uuid": st.session_state.get('participant_uuid')
        }
