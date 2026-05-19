"""
Yetkinlik Değerlendirme ve Tavsiye Sistemi
Dreyfus Model of Skill Acquisition bazlı

Matematiksel recommendation engine ile entegre
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from datetime import datetime
import json

try:
    from recommendation_engine import RecommendationEngine, UserVector
    RECOMMENDATION_ENGINE_AVAILABLE = True
except ImportError:
    RECOMMENDATION_ENGINE_AVAILABLE = False


@dataclass
class CompetencyProfile:
    """Kullanıcı yetkinlik profili - DUAL DOMAIN"""
    user_id: str
    # Dual domain scores
    technical_score: float  # Blockchain/teknik (0-100)
    educational_score: float  # Eğitim/pedagoji (0-100)
    technical_level: str  # Teknik yetkinlik seviyesi
    educational_level: str  # Eğitimsel yetkinlik seviyesi
    # Genel
    overall_score: float  # Ortalama skor
    dominant_domain: str  # "technical" veya "educational" (hangisi güçlü)
    weak_domain: str  # Zayıf olan domain
    assessment_date: str
    responses: Dict
    recommended_personas_similarity: List[str]  # Benzerlik bazlı
    recommended_personas_complementary: List[str]  # Tamamlayıcı bazlı


class CompetencyAssessment:
    """Yetkinlik değerlendirme sistemi"""
    
    # Dreyfus Modeli Seviyeleri (Likert 1-5 bazlı)
    LEVELS = {
        "novice": {"min": 1.0, "max": 1.8, "name": "Novice (Acemi)"},
        "advanced_beginner": {"min": 1.9, "max": 2.8, "name": "Advanced Beginner (İleri Başlangıç)"},
        "competent": {"min": 2.9, "max": 3.8, "name": "Competent (Yetkin)"},
        "proficient": {"min": 3.9, "max": 4.5, "name": "Proficient (Deneyimli)"},
        "expert": {"min": 4.6, "max": 5.0, "name": "Expert (Uzman)"}
    }
    
    # BÖLÜM A: Demografik Bilgiler
    DEMOGRAPHIC_QUESTIONS = {
        "age": {
            "question": "Yaşınız",
            "type": "number",
            "min": 18,
            "max": 100
        },
        "gender": {
            "question": "Cinsiyetiniz",
            "type": "select",
            "options": ["Kadın", "Erkek", "Belirtmek istemiyorum"]
        },
        "education": {
            "question": "Eğitim Durumunuz",
            "type": "select",
            "options": ["Lise", "Ön Lisans", "Lisans", "Yüksek Lisans", "Doktora", "Diğer"]
        },
        "experience": {
            "question": "Mesleki Deneyim Süreniz",
            "type": "select",
            "options": ["0-6 ay", "6 ay - 1 yıl", "1-3 yıl", "3-5 yıl", "5-10 yıl", "10+ yıl"]
        },
        "sector": {
            "question": "Çalıştığınız Sektör",
            "type": "select",
            "options": ["Eğitim", "Teknoloji/Yazılım", "Finans", "Akademi/Araştırma", "Diğer"]
        }
    }

    # English options for demographic (when locale is "en")
    DEMOGRAPHIC_OPTIONS_EN = {
        "gender": ["Female", "Male", "Prefer not to say"],
        "education": ["High School", "Associate", "Bachelor", "Master", "Doctorate", "Other"],
        "experience": ["0-6 months", "6 months - 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
        "sector": ["Education", "Technology/Software", "Finance", "Academia/Research", "Other"]
    }
    
    # BÖLÜM B: Teknik Yetkinlik (Likert 1-5)
    # CAQ Formu - Blockchain Teknolojileri ve Genel Programlama
    TECHNICAL_QUESTIONS = [
        {
            "id": "tech_blockchain_1",
            "category": "Blockchain Teknolojileri",
            "question": "Blockchain temel kavramları (blok, hash, zincir yapısı)",
            "scale": "likert_5",
            "description": "1 = Hiç bilmiyorum, 5 = Uzman seviyesinde biliyorum"
        },
        {
            "id": "tech_blockchain_2",
            "category": "Blockchain Teknolojileri",
            "question": "Smart contract geliştirme (Solidity, Vyper)",
            "scale": "likert_5"
        },
        {
            "id": "tech_blockchain_3",
            "category": "Blockchain Teknolojileri",
            "question": "Konsensus mekanizmaları (PoW, PoS, DPoS)",
            "scale": "likert_5"
        },
        {
            "id": "tech_blockchain_4",
            "category": "Blockchain Teknolojileri",
            "question": "Kripto-ekonomi ve tokenomics",
            "scale": "likert_5"
        },
        {
            "id": "tech_programming_1",
            "category": "Genel Programlama",
            "question": "Python/JavaScript gibi dillerde programlama",
            "scale": "likert_5"
        },
        {
            "id": "tech_programming_2",
            "category": "Genel Programlama",
            "question": "Veri yapıları ve algoritmalar",
            "scale": "likert_5"
        },
        {
            "id": "tech_programming_3",
            "category": "Genel Programlama",
            "question": "Yazılım mimarisi ve tasarım kalıpları",
            "scale": "likert_5"
        },
        {
            "id": "tech_programming_4",
            "category": "Genel Programlama",
            "question": "Test odaklı geliştirme (TDD) ve debugging",
            "scale": "likert_5"
        }
    ]

    # Technical questions – English (same ids, for locale "en")
    TECHNICAL_QUESTIONS_EN = [
        {"id": "tech_blockchain_1", "category": "Blockchain Technologies", "question": "Blockchain basic concepts (block, hash, chain structure)", "scale": "likert_5"},
        {"id": "tech_blockchain_2", "category": "Blockchain Technologies", "question": "Smart contract development (Solidity, Vyper)", "scale": "likert_5"},
        {"id": "tech_blockchain_3", "category": "Blockchain Technologies", "question": "Consensus mechanisms (PoW, PoS, DPoS)", "scale": "likert_5"},
        {"id": "tech_blockchain_4", "category": "Blockchain Technologies", "question": "Crypto-economics and tokenomics", "scale": "likert_5"},
        {"id": "tech_programming_1", "category": "General Programming", "question": "Programming in Python/JavaScript or similar", "scale": "likert_5"},
        {"id": "tech_programming_2", "category": "General Programming", "question": "Data structures and algorithms", "scale": "likert_5"},
        {"id": "tech_programming_3", "category": "General Programming", "question": "Software architecture and design patterns", "scale": "likert_5"},
        {"id": "tech_programming_4", "category": "General Programming", "question": "Test-driven development (TDD) and debugging", "scale": "likert_5"}
    ]
    
    # BÖLÜM C: Pedagojik Yetkinlik (Likert 1-5)
    # CAQ Formu - Eğitim Teorileri ve İletişim
    EDUCATIONAL_QUESTIONS = [
        {
            "id": "edu_theory_1",
            "category": "Eğitim Teorileri ve Uygulamaları",
            "question": "Öğrenme teorileri (davranışçı, bilişsel, yapılandırmacı)",
            "scale": "likert_5",
            "description": "1 = Hiç bilmiyorum, 5 = Uzman seviyesinde biliyorum"
        },
        {
            "id": "edu_theory_2",
            "category": "Eğitim Teorileri ve Uygulamaları",
            "question": "Öğretim tasarımı modelleri (ADDIE, SAM, Backward Design)",
            "scale": "likert_5"
        },
        {
            "id": "edu_theory_3",
            "category": "Eğitim Teorileri ve Uygulamaları",
            "question": "Değerlendirme yöntemleri (formatif, sümatif, otantik)",
            "scale": "likert_5"
        },
        {
            "id": "edu_theory_4",
            "category": "Eğitim Teorileri ve Uygulamaları",
            "question": "Dijital okuryazarlık ve e-öğrenme pedagojisi",
            "scale": "likert_5"
        },
        {
            "id": "edu_communication_1",
            "category": "İletişim ve Sunum Becerileri",
            "question": "Etkili sunum ve anlatım teknikleri",
            "scale": "likert_5"
        },
        {
            "id": "edu_communication_2",
            "category": "İletişim ve Sunum Becerileri",
            "question": "Grup yönetimi ve kolaylaştırıcılık (facilitation)",
            "scale": "likert_5"
        },
        {
            "id": "edu_communication_3",
            "category": "İletişim ve Sunum Becerileri",
            "question": "Geri bildirim verme ve alma becerileri",
            "scale": "likert_5"
        },
        {
            "id": "edu_communication_4",
            "category": "İletişim ve Sunum Becerileri",
            "question": "Çevrimiçi etkileşim ve topluluk oluşturma",
            "scale": "likert_5"
        }
    ]

    # Educational questions – English (same ids, for locale "en")
    EDUCATIONAL_QUESTIONS_EN = [
        {"id": "edu_theory_1", "category": "Educational Theory and Practice", "question": "Learning theories (behaviorist, cognitive, constructivist)", "scale": "likert_5"},
        {"id": "edu_theory_2", "category": "Educational Theory and Practice", "question": "Instructional design models (ADDIE, SAM, Backward Design)", "scale": "likert_5"},
        {"id": "edu_theory_3", "category": "Educational Theory and Practice", "question": "Assessment methods (formative, summative, authentic)", "scale": "likert_5"},
        {"id": "edu_theory_4", "category": "Educational Theory and Practice", "question": "Digital literacy and e-learning pedagogy", "scale": "likert_5"},
        {"id": "edu_communication_1", "category": "Communication and Presentation", "question": "Effective presentation and explanation techniques", "scale": "likert_5"},
        {"id": "edu_communication_2", "category": "Communication and Presentation", "question": "Group facilitation and moderation", "scale": "likert_5"},
        {"id": "edu_communication_3", "category": "Communication and Presentation", "question": "Giving and receiving feedback", "scale": "likert_5"},
        {"id": "edu_communication_4", "category": "Communication and Presentation", "question": "Online interaction and community building", "scale": "likert_5"}
    ]
    
    # BÖLÜM D: AI Araçları Kullanım Deneyimi
    AI_TOOLS_QUESTIONS = {
        "tools_used": {
            "question": "Daha önce hangi AI araçlarını kullandınız?",
            "type": "multiselect",
            "options": ["ChatGPT", "Claude", "GitHub Copilot", "Google Bard/Gemini", 
                       "Midjourney/DALL-E", "Hiçbiri", "Diğer"]
        },
        "usage_frequency": {
            "question": "AI araçlarını ne sıklıkla kullanıyorsunuz?",
            "type": "select",
            "options": ["Her gün", "Haftada birkaç kez", "Ayda birkaç kez", 
                       "Nadiren", "Hiç kullanmıyorum"]
        },
        "usage_purposes": {
            "question": "AI araçlarını hangi amaçlarla kullanıyorsunuz?",
            "type": "multiselect",
            "options": ["Kod yazma/hata ayıklama", "Araştırma ve bilgi toplama",
                       "İçerik üretimi", "Öğrenme ve eğitim", "Problem çözme", "Diğer"]
        }
    }

    AI_TOOLS_OPTIONS_EN = {
        "tools_used": ["ChatGPT", "Claude", "GitHub Copilot", "Google Bard/Gemini", "Midjourney/DALL-E", "None", "Other"],
        "usage_frequency": ["Daily", "A few times a week", "A few times a month", "Rarely", "I don't use"],
        "usage_purposes": ["Coding/debugging", "Research", "Content creation", "Learning and education", "Problem solving", "Other"]
    }
    
    # BÖLÜM E: Öğrenme Tercihleri (Likert 1-5)
    LEARNING_PREFERENCES = [
        {
            "id": "learn_pref_1",
            "question": "Yeni bir konuyu öğrenirken önce teorik bilgiyi anlamak isterim",
            "scale": "likert_5",
            "description": "1 = Kesinlikle katılmıyorum, 5 = Kesinlikle katılıyorum"
        },
        {
            "id": "learn_pref_2",
            "question": "Yaparak ve deneyerek öğrenmeyi tercih ederim",
            "scale": "likert_5"
        },
        {
            "id": "learn_pref_3",
            "question": "Kendi hızımda ilerleyebilmek benim için önemlidir",
            "scale": "likert_5"
        },
        {
            "id": "learn_pref_4",
            "question": "Öğrenirken anlık geri bildirim almak benim için önemlidir",
            "scale": "likert_5"
        },
        {
            "id": "learn_pref_5",
            "question": "Grup çalışması ve işbirliği öğrenmemi kolaylaştırır",
            "scale": "likert_5"
        },
        {
            "id": "learn_pref_6",
            "question": "Görsel materyaller (diyagram, video) benim için faydalıdır",
            "scale": "likert_5"
        }
    ]

    LEARNING_PREFERENCES_EN = [
        {"id": "learn_pref_1", "question": "When learning something new I like to understand the theory first", "scale": "likert_5"},
        {"id": "learn_pref_2", "question": "I prefer learning by doing and experimenting", "scale": "likert_5"},
        {"id": "learn_pref_3", "question": "Being able to progress at my own pace is important to me", "scale": "likert_5"},
        {"id": "learn_pref_4", "question": "Getting immediate feedback while learning is important to me", "scale": "likert_5"},
        {"id": "learn_pref_5", "question": "Group work and collaboration make learning easier for me", "scale": "likert_5"},
        {"id": "learn_pref_6", "question": "Visual materials (diagrams, video) are helpful for me", "scale": "likert_5"}
    ]
    
    # BÖLÜM F: Kendini Değerlendirme
    SELF_ASSESSMENT = {
        "dreyfus_level": {
            "question": "Genel olarak kendinizi hangi seviyede görüyorsunuz?",
            "type": "select",
            "options": [
                ("novice", "Acemi (Novice) - Yeni başlıyor, temel bilgiler öğreniyor"),
                ("advanced_beginner", "İleri Başlangıç (Advanced Beginner) - Temel bilgileri biliyor, deneyim kazanıyor"),
                ("competent", "Yetkin (Competent) - Bağımsız çalışabiliyor, standart görevleri yapabiliyor"),
                ("proficient", "Deneyimli (Proficient) - İleri seviye, karmaşık problemleri çözebiliyor"),
                ("expert", "Uzman (Expert) - Alanında otorite, başkalarına öğretebiliyor")
            ]
        },
        "primary_need": {
            "question": "Blockchain eğitimi için en önemli ihtiyacınız nedir?",
            "type": "select",
            "options": ["Teknik bilgi ve beceriler", 
                       "Pedagojik yaklaşım ve öğretim teknikleri",
                       "Her ikisinin dengeli kombinasyonu",
                       "Pratik uygulama fırsatları", 
                       "Diğer"]
        },
        "ai_learning_feature": {
            "question": "AI destekli öğrenme ortamında size en çok yardımcı olacak özellik nedir?",
            "type": "select",
            "options": ["Kişiselleştirilmiş öğrenme yolu",
                       "Anlık geri bildirim",
                       "Adım adım rehberlik",
                       "Zengin örnekler",
                       "Esnek öğrenme hızı",
                       "Diğer"]
        }
    }

    SELF_ASSESSMENT_EN = {
        "dreyfus_level": {
            "question": "Overall, how would you rate your level?",
            "type": "select",
            "options": [
                ("novice", "Novice – Just starting, learning basics"),
                ("advanced_beginner", "Advanced Beginner – Know basics, gaining experience"),
                ("competent", "Competent – Can work independently on standard tasks"),
                ("proficient", "Proficient – Advanced, can solve complex problems"),
                ("expert", "Expert – Authority in the field, can teach others")
            ]
        },
        "primary_need": {
            "question": "What is your main need for blockchain education?",
            "type": "select",
            "options": ["Technical knowledge and skills", "Pedagogical approach and teaching methods",
                        "Balanced combination of both", "Practical application opportunities", "Other"]
        },
        "ai_learning_feature": {
            "question": "What would help you most in an AI-supported learning environment?",
            "type": "select",
            "options": ["Personalized learning path", "Immediate feedback", "Step-by-step guidance",
                       "Rich examples", "Flexible learning pace", "Other"]
        }
    }

    
    def __init__(self):
        """Assessment sistemini başlat"""
        self.rec_engine = RecommendationEngine() if RECOMMENDATION_ENGINE_AVAILABLE else None

    @staticmethod
    def get_demographic_options(field: str, lang: str = "tr") -> list:
        """Return demographic options for the given field in the requested language."""
        if lang == "en" and field in CompetencyAssessment.DEMOGRAPHIC_OPTIONS_EN:
            return CompetencyAssessment.DEMOGRAPHIC_OPTIONS_EN[field]
        return CompetencyAssessment.DEMOGRAPHIC_QUESTIONS[field]["options"]

    @staticmethod
    def get_technical_questions(lang: str = "tr") -> list:
        """Return technical competency questions in the requested language."""
        return CompetencyAssessment.TECHNICAL_QUESTIONS_EN if lang == "en" else CompetencyAssessment.TECHNICAL_QUESTIONS

    @staticmethod
    def get_educational_questions(lang: str = "tr") -> list:
        """Return educational competency questions in the requested language."""
        return CompetencyAssessment.EDUCATIONAL_QUESTIONS_EN if lang == "en" else CompetencyAssessment.EDUCATIONAL_QUESTIONS

    @staticmethod
    def get_ai_tools_options(field: str, lang: str = "tr") -> list:
        """Return AI tools options for the given field."""
        if lang == "en" and field in CompetencyAssessment.AI_TOOLS_OPTIONS_EN:
            return CompetencyAssessment.AI_TOOLS_OPTIONS_EN[field]
        return CompetencyAssessment.AI_TOOLS_QUESTIONS[field]["options"]

    @staticmethod
    def get_learning_preferences(lang: str = "tr") -> list:
        """Return learning preference questions in the requested language."""
        return CompetencyAssessment.LEARNING_PREFERENCES_EN if lang == "en" else CompetencyAssessment.LEARNING_PREFERENCES

    @staticmethod
    def get_self_assessment(lang: str = "tr") -> dict:
        """Return self assessment questions and options in the requested language."""
        return CompetencyAssessment.SELF_ASSESSMENT_EN if lang == "en" else CompetencyAssessment.SELF_ASSESSMENT
    
    def _recommend_with_math_engine(self, competency_profile: Dict) -> List[Dict]:
        """
        Matematiksel recommendation engine ile tavsiye üret
        
        Args:
            competency_profile: Kullanıcı profil dictionary
            
        Returns:
            Matematiksel olarak optimize edilmiş tavsiyeler
        """
        if not self.rec_engine:
            return []
        
        # User vector oluştur
        user_vector = self.rec_engine.create_user_vector(competency_profile)
        
        # Task complexity tahmin et (orta seviye varsayalım)
        task_complexity = 0.5
        
        # Persona'ları rank'le
        rankings = self.rec_engine.rank_personas(
            user_vector, 
            task_complexity=task_complexity,
            top_k=5
        )
        
        # Formata dönüştür
        recommendations = []
        for idx, ranking in enumerate(rankings, 1):
            persona_id = ranking["persona_id"]
            score = ranking["score"]
            components = ranking["components"]
            ci = ranking["confidence_interval"]
            
            # Açıklama üret
            explanation = self.rec_engine.explain_recommendation(user_vector, persona_id)
            
            # Matematiksel detaylar ekle
            math_details = f"""
