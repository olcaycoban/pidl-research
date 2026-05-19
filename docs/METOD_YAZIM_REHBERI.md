# PITL DOKTORA TEZİ - YÖNTEM BÖLÜMÜ YAZIM REHBERİ

Bu belge, Claude'a verilerek tezin **3. YÖNTEM** bölümünün yazılması için hazırlanmıştır.

---

## GÖREV

Aşağıdaki bilgileri kullanarak bir doktora tezinin **3. YÖNTEM (Metodoloji)** bölümünü yaz.

**Gereksinimler:**
- Akademik Türkçe, formal dil
- APA 7 atıf formatı
- 20-25 sayfa uzunluğunda
- Detaylı ve tekrarlanabilir (replicable) açıklamalar
- Tüm ölçüm araçları ve prosedürler net tanımlanmalı

---

## BÖLÜM YAPISI

```
3. YÖNTEM
   3.1 Araştırma Modeli/Deseni
   3.2 Çalışma Grubu (Örneklem)
   3.3 Veri Toplama Araçları
       3.3.1 Yetkinlik Değerlendirme Aracı
       3.3.2 NASA-TLX (Bilişsel Yük Ölçeği)
       3.3.3 Kod Kalitesi Değerlendirme Araçları
       3.3.4 Ön-test / Son-test Formları
       3.3.5 Final Anketi
   3.4 PITL Platformu
       3.4.1 Sistem Mimarisi
       3.4.2 100 Persona Yapısı
       3.4.3 Öneri Algoritması
   3.5 Veri Toplama Süreci (Prosedür)
   3.6 Veri Analizi
   3.7 Geçerlik ve Güvenirlik
   3.8 Etik Hususlar
```

---

## 3.1 ARAŞTIRMA MODELİ

### Araştırma Deseni
**Karma Yöntem (Mixed Methods) - Açımlayıcı Sıralı Desen**

