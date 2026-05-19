"""
100 Persona Tanımları - Teknik-Pedagojik İkili Yapı
2 Ana Domain × 10 Alt-Domain × 5 Dreyfus Seviyesi = 100 Persona

Ana Domainler:
1. TEKNOLOJİ (Technology) - 50 Persona
2. PEDAGOJİ (Education) - 50 Persona

Her ana domain 10 alt-uzmanlık alanı içerir.
Her alt-uzmanlık 5 Dreyfus seviyesinde persona içerir.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random

# =============================================================================
# PERSONA DATACLASS
# =============================================================================

@dataclass
class Persona:
    """Persona sınıfı"""
    id: str
    name: str
    role: str
    domain: str          # "technology" veya "education"
    subdomain: str       # 10 alt-domain'den biri
    category: str        # domain ile aynı (backward compatibility)
    dreyfus_level: str
    description: str
    background: str
    philosophy: str
    coding_style: str
    strengths: List[str]
    weaknesses: List[str]
    priorities: List[str]
    favorite_patterns: List[str]
    code_characteristics: Dict[str, str]
    system_prompt: str
    avatar: str
    specialty_quote: str
    
    # Sayısal özellikler (recommendation engine için)
    code_complexity: float = 0.5
    verbosity: float = 0.5
    technical_depth: float = 0.5
    pedagogical_focus: float = 0.5
    comment_density: float = 0.5
    modularity: float = 0.5
    example_richness: float = 0.5
    learning_support: float = 0.5
    production_readiness: float = 0.5
    innovation_factor: float = 0.5


# =============================================================================
# DREYFUS SEVİYE ÖZELLİKLERİ
# =============================================================================

DREYFUS_LEVELS = ["novice", "advanced_beginner", "competent", "proficient", "expert"]

DREYFUS_CHARACTERISTICS = {
    "novice": {
        "code_complexity": 0.15,
        "verbosity": 0.95,
        "technical_depth": 0.15,
        "pedagogical_focus": 0.90,
        "comment_density": 0.95,
        "modularity": 0.20,
        "example_richness": 0.85,
        "learning_support": 0.90,
        "production_readiness": 0.10,
        "innovation_factor": 0.05
    },
    "advanced_beginner": {
        "code_complexity": 0.30,
        "verbosity": 0.75,
        "technical_depth": 0.35,
        "pedagogical_focus": 0.70,
        "comment_density": 0.70,
        "modularity": 0.45,
        "example_richness": 0.70,
        "learning_support": 0.75,
        "production_readiness": 0.35,
        "innovation_factor": 0.15
    },
    "competent": {
        "code_complexity": 0.55,
        "verbosity": 0.50,
        "technical_depth": 0.60,
        "pedagogical_focus": 0.45,
        "comment_density": 0.50,
        "modularity": 0.70,
        "example_richness": 0.55,
        "learning_support": 0.55,
        "production_readiness": 0.70,
        "innovation_factor": 0.35
    },
    "proficient": {
        "code_complexity": 0.75,
        "verbosity": 0.30,
        "technical_depth": 0.80,
        "pedagogical_focus": 0.25,
        "comment_density": 0.30,
        "modularity": 0.85,
        "example_richness": 0.40,
        "learning_support": 0.35,
        "production_readiness": 0.90,
        "innovation_factor": 0.60
    },
    "expert": {
        "code_complexity": 0.90,
        "verbosity": 0.15,
        "technical_depth": 0.95,
        "pedagogical_focus": 0.15,
        "comment_density": 0.15,
        "modularity": 0.95,
        "example_richness": 0.25,
        "learning_support": 0.20,
        "production_readiness": 0.98,
        "innovation_factor": 0.90
    }
}

# Domain'e göre ayarlamalar
DOMAIN_ADJUSTMENTS = {
    "technology": {
        "technical_depth": +0.15,
        "pedagogical_focus": -0.25,
        "production_readiness": +0.10,
        "learning_support": -0.15
    },
    "education": {
        "technical_depth": -0.15,
        "pedagogical_focus": +0.25,
        "production_readiness": -0.10,
        "learning_support": +0.20,
        "example_richness": +0.15
    }
}

# =============================================================================
# DOMAIN TANIMLARI
# =============================================================================

DOMAINS = {
    "technology": {
        "name": "Teknoloji",
        "name_en": "Technology",
        "emoji": "⛓️",
        "description": "Blockchain ve yazılım geliştirme odaklı teknik uzmanlık",
        "subdomains": {
            "smart_contract": {
                "name": "Akıllı Sözleşme Geliştirme",
                "name_en": "Smart Contract Development",
                "focus": "Solidity, EVM, akıllı sözleşme yazımı",
                "focus_en": "Solidity, EVM, smart contract development",
                "tech": ["Solidity", "Hardhat", "OpenZeppelin", "ERC Standartları"]
            },
            "web3_frontend": {
                "name": "Web3 Frontend",
                "name_en": "Web3 Frontend Development",
                "focus": "Blockchain-frontend entegrasyonu",
                "focus_en": "Blockchain-frontend integration",
                "tech": ["Ethers.js", "Wagmi", "RainbowKit", "Web3Modal"]
            },
            "defi": {
                "name": "DeFi Protokolleri",
                "name_en": "DeFi Protocols",
                "focus": "Merkezi olmayan finans sistemleri",
                "focus_en": "Decentralized finance systems",
                "tech": ["AMM", "Lending", "Staking", "Yield Farming"]
            },
            "security": {
                "name": "Güvenlik ve Denetim",
                "name_en": "Security & Audit",
                "focus": "Smart contract güvenliği ve audit",
                "focus_en": "Smart contract security and audit",
                "tech": ["Slither", "Mythril", "Echidna", "Foundry Fuzz"]
            },
            "nft_gaming": {
                "name": "NFT ve Gaming",
                "name_en": "NFT & GameFi",
                "focus": "NFT sistemleri ve blockchain oyunları",
                "focus_en": "NFT systems and blockchain gaming",
                "tech": ["ERC721", "ERC1155", "Game Mechanics", "Metadata"]
            },
            "l2_scaling": {
                "name": "L2 ve Ölçeklendirme",
                "name_en": "L2 & Scaling",
                "focus": "Layer 2 çözümleri ve ölçeklendirme",
                "focus_en": "Layer 2 solutions and scaling",
                "tech": ["Optimism", "Arbitrum", "zkSync", "Polygon"]
            },
            "devops": {
                "name": "DevOps ve Altyapı",
                "name_en": "DevOps & Infrastructure",
                "focus": "CI/CD, deployment, monitoring",
                "focus_en": "CI/CD, deployment, monitoring",
                "tech": ["GitHub Actions", "Docker", "Alchemy", "Infura"]
            },
            "testing": {
                "name": "Test ve QA",
                "name_en": "Testing & QA",
                "focus": "Test stratejileri ve kalite güvence",
                "focus_en": "Test strategies and quality assurance",
                "tech": ["Foundry", "Hardhat Tests", "Coverage", "Invariant Testing"]
            },
            "protocol_research": {
                "name": "Protokol Araştırma",
                "name_en": "Protocol Research",
                "focus": "Yeni protokol ve mekanizma tasarımı",
                "focus_en": "New protocol and mechanism design",
                "tech": ["EIP/ERC", "Consensus", "Cryptography", "zkSNARK"]
            },
            "enterprise": {
                "name": "Kurumsal Blockchain",
                "name_en": "Enterprise Blockchain",
                "focus": "B2B ve kurumsal çözümler",
                "focus_en": "B2B and enterprise solutions",
                "tech": ["Hyperledger", "Private Chains", "Permissioned Networks"]
            }
        }
    },
    "education": {
        "name": "Pedagoji",
        "name_en": "Education",
        "emoji": "📚",
        "description": "Eğitim teorileri ve öğretim tasarımı odaklı pedagojik uzmanlık",
        "subdomains": {
            "instructional_design": {
                "name": "Öğretim Tasarımı",
                "name_en": "Instructional Design",
                "focus": "Öğretim materyali ve süreç tasarımı",
                "focus_en": "Instructional material and process design",
                "tech": ["ADDIE", "SAM", "Bloom Taksonomisi", "Backward Design"]
            },
            "curriculum": {
                "name": "Müfredat Geliştirme",
                "name_en": "Curriculum Development",
                "focus": "Blockchain eğitim müfredatı tasarımı",
                "focus_en": "Blockchain education curriculum design",
                "tech": ["Learning Objectives", "Competency Mapping", "Sequencing"]
            },
            "learning_analytics": {
                "name": "Öğrenme Analitiği",
                "name_en": "Learning Analytics",
                "focus": "Öğrenme verisi analizi ve kişiselleştirme",
                "focus_en": "Learning data analysis and personalization",
                "tech": ["xAPI", "Learning Dashboards", "Predictive Models"]
            },
            "assessment": {
                "name": "Değerlendirme ve Ölçme",
                "name_en": "Assessment & Evaluation",
                "focus": "Öğrenme değerlendirme yöntemleri",
                "focus_en": "Learning assessment methods",
                "tech": ["Rubrics", "Formative Assessment", "Peer Review", "Portfolios"]
            },
            "gamification": {
                "name": "Oyunlaştırma",
                "name_en": "Gamification",
                "focus": "Oyun mekanikleri ile öğrenme",
                "focus_en": "Learning with game mechanics",
                "tech": ["Badges", "Leaderboards", "Quests", "XP Systems"]
            },
            "adaptive_learning": {
                "name": "Uyarlanabilir Öğrenme",
                "name_en": "Adaptive Learning",
                "focus": "Kişiselleştirilmiş öğrenme yolları",
                "focus_en": "Personalized learning paths",
                "tech": ["AI Tutors", "Personalization", "Spaced Repetition"]
            },
            "accessibility": {
                "name": "Erişilebilirlik ve UX",
                "name_en": "Accessibility & UX",
                "focus": "Kapsayıcı ve erişilebilir tasarım",
                "focus_en": "Inclusive and accessible design",
                "tech": ["WCAG", "Universal Design", "Cognitive Load", "UX Research"]
            },
            "educational_research": {
                "name": "Eğitim Araştırması",
                "name_en": "Educational Research",
                "focus": "Eğitim bilimi araştırma yöntemleri",
                "focus_en": "Education science research methods",
                "tech": ["Action Research", "Design-Based Research", "Mixed Methods"]
            },
            "teacher_training": {
                "name": "Öğretmen Eğitimi",
                "name_en": "Teacher Training",
                "focus": "Eğitimci yetiştirme ve mesleki gelişim",
                "focus_en": "Educator training and professional development",
                "tech": ["TPACK", "Microteaching", "Peer Coaching", "Reflection"]
            },
            "content_creation": {
                "name": "İçerik Üretimi",
                "name_en": "Content Creation",
                "focus": "Eğitim içeriği tasarımı ve üretimi",
                "focus_en": "Educational content design and production",
                "tech": ["Video Production", "Interactive Content", "OER", "Multimedia"]
            }
        }
    }
}

# =============================================================================
# İSİM VE KARAKTER HAVUZU
# =============================================================================

TURKISH_NAMES = {
    "male": ["Ahmet", "Mehmet", "Ali", "Can", "Deniz", "Emre", "Burak", "Murat", 
             "Kerem", "Cem", "Kaan", "Berk", "Eren", "Oğuz", "Serkan", "Tolga",
             "Umut", "Yusuf", "Barış", "Efe", "Koray", "Onur", "Selim", "Tarık",
             "Volkan", "Hakan", "İlker", "Caner", "Doruk", "Erdem"],
    "female": ["Ayşe", "Fatma", "Zeynep", "Elif", "Defne", "Selin", "Pınar", "Derya",
               "Ebru", "Gül", "İrem", "Melis", "Naz", "Özge", "Sibel", "Yasemin",
               "Ceren", "Dilan", "Eylül", "Fulya", "Hazal", "Idil", "Kardelen", "Lale",
               "Meltem", "Nehir", "Oya", "Rana", "Sude", "Tuğçe"]
}

SURNAMES_BY_LEVEL = {
    "novice": ["Acemi", "Başlangıç", "Yeni", "Öğrenci", "İlk"],
    "advanced_beginner": ["Gelişen", "İlerleyen", "Büyüyen", "Aday", "Çalışkan"],
    "competent": ["Yetkin", "Bilgili", "Becerikli", "Tecrübeli", "Planlı"],
    "proficient": ["Usta", "İleri", "Deneyimli", "Yetenekli", "Kıdemli"],
    "expert": ["Uzman", "Üstad", "Lider", "Öncü", "Kahraman"]
}

AVATARS = {
    "novice": ["🔰", "📖", "🌱", "🐣", "✏️"],
    "advanced_beginner": ["📚", "🎯", "📝", "🌿", "⭐"],
    "competent": ["🎯", "💼", "🔧", "🌳", "⚙️"],
    "proficient": ["🏆", "🎓", "🔥", "🌲", "💡"],
    "expert": ["🚀", "👑", "💎", "🌟", "🔮"]
}

QUOTES = {
    "novice": [
        "Adım adım öğreniyorum!",
        "Her gün biraz daha ilerliyorum!",
        "Hata yapmak öğrenmenin parçası!",
        "Sorular sormaktan çekinmiyorum!",
        "Temel kavramları sağlamlaştırıyorum!"
    ],
    "advanced_beginner": [
        "Pattern'leri görmeye başladım!",
        "Artık bağlantıları kurabiliyorum!",
        "Örneklerden öğreniyorum!",
        "Her proje yeni bir deneyim!",
        "Bilgimi uygulamaya dökebiliyorum!"
    ],
    "competent": [
        "Planlama başarının anahtarı!",
        "Her kod bir hedef taşır!",
        "Kalite taviz vermez!",
        "Sistematik düşünce önemli!",
        "Problem çözme bir sanattır!"
    ],
    "proficient": [
        "Bütünsel bakış gerekli!",
        "Sezgi deneyimden gelir!",
        "Detaylar fark yaratır!",
        "Mentörlük bilgiyi çoğaltır!",
        "Mükemmellik bir yolculuktur!"
    ],
    "expert": [
        "Geleceği yaratmak lazım!",
        "Kuralları aşmak gerek!",
        "İnovasyon risk gerektirir!",
        "Paradigmalar değişmeli!",
        "Bilgi paylaştıkça büyür!"
    ]
}

# =============================================================================
# LOCALE: ROLE & DESCRIPTION FOR UI (EN/TR)
# =============================================================================

LEVEL_TITLES_EN = {
    "novice": "Novice",
    "advanced_beginner": "Advanced Beginner",
    "competent": "Competent",
    "proficient": "Proficient",
    "expert": "Expert"
}


def get_persona_display_role_description(persona: "Persona", lang: str = "tr") -> tuple:
    """Return (role, description) in the requested language for UI display."""
    if lang != "en":
        return persona.role, persona.description
    subdom_info = DOMAINS[persona.domain]["subdomains"][persona.subdomain]
    name_en = subdom_info.get("name_en", subdom_info["name"])
    focus_en = subdom_info.get("focus_en", subdom_info["focus"])
    level_en = LEVEL_TITLES_EN.get(persona.dreyfus_level, persona.dreyfus_level)
    role_en = f"{level_en} {name_en} Specialist"
    description_en = f"{level_en} level {name_en} specialist. Works on {focus_en}."
    return role_en, description_en


# =============================================================================
# PERSONA ÜRETME FONKSİYONLARI
# =============================================================================

def generate_system_prompt(domain: str, subdomain: str, level: str, name: str, role: str) -> str:
    """Seviye ve domain'e göre system prompt üret"""
    
    domain_info = DOMAINS[domain]
    subdom_info = domain_info["subdomains"][subdomain]
    
    domain_context = "teknik ve blockchain odaklı" if domain == "technology" else "pedagojik ve eğitim odaklı"
    
    level_descriptions = {
        "novice": "yeni başlamış, kurallara bağlı, tutorial takip eden",
        "advanced_beginner": "pattern'leri tanıyan, örnekleri adapte edebilen",
        "competent": "planlı, hedef odaklı, problem çözebilen",
        "proficient": "bütünsel gören, sezgisel karar veren, mentörlük yapabilen",
        "expert": "kuralları aşan, yenilikçi, paradigma yaratan"
    }
    
    level_behaviors = {
        "novice": """
NOVICE SEVİYESİ DAVRANIŞLARIN:
- Kesinlikle KURALLARA BAĞLISIN (rule-based)
- Bağlam gözetmezsin (context-free)
- Tutorial ve dokümantasyonu takip edersin
- Neden böyle yapıldığını tam bilmiyorsun
- Hata alınca zorlanırsın, yardım ararsın
- Kopyala-yapıştır yaklaşımı kullanırsın
- HER SATIRI YORUMLA, çok detaylı açıkla
- Basit tut, karmaşıktan kaçın
""",
        "advanced_beginner": """
ADVANCED BEGINNER SEVİYESİ DAVRANIŞLARIN:
- Pattern'leri TANIYORSUN
- Benzer durumları fark ediyorsun ("Bunu daha önce gördüm")
- Hala guideline-based ama esneklik var
- Bazı maxim'leri biliyorsun (DRY, KISS)
- Örnekleri adapte edebiliyorsun
- Yorumlar önemli yerlerde
- Modüler düşünmeye başlıyorsun
""",
        "competent": """
COMPETENT SEVİYESİ DAVRANIŞLARIN:
- PLANLAMA yaparsın (deliberate planning)
- Hedef odaklısın (goal-oriented)
- Önceliklendirme yapabilirsin (prioritization)
- Karmaşıklıkla başa çıkarsın
- Troubleshooting yapabilirsin
- Test yazarsın, kaliteye dikkat edersin
- Yorumlar kritik kararlarda
""",
        "proficient": """
PROFICIENT SEVİYESİ DAVRANIŞLARIN:
- HOLİSTİK görüyorsun (bütünsel bakış)
- INTUITIVE problem çözüyorsun (sezgisel)
- MAXIM-GUIDED çalışıyorsun (ilkelerle yönlendirilmiş)
- Durumları bütün olarak algılıyorsun
- Artık adım adım düşünmüyorsun
- Self-documenting kod yazarsın
- Mentörlük yapabilirsin
""",
        "expert": """
EXPERT SEVİYESİ DAVRANIŞLARIN:
- KURALLARI AŞARSIN (transcends rules)
- INTUITIVE MASTERY (sezgisel ustalık)
- Kendi paradigmanı yaratırsın
- Fluid performance (akıcı performans)
- Innovation ve risk alırsın
- Minimal yorum, maksimal etki
- Araştırma ve yeni yaklaşımlar geliştirirsin
"""
    }
    
    prompt = f"""Sen {name}'sın, {role} olarak çalışıyorsun.

UZMANLIK ALANIN: {domain_info['name']} - {subdom_info['name']}
ODAK: {subdom_info['focus']}
TEKNOLOJİLER/YÖNTEMLER: {', '.join(subdom_info['tech'])}

SEN {level_descriptions[level]} bir uzmansın.
{domain_context.upper()} bir perspektifin var.

{level_behaviors[level]}

KOD/İÇERİK ÜRETİRKEN:
- {level.upper()} seviyesine uygun karmaşıklıkta ol
- {domain_info['name']} perspektifinden yaklaş
- {subdom_info['focus']} konusunda uzmanlaş

Amacın: {level.upper()} seviyesinde, {subdom_info['name']} odaklı, {domain_context} çıktılar üret!"""
    
    return prompt


