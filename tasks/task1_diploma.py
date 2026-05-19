"""
Görev 1: Diploma Doğrulama Sistemi
Zorluk: Düşük
"""

from .base_task import BaseTask
from typing import List, Dict, Any


class Task1Diploma(BaseTask):
    def __init__(self):
        super().__init__()
        self.task_number = 1
        self.difficulty = "Düşük"
        self.title = "Diploma Doğrulama Sistemi"
        self.description = """Üniversite için blockchain tabanlı diploma doğrulama sistemi oluşturun:

**Gereksinimler:**
- Sadece üniversite yönetimi diploma ekleyebilsin
- Diploma hash'i ve öğrenci bilgileri saklanacak
- Mezuniyet tarihi kaydedilecek
- Herkes diploma doğrulayabilsin
- İptal edilebilir diploma özelliği

**Beklenen Fonksiyonlar:**
- `addDiploma(address student, bytes32 diplomaHash, string memory studentName, uint256 graduationDate)`
- `verifyDiploma(address student) returns (bool, bytes32, string, uint256)`
- `revokeDiploma(address student)`
- `isDiplomaValid(address student) returns (bool)`
"""

    def _get_pre_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "Blockchain'de diploma saklamanın avantajı nedir?", "type": "multiple_choice",
             "options": ["Değiştirilemez kayıt", "Daha ucuz", "Daha hızlı", "Bilmiyorum"], "correct_answer": "Değiştirilemez kayıt"},
            {"id": "q2", "question": "Hash fonksiyonu ne işe yarar?", "type": "multiple_choice",
             "options": ["Şifreleme yapar", "Benzersiz parmak izi oluşturur", "Veri sıkıştırır", "Bilmiyorum"], "correct_answer": "Benzersiz parmak izi oluşturur"},
            {"id": "q3", "question": "onlyOwner modifier'ı eğitim kurumları için neden önemlidir?", "type": "open_ended", "placeholder": "Cevabınızı buraya yazın..."}
        ]

    def _get_pre_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "What is the advantage of storing diplomas on blockchain?", "type": "multiple_choice",
             "options": ["Immutable record", "Cheaper", "Faster", "I don't know"], "correct_answer": "Immutable record"},
            {"id": "q2", "question": "What does a hash function do?", "type": "multiple_choice",
             "options": ["Encrypts data", "Creates a unique fingerprint", "Compresses data", "I don't know"], "correct_answer": "Creates a unique fingerprint"},
            {"id": "q3", "question": "Why is the onlyOwner modifier important for educational institutions?", "type": "open_ended", "placeholder": "Write your answer here..."}
        ]

    def get_pre_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_pre_test_questions_en() if self._get_lang() == "en" else self._get_pre_test_questions_tr()

    def _get_post_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q4", "question": "Diploma hash'i yerine tüm diploma verisini saklamak ne gibi sorunlar yaratır?", "type": "multiple_choice",
             "options": ["Gas maliyeti artar", "Gizlilik sorunu", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q5", "question": "Sahte diploma ile mücadelede blockchain nasıl yardımcı olur?", "type": "open_ended", "placeholder": "Cevabınızı buraya yazın..."}
        ]

    def _get_post_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q4", "question": "What problems does storing full diploma data instead of a hash create?", "type": "multiple_choice",
             "options": ["Higher gas cost", "Privacy issues", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q5", "question": "How does blockchain help combat fake diplomas?", "type": "open_ended", "placeholder": "Write your answer here..."}
        ]

    def get_post_test_questions(self) -> List[Dict[str, Any]]:
        pre = self.get_pre_test_questions()
        post_only = self._get_post_test_questions_en() if self._get_lang() == "en" else self._get_post_test_questions_tr()
        return pre + post_only

    def get_evaluation_criteria(self) -> Dict[str, Dict[str, int]]:
        return {
            "functionality": {
                "compiles": 10,
                "has_add_diploma": 10,
                "has_verify_diploma": 10,
                "total": 30
            },
            "security": {
                "onlyOwner_modifier": 10,
                "input_validation": 8,
                "revoke_function": 7,
                "total": 25
            },
            "gas_optimization": {
                "efficient_storage": 10,
                "minimal_operations": 8,
                "events_usage": 7,
                "total": 25
            },
            "code_quality": {
                "naming_convention": 7,
                "comments": 6,
                "structure": 7,
                "total": 20
            }
        }
