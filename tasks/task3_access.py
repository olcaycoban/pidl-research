"""
Görev 3: Eğitim Materyali Erişim Kontrolü
Zorluk: Orta
"""

from .base_task import BaseTask
from typing import List, Dict, Any


class Task3Access(BaseTask):
    def __init__(self):
        super().__init__()
        self.task_number = 3
        self.difficulty = "Orta"
        self.title = "Eğitim Materyali Erişim Kontrolü"
        self.description = """Ücretli eğitim içerikleri için akıllı kontrat:

**Gereksinimler:**
- Öğretmen içerik ekleyebilsin (IPFS hash)
- Her içeriğin farklı ücreti olsun
- Öğrenci ödeme yapınca erişim kazansın
- Erişim süresi belirlenebilsin (30 gün, 90 gün, süresiz)
- Öğretmene otomatik ödeme yapılsın
- Komisyon sistemi (%5 platform ücreti)

**Beklenen Fonksiyonlar:**
- `addContent(string memory ipfsHash, uint256 price, uint256 accessDuration)`
- `purchaseAccess(uint256 contentId) payable`
- `hasAccess(address student, uint256 contentId) returns (bool)`
- `withdrawEarnings()`
"""

    def _get_pre_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "IPFS ile blockchain ilişkisi nedir?", "type": "multiple_choice",
             "options": ["Aynı teknoloji", "IPFS içerik saklar, blockchain referans tutar", "Blockchain içerik saklar", "Bilmiyorum"], "correct_answer": "IPFS içerik saklar, blockchain referans tutar"},
            {"id": "q2", "question": "Eğitim içeriği erişiminde zaman kontrolü neden önemlidir?", "type": "multiple_choice",
             "options": ["Abonelik modeli için", "Gas tasarrufu için", "Hız için", "Bilmiyorum"], "correct_answer": "Abonelik modeli için"},
            {"id": "q3", "question": "Payable fonksiyonlar nasıl çalışır?", "type": "multiple_choice",
             "options": ["Fonksiyon çağrısıyla birlikte ETH transferine izin verir", "Ücretsiz işlem yapar", "Sadece admin çağırabilir", "Bilmiyorum"],
             "correct_answer": "Fonksiyon çağrısıyla birlikte ETH transferine izin verir"}
        ]

    def _get_pre_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "What is the relationship between IPFS and blockchain?", "type": "multiple_choice",
             "options": ["Same technology", "IPFS stores content, blockchain holds reference", "Blockchain stores content", "I don't know"], "correct_answer": "IPFS stores content, blockchain holds reference"},
            {"id": "q2", "question": "Why is time control important for educational content access?", "type": "multiple_choice",
             "options": ["For subscription model", "Gas savings", "Speed", "I don't know"], "correct_answer": "For subscription model"},
            {"id": "q3", "question": "How do payable functions work?", "type": "multiple_choice",
             "options": ["Allow ETH transfers alongside the function call", "Execute transactions for free", "Only admin can call them", "I don't know"],
             "correct_answer": "Allow ETH transfers alongside the function call"}
        ]

    def get_pre_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_pre_test_questions_en() if self._get_lang() == "en" else self._get_pre_test_questions_tr()

    def _get_post_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q4", "question": "block.timestamp kullanarak süre kontrolü güvenli mi?", "type": "multiple_choice",
             "options": ["Tamamen güvenli", "Manipüle edilebilir (±15 saniye)", "Hiç güvenli değil", "Bilmiyorum"], "correct_answer": "Manipüle edilebilir (±15 saniye)"},
            {"id": "q5", "question": "Eğitimde mikro ödemeler için blockchain avantajları?", "type": "multiple_choice",
             "options": ["İçeriğe esnek ve uygun fiyatlı erişim sağlar", "Tamamen ücretsiz işlem yapar", "İçerikleri otomatik üretir", "Bilmiyorum"],
             "correct_answer": "İçeriğe esnek ve uygun fiyatlı erişim sağlar"}
        ]

    def _get_post_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q4", "question": "Is duration control using block.timestamp secure?", "type": "multiple_choice",
             "options": ["Fully secure", "Can be manipulated (±15 seconds)", "Not secure at all", "I don't know"], "correct_answer": "Can be manipulated (±15 seconds)"},
            {"id": "q5", "question": "Blockchain advantages for micro-payments in education?", "type": "multiple_choice",
             "options": ["Enables flexible and affordable content access", "Makes all transactions free", "Auto-generates content", "I don't know"],
             "correct_answer": "Enables flexible and affordable content access"}
        ]

    def get_post_test_questions(self) -> List[Dict[str, Any]]:
        pre = self.get_pre_test_questions()
        post_only = self._get_post_test_questions_en() if self._get_lang() == "en" else self._get_post_test_questions_tr()
        return pre + post_only

    def get_evaluation_criteria(self) -> Dict[str, Dict[str, int]]:
        return {
            "functionality": {
                "compiles": 10,
                "payment_logic": 10,
                "access_control": 10,
                "total": 30
            },
            "security": {
                "reentrancy_guard": 10,
                "overflow_protection": 8,
                "access_validation": 7,
                "total": 25
            },
            "gas_optimization": {
                "storage_efficiency": 10,
                "commission_calc": 8,
                "event_usage": 7,
                "total": 25
            },
            "code_quality": {
                "naming": 7,
                "comments": 6,
                "structure": 7,
                "total": 20
            }
        }