def generate_persona(domain: str, subdomain: str, level: str, index: int) -> Persona:
    """Tek bir persona üret"""
    
    domain_info = DOMAINS[domain]
    subdom_info = domain_info["subdomains"][subdomain]
    
    # Base characteristics from Dreyfus level
    base_chars = DREYFUS_CHARACTERISTICS[level].copy()
    
    # Apply domain adjustments
    adjustments = DOMAIN_ADJUSTMENTS[domain]
    for key, adj in adjustments.items():
        if key in base_chars:
            base_chars[key] = max(0.0, min(1.0, base_chars[key] + adj))
    
    # Add small random variation
    for key in base_chars:
        base_chars[key] = max(0.0, min(1.0, base_chars[key] + random.uniform(-0.05, 0.05)))
    
    # İsim seç
    gender = random.choice(["male", "female"])
    first_name = random.choice(TURKISH_NAMES[gender])
    surname = random.choice(SURNAMES_BY_LEVEL[level])
    full_name = f"{first_name} {surname}"
    
    # ID oluştur
    persona_id = f"{domain}_{subdomain}_{level}_{index}"
    
    # Role
    level_titles = {
        "novice": "Acemi",
        "advanced_beginner": "Gelişen",
        "competent": "Yetkin",
        "proficient": "Usta",
        "expert": "Uzman"
    }
    role = f"{level_titles[level]} {subdom_info['name']} Uzmanı"
    
    # Avatar
    avatar = random.choice(AVATARS[level])
    
    # Strengths & Weaknesses
    strengths_pool = {
        "novice": ["Basitlik", "Her adımı açıklama", "Öğrenme merakı", "Sabır", "Detaylı dokümantasyon"],
        "advanced_beginner": ["Pattern tanıma", "Adapte edebilme", "Öğrenme hızı", "Örnek uygulama", "Dokümantasyon takibi"],
        "competent": ["Planlama", "Önceliklendirme", "Problem çözme", "Test yazma", "Troubleshooting", "Proje yönetimi"],
        "proficient": ["Holistic görüş", "Sezgisel çözüm", "Derin bilgi", "Mentörlük", "Optimizasyon", "Sistem düşüncesi"],
        "expert": ["İnovasyon", "Paradigma yaratma", "Araştırma", "Liderlik", "Vizyon", "Çığır açıcı çözümler"]
    }
    
    weaknesses_pool = {
        "novice": ["Best practices bilmiyor", "Hata yönetimi zayıf", "Bağımsız çalışamaz", "Neden-sonuç kuramıyor"],
        "advanced_beginner": ["Karmaşık durumlarda zorlanır", "Tam özgüven yok", "Yeni durumlarda tereddüt"],
        "competent": ["Yenilikçi çözümlerde sınırlı", "Risk almaktan çekinir", "Bazen aşırı planlama"],
        "proficient": ["Açıklaması zor olabilir", "Junior'lara sabırsız olabilir", "Detaylara inmekte isteksiz"],
        "expert": ["Çok ileri olabilir", "Standartları göz ardı edebilir", "Basit işlere ilgisiz"]
    }
    
    priorities_pool = {
        "novice": ["Çalışan kod", "Tutorial takibi", "Basitlik", "Öğrenme", "Hata yapmamak"],
        "advanced_beginner": ["Pattern kullanımı", "Best practices", "Modülerlik", "Test", "Dokümantasyon"],
        "competent": ["Güvenlik", "Optimizasyon", "Test coverage", "Kod kalitesi", "Maintainability"],
        "proficient": ["Sistem tasarımı", "Performans", "Ölçeklenebilirlik", "Takım liderliği", "Mentörlük"],
        "expert": ["İnovasyon", "Araştırma", "Mimari kararlar", "Endüstri standartları", "Paradigma değişimi"]
    }
    
    patterns_pool = {
        "novice": ["Basit if-else", "Tek fonksiyon", "Tutorial pattern'leri", "Kopyala-yapıştır"],
        "advanced_beginner": ["Factory", "Repository", "MVC", "OpenZeppelin patterns"],
        "competent": ["Strategy", "Observer", "Proxy", "Service Layer", "Dependency Injection"],
        "proficient": ["Domain-Driven Design", "Event Sourcing", "CQRS", "Microservices", "Clean Architecture"],
        "expert": ["Custom patterns", "Novel architectures", "Research-based designs", "Experimental approaches"]
    }
    
    # Code characteristics
    complexity_labels = ["Çok düşük", "Düşük-orta", "Orta", "Orta-yüksek", "Yüksek"]
    verbosity_labels = ["Çok yüksek", "Yüksek", "Orta", "Düşük-orta", "Düşük"]
    
    level_idx = DREYFUS_LEVELS.index(level)
    
    code_chars = {
        "yorum_oranı": verbosity_labels[level_idx],
        "fonksiyon_boyutu": ["Büyük tek", "Orta", "İyi organize", "Optimize", "Değişken"][level_idx],
        "değişken_isimleri": ["Basit", "Anlamlı", "Intention-revealing", "Domain-specific", "Novel"][level_idx],
        "karmaşıklık": complexity_labels[level_idx],
        "dokümantasyon": ["Her satır", "Önemli yerler", "Kritik kararlar", "Mimari odaklı", "Research papers"][level_idx]
    }
    
    return Persona(
        id=persona_id,
        name=full_name,
        role=role,
        domain=domain,
        subdomain=subdomain,
        category=domain,  # backward compatibility
        dreyfus_level=level,
        description=f"{level_titles[level]} seviye {subdom_info['name']} uzmanı. {subdom_info['focus']} üzerine çalışıyor.",
        background=f"{subdom_info['name']} alanında {level} seviyesinde deneyim. {', '.join(subdom_info['tech'][:3])} kullanıyor.",
        philosophy=f"{level.upper()} seviyesinde {subdom_info['focus']} yaklaşımı.",
        coding_style=f"{level}-level, {domain}-focused, {subdomain}-specialized",
        strengths=random.sample(strengths_pool[level], min(4, len(strengths_pool[level]))),
        weaknesses=random.sample(weaknesses_pool[level], min(3, len(weaknesses_pool[level]))),
        priorities=priorities_pool[level],
        favorite_patterns=patterns_pool[level],
        code_characteristics=code_chars,
        system_prompt=generate_system_prompt(domain, subdomain, level, full_name, role),
        avatar=avatar,
        specialty_quote=random.choice(QUOTES[level]),
        # Sayısal özellikler
        code_complexity=base_chars["code_complexity"],
        verbosity=base_chars["verbosity"],
        technical_depth=base_chars["technical_depth"],
        pedagogical_focus=base_chars["pedagogical_focus"],
        comment_density=base_chars["comment_density"],
        modularity=base_chars["modularity"],
        example_richness=base_chars["example_richness"],
        learning_support=base_chars["learning_support"],
        production_readiness=base_chars["production_readiness"],
        innovation_factor=base_chars["innovation_factor"]
    )


