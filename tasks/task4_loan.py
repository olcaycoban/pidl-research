"""
Görev 4: Öğrenci Kredisi Havuzu
Zorluk: Orta-Yüksek
"""

from .base_task import BaseTask
from typing import List, Dict, Any


class Task4Loan(BaseTask):
    def __init__(self):
        super().__init__()
        self.task_number = 4
        self.difficulty = "Orta-Yüksek"
        self.title = "Öğrenci Kredisi Havuzu"
        self.description = """Merkezi olmayan öğrenci kredisi havuzu:

**Gereksinimler:**
- Yatırımcılar fon sağlasın
- Öğrenciler kredi başvurusu yapsın
- Öğrenci bilgileri: Bölüm, dönem, not ortalaması
- Otomatik risk skorlaması
- Geri ödeme takibi
- Temerrüt durumu yönetimi
- Yatırımcılara orantılı gelir dağıtımı

**Beklenen Fonksiyonlar:**
- `deposit() payable` - Yatırımcı fon ekler
- `requestLoan(uint256 amount, string memory department, uint8 semester, uint8 gpa)`
- `approveLoan(address student)`
- `repayLoan() payable`
- `calculateRiskScore(address student) returns (uint8)`
"""

    def _get_pre_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "DeFi lending protokollerinin eğitimdeki potansiyeli nedir?", "type": "multiple_choice",
             "options": ["Öğrenciye erişim kolaylığı", "Şeffaf kredi sistemi", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q2", "question": "Collateral (teminat) olmadan kredi vermenin riskleri nelerdir?", "type": "multiple_choice",
             "options": ["Geri ödememe riski", "Sybil attack riski", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q3", "question": "Havuz bazlı kredi sisteminin temel avantajı nedir?", "type": "multiple_choice",
             "options": ["Riski çok sayıda yatırımcıya dağıtır", "Her krediyi merkezi onaylar", "Faizi sıfıra indirir", "Bilmiyorum"],
             "correct_answer": "Riski çok sayıda yatırımcıya dağıtır"},
            {"id": "q4", "question": "DeFi'de `collateral ratio` neden önemlidir?", "type": "multiple_choice",
             "options": ["Borcun teminat değerini aşmaması için", "Gas maliyetini düşürmek için", "İşlemi hızlandırmak için", "Bilmiyorum"],
             "correct_answer": "Borcun teminat değerini aşmaması için"},
            {"id": "q5", "question": "Solidity 0.8+ sürümünde sayısal taşma (overflow) neden sorun değildir?", "type": "multiple_choice",
             "options": ["Yerleşik overflow koruması mevcuttur", "Büyük sayılar desteklenmez", "Floating point kullanılır", "Bilmiyorum"],
             "correct_answer": "Yerleşik overflow koruması mevcuttur"},
        ]

    def _get_pre_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "What is the potential of DeFi lending protocols in education?", "type": "multiple_choice",
             "options": ["Easier access for students", "Transparent credit system", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q2", "question": "What are the risks of lending without collateral?", "type": "multiple_choice",
             "options": ["Default risk", "Sybil attack risk", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q3", "question": "What is the main advantage of a pool-based lending system?", "type": "multiple_choice",
             "options": ["Distributes risk across many investors", "Requires central approval for every loan", "Reduces interest to zero", "I don't know"],
             "correct_answer": "Distributes risk across many investors"},
            {"id": "q4", "question": "Why is the collateral ratio important in DeFi?", "type": "multiple_choice",
             "options": ["To ensure the debt does not exceed collateral value", "To reduce gas cost", "To speed up transactions", "I don't know"],
             "correct_answer": "To ensure the debt does not exceed collateral value"},
            {"id": "q5", "question": "Why is numeric overflow not a problem in Solidity 0.8+?", "type": "multiple_choice",
             "options": ["Built-in overflow protection is included", "Large numbers are not supported", "Floating point is used", "I don't know"],
             "correct_answer": "Built-in overflow protection is included"},
        ]

    def get_pre_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_pre_test_questions_en() if self._get_lang() == "en" else self._get_pre_test_questions_tr()

    def _get_post_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "DeFi lending protokollerinin eğitimdeki potansiyeli nedir?", "type": "multiple_choice",
             "options": ["Öğrenciye erişim kolaylığı", "Şeffaf kredi sistemi", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q2", "question": "Collateral (teminat) olmadan kredi vermenin riskleri nelerdir?", "type": "multiple_choice",
             "options": ["Geri ödememe riski", "Sybil attack riski", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q3", "question": "Havuz bazlı kredi sisteminin temel avantajı nedir?", "type": "multiple_choice",
             "options": ["Riski çok sayıda yatırımcıya dağıtır", "Her krediyi merkezi onaylar", "Faizi sıfıra indirir", "Bilmiyorum"],
             "correct_answer": "Riski çok sayıda yatırımcıya dağıtır"},
            {"id": "q4", "question": "Öğrenci kredilerinde oracle kullanımı ne sağlar?", "type": "multiple_choice",
             "options": ["Not ortalaması verisi", "Mezuniyet durumu", "Her ikisi de", "Bilmiyorum"],
             "correct_answer": "Her ikisi de"},
            {"id": "q5", "question": "Eğitimde reputation-based lending'in teminat sistemine göre avantajı nedir?", "type": "multiple_choice",
             "options": ["Teminat olmadan geçmiş performansa göre güvenilirlik değerlendirmesi yapar", "Her öğrenciye eşit kredi verir", "Faizi tamamen kaldırır", "Bilmiyorum"],
             "correct_answer": "Teminat olmadan geçmiş performansa göre güvenilirlik değerlendirmesi yapar"},
        ]

    def _get_post_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "What is the potential of DeFi lending protocols in education?", "type": "multiple_choice",
             "options": ["Easier access for students", "Transparent credit system", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q2", "question": "What are the risks of lending without collateral?", "type": "multiple_choice",
             "options": ["Default risk", "Sybil attack risk", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q3", "question": "What is the main advantage of a pool-based lending system?", "type": "multiple_choice",
             "options": ["Distributes risk across many investors", "Requires central approval for every loan", "Reduces interest to zero", "I don't know"],
             "correct_answer": "Distributes risk across many investors"},
            {"id": "q4", "question": "What does oracle use provide in student loans?", "type": "multiple_choice",
             "options": ["GPA data", "Graduation status", "Both", "I don't know"],
             "correct_answer": "Both"},
            {"id": "q5", "question": "Advantage of reputation-based lending over collateral-based in education?", "type": "multiple_choice",
             "options": ["Assesses trustworthiness based on past performance without collateral", "Gives equal credit to every student", "Eliminates interest entirely", "I don't know"],
             "correct_answer": "Assesses trustworthiness based on past performance without collateral"},
        ]

    def get_post_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_post_test_questions_en() if self._get_lang() == "en" else self._get_post_test_questions_tr()

    def get_evaluation_criteria(self) -> Dict[str, Dict[str, int]]:
        return {
            "functionality": {
                "compiles": 10,
                "deposit_withdraw": 10,
                "loan_logic": 10,
                "total": 30
            },
            "security": {
                "reentrancy_guard": 10,
                "access_control": 8,
                "risk_validation": 7,
                "total": 25
            },
            "gas_optimization": {
                "storage": 10,
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
