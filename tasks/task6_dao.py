"""
Görev 6: Merkezi Olmayan Üniversite DAO'su
Zorluk: Yüksek
"""

from .base_task import BaseTask
from typing import List, Dict, Any


class Task6DAO(BaseTask):
    def __init__(self):
        super().__init__()
        self.task_number = 6
        self.difficulty = "Yüksek"
        self.title = "Merkezi Olmayan Üniversite DAO'su"
        self.description = """Blockchain tabanlı üniversite yönetim DAO'su:

**Gereksinimler:**
- Öğrenci, öğretmen ve yönetici rolleri
- Müfredat değişikliği önerileri
- Bütçe tahsisi oylamaları
- Öğretmen işe alım oylaması
- Token bazlı oy ağırlığı (öğrenci %40, öğretmen %40, yönetim %20)
- 72 saat oylama süresi
- %30 quorum gerekliliği
- Timelock execution (48 saat)

**Beklenen Fonksiyonlar:**
- `createProposal(string memory description, ProposalType propType)`
- `vote(uint256 proposalId, bool support)`
- `executeProposal(uint256 proposalId)`
- `delegateVote(address delegate)`
- `getProposalState(uint256 proposalId) returns (ProposalState)`
"""

    def _get_pre_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "Eğitim kurumlarında DAO modelinin faydaları nelerdir?", "type": "multiple_choice",
             "options": ["Şeffaf yönetim", "Demokratik karar alma", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q2", "question": "Role-based voting eğitimde neden önemlidir?", "type": "multiple_choice",
             "options": ["Farklı paydaş perspektiflerini dengelemek için", "Gas tasarrufu için", "Hız için", "Bilmiyorum"], "correct_answer": "Farklı paydaş perspektiflerini dengelemek için"},
            {"id": "q3", "question": "Eğitim DAO'sunda timelock neden kritiktir?", "type": "multiple_choice",
             "options": ["Ani ve zararlı değişikliklere karşı itiraz süresi tanır", "İşlem maliyetini düşürür", "Oy sayımını hızlandırır", "Bilmiyorum"],
             "correct_answer": "Ani ve zararlı değişikliklere karşı itiraz süresi tanır"},
            {"id": "q4", "question": "Quorum gerekliliği neden önemlidir?", "type": "multiple_choice",
             "options": ["Az katılımla alınan kararları önler", "Gas maliyetini azaltır", "Oy sayımını hızlandırır", "Bilmiyorum"],
             "correct_answer": "Az katılımla alınan kararları önler"},
            {"id": "q5", "question": "Governance token ne işlevi görür?", "type": "multiple_choice",
             "options": ["Oy hakkı ve karar alma yetkisi verir", "Para birimi olarak kullanılır", "NFT oluşturur", "Bilmiyorum"],
             "correct_answer": "Oy hakkı ve karar alma yetkisi verir"},
        ]

    def _get_pre_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "What are the benefits of the DAO model in educational institutions?", "type": "multiple_choice",
             "options": ["Transparent governance", "Democratic decision-making", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q2", "question": "Why is role-based voting important in education?", "type": "multiple_choice",
             "options": ["To balance different stakeholder perspectives", "Gas savings", "Speed", "I don't know"], "correct_answer": "To balance different stakeholder perspectives"},
            {"id": "q3", "question": "Why is timelock critical in an education DAO?", "type": "multiple_choice",
             "options": ["It gives a challenge period against sudden harmful changes", "Reduces transaction costs", "Speeds up vote counting", "I don't know"],
             "correct_answer": "It gives a challenge period against sudden harmful changes"},
            {"id": "q4", "question": "Why is a quorum requirement important?", "type": "multiple_choice",
             "options": ["Prevents decisions made with low participation", "Reduces gas cost", "Speeds up vote counting", "I don't know"],
             "correct_answer": "Prevents decisions made with low participation"},
            {"id": "q5", "question": "What function does a governance token serve?", "type": "multiple_choice",
             "options": ["Grants voting rights and decision-making power", "Used as currency", "Creates NFTs", "I don't know"],
             "correct_answer": "Grants voting rights and decision-making power"},
        ]

    def get_pre_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_pre_test_questions_en() if self._get_lang() == "en" else self._get_pre_test_questions_tr()

    def _get_post_test_questions_tr(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "Eğitim kurumlarında DAO modelinin faydaları nelerdir?", "type": "multiple_choice",
             "options": ["Şeffaf yönetim", "Demokratik karar alma", "Her ikisi de", "Bilmiyorum"], "correct_answer": "Her ikisi de"},
            {"id": "q2", "question": "Role-based voting eğitimde neden önemlidir?", "type": "multiple_choice",
             "options": ["Farklı paydaş perspektiflerini dengelemek için", "Gas tasarrufu için", "Hız için", "Bilmiyorum"], "correct_answer": "Farklı paydaş perspektiflerini dengelemek için"},
            {"id": "q3", "question": "Eğitim DAO'sunda timelock neden kritiktir?", "type": "multiple_choice",
             "options": ["Ani ve zararlı değişikliklere karşı itiraz süresi tanır", "İşlem maliyetini düşürür", "Oy sayımını hızlandırır", "Bilmiyorum"],
             "correct_answer": "Ani ve zararlı değişikliklere karşı itiraz süresi tanır"},
            {"id": "q4", "question": "Delegation (temsili oy) eğitim DAO'sunda nasıl işler?", "type": "multiple_choice",
             "options": ["Öğrenci temsilcileri sistemi", "Uzman delegeler", "Her ikisi de", "Bilmiyorum"],
             "correct_answer": "Her ikisi de"},
            {"id": "q5", "question": "Eğitim kurumlarında on-chain governance'ın off-chain'e göre avantajı nedir?", "type": "multiple_choice",
             "options": ["Şeffaf ve manipülasyona kapalı karar alma sağlar", "Kararlar daha hızlı alınır", "Her zaman daha ucuzdur", "Bilmiyorum"],
             "correct_answer": "Şeffaf ve manipülasyona kapalı karar alma sağlar"},
        ]

    def _get_post_test_questions_en(self) -> List[Dict[str, Any]]:
        return [
            {"id": "q1", "question": "What are the benefits of the DAO model in educational institutions?", "type": "multiple_choice",
             "options": ["Transparent governance", "Democratic decision-making", "Both", "I don't know"], "correct_answer": "Both"},
            {"id": "q2", "question": "Why is role-based voting important in education?", "type": "multiple_choice",
             "options": ["To balance different stakeholder perspectives", "Gas savings", "Speed", "I don't know"], "correct_answer": "To balance different stakeholder perspectives"},
            {"id": "q3", "question": "Why is timelock critical in an education DAO?", "type": "multiple_choice",
             "options": ["It gives a challenge period against sudden harmful changes", "Reduces transaction costs", "Speeds up vote counting", "I don't know"],
             "correct_answer": "It gives a challenge period against sudden harmful changes"},
            {"id": "q4", "question": "How does vote delegation work in an education DAO?", "type": "multiple_choice",
             "options": ["Student representative system", "Expert delegates", "Both", "I don't know"],
             "correct_answer": "Both"},
            {"id": "q5", "question": "Advantage of on-chain governance over off-chain in educational institutions?", "type": "multiple_choice",
             "options": ["Provides transparent and tamper-proof decision-making", "Decisions are made faster", "Always cheaper", "I don't know"],
             "correct_answer": "Provides transparent and tamper-proof decision-making"},
        ]

    def get_post_test_questions(self) -> List[Dict[str, Any]]:
        return self._get_post_test_questions_en() if self._get_lang() == "en" else self._get_post_test_questions_tr()

    def get_evaluation_criteria(self) -> Dict[str, Dict[str, int]]:
        return {
            "functionality": {
                "compiles": 10,
                "proposal_creation": 10,
                "voting_logic": 10,
                "total": 30
            },
            "security": {
                "access_control": 10,
                "timelock": 8,
                "quorum_check": 7,
                "total": 25
            },
            "gas_optimization": {
                "storage": 10,
                "vote_counting": 8,
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
