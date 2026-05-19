"""
Pre-test ve Post-test Form Modülü
Her görev öncesi ve sonrası bilgi testleri
"""

import streamlit as st
from typing import Dict, Any, List

try:
    from i18n import t
except ImportError:
    def t(key: str, **kwargs) -> str:
        return key if not kwargs else key


class PrePostTestForm:
    """Pre-test ve Post-test formları"""

    @staticmethod
    def show_test(questions: List[Dict[str, Any]], test_type: str = "pre") -> Dict[str, str]:
        """
        Test sorularını göster ve cevapları topla

        Args:
            questions: Soru listesi
            test_type: "pre" veya "post"

        Returns:
            Cevaplar dictionary {question_id: answer}
        """
        test_title = "📝 " + (t("pre_post.pretest_title") if test_type == "pre" else t("pre_post.posttest_title"))
        st.markdown(f"### {test_title}")

        if test_type == "pre":
            st.info("**" + t("pre_post.pretest_info") + "**")
        else:
            st.info("**" + t("pre_post.posttest_info") + "**")

        answers = {}

        for i, question in enumerate(questions):
            question_id = question.get("id", f"q{i+1}")
            question_text = question.get("question", "")
            question_type = question.get("type", "multiple_choice")

            st.markdown(f"**{i+1}. {question_text}**")

            if question_type == "multiple_choice":
                options = question.get("options", [])
                answer = st.radio(
                    t("pre_post.select_answer"),
                    options,
                    key=f"{test_type}_{question_id}",
                    label_visibility="collapsed"
                )
                answers[question_id] = answer

            elif question_type == "open_ended":
                placeholder = question.get("placeholder", t("pre_post.placeholder"))
                answer = st.text_area(
                    t("pre_post.your_answer"),
                    placeholder=placeholder,
                    key=f"{test_type}_{question_id}",
                    height=100,
                    label_visibility="collapsed"
                )
                answers[question_id] = answer

            st.markdown("---")

        return answers

    @staticmethod
    def calculate_score(answers: Dict[str, str], questions: List[Dict[str, Any]]) -> int:
        """
        Test skorunu hesapla

        Args:
            answers: Kullanıcı cevapları
            questions: Soru listesi

        Returns:
            Puan (0-100)
        """
        correct_count = 0
        total_questions = len(questions)

        for question in questions:
            question_id = question.get("id", "")
            user_answer = answers.get(question_id, "")

            if question.get("type") == "multiple_choice":
                correct_answer = question.get("correct_answer", "")
                if user_answer == correct_answer:
                    correct_count += 1

            elif question.get("type") == "open_ended":
                # Açık uçlu sorular için basit kontrol
                if len(user_answer.strip()) > 20:
                    correct_count += 0.5  # Kısmi puan

        if total_questions == 0:
            return 0

        score = int((correct_count / total_questions) * 100)
        return score

    @staticmethod
    def show_score_feedback(score: int, test_type: str = "pre"):
        """Skor geri bildirimi göster"""
        if test_type == "post":
            if score >= 80:
                st.success(f"🎉 " + t("pre_post.score_excellent", score=score))
                st.balloons()
            elif score >= 60:
                st.success(f"✅ " + t("pre_post.score_good", score=score))
            elif score >= 40:
                st.info(f"📊 " + t("pre_post.score_info_msg", score=score))
            else:
                st.warning(f"📊 " + t("pre_post.score_info_msg", score=score))
        else:
            # Pre-test için sadece bilgilendirme
            st.info("📊 " + t("pre_post.pretest_done_info"))
