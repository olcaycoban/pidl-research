"""
================================================================================
RECOMMENDATION_ENGINE_ACIKLAMALI.PY
================================================================================
Bu dosya, recommendation_engine.py'nin birebir kopyasıdır.
Her kod bölümünün amacı Türkçe olarak detaylı açıklanmıştır.

ANA AMAÇ:
  Kullanıcı yetkinlik profiline göre en uygun AI persona'sını matematiksel
  formüllerle (MCDA, CLT, ZPD) önermek. R(u,p) = α·S + β·C + γ·P + δ·L
  formülüyle her persona için tek bir tavsiye skoru üretilir.

TEORİK TEMELLER:
  - Cognitive Load Theory (Sweller, 1988): Bilişsel yük (intrinsic, extraneous, germane)
  - Dreyfus Model: Yetkinlik seviyeleri (Novice → Expert)
  - MCDA: Çok kriterli karar analizi (S, C, P, L ağırlıklı toplam)
  - ZPD (Vygotsky): Yakınsal Gelişim Alanı - optimal zorluk
  - Nonaka & Takeuchi: Bilgi türleri (procedural, declarative, conditional)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

# =============================================================================
# YARDIMCI FONKSİYONLAR - Benzerlik ve mesafe hesapları
# =============================================================================
# AMAÇ: Scipy kullanmadan NumPy ile vektör benzerliği ve mesafe hesaplamak.
# cosine_similarity = iki vektörün YÖN benzerliği (profil deseni).
# euclidean_distance = iki nokta arası uzaklık (seviye benzerliği).
# Bu iki metrik, kullanıcı-persona vektörlerinin ne kadar uyumlu olduğunu sayar.

def cosine_similarity(a, b):
    """
    Cosine similarity: İki vektörün yön benzerliği.
    Sonuç -1 ile 1 arası; 1 = aynı yön, 0 = dik, -1 = zıt.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a, b):
    """
    Euclidean mesafesi: İki nokta arası "düz çizgi" uzaklığı.
    Küçük mesafe = değerler birbirine yakın.
    """
    return np.linalg.norm(a - b)


# =============================================================================
# USER VECTOR - Kullanıcı yetkinlik vektörü (10 boyut)
# =============================================================================
# AMAÇ: Kullanıcıyı tek sayı yerine 10 boyutlu vektörle temsil etmek.
# Böylece benzerlik/uyum hesaplarında "hangi yönlerde güçlü/zayıf" bilgisi
# kullanılır. Teori: Nonaka & Takeuchi bilgi türleri + bilişsel faktörler.

@dataclass
class UserVector:
    """Kullanıcı yetkinlik vektörü - Tüm değerler 0-1 arası."""
    # Temel yetkinlik boyutları
    technical_skill: float      # Teknik beceri (Dreyfus seviyesine map)
    domain_knowledge: float     # Alan bilgisi (teknik vs eğitimsel)
    ai_experience: float        # AI araçları deneyimi
    learning_goal: float        # 0 = üretim odaklı, 1 = öğrenme odaklı

    # Bilgi türleri (Nonaka & Takeuchi, 1995)
    procedural_knowledge: float   # "Nasıl" yapılır bilgisi
    declarative_knowledge: float # "Ne" bilgisi (kavramlar)
    conditional_knowledge: float  # "Ne zaman" kullanılır bilgisi

    # Bilişsel faktörler
    cognitive_capacity: float    # İşlem kapasitesi (bilişsel yük taşıma)
    pattern_recognition: float   # Örüntü tanıma yeteneği
    abstraction_level: float     # Soyutlama seviyesi (expert = yüksek)


# =============================================================================
# PERSONA VECTOR - Persona karakteristik vektörü
# =============================================================================
# AMAÇ: Her AI persona'sını (Ayşe, Mehmet, tech_expert vb.) sayısal özelliklerle
# tanımlamak. Kod stili, pedagojik odak, karmaşıklık vb. Dreyfus seviyelerine
# göre (novice → expert) değerler artar/azalır.

@dataclass
class PersonaVector:
    """Persona karakteristik vektörü - 10 özellik (persona_id hariç)."""
    persona_id: str
    code_complexity: float    # Kod karmaşıklığı (0=basit, 1=karmaşık)
    verbosity: float         # Açıklayıcılık / yorum yoğunluğu
    technical_depth: float   # Teknik derinlik (seviye)
    pedagogical_focus: float # Pedagojik odak (eğitim vs üretim)
    comment_density: float   # Yorum yoğunluğu
    modularity: float        # Modülerlik (parçalı yapı)
    example_richness: float  # Örnek zenginliği
    learning_support: float  # Öğrenme desteği
    production_readiness: float  # Production'a hazırlık
    innovation_factor: float     # Yenilikçilik / ileri pattern'ler


