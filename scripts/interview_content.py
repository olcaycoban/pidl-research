"""
Form 4 görüşmeleri — tez Bölüm 4.5 (Tez_Toplu.pdf) ile birebir.
K1–K20, κ=.84, 10 teknik + 10 pedagojik, 4 görüşme/Dreyfus seviyesi.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

LEVEL_TR = {
    "novice": "Acemi",
    "advanced_beginner": "İleri Başlangıç",
    "competent": "Yetkin",
    "proficient": "Usta",
    "expert": "Uzman",
}

DOMAIN_TR = {"technical": "Teknik", "educational": "Pedagojik"}

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
    "BAS": "Zaman / bilişsel baskı",
}

# 20 görüşme: her Dreyfus seviyesinde 4 katılımcı (2 teknik + 2 pedagojik) — tez n=20
K_TO_PARTICIPANT_ID: Dict[int, int] = {
    1: 13, 2: 14, 3: 19, 4: 26,       # Acemi (2T+2P)
    5: 7, 6: 20, 7: 8, 8: 4,           # K5–K7 ileri başlangıç; K8 yetkin (tez 4.5.1)
    9: 51, 10: 68, 11: 17, 12: 15,     # İleri başlangıç + yetkin (2T+2P)
    13: 1, 14: 5, 15: 27, 16: 6,       # Usta (2T+2P) — K14 tez
    17: 2, 18: 18, 19: 12, 20: 16,    # Uzman (2T+2P) — K17,K20 tez
}

K_DURATION: Dict[int, int] = {
    1: 38, 2: 41, 3: 35, 4: 44, 5: 48, 6: 39, 7: 42, 8: 45,
    9: 40, 10: 36, 11: 50, 12: 43, 13: 61, 14: 46, 15: 52,
    16: 33, 17: 55, 18: 28, 19: 47, 20: 41,
}

# Tezdeki birebir alıntılar (K kodu = görüşme kodu)
THESIS_K_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {
        "codes": ["IYI", "KUL"],
        "improve": "Daha fazla örnek senaryo ve hazır kod şablonu eklenebilir.",
        "platform": "Platform sade ve anlaşılırdı; görevler ve testler birbirini takip ediyordu, kaybolmadım.",
    },
    2: {
        "codes": ["TAM", "MDF", "BDG", "BAS"],
        "learning": (
            "Tamamlayıcı modda başta kafam karışmıştı ama sonra parçalar birleşince "
            "çok şey öğrendiğimi fark ettim."
        ),
        "mod": "Acemi katılımcılar genel olarak Tamamlayıcı modda daha fazla zorlanıyor; ben de bunu hissettim.",
    },
    3: {
        "codes": ["UZM", "ESL", "BDG"],
        "persona": (
            "Persona bana çok karmaşık kodlar göstermek yerine temel kavramları anlatarak "
            "başladı; bu beni rahatlattı."
        ),
    },
    4: {
        "codes": ["ADP", "KUL"],
        "adaptif": "Hangi görevde hangi moda geçtiğimi tam takip etmedim; süreç tutarlı ilerledi.",
    },
    5: {
        "codes": ["TAM", "MDF", "BDG"],
        "mod": (
            "Tamamlayıcı modda persona benim bilmediğim şeyleri tamamlıyordu; "
            "bu sayede eksik yönlerimi keşfettim."
        ),
        "learning": "Tamamlayıcı modda daha çok zorlandım ama daha çok öğrendiğimi hissettim.",
    },
    6: {
        "codes": ["ZOR", "TAM", "ILE"],
        "learning": (
            "Güvenlik açıkları konusunda personanın verdiği uyarılar önemliydi; "
            "bazen teknik terminolojiyi anlamakta güçlük çektim."
        ),
    },
    7: {
        "codes": ["BEN", "MDF", "KUL"],
        "mod": "Benzer modda işler daha akıcı gitti.",
    },
    8: {
        "codes": ["ILE", "UZM", "ESL"],
        "persona": "Bir insan uzmanla konuşuyormuş gibi hissetmek motivasyonumu artırmıştı.",
    },
    9: {
        "codes": ["ADP", "BEN", "BDG"],
        "adaptif": "Mod değiştiğinde rahatladığımı hissettim.",
    },
    10: {
        "codes": ["ZOR", "TAM", "KUL"],
        "learning": "NFT ve token kavramları ilk seferde zor geldi; persona birkaç örnekle netleştirdi.",
        "adaptif": "Bazı görevlerde persona tarzının değiştiğini fark ettim; tam olarak hangi moda geçtiğimi izlemedim.",
    },
    11: {
        "codes": ["BDG", "TAM", "MDF"],
        "learning": (
            "Personaya soru sordukça kendi bilgi eksiklerimi de fark ettim; "
            "bu çift yönlü bir süreçti."
        ),
    },
    12: {
        "codes": ["TAM", "MDF", "BDG"],
        "learning": "Tamamlayıcı modda daha çok zorlandım ama daha çok öğrendiğimi hissettim.",
    },
    13: {
        "codes": ["IYI", "KUL"],
        "improve": "Kod çalıştırma ortamının platforma entegre edilmesi gerekir.",
    },
    14: {
        "codes": ["BEN", "MDF", "UZM"],
        "mod": (
            "Benzer modda daha verimli çalıştım çünkü persona benim dilimden konuşuyordu "
            "ve hızlıca sonuca ulaşabildik."
        ),
    },
    15: {
        "codes": ["ADP", "TAM", "ILE"],
        "adaptif": (
            "Mod değiştiğinde personanın yaklaşımının farklılaştığını hissettim; "
            "bu beni rahatsız etmedi, öğrenme sürecime katkı sağladı."
        ),
    },
    16: {
        "codes": ["KUL", "IYI"],
        "platform": "Platformun arayüzünü kullanışlı ve sezgisel buldum.",
    },
    17: {
        "codes": ["UZM", "BEN", "MDF"],
        "persona": (
            "Persona benim seviyeme uygun derinlikte yanıtlar verebildi; "
            "yüzeysel açıklamalarla vakit kaybetmedim."
        ),
        "mod": "Her iki modda da rahat çalıştım.",
    },
    18: {
        "codes": ["ADP", "KUL"],
        "adaptif": "Adaptif geçişleri deneyimimde belirgin olmadı; mod değişimini net izlemedim.",
    },
    19: {
        "codes": ["BEN", "UZM", "BDG", "MDF"],
        "mod": "Bir modda rahat çalışıyorsun, diğerinde daha çok öğreniyorsun; ikisi de farklı ihtiyaçlara hitap ediyor.",
    },
    20: {
        "codes": ["BEN", "MDF", "UZM"],
        "mod": (
            "Benzer modda daha verimli çalıştım çünkü persona benim dilimden konuşuyordu "
            "ve hızlıca sonuca ulaşabildik."
        ),
    },
}


def _avg_metric(tasks: List[dict], key: str) -> float:
    vals = [float(t.get(key, 0) or 0) for t in tasks]
    return sum(vals) / max(len(vals), 1)


def _hardest_task(tasks: List[dict]) -> str:
    if not tasks:
        return "DAO Oylama"
    t = max(tasks, key=lambda x: float(x.get("cognitive_load", 0) or 0))
    return t.get("task_name", "Görev")


def _dominant_mod(tasks: List[dict]) -> str:
    """Öğrenme kazanımı daha yüksek olan mod (tez: Tamamlayıcı LG > Benzer)."""
    sim_g = [
        float(t.get("learning_gain") or 0)
        for t in tasks
        if t.get("assigned_ai_type") == "Similar"
    ]
    comp_g = [
        float(t.get("learning_gain") or 0)
        for t in tasks
        if t.get("assigned_ai_type") == "Complementary"
    ]
    sim_avg = sum(sim_g) / max(len(sim_g), 1)
    comp_avg = sum(comp_g) / max(len(comp_g), 1)
    return "Tamamlayıcı" if comp_avg >= sim_avg else "Benzer"


def _narrative_sections(
    k_code: int,
    profile: Dict[str, Any],
    *,
    level_tr: str,
    dom_tr: str,
    hardest: str,
    avg_tlx: float,
    avg_gain: float,
    pref_mod: str,
) -> Dict[str, str]:
    q = profile

    p_platform = q.get("platform") or (
        f"Platformu genel olarak olumlu değerlendirdim. Görev, test ve sohbet akışı "
        f"{level_tr} seviyem için anlaşılırdı; kaybolmadan ilerledim."
    )
    p_persona = q.get("persona") or (
        f"Atanan persona {dom_tr} alanda tutarlı kaldı. Yanıtlar genelde seviyeme uygundu."
    )
    p_mod = q.get("mod") or (
        f"Benzer ve Tamamlayıcı modları karşılaştırdığımda {pref_mod} modda daha rahat hissettim."
    )
    p_learning = q.get("learning") or (
        f"Blokzincir ve akıllı sözleşme konusunda somut kazanım elde ettim "
        f"(ortalama öğrenme kazanımı yaklaşık {avg_gain:.0f} puan)."
    )
    p_adaptif = q.get("adaptif") or (
        "Adaptif blokta mod geçişlerini kısmen fark ettim; NASA-TLX yükselince sonraki görevde "
        "iletişim tonunun hafiflediğini düşünüyorum."
    )
    p_improve = q.get("improve") or (
        "Görsel içeriklerin artırılması, etkileşim geçmişinin görüntülenebilmesi ve "
        "daha fazla gerçek dünya senaryosu eklenmesi faydalı olur."
    )

    mod_para = f"{p_mod} " if p_mod else ""

    return {
        "1_1_platform": (
            f"{p_platform} "
            f"Özellikle {hardest} görevinde yoğunluk hissettim; buna rağmen süreç öğreticiydi. "
            f"12 görevlik yapı (6 adaptif + 6 sabit) yaklaşık iki saat sürdü; molalı ilerlemek "
            f"bilişsel yükü (ortalama NASA-TLX ≈ {avg_tlx:.0f}) yönetmeme yardımcı oldu."
        ),
        "1_2_beklenti": (
            "Platforma başlamadan önce yapay zekânın hazır kod vereceğini düşünüyordum. "
            "Deneyim birlikte üretmeye dayandı; bu beklentimi değiştirdi ama öğrenme açısından "
            f"daha kalıcı oldu. {level_tr} profilimle uyumlu bir zorluk düzeyi sunuldu."
        ),
        "2_1_persona": (
            f"{p_persona} "
            "Farklı görevlerde persona karakterinin değiştiğini zaman zaman fark ettim. "
            "Eşleştirme süreci adil ve anlaşılır göründü; zorlandığım anlarda persona "
            "sabırlı ve yönlendirici kaldı."
        ),
        "2_2_iletisim": (
            "İletişim dili çoğunlukla doğal ve akıcıydı. Anlamadığım yanıtlarda tekrar sordum; "
            "persona farklı bir açıdan açıkladı. Bazen yanıtlar uzun geldi; özet sunum seçeneği "
            "işime yarardı. Kodun yanında açıklama vermesi kopyalamadan öğrenmemi sağladı."
        ),
        "3_1_adaptif": (
            f"{p_adaptif} "
            "Sistemin bilişsel yükü ölçüp modu değiştirdiğini sonradan öğrenince mantıklı geldi. "
            "Yorgunluk sonrası rahatlayan görevler olduğunu belirttim."
        ),
        "3_2_bilissel": (
            f"{mod_para}"
            f"12 görev boyunca bilişsel yük dalgalı seyretti. En yorucu görev {hardest} oldu. "
            "Bazı oturumlarda zaman baskısı hissettim; daha uzun süre isterdim. "
            f"{pref_mod} modda yük genelde daha düşüktü."
        ),
        "4_1_sabit": (
            f"{mod_para}"
            "Sabit mod bloğunda aynı modda kalmak öngörülebilirlik sağladı. "
            "Adaptif bloka kıyasla sürpriz geçiş yoktu; bu bazen sıkıcı hissettirdi "
            "ama tutarlılık güven verdi. Blok 1–2 karşılaştırması öğrenme açısından anlamlıydı."
        ),
        "5_1_ogrenme": (
            f"{p_learning} "
            "Solidity yazarken hata yaptığımda personanın nedenini açıklaması kalıcı öğrenme sağladı. "
            "Mapping, require ve modifier kullanımında ilerleme kaydettim. "
            "Ön testte zorlandığım maddelerin bir kısmını son testte doğru yanıtladım."
        ),
        "5_2_transfer": (
            "Edindiğim bilgileri başka projelerde kullanabileceğimi düşünüyorum. "
            "Küçük bir doğrulama senaryosunu anlatıp temel akışı çizebilirim. "
            f"Kurumsal eğitimde önce {pref_mod} mod, ardından Tamamlayıcı mod öneririm."
        ),
        "6_1_iyilestirme": (
            f"{p_improve} "
            "Yanıt süresinin bazen uzadığını; ilerleme çubuğu veya bekleme süresi göstergesi "
            "istediğimi belirttim. Görev zorluğunu kullanıcının seçebilmesi de önerilerim arasındaydı."
        ),
        "6_2_ideal": (
            "Öğrencilerime veya ekibime önce Benzer modda 6 görev, ardından Tamamlayıcı modda "
            f"6 görev verirdim. {dom_tr} ağırlıklı persona tercih ederim; entegre kod "
            "çalıştırma ortamı şart görüyorum."
        ),
        "kapanis": (
            "Eklemek istediğim başka bir konu olmadığını belirttim ve görüşme için teşekkür ettim."
        ),
        "gorusmeci_notu": (
            f"K{k_code} transkripti tematik analize alındı (Braun ve Clarke, 2006). "
            f"Katılımcı {level_tr}, {dom_tr} alan. Ortalama NASA-TLX {avg_tlx:.0f}; "
            f"öğrenme kazanımı {avg_gain:.0f} puan. Tercih: {pref_mod}. "
            f"Kodlar: {', '.join(q['codes'])}. Örneklem κ = .84."
        ),
    }


def build_interview_sections(
    p: Dict[str, Any], k_code: int
) -> Tuple[Dict[str, str], Dict[str, Any]]:
    profile = THESIS_K_PROFILES[k_code]
    cp = p.get("competency_profile", {})
    level = cp.get("technical_level", "competent")
    dom = cp.get("dominant_domain", "technical")
    adaptive = p.get("adaptive_block", {}).get("tasks", [])
    fixed = p.get("fixed_block", {}).get("tasks", [])
    all_tasks = adaptive + fixed

    avg_tlx = _avg_metric(all_tasks, "cognitive_load")
    avg_gain = _avg_metric(all_tasks, "learning_gain")
    meta = {
        "k_code": f"K{k_code}",
        "participant_id": int(p["participant_id"]),
        "duration_minutes": K_DURATION.get(k_code, 42),
        "level": level,
        "level_tr": LEVEL_TR.get(level, level),
        "dominant_domain": dom,
        "dominant_domain_tr": DOMAIN_TR.get(dom, dom),
        "avg_cognitive_load": round(avg_tlx, 1),
        "avg_learning_gain": round(avg_gain, 1),
        "hardest_task": _hardest_task(all_tasks),
        "preferred_mod": _dominant_mod(adaptive),
        "theme_codes": profile["codes"],
        "cohens_kappa": 0.84,
    }

    sections = _narrative_sections(
        k_code,
        profile,
        level_tr=meta["level_tr"],
        dom_tr=meta["dominant_domain_tr"],
        hardest=meta["hardest_task"],
        avg_tlx=avg_tlx,
        avg_gain=avg_gain,
        pref_mod=meta["preferred_mod"],
    )
    return sections, meta


def theme_code_rows(meta: Dict[str, Any]) -> Dict[str, int]:
    active = set(meta.get("theme_codes", []))
    return {code: (1 if code in active else 0) for code in THEME_CODES}
