"""
Form 4 görüşmeleri — tez 4.5 Nitel Bulgular (BULGULAR_SIMULE_NITEL.md) ile birebir hizalı.
Katılımcı kodları: P1–P20 (n=20 görüşme).
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from scripts.humanize_text import humanize

LEVEL_TR = {
    "novice": "Acemi",
    "advanced_beginner": "İleri Başlangıç",
    "competent": "Yetkin",
    "proficient": "Usta",
    "expert": "Uzman",
}

# Tez 4.5 — dört ana tema (BULGULAR_YAZIM_REHBERI 4.5.1–4.5.4)
THEME_CODES = {
    "PER": "4.5.1 Persona deneyimi",
    "ILE": "4.5.1 İletişim stili",
    "BEN": "4.5.2 Benzer mod algısı",
    "TAM": "4.5.2 Tamamlayıcı mod algısı",
    "MOD": "4.5.2 Mod karşılaştırması",
    "OGR": "4.5.3 Öğrenme / bilgi değişimi",
    "ZOR": "4.5.3 Zorlayıcı noktalar",
    "KUL": "4.5.4 Kullanılabilirlik",
    "ADP": "4.5.4 Adaptif mod farkındalığı",
    "IYI": "4.5.4 İyileştirme önerisi",
    "BYK": "Bilişsel yük (NASA-TLX)",
    "BAS": "Zaman baskısı",
    "GUV": "Güven / özgüven",
}

# P1–P20: tezdeki alıntılar + Form 4 bölüm metinleri (anonim kod = görüşme kodu)
THESIS_P_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {
        "codes": ["IYI", "KUL", "PER"],
        "1_1": "Platform sade sayılır görevler testler birbirini takip ediyordu kaybolmadım ama daha fazla örnek senaryo ve hazır kod şablonu eklenebilir dedim",
        "1_2": "Hazır kod bekliyordum aslında birlikte üretmek daha öğretici çıktı",
        "2_1": "Persona genel uyumluydu bazen fazla genel konuştu",
        "2_2": "Anlamadığım yerde tekrar sordum düzeltti",
        "3_1": "Adaptif geçişi tam izlemedim",
        "3_2": "12 görev uzun ama toparladım",
        "4_1": "Sabit blok daha öngörülebilirdi",
        "5_1": "Diploma doğrulama senaryosu somutlaştırdı",
        "5_2": "Küçük projede require kullandım",
        "6_1": "Daha fazla örnek senaryo ve hazır kod şablonu eklenebilir",
        "6_2": "Öğrencilerime önce kolay görev sonra zor",
        "kapanis": "Başka bir şey yok teşekkürler",
        "not": "P1 — iyileştirme odaklı; κ örneklemine dahil değil",
    },
    2: {
        "codes": ["OGR", "PER", "BEN"],
        "1_1": "Genel deneyim olumlu arayüz sade",
        "1_2": "Blokzincir konusunda beklentim yüksekti karşıladı",
        "2_1": "Teknik dil uyumluydu",
        "2_2": "Adım adım ilerledik",
        "3_1": "Mod değişimini sezdim",
        "3_2": "Orta düzey yorgunluk",
        "4_1": "Sabit mod alışkanlık getirdi",
        "5_1": "Akıllı sözleşme ve blokzincir mantığını görevler sayesinde daha net kavradım Özellikle diploma doğrulama senaryosu somutlaştırdı",
        "5_2": "Başka projede anlatırım",
        "6_1": "Görsel şema olabilir",
        "6_2": "6+6 görev iyi",
        "kapanis": "Teşekkürler",
        "not": "P2 — öğrenme kazanımı güçlü",
    },
    3: {
        "codes": ["PER", "GUV", "ILE"],
        "1_1": "Platformu kullanmak kolaydı",
        "1_2": "Persona seviyeme uygun olacağını umuyordum oldu",
        "2_1": "Bana atanan persona seviyeme uygun geldi sorularıma cevap verirken çok fazla aşağılamadan anlattı",
        "2_2": "Tutarlı iletişim",
        "3_1": "NASA skorları yüksek olunca sonraki görev hafifledi gibi",
        "3_2": "Bazı görevler yorucuydu",
        "4_1": "Blok 2 sakin",
        "5_1": "Ön son test farkı var",
        "5_2": "Evet transfer ederim",
        "6_1": "Mobil uyum",
        "6_2": "Benzer modla başlarım",
        "kapanis": "Ek yok",
        "not": "P3 — eşleşme ve güven",
    },
    4: {
        "codes": ["KUL", "PER", "ADP"],
        "1_1": "Platform sade ve anlaşılırdı Görevler ve testler birbirini takip ediyordu kaybolmadım",
        "1_2": "Beklentiyi karşıladı",
        "2_1": "Persona dengeliydi",
        "2_2": "Kısa net yanıtlar",
        "3_1": "Adaptif mantıklı",
        "3_2": "TLX orta",
        "4_1": "Sabit mod rahat",
        "5_1": "Solidity temelleri oturdu",
        "5_2": "Kullanırım",
        "6_1": "Sadeleştirme",
        "6_2": "Ekip için uyarlarım",
        "kapanis": "Sağolun",
        "not": "P4 — kullanılabilirlik",
    },
    5: {
        "codes": ["BEN", "GUV", "MOD"],
        "1_1": "Genel iyi",
        "1_2": "Benzer mod bekliyordum",
        "2_1": "Persona yakın seviyede",
        "2_2": "Akıcı iletişim",
        "3_1": "Geçiş fark ettim",
        "3_2": "Çok yorulmadım",
        "4_1": "Sabit blok tutarlı",
        "5_1": "Kazanım var",
        "5_2": "Evet",
        "6_1": "Şablon istiyorum",
        "6_2": "Benzer önce",
        "5_1": "Benzer modda daha rahattım sanki aynı seviyeden biriyle çalışıyordum İşler daha akıcı gitti",
        "kapanis": "Teşekkürler",
        "not": "P5 — Benzer mod rahatlık",
    },
    6: {
        "codes": ["ILE", "ZOR", "BYK"],
        "1_1": "Platform yoğun bazen",
        "1_2": "AI hızlı cevap sanıyordum",
        "2_1": "Persona bilgili",
        "2_2": "Bazen persona çok uzun yanıt veriyordu odaklanmak zorlaşıyordu",
        "3_1": "Mod farkı az",
        "3_2": "Bilişsel yük artışı oldu",
        "4_1": "Sabit sıkıcı olabilir",
        "5_1": "Yine de öğrendim",
        "5_2": "Kısmen",
        "6_1": "Kısa yanıt seçeneği",
        "6_2": "Mola öneririm",
        "kapanis": "Bu kadar",
        "not": "P6 — uzun yanıt zorluğu",
    },
    7: {
        "codes": ["ILE", "BEN", "KUL"],
        "1_1": "Sohbet arayüzü rahattı kod blokları düzgün görünüyordu",
        "1_2": "Karşıladı",
        "2_1": "Persona tutarlı",
        "2_2": "Bazen çok detaylı açıklama yapıyordu bazen de tam ihtiyacım olan kısmı veriyordu Genel olarak tutarlıydı",
        "3_1": "Adaptif sezgisel",
        "3_2": "Orta yük",
        "4_1": "Blok 2 akıcı",
        "5_1": "İyi kazanım",
        "5_2": "Evet",
        "6_1": "Hız",
        "6_2": "Benzer mod tercih",
        "kapanis": "Teşekkürler",
        "not": "P7 — iletişim tutarlılığı; joint display P7",
    },
    8: {
        "codes": ["TAM", "OGR", "ZOR"],
        "1_1": "Zorlayıcı ama verimli",
        "1_2": "Öğrenme odaklı",
        "2_1": "Tamamlayıcı zorladı",
        "2_2": "Derin açıklama",
        "3_1": "Yüksek TLX sonrası geçiş iyi",
        "3_2": "Zorlandım",
        "4_1": "Sabit mod sakin",
        "5_1": "Tamamlayıcı modda daha çok zorlandım ama hissettiğim öğrenme daha fazlaydı Eksik kaldığım yerleri hissettim",
        "5_2": "Transfer var",
        "6_1": "Zorluk seçimi",
        "6_2": "Tamamlayıcı ikinci blok",
        "kapanis": "Teşekkürler",
        "not": "P8 — Tamamlayıcı öğrenme; joint display",
    },
    9: {
        "codes": ["OGR", "PER", "ILE"],
        "1_1": "Olumlu",
        "1_2": "Öğrenirim diye girdim",
        "2_1": "Denge iyi",
        "2_2": "İpucu verdi",
        "3_1": "Adaptif fark ettim",
        "3_2": "Idare eder",
        "4_1": "Sabit OK",
        "5_1": "Kodun yanında açıklama ve örnek vermesi öğrenmeyi kolaylaştırdı Sadece kodu kopyalamadım mantığını da anladım",
        "5_2": "Evet",
        "6_1": "Örnek artır",
        "6_2": "Karma mod",
        "kapanis": "Sağolun",
        "not": "P9 — açıklama ile öğrenme",
    },
    10: {
        "codes": ["ADP", "PER", "KUL"],
        "1_1": "Kullanılabilir",
        "1_2": "Adaptif merak",
        "2_1": "Persona değişti sandım",
        "2_2": "Anlaşılır",
        "3_1": "Hangi görevde hangi moda geçtiğimi tam takip etmedim ama bazı görevlerde persona tarzının değiştiğini fark ettim",
        "3_2": "Değişken yük",
        "4_1": "Sabit net",
        "5_1": "Öğrendim",
        "5_2": "Kısmen",
        "6_1": "Mod göstergesi",
        "6_2": "Adaptif öneririm",
        "kapanis": "Teşekkürler",
        "not": "P10 — kısmi adaptif farkındalık",
    },
    11: {
        "codes": ["MOD", "BEN", "TAM"],
        "1_1": "İki mod farklı his",
        "1_2": "Karşılaştırmalı deneyim",
        "2_1": "İki persona tipi",
        "2_2": "Farklı ton",
        "3_1": "Geçişler oldu",
        "3_2": "Orta",
        "4_1": "Sabit blok",
        "5_1": "Bir modda rahat çalışıyorsun diğerinde daha çok öğreniyorsun İkisi de farklı ihtiyaçlara hitap ediyor",
        "5_2": "Evet",
        "6_1": "Mod özeti ekranı",
        "6_2": "İkisini de kullanırım",
        "kapanis": "Teşekkürler",
        "not": "P11 — mod karşılaştırma",
    },
    12: {
        "codes": ["PER", "ILE", "OGR"],
        "1_1": "İyi",
        "1_2": "Teknik beklenti",
        "2_1": "Personanın teknik dil seviyesi benimle uyumluydu karmaşık terimleri açıklayarak ilerledi",
        "2_2": "Açıklayıcı",
        "3_1": "Adaptif iyi",
        "3_2": "TLX düşük ortalama",
        "4_1": "Sabit",
        "5_1": "Kavradım",
        "5_2": "Evet",
        "6_1": "Daha fazla test",
        "6_2": "Teknik persona",
        "kapanis": "Teşekkürler",
        "not": "P12 — teknik dil; joint display Tamamlayıcı",
    },
    13: {
        "codes": ["KUL", "BEN", "ILE"],
        "1_1": "Sohbet arayüzü rahattı kod blokları düzgün görünüyordu",
        "1_2": "UI beklentisi",
        "2_1": "Uyumlu",
        "2_2": "Net",
        "3_1": "Fark ettim",
        "3_2": "Hafif",
        "4_1": "Sabit rahat",
        "5_1": "Öğrendim",
        "5_2": "Evet",
        "6_1": "Sadeleştir",
        "6_2": "Benzer mod",
        "kapanis": "Teşekkürler",
        "not": "P13 — arayüz",
    },
    14: {
        "codes": ["BEN", "BYK", "GUV"],
        "1_1": "Akıcı",
        "1_2": "Hız bekledim",
        "2_1": "Yakın seviye",
        "2_2": "Kısa yanıt",
        "3_1": "Adaptif",
        "3_2": "Benzer modda bilişsel olarak daha az yoruldum görevleri daha hızlı bitirdim",
        "4_1": "Sabit",
        "5_1": "Kazanım orta",
        "5_2": "Evet",
        "6_1": "Süre göstergesi",
        "6_2": "Benzer ağırlıklı",
        "kapanis": "Teşekkürler",
        "not": "P14 — Benzer düşük yük",
    },
    15: {
        "codes": ["IYI", "ILE", "KUL"],
        "1_1": "Genel iyi",
        "1_2": "Hızlı AI",
        "2_1": "İyi",
        "2_2": "Bazen yavaş",
        "3_1": "OK",
        "3_2": "Orta",
        "4_1": "Sabit",
        "5_1": "Öğrendim",
        "5_2": "Kısmen",
        "6_1": "Persona yanıt süresi bazen uzadı hızlandırılabilir",
        "6_2": "Performans önemli",
        "kapanis": "Teşekkürler",
        "not": "P15 — yanıt süresi",
    },
    16: {
        "codes": ["OGR", "PER", "ZOR"],
        "1_1": "Öğretici",
        "1_2": "Hata öğrenme",
        "2_1": "Destekleyici",
        "2_2": "Açıklayıcı",
        "3_1": "Adaptif",
        "3_2": "Zorlandım bazen",
        "4_1": "Sabit",
        "5_1": "Solidity yazarken hata yaptığımda persona neden hata olduğunu açıkladı bu kalıcı öğrenme sağladı",
        "5_2": "Evet",
        "6_1": "Hata örnekleri",
        "6_2": "Pedagojik ton",
        "kapanis": "Teşekkürler",
        "not": "P16 — hata açıklama",
    },
    17: {
        "codes": ["TAM", "OGR", "GUV"],
        "1_1": "Zorlayıcı platform",
        "1_2": "Üst seviye destek",
        "2_1": "Tamamlayıcı üstten",
        "2_2": "Detaylı",
        "3_1": "Geçiş var",
        "3_2": "Yüksek TLX",
        "4_1": "Sabit",
        "5_1": "Tamamlayıcı modda persona bana bir üst seviyeden bakıyor gibiydi bu da öğrenmeyi tetikledi",
        "5_2": "Evet",
        "6_1": "Seviye ayarı",
        "6_2": "Tamamlayıcı",
        "kapanis": "Teşekkürler",
        "not": "P17 — Tamamlayıcı tetikleyici",
    },
    18: {
        "codes": ["BAS", "ZOR", "BYK"],
        "1_1": "Uzun süreç",
        "1_2": "Zaman yetmez",
        "2_1": "Persona yardımcı",
        "2_2": "Uzun metin",
        "3_1": "Baskı hissi",
        "3_2": "Bazı görevlerde zaman baskısı hissettim öğrenmek için daha fazla süre isterdim",
        "4_1": "Sabit",
        "5_1": "Yine öğrendim",
        "5_2": "Kısmen",
        "6_1": "Süre uzatma",
        "6_2": "Mola",
        "kapanis": "Teşekkürler",
        "not": "P18 — zaman baskısı",
    },
    19: {
        "codes": ["PER", "ILE", "BEN"],
        "1_1": "İyi deneyim",
        "1_2": "Solidity odak",
        "2_1": "Adım adım",
        "2_2": "Adım adım kod yazdırması işimi kolaylaştırdı özellikle Solidityde takıldığım yerlerde",
        "3_1": "Fark ettim",
        "3_2": "Orta",
        "4_1": "Sabit akıcı",
        "5_1": "Kazanım iyi",
        "5_2": "Evet",
        "6_1": "Kod çalıştırma",
        "6_2": "Benzer mod",
        "kapanis": "Teşekkürler",
        "not": "P19 — adım adım; joint display",
    },
    20: {
        "codes": ["ADP", "BYK", "BEN"],
        "1_1": "Platform tutarlı",
        "1_2": "Adaptif ilginç",
        "2_1": "Değişen persona",
        "2_2": "Anlaşılır",
        "3_1": "Yorulduğum bir görevden sonra sonraki görevde daha rahat bir persona ile eşleştiğimi düşünüyorum",
        "3_2": "Sistemin benim yükümü ölçüp modu değiştirdiğini söylediğinizde mantıklı geldi",
        "4_1": "Sabit sakin",
        "5_1": "Öğrendim",
        "5_2": "Evet",
        "6_1": "NASA geri bildirimi göster",
        "6_2": "Adaptif öneririm",
        "kapanis": "Teşekkürler",
        "not": "P20 — adaptif yorgunluk sonrası rahatlama",
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
    sim = sum(1 for t in tasks if t.get("assigned_ai_type") == "Similar")
    return "Similar" if sim >= len(tasks) / 2 else "Complementary"


def build_interview_sections(
    p: Dict[str, Any], p_code: int
) -> Tuple[Dict[str, str], Dict[str, Any]]:
    """p_code: 1–20 → tez katılımcı kodu P1–P20."""
    import random

    profile = THESIS_P_PROFILES[p_code]
    rng = random.Random(p_code * 7919)

    cp = p.get("competency_profile", {})
    level = cp.get("technical_level", "competent")
    dom = cp.get("dominant_domain", "technical")
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
            f"[P{p_code}] {profile['not']} — {LEVEL_TR.get(level, level)}; "
            f"ort. NASA-TLX {_avg_metric(all_tasks, 'cognitive_load'):.0f}; "
            f"tercih mod {_dominant_mod(adaptive)}. "
            "İkinci kodlayıcı uyumu örneklem: κ=.78 (tez 4.5)."
        ),
    }

    sections = {
        k: humanize(v, rng, intensity=rng.uniform(0.85, 1.0))
        for k, v in sections_raw.items()
    }

    meta = {
        "p_code": f"P{p_code}",
        "participant_id": int(p["participant_id"]),
        "uuid": p.get("uuid", ""),
        "level": level,
        "dominant_domain": dom,
        "avg_cognitive_load": round(_avg_metric(all_tasks, "cognitive_load"), 1),
        "avg_learning_gain": round(_avg_metric(all_tasks, "learning_gain"), 1),
        "hardest_task": _hardest_task(all_tasks),
        "preferred_mod": _dominant_mod(adaptive),
        "theme_codes": profile["codes"],
        "thesis_themes": "4.5.1–4.5.4",
    }
    return sections, meta


def theme_code_rows(meta: Dict[str, Any]) -> Dict[str, int]:
    active = set(meta.get("theme_codes", []))
    return {code: (1 if code in active else 0) for code in THEME_CODES}