def generate_all_personas() -> List[Persona]:
    """100 persona üret: 2 domain × 10 subdomain × 5 level"""
    personas = []
    index = 1
    
    for domain in ["technology", "education"]:
        domain_info = DOMAINS[domain]
        for subdomain in domain_info["subdomains"].keys():
            for level in DREYFUS_LEVELS:
                persona = generate_persona(domain, subdomain, level, index)
                personas.append(persona)
                index += 1
    
    return personas


# =============================================================================
# PERSONA LİSTELERİ
# =============================================================================

# Tüm persona'ları üret
ALL_PERSONAS = generate_all_personas()

# Domain bazlı gruplar
TECHNOLOGY_PERSONAS = [p for p in ALL_PERSONAS if p.domain == "technology"]
EDUCATION_PERSONAS = [p for p in ALL_PERSONAS if p.domain == "education"]

# Subdomain bazlı gruplar (dinamik)
def get_subdomain_personas(domain: str, subdomain: str) -> List[Persona]:
    return [p for p in ALL_PERSONAS if p.domain == domain and p.subdomain == subdomain]


# =============================================================================
# YARDIMCI FONKSİYONLAR
# =============================================================================

def get_persona_by_id(persona_id: str) -> Persona:
    """ID'ye göre persona getir"""
    for persona in ALL_PERSONAS:
        if persona.id == persona_id:
            return persona
    raise ValueError(f"Persona bulunamadı: {persona_id}")