```
┌─────────────────────────────────────────────────────────────┐
│                    ARAŞTIRMA DESENİ                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  AŞAMA 1: NİCEL (Quantitative)                             │
│  ├── Deneysel tasarım                                       │
│  ├── 2×5 faktöriyel desen                                   │
│  │   • Bağımsız değişken 1: Mod (Similar vs Complementary)  │
│  │   • Bağımsız değişken 2: Dreyfus seviyesi (5 seviye)     │
│  ├── Bağımlı değişkenler:                                   │
│  │   • Kod kalitesi (teknik + pedagojik)                    │
│  │   • Bilişsel yük (NASA-TLX)                              │
│  │   • Öğrenme kazanımı (pre-post fark)                     │
│  │   • Görev tamamlama süresi                               │
│  └── N=150 katılımcı                                        │
│                                                             │
│  AŞAMA 2: NİTEL (Qualitative)                              │
│  ├── Yarı-yapılandırılmış görüşmeler (N=30)                │
│  ├── Persona geçerlilik doğrulaması                        │
│  └── Deneyim ve algı derinlemesine analiz                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Deneysel Faktörler

| Faktör | Düzeyler | Açıklama |
|--------|----------|----------|
| **Mod (within-subject)** | Similar, Complementary | Her katılımcı her iki modu da deneyimler (6 görevde 3+3) |
| **Dreyfus Seviyesi (between-subject)** | Novice, Adv. Beginner, Competent, Proficient, Expert | Ön değerlendirmeyle belirlenir |
| **Domain (between-subject)** | Technical, Educational | Katılımcının dominant alanı |

### Değişkenler

**Bağımsız Değişkenler:**
1. Öneri modu (Similar / Complementary)
2. Kullanıcı yetkinlik seviyesi (Dreyfus 5 aşama)
3. Kullanıcı dominant domain (Teknoloji / Pedagoji)
4. Görev karmaşıklığı (Düşük / Orta / Yüksek)

**Bağımlı Değişkenler:**
1. Kod kalitesi skoru (0-100)
2. Bilişsel yük (NASA-TLX, 0-100)
3. Öğrenme kazanımı (post-test - pre-test)
4. Görev tamamlama süresi (dakika)
5. Kullanıcı memnuniyeti (Likert 1-5)

**Kontrol Değişkenleri:**
- Yaş
- Cinsiyet
- Eğitim düzeyi
- Önceki AI deneyimi
- Önceki Blockchain deneyimi

---

## 3.2 ÇALIŞMA GRUBU (ÖRNEKLEM)

### Örneklem Büyüklüğü
**N = 150 katılımcı**

### Güç Analizi
```
G*Power 3.1 Analizi:
- Test ailesi: F tests
- İstatistiksel test: ANOVA (fixed effects, special, main effects and interactions)
- Etki büyüklüğü: f = 0.25 (orta)
- α hata olasılığı: 0.05
- Güç (1-β): 0.80
- Gruplar: 10 (2 mod × 5 seviye)
- Hesaplanan minimum N: 107
- Hedeflenen N: 150 (%40 yedek, dropout için)
```

### Örnekleme Yöntemi
**Amaçlı Örnekleme + Tabakalı Örnekleme**

### Katılımcı Profili

| Tabaka | Hedef N | Kaynak |
|--------|---------|--------|
| Novice (Teknik) | 15 | Bilgisayar Müh. 1-2. sınıf öğrencileri |
| Novice (Pedagoji) | 15 | Eğitim Fak. 1-2. sınıf öğrencileri |
| Adv. Beginner (Teknik) | 15 | Bilgisayar Müh. 3-4. sınıf + yeni mezun |
| Adv. Beginner (Pedagoji) | 15 | Eğitim Fak. 3-4. sınıf + yeni mezun |
| Competent (Teknik) | 15 | 2-4 yıl deneyimli yazılımcılar |
| Competent (Pedagoji) | 15 | 2-4 yıl deneyimli eğitimciler |
| Proficient (Teknik) | 15 | 5-8 yıl deneyimli senior developerlar |
| Proficient (Pedagoji) | 15 | 5-8 yıl deneyimli öğretim görevlileri |
| Expert (Teknik) | 15 | 10+ yıl, blockchain/yazılım uzmanları |
| Expert (Pedagoji) | 15 | 10+ yıl, eğitim teknolojisi uzmanları |

### Dahil Etme Kriterleri
- 18 yaş ve üzeri
- Temel bilgisayar okuryazarlığı
- Türkçe yeterlilik
- Gönüllü katılım ve onam

### Dışlama Kriterleri
- Araştırma ekibiyle yakın ilişki
- Daha önce PITL sistemini kullananlar
- Ciddi görsel/motor engel (erişilebilirlik sınırları)

### Katılımcı Kaynakları
- Türkiye'deki üniversiteler (İstanbul, Ankara, İzmir)
- EdTech şirketleri
- Blockchain geliştirici toplulukları
- Öğretmen dernekleri

---

## 3.3 VERİ TOPLAMA ARAÇLARI

### 3.3.1 Yetkinlik Değerlendirme Aracı

**Amaç:** Katılımcının Dreyfus seviyesini ve Teknik/Pedagojik skorunu belirlemek

**Yapı:**
```
BÖLÜM A: Demografik Bilgiler (10 soru)
- Yaş, cinsiyet, eğitim
- Mesleki deneyim (yıl)
- Blockchain deneyimi
- AI araç kullanım deneyimi

BÖLÜM B: Teknik Yetkinlik (20 soru)
- Solidity bilgisi (5 soru, çoktan seçmeli)
- Smart contract kavramları (5 soru)
- Blockchain mimarisi (5 soru)
- Web3 araçları (5 soru)
- Likert ölçeği (1-5) öz-değerlendirme

BÖLÜM C: Pedagojik Yetkinlik (20 soru)
- Öğretim tasarımı ilkeleri (5 soru)
- Öğrenme teorileri (5 soru)
- Değerlendirme yöntemleri (5 soru)
- Eğitim teknolojisi (5 soru)
- Likert ölçeği (1-5) öz-değerlendirme

BÖLÜM D: Dreyfus Seviye Belirleme (10 senaryo)
- Her senaryo için davranış seçimi
- Seçenekler Dreyfus seviyelerine kodlanmış
```

**Puanlama:**
```python
Technical_Score = (Bölüm_B_Doğru / 20) × 100  # 0-100
Educational_Score = (Bölüm_C_Doğru / 20) × 100  # 0-100
Dreyfus_Level = mode(Bölüm_D_Yanıtları)  # En sık seçilen seviye

