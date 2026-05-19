"""
Persona Tanımları - Dreyfus 5 Aşamalı Yetkinlik Modeli
100 Persona: 2 Ana Domain × 10 Alt-uzmanlık × 5 Dreyfus Seviyesi

Dreyfus Model Stages:
1. Novice: Rule-based, context-free, rigid
2. Advanced Beginner: Pattern recognition, guideline-based
3. Competent: Prioritization, troubleshooting, deliberate planning
4. Proficient: Holistic understanding, intuitive, maxim-guided
5. Expert: Transcends rules, intuitive mastery, innovative

Ana Domainler:
1. Technology (Teknoloji) - 50 persona (10 alt-uzmanlık × 5 seviye)
2. Education (Pedagoji) - 50 persona (10 alt-uzmanlık × 5 seviye)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

# 100 Persona sistemini import et
from src.personas_100 import (
    Persona,
    ALL_PERSONAS,
    EDUCATION_PERSONAS,
    TECHNOLOGY_PERSONAS,
    DOMAINS,
    DREYFUS_CHARACTERISTICS,
    get_persona_by_id,
    get_personas_by_domain,
    get_personas_by_category,
    get_personas_by_subdomain,
    get_personas_by_level,
    get_subdomain_personas,
    get_all_personas,
    get_random_persona,
    get_personas_info,
    get_persona_for_recommendation,
    get_complementary_personas,
    get_persona_display_role_description,
)


# ============================================================================
# GERİYE UYUMLULUK - ESKİ PERSONA ID'LERİ
# ============================================================================

# Orijinal 10 persona ID'leri için mapping
LEGACY_PERSONA_MAPPING = {
    "edu_novice": "education_pedagogical_novice_1",
    "edu_advanced_beginner": "education_pedagogical_advanced_beginner_2",
    "edu_competent": "education_pedagogical_competent_3",
    "edu_proficient": "education_pedagogical_proficient_4",
    "edu_expert": "education_pedagogical_expert_5",
    "tech_novice": "technology_blockchain_novice_11",
    "tech_advanced_beginner": "technology_blockchain_advanced_beginner_12",
    "tech_competent": "technology_blockchain_competent_13",
    "tech_proficient": "technology_blockchain_proficient_14",
    "tech_expert": "technology_blockchain_expert_15"
}


def get_legacy_persona(legacy_id: str) -> Persona:
    """Eski ID ile persona getir (backward compatibility)"""
    if legacy_id in LEGACY_PERSONA_MAPPING:
        return get_persona_by_id(LEGACY_PERSONA_MAPPING[legacy_id])
    # Yeni ID ile dene
    return get_persona_by_id(legacy_id)


def get_persona_details(persona_id: str) -> Dict:
    """Bir persona'nın tüm detaylarını dict olarak getir"""
    try:
        persona = get_persona_by_id(persona_id)
    except ValueError:
        # Legacy ID olabilir
        persona = get_legacy_persona(persona_id)
    
    return {
        "id": persona.id,
        "name": persona.name,
        "role": persona.role,
        "category": persona.category,
        "subcategory": getattr(persona, 'subcategory', persona.category),
        "dreyfus_level": persona.dreyfus_level,
        "description": persona.description,
        "background": persona.background,
        "philosophy": persona.philosophy,
        "coding_style": persona.coding_style,
        "strengths": persona.strengths,
        "weaknesses": persona.weaknesses,
        "priorities": persona.priorities,
        "favorite_patterns": persona.favorite_patterns,
        "code_characteristics": persona.code_characteristics,
        "avatar": persona.avatar,
        "specialty_quote": persona.specialty_quote,
        # Sayısal özellikler
        "code_complexity": getattr(persona, 'code_complexity', 0.5),
        "verbosity": getattr(persona, 'verbosity', 0.5),
        "technical_depth": getattr(persona, 'technical_depth', 0.5),
        "pedagogical_focus": getattr(persona, 'pedagogical_focus', 0.5),
        "comment_density": getattr(persona, 'comment_density', 0.5),
        "modularity": getattr(persona, 'modularity', 0.5),
        "example_richness": getattr(persona, 'example_richness', 0.5),
        "learning_support": getattr(persona, 'learning_support', 0.5),
        "production_readiness": getattr(persona, 'production_readiness', 0.5),
        "innovation_factor": getattr(persona, 'innovation_factor', 0.5)
    }