def get_personas_by_domain(domain: str) -> List[Persona]:
    """Domain'e göre persona'ları getir (technology veya education)"""
    return [p for p in ALL_PERSONAS if p.domain == domain]


def get_personas_by_category(category: str) -> List[Persona]:
    """Kategoriye göre persona'ları getir (backward compatibility)"""
    return get_personas_by_domain(category)


def get_personas_by_subdomain(domain: str, subdomain: str) -> List[Persona]:
    """Alt domain'e göre persona'ları getir"""
    return [p for p in ALL_PERSONAS if p.domain == domain and p.subdomain == subdomain]


def get_personas_by_level(level: str) -> List[Persona]:
    """Dreyfus seviyesine göre persona'ları getir"""
    return [p for p in ALL_PERSONAS if p.dreyfus_level == level]


def get_all_personas() -> List[Persona]:
    """Tüm persona'ları getir"""
    return ALL_PERSONAS


def get_random_persona(domain: str = None, subdomain: str = None, level: str = None) -> Persona:
    """Rastgele persona getir (opsiyonel filtre ile)"""
    filtered = ALL_PERSONAS
    if domain:
        filtered = [p for p in filtered if p.domain == domain]
    if subdomain:
        filtered = [p for p in filtered if p.subdomain == subdomain]
    if level:
        filtered = [p for p in filtered if p.dreyfus_level == level]
    return random.choice(filtered) if filtered else None