Dominant_Domain = "technology" if Technical > Educational else "education"
```

### 3.3.2 NASA-TLX (Task Load Index)

**Kaynak:** Hart, S. G., & Staveland, L. E. (1988)

**6 Alt Boyut:**

| Boyut | İngilizce | Soru | Ölçek |
|-------|-----------|------|-------|
| Zihinsel Talep | Mental Demand | "Bu görev zihinsel olarak ne kadar zordu?" | 0-100 |
| Fiziksel Talep | Physical Demand | "Bu görev fiziksel olarak ne kadar zordu?" | 0-100 |
| Zamansal Talep | Temporal Demand | "Ne kadar zaman baskısı hissettiniz?" | 0-100 |
| Performans | Performance | "Hedefinize ne kadar ulaştınız?" | 0-100 |
| Çaba | Effort | "Ne kadar çaba harcadınız?" | 0-100 |
| Hayal Kırıklığı | Frustration | "Ne kadar stres/hayal kırıklığı yaşadınız?" | 0-100 |

**Uygulama:** Her görev sonrası (6 kez toplam)

**Hesaplama:**
```python
NASA_TLX_Total = (Mental + Physical + Temporal + (100-Performance) + Effort + Frustration) / 6
```

### 3.3.3 Kod Kalitesi Değerlendirme

**İki Perspektif:** Teknik + Pedagojik

#### A. Teknik Kalite Metrikleri (Otomatik)

| Metrik | Araç | Ölçek | Ağırlık |
|--------|------|-------|---------|
| Pylint Skoru | Pylint | 0-10 | 0.20 |
| Güvenlik | Bandit | Severity count | 0.25 |
| Cyclomatic Complexity | Radon | 1-∞ (normalize) | 0.20 |
| Maintainability Index | Radon | 0-100 | 0.20 |
| Test Coverage | Coverage.py | 0-100% | 0.15 |

```python
Technical_Quality = (
    0.20 × (Pylint / 10 × 100) +
    0.25 × Security_Score +
    0.20 × (1 - Complexity_Normalized) × 100 +
    0.20 × Maintainability +
    0.15 × Coverage
)
```

#### B. Pedagojik Kalite Metrikleri (Manuel + Otomatik)

| Metrik | Yöntem | Ölçek | Ağırlık |
|--------|--------|-------|---------|
| Yorum Kalitesi | NLP + Manuel | 0-100 | 0.25 |
| Örnek Zenginliği | Manuel rubrik | 1-5 → 0-100 | 0.20 |
| Öğrenme Kolaylığı | Katılımcı anketi | 1-5 → 0-100 | 0.20 |
| Bilişsel Yük Uygunluğu | CLT analizi | 0-100 | 0.20 |
| Açıklayıcılık | Readability + Manuel | 0-100 | 0.15 |

```python
Pedagogical_Quality = (
    0.25 × Comment_Quality +
    0.20 × Example_Richness +
    0.20 × Learning_Ease +
    0.20 × CLT_Appropriateness +
    0.15 × Explainability
)
```

#### C. Birleşik Kod Kalitesi

```python
Code_Quality = γ × Technical_Quality + (1-γ) × Pedagogical_Quality

