# PIDL Araştırma Sistemi – Detaylı Sistem Akışı (v2.0)
## Adaptive Dual-Mode Recommendation Framework

**Versiyon:** 2.0 (Güncellenmiş - Şubat 2026)  
**Yeni Özellikler:** CLT Entegrasyonu + NASA-TLX Bazlı Adaptive Mod

---

## 📋 İÇİNDEKİLER

1. [Genel Bakış](#1-genel-bakış)
2. [Teorik Temeller](#2-teorik-temeller)
3. [Sistem Akışı - Aşama Aşama](#3-sistem-akışı---aşama-aşama)
4. [Matematiksel Formülasyon](#4-matematiksel-formülasyon)
5. [Adaptive Mode Mekanizması](#5-adaptive-mode-mekanizması)
6. [Örnek Hesaplama](#6-örnek-hesaplama)
7. [Özet Tablolar](#7-özet-tablolar)

---

## 1. GENEL BAKIŞ

### 1.1 Sistemin Amacı

PIDL (Persona-Integrated Dual-mode Learning) sistemi, kullanıcının yetkinlik profiline göre **en uygun AI persona'sını** matematiksel formüllerle seçer ve görevler boyunca **bilişsel yük geri bildirimine** göre dinamik olarak persona modunu ayarlar.

### 1.2 Yeni Özellikler (v2.0)

| Özellik | v1.0 | v2.0 |
|---------|------|------|
| Persona seçimi | MCDA (S, C, P, L) | MCDA × **CLT Modifier** |
| İlk görev ataması | Sabit (Similar) | **learning_goal'e göre** |
| Görev sıralaması | Sabit (S-C-S-C-S-C) | **NASA-TLX bazlı adaptive** |
| Bilişsel yük | Sadece hesaplama | **Skora etki ediyor** |
| Weight optimization | Tanımlı ama kullanılmıyor | **Aktif ve çağrılabilir** |

### 1.3 Yüksek Seviye Akış

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PIDL SİSTEM AKIŞI (v2.0)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Onay      │ →  │  Yetkinlik  │ →  │   Persona   │ →  │   Görevler  │  │
│  │   Formu     │    │ Değerlend.  │    │   Seçimi    │    │   (1-6)     │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│                            │                  │                  │          │
│                            ▼                  ▼                  ▼          │
│                     CompetencyProfile   MCDA + CLT         NASA-TLX        │
│                     + UserVector        Modifier           Adaptive        │
│                     + learning_goal                        Mode Switch     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. TEORİK TEMELLER

### 2.1 Kullanılan Teoriler ve Uygulama Yerleri

| Teori | Kaynak | Sistem İçinde Kullanım |
|-------|--------|------------------------|
| **Dreyfus Model** | Dreyfus & Dreyfus (1986) | Yetkinlik seviyeleri (novice → expert), persona tanımları |
| **Zone of Proximal Development (ZPD)** | Vygotsky (1978) | Competency Match (C) - optimal zorluk hesabı |
| **Cognitive Load Theory (CLT)** | Sweller (1988) | Intrinsic/Extraneous/Germane Load, **CLT Modifier** |
| **Power Law of Practice** | Newell & Rosenbloom (1981) | Learning Trajectory (L) hesabı |
| **Nonaka & Takeuchi** | (1995) | Bilgi türleri: procedural, declarative, conditional |
| **MCDA** | Multi-Criteria Decision Analysis | R = α·S + β·C + γ·P + δ·L formülü |
| **NASA-TLX** | Hart & Staveland (1988) | Bilişsel yük ölçümü, **adaptive mod kararı** |

### 2.2 Teorilerin Entegrasyonu

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TEORİ ENTEGRASYON HARİTASI                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   BAŞLANGIÇ (Bir kez)                    GÖREVLER (Her görev sonrası)      │
│   ─────────────────────                  ────────────────────────────       │
│                                                                             │
│   Dreyfus Model ──→ UserVector           NASA-TLX ──→ Adaptive Decision    │
│         │               │                    │              │               │
│         ▼               ▼                    ▼              ▼               │
│   learning_goal    10 boyutlu           CLT Feedback   Mod Değişimi        │
│   hesaplama        vektör                   │         (S ↔ C)              │
│         │               │                    │                              │
│         ▼               ▼                    ▼                              │
│   İlk görev        MCDA + CLT          Sonraki görev                       │
│   modu belirleme   persona seçimi      modu belirleme                      │
│                                                                             │
│   ZPD ──────────→ Competency Match (C)                                     │
│   CLT ──────────→ Intrinsic/Extraneous/Germane → CLT Modifier              │
│   Nonaka ───────→ Knowledge types → UserVector boyutları                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. SİSTEM AKIŞI - AŞAMA AŞAMA

### 3.1 AŞAMA 1: Yetkinlik Değerlendirmesi

**Girdi:** CAQ (Competency Assessment Questionnaire) form cevapları

**Süreç:**
```python
# competency_assessment.py
form_cevapları → create_profile() → CompetencyProfile

CompetencyProfile:
├── technical_score (0-100)      # Teknik alan puanı
├── educational_score (0-100)    # Eğitimsel alan puanı
├── technical_level              # novice → expert
├── educational_level            # novice → expert
├── dominant_domain              # Güçlü alan (technical/educational)
└── weak_domain                  # Zayıf alan
```

**Dreyfus Level Belirleme:**

| Likert Ortalaması | Dreyfus Seviyesi |
|-------------------|------------------|
| 1.0 - 1.8 | novice |
| 1.9 - 2.8 | advanced_beginner |
| 2.9 - 3.8 | competent |
| 3.9 - 4.5 | proficient |
| 4.6 - 5.0 | expert |

---

### 3.2 AŞAMA 2: UserVector Oluşturma

**Girdi:** CompetencyProfile

**Süreç:**
```python
# recommendation_engine.py
profile → create_user_vector() → UserVector (10 boyut)
```

**UserVector Parametreleri:**

| # | Parametre | Formül/Kaynak | Örnek |
|---|-----------|---------------|-------|
| 1 | `technical_skill` | Dreyfus level mapping | 0.5 (competent) |
| 2 | `domain_knowledge` | domain == 'technical' → 0.8, else 0.7 | 0.8 |
| 3 | `ai_experience` | responses.ai_experience → 0.7, else 0.2 | 0.2 |
| 4 | `learning_goal` | **Aşağıdaki tabloya göre** | 0.6 |
| 5 | `procedural_knowledge` | min(1.0, score × 1.2) | 0.6 |
| 6 | `declarative_knowledge` | score | 0.5 |
| 7 | `conditional_knowledge` | max(0.3, score - 0.2) | 0.3 |
| 8 | `cognitive_capacity` | 0.5 + (score × 0.5) | 0.75 |
| 9 | `pattern_recognition` | max(0.3, score - 0.1) | 0.4 |
| 10 | `abstraction_level` | score | 0.5 |

**learning_goal Hesaplama (Kritik!):**

| Dreyfus Level | learning_goal | Anlam |
|---------------|---------------|-------|
| novice | 0.9 | Ağırlıklı öğrenme |
| advanced_beginner | 0.9 | Ağırlıklı öğrenme |
| competent | 0.6 | Öğrenme + üretim arası |
| proficient | 0.3 | Ağırlıklı üretim |
| expert | 0.3 | Ağırlıklı üretim |

**Neden Önemli:** `learning_goal` değeri **ilk görevin modunu** ve **adaptive hesaplamaları** belirliyor.

---

### 3.3 AŞAMA 3: Persona Seçimi (MCDA + CLT)

**Girdi:** UserVector + Persona havuzu (10 persona)

**Süreç:**
```python
# recommendation_engine.py
for persona in candidates:
    score = calculate_recommendation_score(user, persona, mode="similarity/complementary")
    # score artık CLT modifier içeriyor!
```

#### 3.3.1 Similar Persona Seçimi

**Adaylar:** `dominant_domain` kategorisindeki 5 persona

**Formül (YENİ - CLT Entegre):**
```
R_similar = (α·S + β·C + γ·P + δ·L) × CLT_modifier
```

#### 3.3.2 Complementary Persona Seçimi

**Adaylar:** `weak_domain` kategorisindeki 5 persona

**Formül (YENİ - CLT Entegre):**
```
R_complementary = (α·(1-S) + β·D + γ·P + δ·L) × CLT_modifier
```

#### 3.3.3 CLT Modifier Hesaplama

**Kaynak:** `calculate_total_cognitive_load()` fonksiyonu

```python
CLT_modifier = 1.0  # Başlangıç

# Bonus durumları
if is_in_optimal_zone:
    CLT_modifier += 0.10  # +10%
    
if germane_load > 0.7:
    CLT_modifier += 0.05  # +5%

# Ceza durumları
if is_overloaded:
    penalty = min(0.30, overload_amount × 0.3)
    CLT_modifier -= penalty  # -%30'a kadar
    
if extraneous_load > 0.5:
    CLT_modifier -= 0.10  # -10%
```

**CLT Modifier Etki Tablosu:**

| Durum | Modifier | Etki |
|-------|----------|------|
| Optimal Zone | ×1.10 | Bonus: Persona ideal |
| High Germane | ×1.05 | Bonus: Öğretici persona |
| Normal | ×1.00 | Değişiklik yok |
| High Extraneous | ×0.90 | Ceza: Kötü sunum |
| Overload | ×0.70-0.90 | Ceza: Aşırı yük |

**Sonuç:** 2 persona seçilir:
- 1 **Similar** (dominant domain'den en yüksek skor)
- 1 **Complementary** (weak domain'den en yüksek skor)

---

### 3.4 AŞAMA 4: İlk Görev Ataması (learning_goal Bazlı)

**YENİ ÖZELLİK:** İlk görev artık `learning_goal`'e göre belirleniyor.

```python
# research_app.py → calculate_adaptive_decision()
if task_number == 1:
    if learning_goal > 0.7:
        return "Complementary"  # Öğrenme odaklı → eksik kapatma
    elif learning_goal < 0.3:
        return "Similar"        # Üretim odaklı → rahat çalışma
    else:
        return "Similar"        # Varsayılan
```

**İlk Görev Karar Tablosu:**

| Kullanıcı Seviyesi | learning_goal | İlk Görev Modu |
|--------------------|---------------|----------------|
| Novice | 0.9 | **Complementary** |
| Advanced Beginner | 0.9 | **Complementary** |
| Competent | 0.6 | Similar |
| Proficient | 0.3 | Similar |
| Expert | 0.3 | Similar |

---

### 3.5 AŞAMA 5: Görev Döngüsü (NASA-TLX Adaptive)

Her görev şu alt adımlardan oluşur:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         GÖREV N AKIŞI                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   1. Pre-Test (Ön bilgi ölçümü)                                         │
│            │                                                             │
│            ▼                                                             │
│   2. Kod Üretimi (Seçilen persona ile GPT-4)                            │
│            │                                                             │
│            ▼                                                             │
│   3. Post-Test (Öğrenme ölçümü)                                         │
│            │                                                             │
│            ▼                                                             │
│   4. NASA-TLX (Bilişsel yük anketi) ◄─── YENİ: Adaptive karar için     │
│            │                                                             │
│            ▼                                                             │
│   5. AI Değerlendirmesi                                                 │
│            │                                                             │
│            ▼                                                             │
│   6. ┌─────────────────────────────────────────────────────────────┐    │
│      │            ADAPTIVE KARAR MEKANİZMASI                       │    │
│      │                                                             │    │
│      │   NASA-TLX Skoru (total_cognitive_load)                     │    │
│      │            │                                                │    │
│      │            ▼                                                │    │
│      │   ┌───────────────────────────────────────────┐            │    │
│      │   │ > 40 (Yüksek yük)?                        │            │    │
│      │   │   EVET → MOD DEĞİŞTİR (S↔C)              │            │    │
│      │   │   HAYIR → AYNI MOD veya DENGELE          │            │    │
│      │   └───────────────────────────────────────────┘            │    │
│      └─────────────────────────────────────────────────────────────┘    │
│            │                                                             │
│            ▼                                                             │
│   7. Görev N+1 için mod belirlendi                                      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

### 3.6 AŞAMA 6: NASA-TLX Bazlı Adaptive Karar

**Kaynak:** `calculate_adaptive_decision()` fonksiyonu

```python
def calculate_adaptive_decision(task_number):
    # Görev 1: learning_goal'e göre (yukarıda açıklandı)
    
    # Görev 2-6: NASA-TLX'e göre
    if nasa_tlx_history:
        last_score = history[-1]['score']
        last_ai_type = history[-1]['ai_type']
        
        HIGH_LOAD_THRESHOLD = 40
        
        if last_score > HIGH_LOAD_THRESHOLD:
            # Yoruldu → Mod değiştir
            next_ai = "Complementary" if last_ai_type == "Similar" else "Similar"
        else:
            # Normal → Devam veya dengele
            if similar_count < complementary_count:
                next_ai = "Similar"
            elif complementary_count < similar_count:
                next_ai = "Complementary"
            else:
                next_ai = last_ai_type  # Aynı modla devam
        
        return next_ai
```

**Adaptive Karar Tablosu:**

| NASA-TLX Skoru | Anlam | Sonraki Görev Kararı |
|----------------|-------|---------------------|
| 6-20 | Düşük yük | Aynı mod veya dengele |
| 21-40 | Normal yük | Aynı mod veya dengele |
| 41-50 | Yüksek yük | **MOD DEĞİŞTİR** |
| 51-60 | Çok yüksek | **MOD DEĞİŞTİR** |

**Denge Kuralı:** Her zaman 3 Similar + 3 Complementary hedeflenir.

---

## 4. MATEMATİKSEL FORMÜLASYON

### 4.1 Ana Tavsiye Formülü (v2.0 - CLT Entegre)

**Genel Form:**
```
R_final(u,p) = R_base(u,p) × CLT_modifier
```

**Similarity Modu:**
```
R_base_sim = α·S(u,p) + β·C(u,p) + γ·P(u,p,t) + δ·L(u,p,τ)
```

**Complementary Modu:**
```
R_base_comp = α·(1-S(u,p)) + β·D(u,p) + γ·P(u,p,t) + δ·L(u,p,τ)
```

**Hybrid/Adaptive Modu:**
```
R_adaptive = g·R_comp + (1-g)·R_sim
```
Burada `g = learning_goal`

### 4.2 Bileşen Formülleri

#### S - Benzerlik (Similarity)
```
S(u,p) = 0.6·cos(u_vec, p_vec) + 0.4·(1 - d_euclidean/d_max)
```

#### C - Yetkinlik Uyumu (Competency Match - ZPD)
```
C(u,p) = 0.5·exp(-λ|skill_diff|²) + 0.3·alignment + 0.2·knowledge_match

knowledge_match = 0.4·(proc_u × mod_p) + 0.3·(decl_u × verb_p) + 0.3·(cond_u × learn_p)
```

#### P - Performans Tahmini
```
P(u,p,t) = σ(β₀ + β₁·user_skill + β₂·persona_quality + β₃·match - β₄·task_complexity)
```

#### L - Öğrenme Yörüngesi
```
L(u,p,τ) = L_max·(1 - e^(-k·τ))·learning_support·learning_capacity
```

#### D - Tamamlayıcılık
```
D(u,p) = mean(persona_strength_i × user_weakness_i)
```

### 4.3 CLT Bileşenleri

#### Intrinsic Load (İçsel Yük)
```
IL(u,t) = task_complexity × (1 - user_expertise)

user_expertise = 0.4·technical_skill + 0.3·domain_knowledge + 0.3·procedural_knowledge
```

#### Extraneous Load (Dışsal Yük)
```
EL(p) = 0.4·(1 - modularity) + 0.3·excessive_verbosity + 0.3·code_complexity_load
```

#### Germane Load (Faydalı Yük)
```
GL(u,p) = 0.35·learning_support + 0.30·pedagogical_focus + 0.20·learning_capacity + 0.15·example_richness
```

#### Total Load
```
Total_Load = IL + EL - GL
Optimal_Zone = (IL + GL ≤ capacity) AND (EL < 0.3)
```

### 4.4 Ağırlık Katsayıları

**Varsayılan Değerler:**
```
α = 0.30  # Benzerlik/Farklılık
β = 0.35  # Yetkinlik Uyumu/Tamamlayıcılık (EN AĞIR - ZPD öncelikli)
γ = 0.25  # Performans Tahmini
δ = 0.10  # Öğrenme Yörüngesi
───────
Σ = 1.00
```

**Neden Bu Değerler?**
- **β en yüksek (0.35):** ZPD (Vygotsky) temel teori; optimal zorluk en kritik faktör
- **α ikinci (0.30):** Profil uyumu önemli ama zorluk kadar kritik değil
- **γ üçüncü (0.25):** Başarı beklentisi destekleyici
- **δ en düşük (0.10):** Uzun vadeli öğrenme destekleyici rol

---

## 5. ADAPTIVE MODE MEKANİZMASI

### 5.1 Üç Katmanlı Adaptasyon

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ÜÇ KATMANLI ADAPTİF SİSTEM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  KATMAN 1: PERSONA SEÇİMİ (Başlangıçta)                                    │
│  ─────────────────────────────────────────                                  │
│  • UserVector'e göre 2 persona seçilir                                     │
│  • CLT Modifier persona skorlarını etkiler                                 │
│  • Similar: dominant domain'den                                            │
│  • Complementary: weak domain'den                                          │
│                                                                             │
│  KATMAN 2: İLK GÖREV MODU (learning_goal bazlı)                            │
│  ──────────────────────────────────────────────                             │
│  • learning_goal > 0.7 → Complementary ile başla                           │
│  • learning_goal < 0.3 → Similar ile başla                                 │
│  • 0.3 - 0.7 arası → Similar ile başla (varsayılan)                        │
│                                                                             │
│  KATMAN 3: GÖREV SÜRESİ ADAPTASYONU (NASA-TLX bazlı)                       │
│  ────────────────────────────────────────────────────                       │
│  • Her görev sonrası NASA-TLX (bilişsel yük) ölçülür                       │
│  • Yüksek yük (>40) → Mod değiştirilir                                     │
│  • Normal yük (≤40) → Aynı mod veya denge                                  │
│  • Hedef: 3 Similar + 3 Complementary                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Adaptive Karar Akış Şeması

```
                    GÖREV N TAMAMLANDI
                           │
                           ▼
                    NASA-TLX TOPLANDI
                    (score: 6-60)
                           │
                           ▼
              ┌────────────────────────┐
              │   score > 40?          │
              └────────────────────────┘
                    │            │
                   EVET        HAYIR
                    │            │
                    ▼            ▼
           ┌──────────────┐  ┌──────────────┐
           │ MOD DEĞİŞTİR │  │ DENGE KONTROL│
           │ (S↔C)        │  │              │
           └──────────────┘  └──────────────┘
                    │            │
                    ▼            ▼
           ┌──────────────┐  ┌──────────────────────┐
           │ Yoruldu,     │  │ S_count < C_count?   │
           │ farklı mod   │  │   → Similar          │
           │ dene         │  │ C_count < S_count?   │
           └──────────────┘  │   → Complementary    │
                             │ Eşit?                │
                             │   → Önceki mod       │
                             └──────────────────────┘
                                      │
                                      ▼
                           GÖREV N+1 MODU BELİRLENDİ
```

### 5.3 Örnek Adaptive Senaryo

**Kullanıcı:** Novice seviye, learning_goal = 0.9

| Görev | Karar Kriteri | Atanan Mod | NASA-TLX | Sonraki Karar |
|-------|---------------|------------|----------|---------------|
| 1 | learning_goal=0.9 > 0.7 | **Complementary** | 48 | Yüksek → S'e geç |
| 2 | NASA-TLX=48 > 40 | **Similar** | 35 | Normal → Denge |
| 3 | Denge (S=1, C=1) | **Complementary** | 42 | Yüksek → S'e geç |
| 4 | NASA-TLX=42 > 40 | **Similar** | 30 | Normal → Denge |
| 5 | Denge (S=2, C=2) | **Complementary** | 38 | Normal → Devam |
| 6 | Denge (S=2, C=3) | **Similar** | - | Final |

**Sonuç:** 3 Similar + 3 Complementary (Denge korundu)

---

## 6. ÖRNEK HESAPLAMA

### 6.1 Örnek Kullanıcı Profili

**CAQ Cevapları:**
- Teknik sorular ortalaması: 3.5 (Likert 1-5)
- Eğitimsel sorular ortalaması: 2.5 (Likert 1-5)
- Dreyfus öz-değerlendirme: "Competent"

### 6.2 CompetencyProfile Oluşturma

```
technical_score = (3.5 - 1) / 4 × 100 = 62.5
educational_score = (2.5 - 1) / 4 × 100 = 37.5
technical_level = competent (3.5 ∈ [2.9, 3.8])
educational_level = advanced_beginner (2.5 ∈ [1.9, 2.8])
dominant_domain = technical (62.5 > 37.5)
weak_domain = educational
```

### 6.3 UserVector Hesaplama

```
score = (62.5 + 37.5) / 2 / 100 = 0.5
level = competent

UserVector:
├── technical_skill = 0.5 (level_mapping["competent"])
├── domain_knowledge = 0.8 (technical domain)
├── ai_experience = 0.2 (varsayılan)
├── learning_goal = 0.6 (competent → 0.6)
├── procedural_knowledge = min(1, 0.5 × 1.2) = 0.6
├── declarative_knowledge = 0.5
├── conditional_knowledge = max(0.3, 0.5 - 0.2) = 0.3
├── cognitive_capacity = 0.5 + (0.5 × 0.5) = 0.75
├── pattern_recognition = max(0.3, 0.5 - 0.1) = 0.4
└── abstraction_level = 0.5
```

### 6.4 Similar Persona Seçimi (tech_competent örneği)

**PersonaVector (tech_competent):**
```
├── code_complexity = 0.55
├── verbosity = 0.50
├── technical_depth = 0.65
├── pedagogical_focus = 0.25
├── comment_density = 0.50
├── modularity = 0.70
├── example_richness = 0.50
├── learning_support = 0.55
├── production_readiness = 0.75
└── innovation_factor = 0.45
```

**Bileşen Hesaplamaları:**

```
S (Similarity):
  user_vec = [0.5, 0.8, 0.2, 0.6, 0.6, 0.5, 0.3, 0.75, 0.4, 0.5]
  persona_vec = [0.65, 0.25, 0.45, 0.25, 0.70, 0.50, 0.55, 0.45, 0.50, 0.55]
  cos_sim ≈ 0.85
  euclidean_sim ≈ 0.70
  S = 0.6 × 0.85 + 0.4 × 0.70 = 0.79

C (Competency Match):
  persona_difficulty = (0.55 + 0.65) / 2 = 0.60
  user_skill = (0.5 + 0.8) / 2 = 0.65
  skill_diff = |0.65 - 0.60| = 0.05
  gaussian_match = exp(-2 × 0.05²) = 0.995
  alignment = 0.75 (production_readiness, çünkü learning_goal=0.6 < 0.7)
  knowledge_match = 0.4×(0.6×0.70) + 0.3×(0.5×0.50) + 0.3×(0.3×0.55) = 0.27
  C = 0.5×0.995 + 0.3×0.75 + 0.2×0.27 = 0.78

P (Performance):
  user_skill_feature = 0.65
  persona_quality = (0.75 + 0.55) / 2 = 0.65
  z = 0.3 + 0.4×0.65 + 0.3×0.65 + 0.25×0.79 - 0.2×0.5 = 0.85
  P = σ(0.85) = 1 / (1 + e^(-0.85)) ≈ 0.70

L (Learning Trajectory):
  time_learning = 1 × (1 - e^(-2×0.5)) = 0.63
  learning_capacity = 0.4×0.75 + 0.3×0.4 + 0.3×(1-0.5) = 0.57
  L = 0.63 × 0.55 × 0.57 = 0.20

CLT Analysis:
  intrinsic = 0.5 × (1 - 0.60) = 0.20
  extraneous = 0.4×(1-0.70) + 0.3×0 + 0.3×(0.55×0.5) = 0.20
  germane = 0.35×0.55 + 0.30×0.25 + 0.20×0.57 + 0.15×0.50 = 0.45
  total_load = 0.20 + 0.20 - 0.45 = -0.05 (very low)
  is_in_optimal_zone = True (productive_load ≤ capacity)
  CLT_modifier = 1.00 + 0.10 = 1.10 (Optimal Zone bonus)

Base Score:
  R_base = 0.30×0.79 + 0.35×0.78 + 0.25×0.70 + 0.10×0.20
        = 0.237 + 0.273 + 0.175 + 0.020
        = 0.705

Final Score:
  R_final = 0.705 × 1.10 = 0.776
```

### 6.5 İlk Görev Modu Belirleme

```
learning_goal = 0.6
0.6 > 0.7? HAYIR
0.6 < 0.3? HAYIR
→ İlk görev: Similar (varsayılan)
```

---

## 7. ÖZET TABLOLAR

### 7.1 Teori-Kod Eşleştirmesi

| Teori | Fonksiyon | Dosya |
|-------|-----------|-------|
| Dreyfus Model | `determine_level()`, `level_mapping` | competency_assessment.py, recommendation_engine.py |
| ZPD (Vygotsky) | `calculate_competency_match()` | recommendation_engine.py |
| CLT (Sweller) | `calculate_intrinsic_load()`, `calculate_extraneous_load()`, `calculate_germane_load()`, `calculate_total_cognitive_load()` | recommendation_engine.py |
| Nonaka & Takeuchi | `procedural_knowledge`, `declarative_knowledge`, `conditional_knowledge` | recommendation_engine.py (UserVector) |
| Power Law | `calculate_learning_trajectory()` | recommendation_engine.py |
| MCDA | `calculate_recommendation_score()` | recommendation_engine.py |
| NASA-TLX | `NASATLXForm.show()`, `calculate_adaptive_decision()` | research_modules/nasa_tlx.py, research_app.py |

### 7.2 Yeni (v2.0) vs Eski (v1.0) Karşılaştırması

| Özellik | v1.0 | v2.0 |
|---------|------|------|
| Persona seçim formülü | R = α·S + β·C + γ·P + δ·L | R = (α·S + β·C + γ·P + δ·L) × **CLT_modifier** |
| CLT'nin rolü | Sadece hesaplama, etkisiz | **Persona sıralamasını değiştiriyor** |
| İlk görev modu | Sabit: Similar | **learning_goal'e göre** |
| Görev sıralaması | Sabit: S-C-S-C-S-C | **NASA-TLX'e göre dinamik** |
| Weight optimization | Tanımlı, kullanılmıyor | **Aktif, çağrılabilir** |

### 7.3 Formül Özet Kartı

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FORMÜL ÖZET KARTI                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PERSONA SEÇİMİ (Başlangıçta):                                             │
│  ──────────────────────────────                                             │
│  R_final = R_base × CLT_modifier                                           │
│                                                                             │
│  R_sim = α·S + β·C + γ·P + δ·L         (Similarity modu)                   │
│  R_comp = α·(1-S) + β·D + γ·P + δ·L    (Complementary modu)                │
│  R_adaptive = g·R_comp + (1-g)·R_sim   (Adaptive modu)                     │
│                                                                             │
│  Ağırlıklar: α=0.30, β=0.35, γ=0.25, δ=0.10                               │
│                                                                             │
│  CLT_modifier:                                                              │
│    +10% if optimal_zone                                                    │
│    +5%  if germane_load > 0.7                                              │
│    -10% if extraneous_load > 0.5                                           │
│    -30% max if overloaded                                                  │
│                                                                             │
│  İLK GÖREV MODU (learning_goal bazlı):                                     │
│  ────────────────────────────────────                                       │
│  learning_goal > 0.7 → Complementary                                       │
│  learning_goal < 0.3 → Similar                                             │
│  else → Similar (varsayılan)                                               │
│                                                                             │
│  GÖREV SÜRESİ (NASA-TLX bazlı):                                            │
│  ────────────────────────────────                                           │
│  NASA-TLX > 40 → MOD DEĞİŞTİR                                              │
│  NASA-TLX ≤ 40 → DEVAM veya DENGELE                                        │
│  Hedef: 3 Similar + 3 Complementary                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. SONUÇ

PIDL v2.0, üç katmanlı adaptif bir sistem sunmaktadır:

1. **Persona Seçimi:** MCDA + CLT Modifier ile en uygun 2 persona
2. **İlk Görev:** learning_goal ile kişiye özel başlangıç
3. **Görev Süresi:** NASA-TLX ile dinamik mod değişimi

Bu sistem, kullanıcının hem **"kim olduğuna"** (yetkinlik profili) hem de **"nasıl hissettiğine"** (bilişsel yük geri bildirimi) göre adaptif davranır.

---

**SON GÜNCELLEME:** Şubat 2026  
**VERSİYON:** 2.0  
**DURUM:** Tüm özellikler aktif ve test edilmiş
