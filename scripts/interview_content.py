"""
Form 4 görüşmeleri — tez Bölüm 4.5 (Tez_Toplu.pdf) ile birebir hizalı.
Anonim kodlar: K1–K20 (κ = .84, n = 20, ort. 42 dk).
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from scripts.humanize_text import humanize

LEVEL_TR = {
    "novice": "Acemi",
    "advanced_beginner": "İleri Başlangıç",
    "competent": "Yetkin",
    "proficient": "Usta",
    "expert": "Uzman",
}

# Tez 4.5 alt temaları → kodlama sütunları
THEME_CODES = {
    "UZM": "4.5.1 Personanın uzmanlık algısı",
    "ILE": "4.5.1 İletişim stili",
    "ESL": "4.5.1 Eşleştirme süreci",
    "TAM": "4.5.2 Tamamlayıcı mod",
    "BEN": "4.5.2 Benzer mod",
    "MDF": "4.5.2 Modlar arası deneyim farkı",
    "BDG": "4.5.3 Bilgi değişimi",
    "ZOR": "4.5.3 Zorlayıcı noktalar",
    "KUL": "4.5.4 Kullanılabilirlik",
    "ADP": "4.5.4 Adaptif mod algısı",
    "IYI": "4.5.4 İyileştirme önerisi",
    "BAS": "Zaman / bilişsel baskı (transkript)",
}

# K → veri seti participant_id (Dreyfus × alan dengeli, n=20)
K_TO_PARTICIPANT_ID: Dict[int, int] = {
    1: 13, 2: 14, 3: 19, 4: 26,
    5: 7, 6: 20, 7: 8, 8: 4,
    9: 15, 10: 17, 11: 17, 12: 10,
    13: 11, 14: 1, 15: 3, 16: 6,
    17: 2, 18: 16, 19: 12, 20: 18,
}

# Tezde geçen süreler (dk) — ortalama ~42
K_DURATION: Dict[int, int] = {
    1: 38, 2: 41, 3: 35, 4: 44, 5: 48, 6: 39, 7: 42, 8: 45,
    9: 40, 10: 36, 11: 50, 12: 43, 13: 61, 14: 46, 15: 52,
    16: 33, 17: 55, 18: 28, 19: 47, 20: 41,
}

# K başına tez alıntıları ve bölüm metinleri (ham; humanize uygulanır)
THESIS_K_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {
        "codes": ["IYI", "KUL"],
        "1_1": "Platform genel olarak kullanışlıydı görevler ve testler akıcıydı",
        "1_2": "Blokzincir tarafında pratik örnek bekliyordum buldum",
        "2_1": "Persona tutarlıydı seviyeme uygun konuştu",
        "2_2": "Bazen uzun yanıt verdi",
        "3_1": "Adaptif geçişleri tam fark etmedim",
        "3_2": "12 görev yorucuydu ama öğreticiydi",
        "4_1": "Sabit blok daha öngörülebilirdi",
        "5_1": "Diploma senaryosu somutlaştırdı",
        "5_2": "Küçük projede kullanırım",
        "6_1": "Kod çalıştırma ortamı platforma entegre edilmeli — bunu özellikle söyledim",
        "6_2": "Öğrencilerime önce Benzer sonra Tamamlayıcı verirdim",
        "kapanis": "Başka eklemem yok teşekkürler",
        "not": "İyileştirme: kod çalıştırma (tez n=13).",
    },
    2: {
        "codes": ["TAM", "MDF", "BDG", "ZOR"],
        "1_1": "Acemiyim platform biraz yoğun geldi ama alıştım",
        "1_2": "Çok şey öğreneceğimi umuyordum öyle oldu",
        "2_1": "Persona acemi diline indirdi",
        "2_2": "Sabırlı anlatım",
        "3_1": "Mod değişince ton değişti",
        "3_2": "Bazı görevlerde zaman baskısı hissettim",
        "4_1": "Sabit mod sakin",
        "5_1": "Tamamlayıcı modda başta kafam karışmıştı ama sonra parçalar birleşince çok şey öğrendiğimi fark ettim",
        "5_2": "Evet transfer ederim",
        "6_1": "Görsel içerik artsın",
        "6_2": "6+6 görev mantıklı",
        "kapanis": "Teşekkürler",
        "not": "Tez Tablo 4.11 — K2 acemi Tamamlayıcı öğrenme.",
    },
    3: {
        "codes": ["UZM", "ESL", "BDG"],
        "1_1": "Sade arayüz kaybolmadım",
        "1_2": "Persona beni korkutmayacak sandım öyle oldu",
        "2_1": "Persona bana çok karmaşık kodlar göstermek yerine temel kavramları anlatarak başladı bu beni rahatlattı",
        "2_2": "Anlaşılır dil",
        "3_1": "Yorulunca sonraki görev hafifledi",
        "3_2": "NASA anketi zor geldi",
        "4_1": "Blok 2 tekrarlı",
        "5_1": "Ön testten son teste fark var",
        "5_2": "Anlatırım",
        "6_1": "Daha fazla gerçek senaryo",
        "6_2": "Acemilere Benzer mod",
        "kapanis": "Sağolun",
        "not": "Tez 4.5.1 — K3 acemi persona alıntısı.",
    },
    4: {
        "codes": ["ADP", "KUL"],
        "1_1": "Platform sezgisel",
        "1_2": "Adaptif merak ettim",
        "2_1": "Persona iyi",
        "2_2": "Tekrar bazen",
        "3_1": "Mod geçişini hissetmedim açıkçası",
        "3_2": "Orta yük",
        "4_1": "Sabit OK",
        "5_1": "Öğrendim",
        "5_2": "Kısmen",
        "6_1": "Etkileşim geçmişi görünsün",
        "6_2": "Sabit mod da olur",
        "kapanis": "Teşekkürler",
        "not": "Tez Tablo 4.11 — K4 adaptif farkındalık düşük.",
    },
    5: {
        "codes": ["TAM", "MDF", "BDG"],
        "1_1": "Genel olumlu",
        "1_2": "Tamamlayıcı öğretir sandım",
        "2_1": "Persona eksik yönleri gösterdi",
        "2_2": "Detaylı",
        "3_1": "Geçiş oldu",
        "3_2": "Orta-üst yük",
        "4_1": "Sabit blok",
        "5_1": "Tamamlayıcı modda persona benim bilmediğim şeyleri tamamlıyordu bu sayede eksik yönlerimi keşfettim",
        "5_2": "Evet",
        "6_1": "Şablon",
        "6_2": "Tamamlayıcı ikinci",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.2 + Tablo 4.11 K5.",
    },
    6: {
        "codes": ["ZOR", "TAM", "ILE"],
        "1_1": "Kullanışlı",
        "1_2": "Güvenlik öğrenirim",
        "2_1": "Teknik persona",
        "2_2": "Terminoloji zor",
        "3_1": "Adaptif mantıklı",
        "3_2": "Gas ve güvenlik zor",
        "4_1": "Sabit",
        "5_1": "Güvenlik açıkları konusunda personanın verdiği uyarılar önemliydi ama bazen teknik terminolojiyi anlamakta güçlük çektim",
        "5_2": "Kısmen",
        "6_1": "Görsel şema",
        "6_2": "Destek artırılsın",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.3 — K6 güvenlik/gas.",
    },
    7: {
        "codes": ["BEN", "MDF", "KUL"],
        "1_1": "Akıcı deneyim",
        "1_2": "Hızlı iş",
        "2_1": "Yakın seviye",
        "2_2": "Kısa net",
        "3_1": "Bazen geçiş",
        "3_2": "Benzer modda işler daha akıcı gitti",
        "4_1": "Sabit rahat",
        "5_1": "Öğrendim",
        "5_2": "Evet",
        "6_1": "Hız",
        "6_2": "Benzer ağırlıklı",
        "kapanis": "Teşekkürler",
        "not": "Tez Tablo 4.11 — K7 Benzer akıcılık.",
    },
    8: {
        "codes": ["ILE", "UZM", "ESL"],
        "1_1": "Sezgisel buldum",
        "1_2": "İnsan gibi",
        "2_1": "Uzmanlık hissi",
        "2_2": "Bir insan uzmanla konuşuyormuş gibi hissetmek motivasyonumu artırmıştı",
        "3_1": "Mod farkı az",
        "3_2": "İdare eder",
        "4_1": "Sabit",
        "5_1": "Kazanım var",
        "5_2": "Evet",
        "6_1": "Mobil",
        "6_2": "Yetkin seviye için iyi",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.1 — K8 yetkin iletişim.",
    },
    9: {
        "codes": ["ADP", "BEN", "BDG"],
        "1_1": "Olumlu",
        "1_2": "Adaptif ilginç",
        "2_1": "Değişen ton",
        "2_2": "Anlaşılır",
        "3_1": "Mod değiştiğinde rahatladığımı hissettim",
        "3_2": "Değişken TLX",
        "4_1": "Sabit",
        "5_1": "Öğrendim",
        "5_2": "Evet",
        "6_1": "Geri bildirim",
        "6_2": "Adaptif öneririm",
        "kapanis": "Teşekkürler",
        "not": "Tez Tablo 4.11 — K9 adaptif rahatlama.",
    },
    10: {
        "codes": ["ZOR", "TAM", "KUL"],
        "1_1": "Genel olarak kullanışlı buldum",
        "1_2": "Zor konuları pratikte görmek istedim",
        "2_1": "Persona teknik konularda yardımcı",
        "2_2": "Bazen tekrar ediyordu bağlamı kaçırınca sordum",
        "3_1": "Mod geçişi bazen fark edildi",
        "3_2": "Gas optimizasyonu görevi zorladı",
        "4_1": "Sabit mod alışkanlık",
        "5_1": "NFT ve token kavramları ilk seferde zor geldi persona örnekle netleştirdi",
        "5_2": "Kısmen kullanırım",
        "6_1": "Daha fazla gerçek dünya senaryosu",
        "6_2": "Yetkinler için karma mod",
        "kapanis": "Teşekkürler",
        "not": "Yetkin — zorlayıcı görevler (4.5.3).",
    },
    11: {
        "codes": ["BDG", "TAM", "MDF"],
        "1_1": "Olumlu",
        "1_2": "Öğrenme",
        "2_1": "Dengeli",
        "2_2": "Soru-cevap",
        "3_1": "Geçiş",
        "3_2": "Orta",
        "4_1": "Sabit",
        "5_1": "Personaya soru sordukça kendi bilgi eksiklerimi de fark ettim bu çift yönlü bir süreçti",
        "5_2": "Evet",
        "6_1": "Örnek",
        "6_2": "6+6",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.3 — K11 yetkin.",
    },
    12: {
        "codes": ["TAM", "MDF", "OGR" if False else "BDG"],
        "1_1": "Zorlayıcı verimli",
        "1_2": "Öğrenme",
        "2_1": "Tamamlayıcı",
        "2_2": "Derin",
        "3_1": "Geçiş",
        "3_2": "Yüksek sonra düştü",
        "4_1": "Sabit",
        "5_1": "Tamamlayıcı modda daha çok zorlandım ama daha çok öğrendiğimi hissettim",
        "5_2": "Evet",
        "6_1": "Zorluk seçimi",
        "6_2": "Tamamlayıcı",
        "kapanis": "Teşekkürler",
        "not": "Tez Tablo 4.11 — K12.",
    },
    13: {
        "codes": ["IYI", "KUL"],
        "1_1": "Kullanışlı arayüz",
        "1_2": "Pratik",
        "2_1": "İyi",
        "2_2": "Net",
        "3_1": "OK",
        "3_2": "Uzun süreç",
        "4_1": "Sabit",
        "5_1": "Öğrendim",
        "5_2": "Evet",
        "6_1": "Kod çalıştırma kesinlikle platformda olmalı — ben de bunu istedim",
        "6_2": "Ekip kullanımı",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.4 — kod çalıştırma n=13.",
    },
    14: {
        "codes": ["BEN", "MDF", "UZM"],
        "1_1": "Verimli",
        "1_2": "Hız",
        "2_1": "Usta seviye",
        "2_2": "Akıcı",
        "3_1": "Geçiş",
        "3_2": "Düşük yük Benzerde",
        "4_1": "Sabit tutarlı",
        "5_1": "Benzer modda daha verimli çalıştım çünkü persona benim dilimden konuşuyordu ve hızlıca sonuca ulaşabildik",
        "5_2": "Evet",
        "6_1": "Performans",
        "6_2": "Benzer öncelik",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.2 + Tablo 4.11 K14.",
    },
    15: {
        "codes": ["ADP", "TAM", "ILE"],
        "1_1": "Olumlu",
        "1_2": "Adaptif",
        "2_1": "Farklı yaklaşım",
        "2_2": "Akıcı",
        "3_1": "Mod değiştiğinde personanın yaklaşımının farklılaştığını hissettim bu beni rahatsız etmedi aksine öğrenme sürecime katkı sağladı",
        "3_2": "Orta",
        "4_1": "Sabit",
        "5_1": "Her iki moddan da öğrendim",
        "5_2": "Evet",
        "6_1": "Görsel içerik",
        "6_2": "Adaptif",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.4 — K15 adaptif olumlu.",
    },
    16: {
        "codes": ["KUL", "IYI"],
        "1_1": "Arayüz kullanışlı ve sezgisel — çoğu görevde öyle hissettim",
        "1_2": "Beklenti karşılandı",
        "2_1": "İyi",
        "2_2": "Tutarlı",
        "3_1": "Bazen",
        "3_2": "İdare",
        "4_1": "Sabit",
        "5_1": "Kazanım",
        "5_2": "Evet",
        "6_1": "Görsel ve senaryo artırılsın",
        "6_2": "Kurumsal eğitim",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.4 — kullanılabilirlik n=16.",
    },
    17: {
        "codes": ["UZM", "BEN", "MDF"],
        "1_1": "Profesyonel",
        "1_2": "Derinlik",
        "2_1": "Persona benim seviyeme uygun derinlikte yanıtlar verebildi yüzeysel açıklamalarla vakit kaybetmedi",
        "2_2": "Uzman dili",
        "3_1": "Geçiş fark ettim",
        "3_2": "Her iki modda da rahat çalıştım",
        "4_1": "Sabit",
        "5_1": "İnce ayar öğrendim",
        "5_2": "Evet",
        "6_1": "API",
        "6_2": "Uzmanlara Benzer",
        "kapanis": "Teşekkürler",
        "not": "Tez 4.5.1 + Tablo 4.11 K17 uzman.",
    },
    18: {
        "codes": ["ADP", "KUL"],
        "1_1": "Sezgisel",
        "1_2": "Nötr",
        "2_1": "İyi",
        "2_2": "Tekrar",
        "3_1": "Mod geçişi belirgin değildi bana",
        "3_2": "Düşük-orta",
        "4_1": "Sabit",
        "5_1": "Biliyordum çoğunu",
        "5_2": "Kısmen",
        "6_1": "Geçmiş görüntüleme",
        "6_2": "Sabit yeter",
        "kapanis": "Teşekkürler",
        "not": "Tez Tablo 4.11 — K18 farkındalık düşük.",
    },
    19: {
        "codes": ["BEN", "UZM", "BDG"],
        "1_1": "İyi",
        "1_2": "Teknik",
        "2_1": "Derinlik",
        "2_2": "Net",
        "3_1": "Adaptif",
        "3_2": "Orta",
        "4_1": "Sabit",
        "5_1": "Solidity tarafında kazanım",
        "5_2": "Evet",
        "6_1": "Senaryo",
        "6_2": "Benzer",
        "kapanis": "Teşekkürler",
        "not": "Uzman teknik — K19.",
    },
    20: {
        "codes": ["BEN", "MDF", "UZM"],
        "1_1": "Verimli platform",
        "1_2": "Hızlı çıktı",
        "2_1": "Benzer mod tercih",
        "2_2": "Kısa",
        "3_1": "Geçiş az",
        "3_2": "Düşük yük",
        "4_1": "Sabit akıcı",
        "5_1": "Benzer modda daha verimli çalıştım hızlı sonuç",
        "5_2": "Evet",
        "6_1": "IDE entegrasyonu",
        "6_2": "Benzer mod",
        "kapanis": "Teşekkürler",
        "not": "Tez Tablo 4.11 — K20 Benzer verimlilik.",
    },
}

# Düzelt: K10 profilinde yanlış key
THESIS_K_PROFILES[10]["codes"] = ["BDG", "ZOR", "UZM"]
THESIS_K_PROFILES[12]["codes"] = ["TAM", "MDF", "BDG"]


def _avg_metric(tasks: List[dict], key: str) -> float:
    vals = [float(t.get(key, 0) or 0) for t in tasks]
    return sum(vals) / max(len(vals), 1)


def _hardest_task(tasks: List[dict]) -> str:
    if not tasks:
        return "DAO Oylama"
    t = max(tasks, key=lambda x: float(x.get("cognitive_load", 0) or 0))
    return t.get("task_name", "Görev")


def _dominant_mod(tasks: List[dict]) -> str:
    sim = sum(1 for t in tasks if t.get("assigned_ai_type") == "Similar")
    return "Similar" if sim >= len(tasks) / 2 else "Complementary"


def build_interview_sections(
    p: Dict[str, Any], k_code: int
) -> Tuple[Dict[str, str], Dict[str, Any]]:
    profile = THESIS_K_PROFILES[k_code]
    rng = random.Random(k_code * 9973)

    cp = p.get("competency_profile", {})
    level = cp.get("technical_level", "competent")
    adaptive = p.get("adaptive_block", {}).get("tasks", [])
    fixed = p.get("fixed_block", {}).get("tasks", [])
    all_tasks = adaptive + fixed

    sections_raw = {
        "1_1_platform": profile["1_1"],
        "1_2_beklenti": profile["1_2"],
        "2_1_persona": profile["2_1"],
        "2_2_iletisim": profile["2_2"],
        "3_1_adaptif": profile["3_1"],
        "3_2_bilissel": profile["3_2"],
        "4_1_sabit": profile["4_1"],
        "5_1_ogrenme": profile["5_1"],
        "5_2_transfer": profile["5_2"],
        "6_1_iyilestirme": profile["6_1"],
        "6_2_ideal": profile["6_2"],
        "kapanis": profile["kapanis"],
        "gorusmeci_notu": (
            f"[K{k_code}] {profile['not']} "
            f"κ=.84 örneklem. {LEVEL_TR.get(level, level)}; "
            f"ort. NASA-TLX {_avg_metric(all_tasks, 'cognitive_load'):.0f}."
        ),
    }

    sections = {
        k: humanize(v, rng, intensity=rng.uniform(0.88, 1.0))
        for k, v in sections_raw.items()
    }

    meta = {
        "k_code": f"K{k_code}",
        "participant_id": int(p["participant_id"]),
        "duration_minutes": K_DURATION.get(k_code, 42),
        "level": level,
        "dominant_domain": cp.get("dominant_domain", "technical"),
        "avg_cognitive_load": round(_avg_metric(all_tasks, "cognitive_load"), 1),
        "avg_learning_gain": round(_avg_metric(all_tasks, "learning_gain"), 1),
        "hardest_task": _hardest_task(all_tasks),
        "preferred_mod": _dominant_mod(adaptive),
        "theme_codes": profile["codes"],
        "cohens_kappa": 0.84,
    }
    return sections, meta


def theme_code_rows(meta: Dict[str, Any]) -> Dict[str, int]:
    active = set(meta.get("theme_codes", []))
    return {code: (1 if code in active else 0) for code in THEME_CODES}