# γ değeri kullanıcının learning_goal parametresine göre:
# γ = 0.7 → Production odaklı (teknik ağırlıklı)
# γ = 0.3 → Learning odaklı (pedagojik ağırlıklı)
# γ = 0.5 → Dengeli (varsayılan)
```

### 3.3.4 Ön-test / Son-test Formları

**Her görev için ayrı form**

**Yapı:**
- 5 çoktan seçmeli soru (bilgi düzeyi)
- 2 kısa cevaplı soru (anlama)
- 1 uygulama sorusu (küçük kod parçası)

**Görevler ve Konuları:**

| Görev | Konu | Karmaşıklık |
|-------|------|-------------|
| Görev 1 | Diploma Doğrulama Smart Contract | Düşük |
| Görev 2 | Sertifika NFT Sistemi | Orta |
| Görev 3 | Öğrenme Kaydı Blockchain | Düşük |
| Görev 4 | Çoklu İmza Yönetim Sistemi | Yüksek |
| Görev 5 | DAO Tabanlı Oylama | Orta |
| Görev 6 | Token Tabanlı Teşvik Sistemi | Yüksek |

**Puanlama:**
```python
Pre_Test_Score = (Doğru_Cevap / Toplam) × 100
Post_Test_Score = (Doğru_Cevap / Toplam) × 100
Learning_Gain = Post_Test_Score - Pre_Test_Score
```

### 3.3.5 Final Anketi

**Amaç:** Genel deneyim, tercih ve algı ölçümü

**Bölümler:**

```
BÖLÜM A: Genel Memnuniyet (10 soru, Likert 1-5)
- Platform kullanım kolaylığı
- AI persona kalitesi
- Öğrenme deneyimi
- Genel memnuniyet

BÖLÜM B: Mod Karşılaştırma (8 soru, Likert 1-5)
- Similar mod tercihi
- Complementary mod tercihi
- Hangi modda daha rahat hissettiniz?
- Hangi modda daha çok öğrendiniz?

BÖLÜM C: Açık Uçlu Sorular (4 soru)
- En beğendiğiniz özellik?
- Geliştirilebilecek yönler?
- AI persona hakkında görüşler?
- Genel öneriler?

BÖLÜM D: Demografik Doğrulama (5 soru)
- Değerlendirme doğruluğu kontrolü
```

---

## 3.4 PITL PLATFORMU

### 3.4.1 Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                     PITL PLATFORMU                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FRONTEND (Streamlit)                                       │
│  ├── Kullanıcı arayüzü                                      │
│  ├── Yetkinlik değerlendirme formları                       │
│  ├── Görev arayüzü                                          │
│  ├── AI sohbet arayüzü                                      │
│  └── Sonuç görüntüleme                                      │
│                                                             │
│  BACKEND (Python)                                           │
│  ├── Recommendation Engine                                  │
│  │   ├── UserVector oluşturma                               │
│  │   ├── PersonaVector eşleştirme                           │
│  │   ├── MCDA hesaplama                                     │
│  │   └── Adaptif mod seçimi                                 │
│  ├── 100 Persona Kütüphanesi                                │
│  ├── LLM Entegrasyonu (OpenAI API)                          │
│  └── Veri Kayıt Sistemi                                     │
│                                                             │
│  VERİTABANI (SQLite/PostgreSQL)                            │
│  ├── Katılımcı verileri                                     │
│  ├── Görev oturumları                                       │
│  ├── Test sonuçları                                         │
│  ├── NASA-TLX yanıtları                                     │
│  └── Kod değerlendirmeleri                                  │
│                                                             │
│  DIŞ SERVİSLER                                              │
│  ├── OpenAI GPT-4o API                                      │
│  ├── Anthropic Claude API (yedek)                           │
│  └── Ethereum Test Ağı (Sepolia)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.4.2 100 Persona Yapısı

```
2 Ana Domain × 10 Alt-Uzmanlık × 5 Dreyfus = 100 Persona

TEKNOLOJİ (50 Persona)                 PEDAGOJİ (50 Persona)
├── Smart Contract (5)                 ├── Instructional Design (5)
├── Web3 Frontend (5)                  ├── Curriculum Development (5)
├── DeFi Protocols (5)                 ├── Learning Analytics (5)
├── Security & Audit (5)               ├── Assessment (5)
├── NFT & Gaming (5)                   ├── Gamification (5)
├── L2 & Scaling (5)                   ├── Adaptive Learning (5)
├── DevOps (5)                         ├── Accessibility (5)
├── Testing & QA (5)                   ├── Educational Research (5)
├── Protocol Research (5)              ├── Teacher Training (5)
└── Enterprise (5)                     └── Content Creation (5)
```

**Her Persona 10-Boyutlu Vektör:**
```python
PersonaVector = [
    code_complexity,      # 0.0-1.0
    verbosity,            # 0.0-1.0
    technical_depth,      # 0.0-1.0
    pedagogical_focus,    # 0.0-1.0
    comment_density,      # 0.0-1.0
    modularity,           # 0.0-1.0
    example_richness,     # 0.0-1.0
    learning_support,     # 0.0-1.0
    production_readiness, # 0.0-1.0
    innovation_factor     # 0.0-1.0
]
```

### 3.4.3 Öneri Algoritması

**6 Aşamalı Matematiksel Model:**

```
AŞAMA 1: UserVector Oluşturma
─────────────────────────────
user_vector = create_user_vector(competency_profile)
# 10 boyutlu vektör: [technical_skill, domain_knowledge, ai_experience, 
#                     learning_goal, procedural_knowledge, declarative_knowledge,
#                     conditional_knowledge, cognitive_capacity, pattern_recognition,
#                     abstraction_level]