**Matematiksel Skor Detayları:**
- Toplam Skor: {score:.3f}
- Benzerlik (S): {components['similarity']:.3f}
- Yetkinlik Uyumu (C): {components['competency_match']:.3f}
- Performans Tahmini (P): {components['performance_prediction']:.3f}
- Öğrenme Yörüngesi (L): {components['learning_trajectory']:.3f}
- 95% CI: [{ci['lower']:.3f}, {ci['upper']:.3f}]

Formül: R = {self.rec_engine.alpha}·S + {self.rec_engine.beta}·C + {self.rec_engine.gamma}·P + {self.rec_engine.delta}·L
"""
            
            recommendations.append({
                "persona_id": persona_id,
                "reason": explanation,
                "priority": idx,
                "mathematical_score": score,
                "components": components,
                "confidence_interval": ci,
                "math_details": math_details
            })
        
        return recommendations
    
    def calculate_score(self, responses: Dict[str, float], domain: str) -> float:
        """
        Toplam skoru hesapla (Likert 1-5 bazlı)
        
        Args:
            responses: Soru ID ve Likert skoru (1-5) dictionary'si
            domain: "technical" veya "educational"
            
        Returns:
            1.0-5.0 arası ortalama Likert skoru
        """
        if not responses:
            return 0.0
        
        # Domain'e göre ilgili soruları filtrele
        if domain == "technical":
            relevant_scores = [v for k, v in responses.items() 
                             if k.startswith("tech_")]
        elif domain == "educational":
            relevant_scores = [v for k, v in responses.items() 
                             if k.startswith("edu_")]
        else:
            return 0.0
        
        if not relevant_scores:
            return 0.0
        
        # Likert ortalaması (1-5 arası)
        avg_likert = sum(relevant_scores) / len(relevant_scores)
        
        return round(avg_likert, 2)
    
    @staticmethod
    def _likert_to_100(likert: float) -> float:
        """Likert 1-5 skorunu 0-100 ölçeğine çevirir. 1→0, 5→100."""
        if likert is None or likert < 1:
            return 0.0
        if likert > 5:
            return 100.0
        return round((likert - 1) / 4 * 100, 1)
    
    def determine_level(self, score: float) -> str:
        """
        Likert skorundan yetkinlik seviyesini belirle
        
        Args:
            score: 1.0-5.0 arası Likert skoru
            
        Returns:
            Seviye anahtarı (novice, advanced_beginner, competent, proficient, expert)
        """
        for level, ranges in self.LEVELS.items():
            if ranges["min"] <= score <= ranges["max"]:
                return level
        return "novice"
    
    def recommend_personas(self, level: str, domain: str, goal: str = "learning", 
                          use_mathematical_engine: bool = True,
                          competency_profile: Dict = None) -> List[Dict]:
        """
        Yetkinlik seviyesine göre persona öner
        
        İki mod:
        1. Matematiksel Engine (Araştırma için önerilen)
        2. Rule-based Basit (Fallback)
        
        Args:
            level: Yetkinlik seviyesi
            domain: Domain türü
            goal: "learning" (öğrenme) veya "production" (üretim)
            use_mathematical_engine: Matematiksel model kullan mı?
            competency_profile: Tam profil (engine için)
            
        Returns:
            Önerilen persona'lar ve açıklamaları
        """
        # Matematiksel engine kullan (eğer mevcut ve istenmişse)
        if use_mathematical_engine and RECOMMENDATION_ENGINE_AVAILABLE and competency_profile:
            return self._recommend_with_math_engine(competency_profile)
        
        # Basit rule-based tavsiye (fallback)
        recommendations = []
        
        # Domain seçimi
        category = "education" if domain == "educational" else "technology"
        
        # Seviye bazlı tavsiyeler
        if level == "novice":
            # Acemiler için öğretici persona'lar
            recommendations = [
                {
                    "persona_id": "edu_1",
                    "reason": "Çok açıklayıcı ve bol yorumlu kod yazar - öğrenmeniz için ideal",
                    "priority": 1
                },
                {
                    "persona_id": "edu_2", 
                    "reason": "Adım adım yaklaşımı sayesinde kodu takip etmek kolay",
                    "priority": 2
                },
                {
                    "persona_id": "edu_4",
                    "reason": "Modüler yapısı ile kodun parçalarını ayrı ayrı anlayabilirsiniz",
                    "priority": 3
                }
            ]
        
        elif level == "advanced_beginner":
            # İleri başlangıç için dengeli
            recommendations = [
                {
                    "persona_id": "edu_2",
                    "reason": "Yapılandırılmış yaklaşımı seviyenize uygun",
                    "priority": 1
                },
                {
                    "persona_id": "edu_4",
                    "reason": "Takım çalışması prensipleri öğrenmenize yardımcı olur",
                    "priority": 2
                },
                {
                    "persona_id": "tech_1",
                    "reason": "Clean code prensiplerini öğrenmeye başlayabilirsiniz",
                    "priority": 3
                }
            ]
        
        elif level == "competent":
            # Yetkin seviye için profesyonel
            if goal == "learning":
                recommendations = [
                    {
                        "persona_id": "tech_1",
                        "reason": "Clean code ve SOLID prensiplerini mükemmel uygular",
                        "priority": 1
                    },
                    {
                        "persona_id": "edu_3",
                        "reason": "Problem çözme yaklaşımları görmeniz için iyi",
                        "priority": 2
                    },
                    {
                        "persona_id": "tech_4",
                        "reason": "Mimari düşünme becerisi kazanırsınız",
                        "priority": 3
                    }
                ]
            else:
                recommendations = [
                    {
                        "persona_id": "tech_1",
                        "reason": "Production-ready, maintainable kod",
                        "priority": 1
                    },
                    {
                        "persona_id": "tech_2",
                        "reason": "Performans odaklı çözümler",
                        "priority": 2
                    }
                ]
        
        elif level == "proficient":
            # Usta seviye için optimizasyon odaklı
            recommendations = [
                {
                    "persona_id": "tech_2",
                    "reason": "Performans optimizasyonu uzmanlığınızla uyumlu",
                    "priority": 1
                },
                {
                    "persona_id": "tech_3",
                    "reason": "Güvenlik konusunda derinleşmeniz için",
                    "priority": 2
                },
                {
                    "persona_id": "tech_5",
                    "reason": "Algoritma optimizasyonu seviyenize uygun",
                    "priority": 3
                }
            ]
        
        else:  # expert
            # Uzman seviye için tüm spektrum
            recommendations = [
                {
                    "persona_id": "tech_5",
                    "reason": "Algoritma uzmanlığınızla eşleşir",
                    "priority": 1
                },
                {
                    "persona_id": "tech_4",
                    "reason": "Mimari tasarım seviyenize uygun",
                    "priority": 2
                },
                {
                    "persona_id": "tech_3",
                    "reason": "Güvenlik best practices",
                    "priority": 3
                },
                {
                    "persona_id": "edu_3",
                    "reason": "Farklı perspektifler için - alternatif yaklaşımlar",
                    "priority": 4
                }
            ]
        
        return recommendations
    
    def generate_improvement_tips(self, level: str, domain: str) -> List[str]:
        """
        Seviye için iyileştirme önerileri
        
        Args:
            level: Yetkinlik seviyesi
            domain: Domain türü
            
        Returns:
            İyileştirme ipuçları listesi
        """
        tips = {
            "novice": [
                "🎯 Basit görevlerle başlayın (örn: 'İki sayının toplamı')",
                "📚 Üretilen kodları satır satır okuyun ve anlamaya çalışın",
                "💡 Yorumları dikkatlice inceleyin - öğretici bilgiler içerir",
                "🔄 Aynı görevi farklı persona'larla deneyin ve karşılaştırın",
                "📖 Dr. Ayşe Öğretmen'in kodlarından başlayın - en öğretici"
            ],
            "advanced_beginner": [
                "🎯 Orta karmaşıklıkta görevler seçin",
                "🔍 Kod organizasyonuna dikkat edin (fonksiyon yapıları)",
                "💭 Prof. Mehmet'in adım adım yaklaşımını inceleyin",
                "🛠️ Doç. Ali'nin modüler tasarımlarını öğrenin",
                "📊 Farklı persona'ların yaklaşımlarını karşılaştırın"
            ],
            "competent": [
                "🎯 Kompleks problemlere geçin",
                "⚡ Ahmet Senior Developer'dan clean code öğrenin",
                "🏗️ Deniz Architect'in mimari yaklaşımlarını inceleyin",
                "🔒 Elif Security Expert'ten güvenlik prensiplerine bakın",
                "📈 Performans metriklerini karşılaştırın"
            ],
            "proficient": [
                "🎯 Production-ready kod için tech persona'ları kullanın",
                "⚙️ Can DevOps'tan performans optimizasyonu öğrenin",
                "🤖 Burak AI Specialist'in algoritma yaklaşımlarını inceleyin",
                "🔐 Güvenlik zafiyet analizlerini detaylı inceleyin",
                "🏛️ Enterprise pattern'leri keşfedin"
            ],
            "expert": [
                "🎯 Tüm persona'ları deneyin - farklı perspektifler kazanın",
                "🔬 Persona'ların yaklaşımlarını kritik edin",
                "📊 Metrik farklılıklarının nedenlerini analiz edin",
                "🎓 Kendi prompt pattern'lerinizi geliştirin",
                "🤝 Farklı persona kombinasyonlarını test edin"
            ]
        }
        
        return tips.get(level, tips["novice"])
    
    def create_profile(self, user_id: str, responses: Dict[str, int], 
                      goal: str = "learning") -> CompetencyProfile:
        """
        Kullanıcı profili oluştur - DUAL DOMAIN
        
        Args:
            user_id: Kullanıcı ID
            responses: Anket yanıtları (tech_ ve edu_ soruları)
            goal: Amaç
            
        Returns:
            CompetencyProfile objesi (dual domain)
        """
        # Technical ve Educational skorları ayrı hesapla (Likert 1-5 ortalama)
        tech_likert = self.calculate_score(responses, "technical")
        edu_likert = self.calculate_score(responses, "educational")
        
        # Seviyeleri Likert üzerinden belirle
        tech_level = self.determine_level(tech_likert)
        edu_level = self.determine_level(edu_likert)
        
        # 0-100 ölçeğine çevir (gösterim ve DB için)
        tech_score = self._likert_to_100(tech_likert)
        edu_score = self._likert_to_100(edu_likert)
        
        # Genel skor (ortalama, 0-100)
        overall_score = (tech_score + edu_score) / 2
        
        # Dominant ve weak domain (0-100 skorlara göre; 40 = eşik)
        if tech_score >= 40 and edu_score >= 40:
            # İkisi de güçlü - hangisi daha güçlü?
            if tech_score > edu_score:
                dominant = "technical"
                weak = "educational"
                strength_level = "both_strong"
            else:
                dominant = "educational"
                weak = "technical"
                strength_level = "both_strong"
        elif tech_score < 40 and edu_score < 40:
            # İkisi de zayıf - hangisi daha az zayıf?
            if tech_score > edu_score:
                dominant = "technical"  # Daha az zayıf
                weak = "educational"  # Daha zayıf
                strength_level = "both_weak"
            else:
                dominant = "educational"  # Daha az zayıf
                weak = "technical"  # Daha zayıf
                strength_level = "both_weak"
        else:
            # Biri güçlü biri zayıf
            if tech_score >= 40:
                dominant = "technical"
                weak = "educational"
                strength_level = "mixed"
            else:
                dominant = "educational"
                weak = "technical"
                strength_level = "mixed"
        
        # Similarity ve Complementary tavsiyeleri
        # (Şimdilik basit, matematiksel engine kullanacak)
        sim_personas = []
        comp_personas = []
        
        profile = CompetencyProfile(
            user_id=user_id,
            technical_score=tech_score,
            educational_score=edu_score,
            technical_level=tech_level,
            educational_level=edu_level,
            overall_score=overall_score,
            dominant_domain=dominant,
            weak_domain=weak,
            assessment_date=datetime.now().isoformat(),
            responses=responses,
            recommended_personas_similarity=sim_personas,
            recommended_personas_complementary=comp_personas
        )
        
        return profile
    
    def save_profile(self, profile: CompetencyProfile, filepath: str = "data/user_profiles.json"):
        """
        Profili dosyaya kaydet
        
        Args:
            profile: CompetencyProfile objesi
            filepath: Kayıt dosyası yolu
        """
        import os
        
        # data klasörünü oluştur
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Mevcut profilleri oku
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            profiles = []
        
        # Yeni profili ekle
        profile_dict = {
            "user_id": profile.user_id,
            "domain": profile.domain,
            "level": profile.level,
            "score": profile.score,
            "assessment_date": profile.assessment_date,
            "responses": profile.responses,
            "recommended_personas": profile.recommended_personas
        }
        
        profiles.append(profile_dict)
        
        # Kaydet
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)


# Test için
if __name__ == "__main__":
    assessment = CompetencyAssessment()
    
    # Test responses
    test_responses = {
        "tech_1": 30,
        "tech_2": 30,
        "tech_3": 30,
        "tech_4": 30,
        "tech_5": 30
    }
    
    profile = assessment.create_profile(
        user_id="test_user",
        domain="technical",
        responses=test_responses
    )
    
    print(f"Seviye: {profile.level}")
    print(f"Skor: {profile.score}")
    print(f"Öneriler: {profile.recommended_personas}")