# =============================================================================
# RECOMMENDATION ENGINE - Ana tavsiye motoru
# =============================================================================
# AMAÇ: R(u,p) = α·S + β·C + γ·P + δ·L formülüyle her persona için tek skor.
# α,β,γ,δ ağırlıklar (toplam 1). S=benzerlik, C=yetkinlik uyumu, P=performans
# tahmini, L=öğrenme yörüngesi. Dual-Mode: similarity / complementary / adaptive.

class RecommendationEngine:
    """
    Matematiksel Tavsiye Motoru.
    Ana Formül: R(u,p) = α·S(u,p) + β·C(u,p) + γ·P(u,p,g) + δ·L(u,t)
    """

    def __init__(self, alpha=0.30, beta=0.35, gamma=0.25, delta=0.10):
        """
        Engine başlatma.

        NEDEN BU VARSAYILAN DEĞERLER? (THEORETICAL_FRAMEWORK.md: "Pilot Study'den")
        - alpha=0.30: Benzerlik/Farklılık (S veya 1-S). Profil uyumu.
        - beta=0.35:  Yetkinlik uyumu/Tamamlayıcılık (C veya D). ZPD öncelikli; en ağır kriter.
        - gamma=0.25: Performans tahmini (P). Başarı beklentisi.
        - delta=0.10: Öğrenme yörüngesi (L). Destekleyici; adaptive modda complementary öne çıkar.
        Toplam α+β+γ+δ=1. Geri bildirimle optimize_persona_weights() ile güncellenebilir.
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.persona_vectors = self._initialize_persona_vectors()

    def _initialize_persona_vectors(self) -> Dict[str, PersonaVector]:
        """
        Her persona için karakteristik vektör tanımla (Dreyfus Model).
        Eğitim (edu_*) ve Teknoloji (tech_*) alanında 5'er seviye:
        novice, advanced_beginner, competent, proficient, expert.
        0.0 = düşük, 1.0 = yüksek. Novice: düşük technical, yüksek verbosity;
        Expert: yüksek technical, düşük verbosity, yüksek innovation.
        """
        return {
            # ---------- EĞİTİM ALANI (Education) - 5 persona ----------
            "edu_novice": PersonaVector(
                persona_id="edu_novice",
                code_complexity=0.15,
                verbosity=0.98,
                technical_depth=0.10,
                pedagogical_focus=0.95,
                comment_density=0.98,
                modularity=0.15,
                example_richness=0.85,
                learning_support=0.92,
                production_readiness=0.10,
                innovation_factor=0.08
            ),
            "edu_advanced_beginner": PersonaVector(
                persona_id="edu_advanced_beginner",
                code_complexity=0.25,
                verbosity=0.85,
                technical_depth=0.25,
                pedagogical_focus=0.90,
                comment_density=0.80,
                modularity=0.35,
                example_richness=0.80,
                learning_support=0.88,
                production_readiness=0.25,
                innovation_factor=0.20
            ),
            "edu_competent": PersonaVector(
                persona_id="edu_competent",
                code_complexity=0.45,
                verbosity=0.65,
                technical_depth=0.50,
                pedagogical_focus=0.85,
                comment_density=0.60,
                modularity=0.60,
                example_richness=0.70,
                learning_support=0.80,
                production_readiness=0.50,
                innovation_factor=0.40
            ),
            "edu_proficient": PersonaVector(
                persona_id="edu_proficient",
                code_complexity=0.65,
                verbosity=0.50,
                technical_depth=0.75,
                pedagogical_focus=0.88,
                comment_density=0.40,
                modularity=0.80,
                example_richness=0.75,
                learning_support=0.85,
                production_readiness=0.70,
                innovation_factor=0.65
            ),
            "edu_expert": PersonaVector(
                persona_id="edu_expert",
                code_complexity=0.80,
                verbosity=0.35,
                technical_depth=0.88,
                pedagogical_focus=0.95,
                comment_density=0.30,
                modularity=0.85,
                example_richness=0.70,
                learning_support=0.80,
                production_readiness=0.75,
                innovation_factor=0.95
            ),
            # ---------- TEKNOLOJİ ALANI (Technology) - 5 persona ----------
            "tech_novice": PersonaVector(
                persona_id="tech_novice",
                code_complexity=0.12,
                verbosity=0.95,
                technical_depth=0.08,
                pedagogical_focus=0.15,
                comment_density=0.95,
                modularity=0.10,
                example_richness=0.30,
                learning_support=0.35,
                production_readiness=0.05,
                innovation_factor=0.05
            ),
            "tech_advanced_beginner": PersonaVector(
                persona_id="tech_advanced_beginner",
                code_complexity=0.30,
                verbosity=0.75,
                technical_depth=0.35,
                pedagogical_focus=0.20,
                comment_density=0.70,
                modularity=0.40,
                example_richness=0.45,
                learning_support=0.48,
                production_readiness=0.35,
                innovation_factor=0.25
            ),
            "tech_competent": PersonaVector(
                persona_id="tech_competent",
                code_complexity=0.55,
                verbosity=0.50,
                technical_depth=0.65,
                pedagogical_focus=0.25,
                comment_density=0.50,
                modularity=0.70,
                example_richness=0.50,
                learning_support=0.55,
                production_readiness=0.75,
                innovation_factor=0.45
            ),
            "tech_proficient": PersonaVector(
                persona_id="tech_proficient",
                code_complexity=0.75,
                verbosity=0.35,
                technical_depth=0.85,
                pedagogical_focus=0.30,
                comment_density=0.35,
                modularity=0.90,
                example_richness=0.60,
                learning_support=0.60,
                production_readiness=0.90,
                innovation_factor=0.75
            ),
            "tech_expert": PersonaVector(
                persona_id="tech_expert",
                code_complexity=0.88,
                verbosity=0.25,
                technical_depth=0.98,
                pedagogical_focus=0.18,
                comment_density=0.25,
                modularity=0.85,
                example_richness=0.55,
                learning_support=0.50,
                production_readiness=0.85,
                innovation_factor=0.98
            )
        }

    def create_user_vector(self, competency_profile: Dict) -> UserVector:
        """
        Yetkinlik profilinden 10 boyutlu UserVector oluştur.

        GİRDİ: score (0-100) veya technical_score + educational_score,
               level (Dreyfus), domain (technical/educational), responses.
        ÇIKTI: UserVector. Bilgi türleri ve bilişsel faktörler skor/level
        üzerinden formüllerle türetilir.
        """
        if 'score' in competency_profile:
            score = competency_profile['score'] / 100
        else:
            tech = competency_profile.get('technical_score', 50.0)
            edu = competency_profile.get('educational_score', 50.0)
            if tech > 5 or edu > 5:
                score = (tech + edu) / 2 / 100.0
            else:
                score = ((tech + edu) / 2 - 1) / 4
            score = max(0, min(1, score))

        domain = competency_profile.get('domain') or competency_profile.get('dominant_domain', 'technical')
        level = competency_profile.get('level') or competency_profile.get('technical_level', 'novice')
        responses = competency_profile.get('responses', {})

        level_mapping = {
            'novice': 0.1,
            'advanced_beginner': 0.3,
            'competent': 0.5,
            'proficient': 0.7,
            'expert': 0.9
        }
        technical_skill = level_mapping.get(level, 0.5)
        domain_knowledge = 0.8 if domain == 'technical' else 0.7
        ai_experience = 0.7 if responses.get('ai_experience') else 0.2

        if level in ['novice', 'advanced_beginner']:
            learning_goal = 0.9
        elif level == 'competent':
            learning_goal = 0.6
        else:
            learning_goal = 0.3

        procedural = min(1.0, score * 1.2)
        declarative = score
        conditional = max(0.3, score - 0.2)

        cognitive_capacity = 0.5 + (score * 0.5)
        pattern_recognition = max(0.3, score - 0.1)
        abstraction_level = score

        return UserVector(
            technical_skill=technical_skill,
            domain_knowledge=domain_knowledge,
            ai_experience=ai_experience,
            learning_goal=learning_goal,
            procedural_knowledge=procedural,
            declarative_knowledge=declarative,
            conditional_knowledge=conditional,
            cognitive_capacity=cognitive_capacity,
            pattern_recognition=pattern_recognition,
            abstraction_level=abstraction_level
        )

    def calculate_similarity_score(self, user: UserVector, persona: PersonaVector,
                                   focus_dimension: str = "all") -> float:
        """
        S(u,p): Kullanıcı-Persona benzerlik skoru (0-1).

        YÖNTEM: Cosine similarity (yön) + Normalize Euclidean (mesafe)
        hibrit: 0.6·cos + 0.4·(1 - norm_euclidean).
        NEDEN 60/40? Yön = "profil tipi" (kimin tipi sana uyuyor) en belirleyici → 0.6;
        uzaklık = "seviye" yakınlığı destekleyici → 0.4. Kalibrasyon yok; tasarım tercihi.
        User 10 boyut, persona 10 boyuta map edilir (technical_depth,
        pedagogical_focus, modularity, verbosity, learning_support vb.).
        """
        user_vec = np.array([
            user.technical_skill,
            user.domain_knowledge,
            user.ai_experience,
            user.learning_goal,
            user.procedural_knowledge,
            user.declarative_knowledge,
            user.conditional_knowledge,
            user.cognitive_capacity,
            user.pattern_recognition,
            user.abstraction_level
        ])
        persona_vec = np.array([
            persona.technical_depth,
            persona.pedagogical_focus,
            persona.innovation_factor,
            1 - persona.production_readiness,
            persona.modularity,
            persona.verbosity,
            persona.learning_support,
            1 - persona.code_complexity,
            persona.example_richness,
            persona.code_complexity
        ])
        cos_sim = cosine_similarity(user_vec, persona_vec)
        euclidean_dist = euclidean_distance(user_vec, persona_vec)
        max_dist = np.sqrt(len(user_vec))
        norm_euclidean = euclidean_dist / max_dist
        euclidean_sim = 1 - norm_euclidean
        similarity = 0.6 * cos_sim + 0.4 * euclidean_sim
        return max(0, min(1, similarity))

    def calculate_competency_match(self, user: UserVector, persona: PersonaVector) -> float:
        """
        C(u,p): Yetkinlik uyum skoru (ZPD - Vygotsky).

        Persona zorluğu ile kullanıcı becerisi arasındaki optimal mesafe
        Gaussian ile ölçülür. learning_goal'e göre pedagogical_focus veya
        production_readiness ile hizalama; bilgi türü uyumu (procedural-
        modularity, declarative-verbosity, conditional-learning_support).
        """
        persona_difficulty = (persona.code_complexity + persona.technical_depth) / 2
        user_skill = (user.technical_skill + user.domain_knowledge) / 2
        lambda_param = 2.0
        skill_diff = abs(user_skill - persona_difficulty)
        gaussian_match = np.exp(-lambda_param * (skill_diff ** 2))
        if user.learning_goal > 0.7:
            alignment = persona.pedagogical_focus
        else:
            alignment = persona.production_readiness
        knowledge_match = (
            user.procedural_knowledge * persona.modularity * 0.4 +
            user.declarative_knowledge * persona.verbosity * 0.3 +
            user.conditional_knowledge * persona.learning_support * 0.3
        )
        competency_match = (
            gaussian_match * 0.5 +
            alignment * 0.3 +
            knowledge_match * 0.2
        )
        return max(0, min(1, competency_match))

    def predict_performance(self, user: UserVector, persona: PersonaVector,
                          task_complexity: float = 0.5) -> float:
        """
        P(u,p,g): Performans tahmin skoru.

        Regresyon: z = β0 + β1·skill + β2·quality + β3·match + β4·task_complexity;
        çıktı sigmoid(z). Pilot veriden kalibre edilmiş katsayılar.
        """
        beta_0, beta_1, beta_2, beta_3, beta_4 = 0.3, 0.4, 0.3, 0.25, -0.2
        user_skill_feature = (user.technical_skill + user.domain_knowledge) / 2
        persona_quality = (persona.production_readiness + persona.learning_support) / 2
        match_feature = self.calculate_similarity_score(user, persona)
        z = (beta_0 + beta_1 * user_skill_feature + beta_2 * persona_quality +
             beta_3 * match_feature + beta_4 * task_complexity)
        performance = 1 / (1 + np.exp(-z))
        return max(0, min(1, performance))

    def calculate_learning_trajectory(self, user: UserVector, persona: PersonaVector,
                                     time_factor: float = 0.5) -> float:
        """
        L(u,t): Öğrenme yörüngesi. Power Law of Practice: zamanla öğrenme
        (1 - e^(-k·t)) ile persona learning_support ve kullanıcı
        learning_capacity (cognitive_capacity, pattern_recognition, abstraction)
        çarpılarak potansiyel hesaplanır.
        """
        L_max = 1.0
        k = 2.0
        time_learning = L_max * (1 - np.exp(-k * time_factor))
        learning_support = persona.learning_support
        learning_capacity = (
            user.cognitive_capacity * 0.4 +
            user.pattern_recognition * 0.3 +
            (1 - user.abstraction_level) * 0.3
        )
        potential = learning_support * learning_capacity
        trajectory = time_learning * potential
        return max(0, min(1, trajectory))

    def calculate_complementarity(self, user: UserVector, persona: PersonaVector) -> float:
        """
        D(u,p): Tamamlayıcılık skoru. Kullanıcının zayıf (1 - skill) ve
        persona'nın güçlü olduğu boyutlar çarpılıp ortalaması alınır.
        Yüksek D = persona kullanıcının eksiklerini kapatıyor.
        """
        user_weaknesses = {
            'technical': 1 - user.technical_skill,
            'domain': 1 - user.domain_knowledge,
            'ai_experience': 1 - user.ai_experience,
            'abstraction': 1 - user.abstraction_level
        }
        persona_strengths = {
            'technical': persona.technical_depth,
            'domain': persona.pedagogical_focus if user.learning_goal > 0.5 else persona.production_readiness,
            'ai_experience': persona.innovation_factor,
            'abstraction': persona.code_complexity
        }
        complementarity_scores = [
            persona_strengths.get(k, 0) * user_weaknesses.get(k, 0)
            for k in user_weaknesses
        ]
        avg_complementarity = np.mean(complementarity_scores)
        return max(0, min(1, avg_complementarity))

    # ========== COGNITIVE LOAD THEORY (Sweller, 1988) ==========

    def calculate_intrinsic_load(self, user: UserVector, task_complexity: float = 0.5) -> float:
        """
        Intrinsic Load: Görevin doğal karmaşıklığı × (1 - kullanıcı uzmanlığı).
        Novice + zor görev = yüksek IL; Expert + zor görev = düşük IL.
        """
        user_expertise = (
            user.technical_skill * 0.4 +
            user.domain_knowledge * 0.3 +
            user.procedural_knowledge * 0.3
        )
        intrinsic_load = task_complexity * (1 - user_expertise)
        return max(0, min(1, intrinsic_load))

    def calculate_extraneous_load(self, persona: PersonaVector) -> float:
        """
        Extraneous Load: Kötü tasarımdan kaynaklanan yük. Düşük modularity,
        aşırı verbosity (çok az veya çok fazla açıklama), kod karmaşıklığı.
        """
        poor_organization = 1 - persona.modularity
        if persona.verbosity < 0.3:
            excessive_verbosity = 0.3 - persona.verbosity
        elif persona.verbosity > 0.8:
            excessive_verbosity = persona.verbosity - 0.8
        else:
            excessive_verbosity = 0.0
        code_complexity_load = persona.code_complexity * 0.5
        extraneous_load = (
            poor_organization * 0.4 +
            excessive_verbosity * 0.3 +
            code_complexity_load * 0.3
        )
        return max(0, min(1, extraneous_load))

    def calculate_germane_load(self, user: UserVector, persona: PersonaVector) -> float:
        """
        Germane Load: Öğrenmeye yararlı yük. Learning support, pedagogical
        quality, kullanıcı öğrenme kapasitesi, example_richness.
        """
        learning_support = persona.learning_support
        pedagogical_quality = persona.pedagogical_focus
        learning_capacity = (
            user.cognitive_capacity * 0.4 +
            user.pattern_recognition * 0.3 +
            user.learning_goal * 0.3
        )
        example_richness = persona.example_richness
        germane_load = (
            learning_support * 0.35 +
            pedagogical_quality * 0.30 +
            learning_capacity * 0.20 +
            example_richness * 0.15
        )
        return max(0, min(1, germane_load))

    def calculate_total_cognitive_load(self, user: UserVector, persona: PersonaVector,
                                       task_complexity: float = 0.5) -> Dict[str, float]:
        """
        Toplam bilişsel yük: IL + EL - GL. Optimal bölge: productive_load
        (IL+GL) ≤ kapasite ve EL düşük. Overload/underload tespiti ve
        uyarı/öneri listesi döner.
        """
        intrinsic = self.calculate_intrinsic_load(user, task_complexity)
        extraneous = self.calculate_extraneous_load(persona)
        germane = self.calculate_germane_load(user, persona)
        total_load = intrinsic + extraneous - germane
        total_load = max(0, min(2, total_load))
        capacity = user.cognitive_capacity
        productive_load = intrinsic + germane
        is_in_optimal_zone = (productive_load <= capacity) and (extraneous < 0.3)
        is_overloaded = total_load > capacity
        overload_amount = max(0, total_load - capacity)
        is_underloaded = total_load < (capacity * 0.4)
        load_efficiency = germane / (intrinsic + extraneous + 0.001) if total_load > 0 else 0
        warnings = []
        recommendations = []
        if is_overloaded:
            warnings.append(f"⚠️ Cognitive Overload! ({overload_amount:.2f} over capacity)")
            recommendations.append("Consider easier persona or simpler task")
        if is_underloaded:
            warnings.append("ℹ️ Underutilized capacity - task may be too easy")
            recommendations.append("Consider more challenging persona")
        if extraneous > 0.5:
            warnings.append(f"⚠️ High Extraneous Load ({extraneous:.2f})")
            recommendations.append("Persona may have poor organization or excessive verbosity")
        if germane < 0.3:
            warnings.append(f"ℹ️ Low Germane Load ({germane:.2f})")
            recommendations.append("Limited learning support - consider pedagogical persona")
        if is_in_optimal_zone:
            recommendations.append("✅ Optimal Learning Zone - ideal match!")
        return {
            "intrinsic_load": intrinsic,
            "extraneous_load": extraneous,
            "germane_load": germane,
            "total_load": total_load,
            "productive_load": productive_load,
            "cognitive_capacity": capacity,
            "load_efficiency": load_efficiency,
            "is_in_optimal_zone": is_in_optimal_zone,
            "is_overloaded": is_overloaded,
            "is_underloaded": is_underloaded,
            "overload_amount": overload_amount,
            "warnings": warnings,
            "recommendations": recommendations
        }

    def get_clt_optimal_personas(self, user: UserVector, task_complexity: float = 0.5,
                                  top_k: int = 5) -> List[Dict]:
        """
        CLT'ye göre en iyi persona'ları seç: yüksek germane, düşük extraneous,
        optimal zone'da olan, overload yaratmayan. CLT skoru ile sıralanır.
        """
        clt_rankings = []
        for persona_id, persona_vec in self.persona_vectors.items():
            clt_analysis = self.calculate_total_cognitive_load(user, persona_vec, task_complexity)
            clt_score = (
                clt_analysis["germane_load"] * 0.35 +
                (1 - clt_analysis["extraneous_load"]) * 0.30 +
                clt_analysis["load_efficiency"] * 0.20 +
                (1.0 if clt_analysis["is_in_optimal_zone"] else 0.0) * 0.15
            )
            if clt_analysis["is_overloaded"]:
                clt_score *= (1 - clt_analysis["overload_amount"] * 0.5)
            clt_rankings.append({
                "persona_id": persona_id,
                "clt_score": clt_score,
                "clt_analysis": clt_analysis
            })
        clt_rankings.sort(key=lambda x: x["clt_score"], reverse=True)
        return clt_rankings[:top_k]

    def calculate_recommendation_score(self, user: UserVector, persona: PersonaVector,
                                      task_complexity: float = 0.5,
                                      time_factor: float = 0.5,
                                      mode: str = "adaptive",
                                      use_clt: bool = True) -> Dict:
        """
        R(u,p): Ana tavsiye skoru (Dual-Mode + CLT Entegre).
        
        YENİ FORMÜL:
        R_final = R_base × CLT_modifier
        
        CLT_modifier (Sweller, 1988):
        - Optimal zone ise: +10% bonus
        - Overload ise: -30% ceza (max)
        - High extraneous ise: -10% ceza
        - High germane ise: +5% bonus
        
        Similarity mod: R = α·S + β·C + γ·P + δ·L.
        Complementary mod: R = α·(1-S) + β·D + γ·P + δ·L.
        Adaptive: learning_goal > 0.7 → complementary; < 0.3 → similarity;
        arada → hybrid (learning_goal ile ağırlıklı ortalama).
        
        Dönüş: total_score, base_score, clt_modifier, clt_analysis dahil.
        """
        # MCDA bileşenlerini hesapla
        similarity = self.calculate_similarity_score(user, persona)
        competency = self.calculate_competency_match(user, persona)
        performance = self.predict_performance(user, persona, task_complexity)
        learning = self.calculate_learning_trajectory(user, persona, time_factor)
        complementarity = self.calculate_complementarity(user, persona)
        
        # CLT Analizi (Sweller, 1988)
        clt_analysis = self.calculate_total_cognitive_load(user, persona, task_complexity)

        # Adaptive mod belirleme
        if mode == "adaptive":
            if user.learning_goal > 0.7:
                actual_mode = "complementary"
            elif user.learning_goal < 0.3:
                actual_mode = "similarity"
            else:
                actual_mode = "hybrid"
        else:
            actual_mode = mode

        # Mod'a göre base_score hesapla
        if actual_mode == "similarity":
            base_score = (
                self.alpha * similarity +
                self.beta * competency +
                self.gamma * performance +
                self.delta * learning
            )
            strategy = "Benzerlik Bazlı (Rahat Çalışma)"
        elif actual_mode == "complementary":
            dissimilarity = 1 - similarity
            base_score = (
                self.alpha * dissimilarity +
                self.beta * complementarity +
                self.gamma * performance +
                self.delta * learning
            )
            strategy = "Tamamlayıcı (Eksik Kapatma)"
        else:  # hybrid
            similarity_score = (
                self.alpha * similarity +
                self.beta * competency +
                self.gamma * performance +
                self.delta * learning
            )
            dissimilarity = 1 - similarity
            complementary_score = (
                self.alpha * dissimilarity +
                self.beta * complementarity +
                self.gamma * performance +
                self.delta * learning
            )
            base_score = (
                user.learning_goal * complementary_score +
                (1 - user.learning_goal) * similarity_score
            )
            strategy = "Hibrit (Adaptif)"

        # CLT Modifier hesapla
        clt_modifier = 1.0
        clt_adjustments = []
        
        if use_clt:
            if clt_analysis["is_in_optimal_zone"]:
                clt_modifier += 0.10
                clt_adjustments.append("✅ Optimal Zone +10%")
            if clt_analysis["is_overloaded"]:
                penalty = min(0.30, clt_analysis["overload_amount"] * 0.3)
                clt_modifier -= penalty
                clt_adjustments.append(f"⚠️ Overload -{penalty*100:.0f}%")
            if clt_analysis["extraneous_load"] > 0.5:
                clt_modifier -= 0.10
                clt_adjustments.append("⚠️ High Extraneous -10%")
            if clt_analysis["germane_load"] > 0.7:
                clt_modifier += 0.05
                clt_adjustments.append("✅ High Germane +5%")

        # Final skor
        total_score = base_score * clt_modifier
        total_score = max(0, min(1, total_score))

        std_dev = 0.05
        ci_lower = max(0, total_score - 1.96 * std_dev)
        ci_upper = min(1, total_score + 1.96 * std_dev)
        
        return {
            "total_score": total_score,
            "base_score": base_score,
            "clt_modifier": clt_modifier,
            "mode": actual_mode,
            "strategy": strategy,
            "components": {
                "similarity": similarity,
                "dissimilarity": 1 - similarity,
                "competency_match": competency,
                "complementarity": complementarity,
                "performance_prediction": performance,
                "learning_trajectory": learning
            },
            "weights": {
                "alpha": self.alpha,
                "beta": self.beta,
                "gamma": self.gamma,
                "delta": self.delta
            },
            "clt_analysis": {
                "intrinsic_load": clt_analysis["intrinsic_load"],
                "extraneous_load": clt_analysis["extraneous_load"],
                "germane_load": clt_analysis["germane_load"],
                "total_load": clt_analysis["total_load"],
                "cognitive_capacity": clt_analysis["cognitive_capacity"],
                "is_in_optimal_zone": clt_analysis["is_in_optimal_zone"],
                "is_overloaded": clt_analysis["is_overloaded"],
                "load_efficiency": clt_analysis["load_efficiency"],
                "adjustments": clt_adjustments,
                "warnings": clt_analysis["warnings"],
                "recommendations": clt_analysis["recommendations"]
            },
            "confidence_interval": {
                "lower": ci_lower,
                "upper": ci_upper,
                "std_dev": std_dev
            }
        }

    def rank_personas(self, user_vector: UserVector,
                     task_complexity: float = 0.5,
                     top_k: int = 5) -> List[Dict]:
        """
        Tüm persona'ları calculate_recommendation_score ile skorla, skora göre
        sırala, en iyi top_k tanesini döndür (MCDA sıralaması).
        """
        rankings = []
        for persona_id, persona_vec in self.persona_vectors.items():
            scores = self.calculate_recommendation_score(
                user_vector, persona_vec, task_complexity
            )
            rankings.append({
                "persona_id": persona_id,
                "score": scores["total_score"],
                "components": scores["components"],
                "confidence_interval": scores["confidence_interval"]
            })
        rankings.sort(key=lambda x: x["score"], reverse=True)
        return rankings[:top_k]

    def explain_recommendation(self, user_vector: UserVector, persona_id: str) -> str:
        """
        Explainable AI: Bu persona neden önerildi? Bileşenlerden en yüksek
        katkıyı vereni seçip Türkçe cümle ile açıklar.
        """
        persona = self.persona_vectors.get(persona_id)
        if not persona:
            return "Persona bulunamadı"
        scores = self.calculate_recommendation_score(user_vector, persona)
        components = scores["components"]
        max_component = max(components.items(), key=lambda x: x[1])
        explanations = {
            "similarity": f"Sizin yetkinlik profilinize çok benziyor (benzerlik: {components['similarity']:.2f})",
            "competency_match": f"Seviyenize tam uygun - optimal challenge (uyum: {components['competency_match']:.2f})",
            "performance_prediction": f"Yüksek performans beklentisi (tahmin: {components['performance_prediction']:.2f})",
            "learning_trajectory": f"Güçlü öğrenme potansiyeli (yörünge: {components['learning_trajectory']:.2f})"
        }
        main_reason = explanations.get(max_component[0], "Genel uyumluluk")
        return f"{main_reason}. Toplam skor: {scores['total_score']:.2f}"

    def optimize_persona_weights(self, user_vector: UserVector,
                                 feedback_data: Optional[List[Dict]] = None) -> Dict[str, float]:
        """
        Kullanıcı geri bildirimine göre α,β,γ,δ ağırlıklarını güncelle (Basit
        Bayesian tarzı). learning_goal yüksekse similarity/learning artırılır;
        production odaklıysa competency/performance artırılır. Toplam 1 olacak
        şekilde normalize edilir.
        """
        if feedback_data is None or len(feedback_data) == 0:
            return {
                "alpha": self.alpha,
                "beta": self.beta,
                "gamma": self.gamma,
                "delta": self.delta
            }
        positive_feedback = sum(1 for f in feedback_data if f.get('rating', 0) > 3)
        total_feedback = len(feedback_data)
        if total_feedback > 0:
            success_rate = positive_feedback / total_feedback
            if user_vector.learning_goal > 0.7:
                alpha_new = self.alpha + 0.1 * success_rate
                delta_new = self.delta + 0.1 * success_rate
                beta_new = self.beta - 0.05 * success_rate
                gamma_new = self.gamma - 0.05 * success_rate
            else:
                beta_new = self.beta + 0.1 * success_rate
                gamma_new = self.gamma + 0.1 * success_rate
                alpha_new = self.alpha - 0.05 * success_rate
                delta_new = self.delta - 0.05 * success_rate
            total = alpha_new + beta_new + gamma_new + delta_new
            return {
                "alpha": alpha_new / total,
                "beta": beta_new / total,
                "gamma": gamma_new / total,
                "delta": delta_new / total
            }
        return {
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma,
            "delta": self.delta
        }

    def apply_weights(self, weights: Dict[str, float]) -> None:
        """
        Optimize edilmiş ağırlıkları engine'e uygula.
        Adaptive AI: Sistem kendini ayarlar.
        """
        self.alpha = weights.get("alpha", self.alpha)
        self.beta = weights.get("beta", self.beta)
        self.gamma = weights.get("gamma", self.gamma)
        self.delta = weights.get("delta", self.delta)

    def update_weights_from_feedback(self, user_vector: UserVector, 
                                     feedback_data: List[Dict]) -> Dict:
        """
        Geri bildirimden ağırlıkları hesapla VE uygula.
        
        ADAPTIVE AI MEKANİZMASI:
        Bu metod, kullanıcı geri bildirimine göre α,β,γ,δ ağırlıklarını
        dinamik olarak günceller. Bayesian güncelleme prensibi:
        - Pozitif feedback oranı yüksekse → mevcut stratejiyi güçlendir
        - Learning odaklı kullanıcı → similarity/learning ağırlıklarını artır
        - Production odaklı kullanıcı → competency/performance ağırlıklarını artır
        
        Args:
            user_vector: Kullanıcı vektörü
            feedback_data: Feedback listesi [{"persona_id": str, "rating": 1-5}, ...]
            
        Returns:
            Güncellenen ağırlıklar ve değişim raporu
        """
        old_weights = {
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma,
            "delta": self.delta
        }
        
        new_weights = self.optimize_persona_weights(user_vector, feedback_data)
        self.apply_weights(new_weights)
        
        return {
            "old_weights": old_weights,
            "new_weights": new_weights,
            "changes": {
                "alpha": new_weights["alpha"] - old_weights["alpha"],
                "beta": new_weights["beta"] - old_weights["beta"],
                "gamma": new_weights["gamma"] - old_weights["gamma"],
                "delta": new_weights["delta"] - old_weights["delta"]
            },
            "feedback_count": len(feedback_data),
            "applied": True
        }


# =============================================================================
# TEST BLOĞU - __main__ ile çalıştırıldığında
# =============================================================================
# AMAÇ: Örnek bir kullanıcı profili ile engine'i çalıştırıp top 5 persona
# sıralamasını ve bileşen skorlarını yazdırmak. Doğrulama / demo için.

if __name__ == "__main__":
    engine = RecommendationEngine()
    test_profile = {
        "score": 50,
        "level": "competent",
        "domain": "technical",
        "responses": {"ai_experience": True}
    }
    user_vec = engine.create_user_vector(test_profile)
    rankings = engine.rank_personas(user_vec, task_complexity=0.5, top_k=5)
    print("🎯 Top 5 Persona Tavsiyeleri:\n")
    for idx, ranking in enumerate(rankings, 1):
        persona_id = ranking["persona_id"]
        score = ranking["score"]
        components = ranking["components"]
        print(f"{idx}. {persona_id}: {score:.3f}")
        print(f"   Benzerlik: {components['similarity']:.3f}")
        print(f"   Yetkinlik Uyumu: {components['competency_match']:.3f}")
        print(f"   Performans Tahmini: {components['performance_prediction']:.3f}")
        print(f"   Öğrenme Yörüngesi: {components['learning_trajectory']:.3f}")
        print()
