"""
Görev 2: Öğrenci Başarı NFT Sistemi
Zorluk: Düşük-Orta
"""

from .base_task import BaseTask
from typing import List, Dict, Any


class Task2NFT(BaseTask):
    def __init__(self):
        super().__init__()
        self.task_number = 2
        self.difficulty = "Düşük-Orta"
        self.title = "Öğrenci Başarı NFT Sistemi"
        self.description = """Öğrenci başarılarını NFT olarak ödüllendiren sistem:

**Gereksinimler:**
- Her başarı unique NFT olacak (Matematik Şampiyonu, Proje Ödülü vs.)
- Öğretmen/yönetici mint edebilsin
- NFT'ler transfer edilemesin (soulbound)
- Metadata: Başarı türü, tarih, açıklama
- Başarı kategorileri olsun

**Beklenen Fonksiyonlar:**
- `mintAchievement(address student, string memory category, string memory description)`
- `getStudentAchievements(address student) returns (uint256[] memory)`
- `getAchievementDetails(uint256 tokenId) returns (string, string, uint256)`
"""

    def _get_pre_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "Eğitimde NFT kullanımının amacı nedir?", "type": "multiple_choice",
             "options": ["Para kazanmak", "Dijital başarı rozeti vermek", "Öğrenci takibi", "Bilmiyorum"], "correct_answer": "Dijital başarı rozeti vermek"},
            {"id": "q2", "question": "Soulbound token ne demektir?", "type": "multiple_choice",
             "options": ["Pahalı token", "Transfer edilemeyen token", "Yakılabilen token", "Bilmiyorum"], "correct_answer": "Transfer edilemeyen token"},
            {"id": "q3", "question": "Eğitim NFT'lerinde metadata neden önemlidir?", "type": "multiple_choice",
             "options": ["Sertifikanın içeriğini ve özelliklerini tanımlar", "Gas maliyetini azaltır", "Transfer hızını artırır", "Bilmiyorum"],
             "correct_answer": "Sertifikanın içeriğini ve özelliklerini tanımlar"}
        ]

    def _get_pre_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "What is the purpose of using NFTs in education?", "type": "multiple_choice",
             "options": ["To earn money", "To give digital achievement badges", "Student tracking", "I don't know"], "correct_answer": "To give digital achievement badges"},
            {"id": "q2", "question": "What does a soulbound token mean?", "type": "multiple_choice",
             "options": ["Expensive token", "Non-transferable token", "Burnable token", "I don't know"], "correct_answer": "Non-transferable token"},
            {"id": "q3", "question": "Why is metadata important in education NFTs?", "type": "multiple_choice",
             "options": ["It defines the certificate's content and attributes", "Reduces gas cost", "Increases transfer speed", "I don't know"],
             "correct_answer": "It defines the certificate's content and attributes"}
        ]

    def get_pre_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_pre_test_questions_en() if self._get_lang() == "en" else self._get_pre_test_questions_tr()

    def _get_post_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q4", "question": "Başarı NFT'lerinin transfer edilememesi neden önemlidir?", "type": "multiple_choice",
             "options": ["Kişiye özel başarı olması için", "Gas tasarrufu için", "Daha hızlı işlem için", "Bilmiyorum"], "correct_answer": "Kişiye özel başarı olması için"},
            {"id": "q5", "question": "Eğitim kurumları için on-chain vs off-chain metadata farkı?", "type": "multiple_choice",
             "options": ["On-chain kalıcı, off-chain daha ucuz ve esnek", "On-chain daha ucuz", "Aralarında teknik fark yok", "Bilmiyorum"],
             "correct_answer": "On-chain kalıcı, off-chain daha ucuz ve esnek"}
        ]

    def _get_post_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q4", "question": "Why is it important that achievement NFTs cannot be transferred?", "type": "multiple_choice",
             "options": ["So achievement is personal", "Gas savings", "Faster processing", "I don't know"], "correct_answer": "So achievement is personal"},
            {"id": "q5", "question": "On-chain vs off-chain metadata for educational institutions?", "type": "multiple_choice",
             "options": ["On-chain is permanent, off-chain is cheaper and flexible", "On-chain is cheaper", "There is no technical difference", "I don't know"],
             "correct_answer": "On-chain is permanent, off-chain is cheaper and flexible"}
        ]

    def get_post_test_questions(self) -> List[Dict[str, Any]]:
        pre = self.get_pre_test_questions()
        post_only = self._get_post_test_questions_en() if self._get_lang() == "en" else self._get_post_test_questions_tr()
        return pre + post_only

    def get_evaluation_criteria(self) -> Dict[str, Dict[str, int]]:
        return {
            "functionality": {
                "compiles": 10,
                "mint_function": 10,
                "soulbound_logic": 10,
                "total": 30
            },
            "security": {
                "access_control": 10,
                "no_transfer": 10,
                "validation": 5,
                "total": 25
            },
            "gas_optimization": {
                "efficient_storage": 10,
                "batch_operations": 8,
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