AŞAMA 2: Similarity Score (S)
─────────────────────────────
S(u,p) = 0.6 × CosineSimilarity(u,p) + 0.4 × (1 - NormalizedEuclidean(u,p))

AŞAMA 3: Competency Match (C) / Complementarity (D)
───────────────────────────────────────────────────
# Similar mod:
C(u,p) = ZPD_Gaussian(level_diff) × Knowledge_Match(u,p)

# Complementary mod:
D(u,p) = Σᵢ (pᵢ_strong × uᵢ_weak)

AŞAMA 4: Performance Prediction (P)
───────────────────────────────────
P(u,p,g) = σ(w₁×S + w₂×C + w₃×history + b)  # Sigmoid regression

AŞAMA 5: Learning Trajectory (L)
────────────────────────────────
L(u,t) = a × t^(-b)  # Power Law of Practice

AŞAMA 6: Final Score (R)
────────────────────────
R(u,p) = α×S + β×C + γ×P + δ×L  # Similar mod
R(u,p) = α×(1-S) + β×D + γ×P + δ×L  # Complementary mod

Ağırlıklar: α=0.30, β=0.35, γ=0.25, δ=0.10
```

**Adaptif Mod Seçimi:**
```python
def select_mode(task_number, nasa_tlx_history, learning_goal):
    if task_number == 1:
        # İlk görev: learning_goal'a göre
        return "Complementary" if learning_goal > 0.6 else "Similar"
    else:
        # Sonraki görevler: NASA-TLX'e göre
        prev_load = nasa_tlx_history[-1]["total"]
        if prev_load > 60:
            return "Similar"  # Yük yüksek → rahatlat
        elif prev_load < 30:
            return "Complementary"  # Yük düşük → zorla
        else:
            return alternate()  # Denge
```

---

## 3.5 VERİ TOPLAMA SÜRECİ

### Prosedür Akışı

```
┌─────────────────────────────────────────────────────────────┐
│                    VERİ TOPLAMA SÜRECİ                      │
│                    (Yaklaşık 2-2.5 saat)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  0. HAZIRLIK (5 dk)                                         │
│     ├── Bilgilendirme ve onam formu                         │
│     └── Teknik kontrol (internet, tarayıcı)                 │
│                                                             │
│  1. YETKİNLİK DEĞERLENDİRME (20 dk)                        │
│     ├── Demografik bilgiler                                 │
│     ├── Teknik yetkinlik testi                              │
│     ├── Pedagojik yetkinlik testi                           │
│     └── Dreyfus seviye belirleme                            │
│          ↓                                                  │
│     [Sistem: UserVector oluşturma]                          │
│     [Sistem: Persona eşleştirme]                            │
│     [Sistem: İlk mod belirleme]                             │
│                                                             │
│  2. GÖREV DÖNGÜSÜ (6 × 15-20 dk = 90-120 dk)               │
│     ┌──────────────────────────────────────┐                │
│     │  Her görev için:                      │                │
│     │  a) Ön-test (3 dk)                   │                │
│     │  b) Görev açıklaması (2 dk)          │                │
│     │  c) AI persona ile çalışma (10-15 dk)│                │
│     │  d) Kod teslimi                       │                │
│     │  e) Son-test (3 dk)                  │                │
│     │  f) NASA-TLX (2 dk)                  │                │
│     │  g) Kısa değerlendirme (1 dk)        │                │
│     └──────────────────────────────────────┘                │
│          ↓                                                  │
│     [Sistem: NASA-TLX analizi]                              │
│     [Sistem: Sonraki görev için mod belirleme]              │
│                                                             │
│  3. FİNAL DEĞERLENDİRME (15 dk)                            │
│     ├── Final anketi                                        │
│     ├── Genel memnuniyet                                    │
│     └── Açık uçlu sorular                                   │
│                                                             │
│  4. KAPANIŞ (5 dk)                                          │
│     ├── Teşekkür                                            │
│     ├── Çekiliş/ödül bilgilendirme                          │
│     └── İletişim bilgileri                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Görev Dağılımı (Counterbalancing)