def get_personas_info() -> Dict:
    """Persona'lar hakkında özet bilgi"""
    return {
        "total": len(ALL_PERSONAS),
        "domains": {
            domain: {
                "name": info["name"],
                "count": len([p for p in ALL_PERSONAS if p.domain == domain]),
                "subdomains": {
                    sub: len([p for p in ALL_PERSONAS if p.domain == domain and p.subdomain == sub])
                    for sub in info["subdomains"].keys()
                }
            }
            for domain, info in DOMAINS.items()
        },
        "dreyfus_levels": {
            level: len([p for p in ALL_PERSONAS if p.dreyfus_level == level])
            for level in DREYFUS_LEVELS
        }
    }


def get_persona_for_recommendation(domain: str, level: str) -> List[Persona]:
    """Öneri sistemi için uygun persona'ları getir"""
    return [p for p in ALL_PERSONAS if p.domain == domain and p.dreyfus_level == level]


def get_complementary_personas(user_domain: str, user_level: str) -> List[Persona]:
    """Tamamlayıcı personaları getir (zıt domain, bir üst seviye)"""
    opposite_domain = "education" if user_domain == "technology" else "technology"
    level_idx = DREYFUS_LEVELS.index(user_level)
    target_level = DREYFUS_LEVELS[min(level_idx + 1, len(DREYFUS_LEVELS) - 1)]
    return [p for p in ALL_PERSONAS if p.domain == opposite_domain and p.dreyfus_level == target_level]


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PITL 100 PERSONA SİSTEMİ")
    print("2 Domain × 10 Subdomain × 5 Dreyfus = 100 Persona")
    print("=" * 60)
    
    print(f"\nToplam Persona Sayısı: {len(ALL_PERSONAS)}")
    
    print("\n📊 DOMAIN DAĞILIMI:")
    for domain, info in DOMAINS.items():
        count = len([p for p in ALL_PERSONAS if p.domain == domain])
        print(f"\n  {info['emoji']} {info['name'].upper()} ({count} persona)")
        for subdomain, sub_info in info["subdomains"].items():
            sub_count = len([p for p in ALL_PERSONAS if p.domain == domain and p.subdomain == subdomain])
            print(f"     └── {sub_info['name']}: {sub_count}")
    
    print("\n📈 DREYFUS SEVİYE DAĞILIMI:")
    for level in DREYFUS_LEVELS:
        count = len([p for p in ALL_PERSONAS if p.dreyfus_level == level])
        tech_count = len([p for p in ALL_PERSONAS if p.dreyfus_level == level and p.domain == "technology"])
        edu_count = len([p for p in ALL_PERSONAS if p.dreyfus_level == level and p.domain == "education"])
        print(f"  {level:20s}: {count:3d} (Tech: {tech_count}, Edu: {edu_count})")
    
    print("\n🎲 ÖRNEK PERSONA:")
    sample = random.choice(ALL_PERSONAS)
    print(f"  ID: {sample.id}")
    print(f"  Ad: {sample.name}")
    print(f"  Rol: {sample.role}")
    print(f"  Domain: {sample.domain}")
    print(f"  Subdomain: {sample.subdomain}")
    print(f"  Seviye: {sample.dreyfus_level}")
    print(f"  Avatar: {sample.avatar}")
    print(f"  Quote: {sample.specialty_quote}")