# ============================================================================
# PERSONA VEKTÖRLERİ - RECOMMENDATION ENGINE İÇİN
# ============================================================================

def get_persona_vector(persona_id: str) -> List[float]:
    """Persona'nın 10-boyutlu vektörünü döndür (recommendation engine için)"""
    try:
        persona = get_persona_by_id(persona_id)
    except ValueError:
        persona = get_legacy_persona(persona_id)
    
    return [
        getattr(persona, 'code_complexity', 0.5),
        getattr(persona, 'verbosity', 0.5),
        getattr(persona, 'technical_depth', 0.5),
        getattr(persona, 'pedagogical_focus', 0.5),
        getattr(persona, 'comment_density', 0.5),
        getattr(persona, 'modularity', 0.5),
        getattr(persona, 'example_richness', 0.5),
        getattr(persona, 'learning_support', 0.5),
        getattr(persona, 'production_readiness', 0.5),
        getattr(persona, 'innovation_factor', 0.5)
    ]


def get_all_persona_vectors() -> Dict[str, List[float]]:
    """Tüm personaların vektörlerini döndür"""
    return {p.id: get_persona_vector(p.id) for p in ALL_PERSONAS}


# ============================================================================
# 100 PERSONA SİSTEMİ - ÖZET BİLGİ
# ============================================================================

"""
YENİ SİSTEM YAPISI:
==================
10 Domain × 2 Alt-uzmanlık × 5 Dreyfus = 100 Persona

1. Education (education)
   - pedagogical: Pedagojik Tasarım
   - curriculum: Müfredat Geliştirme

2. Technology (technology)
   - blockchain: Smart Contract
   - web3: Web3 Entegrasyon

3. DeFi (defi)
   - lending: Lending/Borrowing
   - trading: DEX/Trading

4. Security (security)
   - audit: Güvenlik Denetimi
   - forensics: Blockchain Forensics

5. NFT/Gaming (nft_gaming)
   - nft: NFT Sistemleri
   - gamefi: GameFi

6. Enterprise (enterprise)
   - corporate: Kurumsal Çözümler
   - government: Kamu Sektörü

7. Research (research)
   - academic: Akademik Araştırma
   - protocol: Protokol Geliştirme

8. UX/Design (ux_design)
   - frontend: Web3 Frontend
   - devex: Developer Experience

9. Testing (testing)
   - qa: QA ve Test
   - formal: Formal Verification

10. Infrastructure (infrastructure)
    - devops: DevOps
    - scaling: L2 ve Scaling

KULLANIM ÖRNEKLERİ:
==================
# Tüm personaları getir
all_personas = get_all_personas()  # 100 persona

# Kategoriye göre
edu_personas = get_personas_by_category("education")  # 10 persona

# Alt kategoriye göre
audit_personas = get_personas_by_subcategory("security", "audit")  # 5 persona

# Seviyeye göre
experts = get_personas_by_level("expert")  # 20 persona

# Rastgele
random_defi = get_random_persona(category="defi", level="competent")

# Persona vektörü (recommendation engine için)
vector = get_persona_vector("education_pedagogical_novice_1")

# Legacy ID ile (geriye uyumluluk)
old_persona = get_legacy_persona("edu_novice")
"""


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    # Classes
    "Persona",
    
    # Persona lists
    "ALL_PERSONAS",
    "EDUCATION_PERSONAS",
    "TECHNOLOGY_PERSONAS",
    
    # Constants
    "DOMAINS",
    "DREYFUS_CHARACTERISTICS",
    "LEGACY_PERSONA_MAPPING",
    
    # Functions
    "get_persona_by_id",
    "get_personas_by_domain",
    "get_personas_by_category",
    "get_personas_by_subdomain",
    "get_subdomain_personas",
    "get_personas_by_level",
    "get_all_personas",
    "get_random_persona",
    "get_personas_info",
    "get_persona_for_recommendation",
    "get_complementary_personas",
    "get_legacy_persona",
    "get_persona_details",
    "get_persona_vector",
    "get_all_persona_vectors"
]
