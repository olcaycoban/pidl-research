"""
Görev 5: Öğretmen Teşvik ve Ödül Sistemi
Zorluk: Yüksek
"""

from .base_task import BaseTask
from typing import List, Dict, Any


class Task5Incentive(BaseTask):
    def __init__(self):
        super().__init__()
        self.task_number = 5
        self.difficulty = "Yüksek"
        self.title = "Öğretmen Teşvik ve Ödül Sistemi"
        self.description = """Kaliteli eğitim içeriği üreten öğretmenler için teşvik sistemi:

**Gereksinimler:**
- Öğretmen içerik yüklesin (kurs, video, materyal)
- Öğrenci oylaması (5 üzerinden puan)
- Öğrenci performansına göre bonus
- Stake edilmiş EDU token ile ağırlıklı oylama
- Aylık ödül havuzu dağıtımı
- En iyi öğretmenlere NFT badge
- Compound rewards sistemi

**Beklenen Fonksiyonlar:**
- `submitContent(string memory contentHash, string memory title)`
- `voteForTeacher(address teacher, uint8 rating, uint256 stakedAmount)`
- `calculateTeacherScore(address teacher) returns (uint256)`
- `distributeMonthlyRewards()`
- `claimRewards()`
"""

    def _get_pre_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "Eğitimde tokenomics nasıl motive edici olabilir?", "type": "multiple_choice",
             "options": ["Finansal teşvik", "Şeffaf değerlendirme", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q2", "question": "Quadratic voting eğitimde nasıl kullanılır?", "type": "multiple_choice",
             "options": ["Adil oylama için", "Whale dominansını önlemek için", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q3", "question": "Öğretmen performansının on-chain ölçümünün avantajı nedir?", "type": "multiple_choice",
             "options": ["Şeffaf ve manipülasyona kapalı değerlendirme sağlar", "Değerlendirmeyi daha hızlı yapar", "Her zaman daha ucuzdur", "Bilmiyorum"],
             "correct_answer": "Şeffaf ve manipülasyona kapalı değerlendirme sağlar"},
            {"id": "q4", "question": "Staking mekanizması ne sağlar?", "type": "multiple_choice",
             "options": ["Token kilitleyerek sisteme bağlılık ve oy ağırlığı kazandırır", "Token çoğaltır", "Gas ücretini azaltır", "Bilmiyorum"],
             "correct_answer": "Token kilitleyerek sisteme bağlılık ve oy ağırlığı kazandırır"},
            {"id": "q5", "question": "Solidity'de `event` yapısı ne işe yarar?", "type": "multiple_choice",
             "options": ["Zincir dışı sistemlere bildirim gönderir", "Başka bir fonksiyon çağırır", "Gas tasarrufu sağlar", "Bilmiyorum"],
             "correct_answer": "Zincir dışı sistemlere bildirim gönderir"},
        ]

    def _get_pre_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "How can tokenomics be motivating in education?", "type": "multiple_choice",
             "options": ["Financial incentive", "Transparent evaluation", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q2", "question": "How is quadratic voting used in education?", "type": "multiple_choice",
             "options": ["For fair voting", "To prevent whale dominance", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q3", "question": "What is the advantage of measuring teacher performance on-chain?", "type": "multiple_choice",
             "options": ["Provides transparent and tamper-proof evaluation", "Makes evaluation faster", "Always cheaper", "I don't know"],
             "correct_answer": "Provides transparent and tamper-proof evaluation"},
            {"id": "q4", "question": "What does staking provide?", "type": "multiple_choice",
             "options": ["Locks tokens to earn commitment and voting weight", "Multiplies tokens", "Reduces gas fees", "I don't know"],
             "correct_answer": "Locks tokens to earn commitment and voting weight"},
            {"id": "q5", "question": "What does an `event` structure do in Solidity?", "type": "multiple_choice",
             "options": ["Sends notifications to off-chain systems", "Calls another function", "Saves gas", "I don't know"],
             "correct_answer": "Sends notifications to off-chain systems"},
        ]

    def get_pre_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_pre_test_questions_en() if self._get_lang() == "en" else self._get_pre_test_questions_tr()

    def _get_post_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "Eğitimde tokenomics nasıl motive edici olabilir?", "type": "multiple_choice",
             "options": ["Finansal teşvik", "Şeffaf değerlendirme", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q2", "question": "Quadratic voting eğitimde nasıl kullanılır?", "type": "multiple_choice",
             "options": ["Adil oylama için", "Whale dominansını önlemek için", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q3", "question": "Öğretmen performansının on-chain ölçümünün avantajı nedir?", "type": "multiple_choice",
             "options": ["Şeffaf ve manipülasyona kapalı değerlendirme sağlar", "Değerlendirmeyi daha hızlı yapar", "Her zaman daha ucuzdur", "Bilmiyorum"],
             "correct_answer": "Şeffaf ve manipülasyona kapalı değerlendirme sağlar"},
            {"id": "q4", "question": "Sybil-resistant oylama neden önemlidir?", "type": "multiple_choice",
             "options": ["Sahte hesapları önlemek", "Adil değerlendirme", "Her ikisi de", "Bilmiyorum"],
             "correct_answer": "Her ikisi de"},
            {"id": "q5", "question": "Eğitimde outcome-based rewards'ın activity-based'e göre avantajı nedir?", "type": "multiple_choice",
             "options": ["Gerçek öğrenme çıktısını ödüllendirir, manipülasyona daha kapalıdır", "Hesaplaması daha kolaydır", "Her öğretmene eşit ödül verir", "Bilmiyorum"],
             "correct_answer": "Gerçek öğrenme çıktısını ödüllendirir, manipülasyona daha kapalıdır"},
        ]

    def _get_post_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "How can tokenomics be motivating in education?", "type": "multiple_choice",
             "options": ["Financial incentive", "Transparent evaluation", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q2", "question": "How is quadratic voting used in education?", "type": "multiple_choice",
             "options": ["For fair voting", "To prevent whale dominance", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q3", "question": "What is the advantage of measuring teacher performance on-chain?", "type": "multiple_choice",
             "options": ["Provides transparent and tamper-proof evaluation", "Makes evaluation faster", "Always cheaper", "I don't know"],
             "correct_answer": "Provides transparent and tamper-proof evaluation"},
            {"id": "q4", "question": "Why is Sybil-resistant voting important?", "type": "multiple_choice",
             "options": ["To prevent fake accounts", "Fair evaluation", "Both", "I don't know"],
             "correct_answer": "Both"},
            {"id": "q5", "question": "Advantage of outcome-based rewards over activity-based in education?", "type": "multiple_choice",
             "options": ["Rewards actual learning outcomes and is harder to game", "Easier to calculate", "Gives equal rewards to all teachers", "I don't know"],
             "correct_answer": "Rewards actual learning outcomes and is harder to game"},
        ]

    def get_post_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_post_test_questions_en() if self._get_lang() == "en" else self._get_post_test_questions_tr()

    def get_evaluation_criteria(self) -> Dict[str, Dict[str, int]]:
        return {
            "functionality": {
                "compiles": 10,
                "voting_system": 10,
                "reward_distribution": 10,
                "total": 30
            },
            "security": {
                "sybil_resistance": 10,
                "overflow_protection": 8,
                "access_control": 7,
                "total": 25
            },
            "gas_optimization": {
                "storage": 10,
                "calculation_efficiency": 8,
                "events": 7,
                "total": 25
            },
            "code_quality": {
                "naming": 7,
                "comments": 6,
                "structure": 7,
                "total": 20
            }
        }