**6 Görev, 2 Mod:**
- Her katılımcı 3 görevde Similar, 3 görevde Complementary mod kullanır
- Mod sırası adaptif olarak belirlenir (NASA-TLX'e göre)
- İlk görev learning_goal'a göre atanır

**Görev Sırası:**
Tüm katılımcılar aynı sırada görevleri yapar (karmaşıklık artışı):
1. Görev 1: Düşük karmaşıklık
2. Görev 2: Orta karmaşıklık
3. Görev 3: Düşük karmaşıklık
4. Görev 4: Yüksek karmaşıklık
5. Görev 5: Orta karmaşıklık
6. Görev 6: Yüksek karmaşıklık

---

## 3.6 VERİ ANALİZİ

### Nicel Analiz

#### Betimsel İstatistikler
- Frekans, yüzde
- Ortalama, standart sapma, medyan
- Çarpıklık, basıklık

#### Karşılaştırma Testleri

| Hipotez | Test | Varsayım Kontrolü |
|---------|------|-------------------|
| Mod etkisi (within-subject) | Paired t-test | Normallik (Shapiro-Wilk) |
| Seviye etkisi (between-subject) | One-way ANOVA | Levene testi |
| Mod × Seviye etkileşimi | Two-way Mixed ANOVA | Box's M |
| Normal dağılım ihlali | Wilcoxon / Kruskal-Wallis | - |

#### Regresyon Analizleri
```
Model 1: Kod Kalitesi
Code_Quality = β₀ + β₁×Mode + β₂×Level + β₃×Domain + β₄×(Mode×Level) + ε

Model 2: Öğrenme Kazanımı
Learning_Gain = β₀ + β₁×Mode + β₂×Level + β₃×NASA_TLX + β₄×Pre_Score + ε

Model 3: Bilişsel Yük
NASA_TLX = β₀ + β₁×Mode + β₂×Level + β₃×Task_Complexity + β₄×Time + ε
```

#### Etki Büyüklüğü
- Cohen's d (t-test için)
- Eta-squared (η²) (ANOVA için)
- R² (Regresyon için)

**Yorumlama:**
| Metrik | Küçük | Orta | Büyük |
|--------|-------|------|-------|
| Cohen's d | 0.2 | 0.5 | 0.8 |
| η² | 0.01 | 0.06 | 0.14 |
| R² | 0.02 | 0.13 | 0.26 |

### Nitel Analiz

**Görüşme Verileri İçin:**
- Tematik analiz (Braun & Clarke, 2006)
- Kodlama: Açık → Eksensel → Seçici
- NVivo 12 yazılımı

**Açık Uçlu Anket Yanıtları:**
- İçerik analizi
- Frekans tabloları
- Kelime bulutu

---

## 3.7 GEÇERLİK VE GÜVENİRLİK

### İç Geçerlik

| Tehdit | Kontrol Stratejisi |
|--------|---------------------|
| Olgunlaşma | Kısa süre (2-2.5 saat), mola |
| Tarihsel | Standart ortam, aynı dönem |
| Test etkisi | Paralel formlar |
| Araç değişimi | Otomatik ölçüm, sabit rubrikler |
| Seçim | Tabakalı örnekleme, ön-test kontrolü |
| Deneysel kayıp | %10 yedek örneklem |

### Dış Geçerlik

| Boyut | Strateji |
|-------|----------|
| Popülasyon | Farklı seviyeler ve alanlar |
| Ekolojik | Doğal ortam (çevrimiçi), gerçek görevler |
| Zamansal | Çoklu oturum, farklı günler |

### Güvenirlik

| Araç | Güvenirlik Yöntemi | Hedef |
|------|---------------------|-------|
| Yetkinlik Testi | Cronbach's α | > 0.70 |
| NASA-TLX | Test-retest (pilot) | r > 0.80 |
| Kod Rubriği | Değerlendiriciler arası (Cohen's κ) | > 0.70 |
| Final Anketi | Cronbach's α | > 0.70 |

### Pilot Çalışma

**N = 15 katılımcı (3 seviye × 2 domain + 3 yedek)**

**Amaç:**
- Araçların anlaşılırlığını test etme
- Süre tahminlerini doğrulama
- Teknik sorunları tespit etme
- Güvenirlik hesaplama

---

## 3.8 ETİK HUSUSLAR

### Etik Kurul Onayı
- Üniversite Etik Kurulu başvurusu
- Onay tarihi ve numarası belirtilecek

### Bilgilendirilmiş Onam
```
Onam formunda belirtilen hususlar:
- Araştırmanın amacı
- Katılımın gönüllülüğü
- İstediği zaman çekilme hakkı
- Veri gizliliği ve anonimlik
- Beklenen süre
- Olası riskler ve faydalar
- İletişim bilgileri
```

### Veri Güvenliği
- Kişisel veriler şifrelenmiş saklanır
- Katılımcı ID ile anonimleştirme
- KVKK uyumu
- 5 yıl saklama, sonra imha

### Gizlilik
- IP adresi toplanmaz
- İsim yerine UUID
- Sonuçlar toplu raporlama

### Teşvik/Ödül
- Tüm katılımcılara sertifika
- Çekiliş ile hediye kartı (10 kişi × 200 TL)
- Araştırma özeti paylaşımı

---

## KULLANILACAK YAZILIMLAR

| Amaç | Yazılım |
|------|---------|
| Platform geliştirme | Python, Streamlit |
| LLM API | OpenAI GPT-4o |
| İstatistik analizi | SPSS 27, R 4.x |
| Nitel analiz | NVivo 12 |
| Güç analizi | G*Power 3.1 |
| Kod kalitesi | Pylint, Bandit, Radon |
| Versiyon kontrolü | Git, GitHub |
| Veri yönetimi | SQLite, PostgreSQL |

---

## ZAMAN ÇİZELGESİ

| Aşama | Süre | Detay |
|-------|------|-------|
| Platform geliştirme | 3 ay | Tamamlandı |
| Pilot çalışma | 1 ay | N=15 |
| Ana veri toplama | 3 ay | N=150 |
| Veri analizi | 2 ay | Nicel + Nitel |
| Raporlama | 2 ay | Tez yazımı |

---

## ÖRNEK PARAGRAFLAR

### Araştırma Deseni Örneği
> Bu araştırmada karma yöntem (mixed methods) araştırma deseni kullanılmıştır (Creswell & Plano Clark, 2018). Araştırmanın nicel boyutu, 2×5 faktöriyel deneysel desen ile tasarlanmıştır. Birinci bağımsız değişken olan öneri modu (benzerlik ve tamamlayıcılık) within-subject faktör olarak, ikinci bağımsız değişken olan Dreyfus yetkinlik seviyesi (acemi, ileri başlangıç, yetkin, usta, uzman) between-subject faktör olarak ele alınmıştır.

### Örneklem Örneği
> Araştırmanın çalışma grubunu, Türkiye'deki üniversiteler ve eğitim teknolojisi şirketlerinden amaçlı ve tabakalı örnekleme yöntemiyle seçilen 150 katılımcı oluşturmaktadır. G*Power 3.1 yazılımı ile yapılan güç analizi, orta düzey etki büyüklüğü (f=0.25), %5 anlamlılık düzeyi ve %80 güç için minimum 107 katılımcı gerektiğini göstermiştir. Olası katılımcı kaybı göz önünde bulundurularak örneklem büyüklüğü 150 olarak belirlenmiştir.

---

*Bu rehber, PITL doktora tezi yöntem bölümü yazımı için Claude'a verilecek referans belgesidir.*
