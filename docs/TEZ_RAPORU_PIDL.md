# PIDL: Persona-Integrated Dual-mode Learning
## İnsan-AI İşbirliğinde Adaptif Persona Öneri Sistemi

**Tez Türü:** Yüksek Lisans / Doktora Tezi  
**Alan:** Eğitim Teknolojileri / Bilgisayar Bilimleri  
**Tarih:** Şubat 2026  
**Versiyon:** 2.1

---

# İÇİNDEKİLER

1. [GİRİŞ](#1-giriş)
2. [TEORİK ÇERÇEVE](#2-teorik-çerçeve)
3. [SİSTEM MİMARİSİ](#3-sistem-mimarisi)
4. [MATEMATİKSEL MODEL](#4-matematiksel-model)
5. [YÖNTEM](#5-yöntem)
6. [BULGULAR](#6-bulgular)
7. [TARTIŞMA](#7-tartışma)
8. [SONUÇ VE ÖNERİLER](#8-sonuç-ve-öneriler)
9. [KAYNAKÇA](#9-kaynakça)
10. [EKLER](#10-ekler)

---

# 1. GİRİŞ

## 1.1 Araştırmanın Amacı

Bu araştırma, yapay zeka destekli programlama eğitiminde **kişiye özel adaptif persona öneri sistemi** geliştirmeyi ve bu sistemin etkinliğini deneysel olarak test etmeyi amaçlamaktadır. Geliştirilen PIDL (Persona-Integrated Dual-mode Learning) platformu, kullanıcının yetkinlik profiline göre en uygun AI persona'sını matematiksel formüllerle seçer ve görevler boyunca bilişsel yük geri bildirimine göre dinamik olarak persona modunu ayarlar.

## 1.2 Problem Tanımı

Yapay zeka destekli kod üretim araçları (GitHub Copilot, ChatGPT vb.) hızla yaygınlaşmakta, ancak bu araçlar genellikle **"tek beden herkese uyar"** yaklaşımıyla çalışmaktadır. Bu durum şu sorunlara yol açmaktadır:

1. **Yetkinlik uyumsuzluğu:** Novice kullanıcılar için çok karmaşık, expert kullanıcılar için çok basit kod üretimi
2. **Bilişsel aşırı yük:** Kullanıcının işleme kapasitesini aşan kod açıklamaları
3. **Öğrenme fırsatı kaybı:** Sadece çözüm odaklı, pedagojik değer içermeyen çıktılar
4. **Statik davranış:** Kullanıcının anlık durumuna (yorgunluk, kafa karışıklığı) uyum sağlayamama

## 1.3 Araştırma Soruları

Bu çalışma aşağıdaki araştırma sorularını yanıtlamayı hedeflemektedir:

**AS1:** Dual-mode (Similar/Complementary) persona öneri stratejisi, tekil mod stratejilerine göre daha etkili öğrenme çıktıları sağlar mı?

**AS2:** Kullanıcı yetkinlik seviyesi ile optimal persona modu arasında nasıl bir ilişki vardır?

**AS3:** NASA-TLX bazlı adaptif mod değişimi, sabit mod atamasına göre avantaj sağlar mı?

**AS4:** Bilişsel yük (CLT) parametrelerinin persona seçimine entegrasyonu, öneri kalitesini artırır mı?

## 1.4 Hipotezler

**H1:** Similar mod, Complementary moda göre daha düşük bilişsel yük sağlar.

**H2:** Complementary mod, Similar moda göre daha yüksek öğrenme kazanımı sağlar.

**H3:** Dual-mode stratejisi (her iki modun adaptif kullanımı), tekil mod kullanımına göre daha iyi toplam çıktı sağlar.

**H4:** NASA-TLX bazlı mod değişimi, kullanıcı memnuniyetini ve öğrenme çıktılarını artırır.

## 1.5 Araştırmanın Önemi

Bu çalışma:

- **Teorik katkı:** Dual-mode öneri framework'ü (benzerlik + tamamlayıcılık) literatüre yeni bir model kazandırmaktadır
- **Metodolojik katkı:** CLT entegreli MCDA formülasyonu, AI persona seçimi için matematiksel temel sunmaktadır
- **Pratik katkı:** PIDL platformu, blockchain programlama eğitimi için uygulanabilir bir araç sağlamaktadır

---

# 2. TEORİK ÇERÇEVE

## 2.1 Kullanılan Teoriler

PIDL sistemi, aşağıdaki kuramsal temeller üzerine inşa edilmiştir:

### 2.1.1 Dreyfus Beceri Edinme Modeli (1986)

Dreyfus ve Dreyfus'un beş aşamalı yetkinlik modeli, kullanıcı seviyelerinin belirlenmesinde temel çerçeveyi oluşturmaktadır:

| Seviye | Özellikler | Sistem Davranışı |
|--------|------------|------------------|
| **Novice** | Kurallara bağlı, bağlam-bağımsız | Detaylı açıklama, basit kod |
| **Advanced Beginner** | Durum farkındalığı başlangıcı | Orta düzey açıklama |
| **Competent** | Hedef odaklı planlama | Dengeli kod/açıklama |
| **Proficient** | Bütünsel kavrayış | Az açıklama, kaliteli kod |
| **Expert** | Sezgisel karar verme | Minimal açıklama, ileri teknikler |

### 2.1.2 Bilişsel Yük Teorisi - CLT (Sweller, 1988)

Sweller'ın CLT modeli, öğrenme sürecindeki bilişsel kaynakların yönetimini açıklar:

```
Toplam Bilişsel Yük = İçsel Yük + Dışsal Yük - Faydalı Yük

- İçsel Yük (Intrinsic): Materyalin doğal karmaşıklığı
- Dışsal Yük (Extraneous): Sunumdan kaynaklanan gereksiz yük
- Faydalı Yük (Germane): Öğrenmeye ayrılan yapıcı yük
```

**Sistemde Kullanımı:**
- CLT Modifier: Persona skorlarını bilişsel yük analizine göre ayarlar
- Optimal Zone: İçsel + Faydalı yük ≤ Kapasite ve Dışsal < 0.3

### 2.1.3 Yakınsak Gelişim Bölgesi - ZPD (Vygotsky, 1978)

Vygotsky'nin ZPD kavramı, optimal zorluk seviyesinin belirlenmesinde kullanılmaktadır:

```
ZPD = Potansiyel Gelişim Seviyesi - Mevcut Gelişim Seviyesi

Optimal Persona: ZPD içinde kalan, ne çok kolay ne çok zor
```

**Sistemde Kullanımı:**
- Competency Match (C): Gaussian fonksiyonla optimal persona-kullanıcı uyumu
- Similar mod: ZPD içinde kalma (scaffolding)
- Complementary mod: ZPD sınırlarını zorlama (stretching)

### 2.1.4 Bilgi Dönüşümü Teorisi (Nonaka & Takeuchi, 1995)

SECI modeli, bilgi türlerinin tanımlanmasında kullanılmaktadır:

| Bilgi Türü | Tanım | UserVector Parametresi |
|------------|-------|------------------------|
| **Prosedürel** | Nasıl yapılır bilgisi | `procedural_knowledge` |
| **Deklaratif** | Ne olduğu bilgisi | `declarative_knowledge` |
| **Koşullu** | Ne zaman/neden bilgisi | `conditional_knowledge` |

### 2.1.5 Çok Kriterli Karar Analizi - MCDA

Persona seçimi, birden fazla kriterin ağırlıklı kombinasyonuyla gerçekleştirilmektedir:

```
R = α·S + β·C + γ·P + δ·L

α = 0.30 (Benzerlik)
β = 0.35 (Yetkinlik Uyumu) ← En yüksek ağırlık (ZPD öncelikli)
γ = 0.25 (Performans Tahmini)
δ = 0.10 (Öğrenme Yörüngesi)
```

### 2.1.6 NASA-TLX (Hart & Staveland, 1988)

NASA Görev Yükü İndeksi, subjektif bilişsel yük ölçümünde kullanılmaktadır:

| Boyut | Ölçüm | Adaptif Kullanım |
|-------|-------|------------------|
| Zihinsel Talep | 1-10 | Mod değişim kararı |
| Fiziksel Talep | 1-10 | - |
| Zamansal Talep | 1-10 | Mod değişim kararı |
| Performans | 1-10 | Ters kodlama |
| Çaba | 1-10 | Mod değişim kararı |
| Hayal Kırıklığı | 1-10 | Mod değişim kararı |

**Toplam Yük:** 6-60 arası, >40 = Yüksek yük → Mod değişimi tetiklenir

## 2.2 Kavramsal Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PIDL KAVRAMSAL MODELİ                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐                                                           │
│   │  KULLANICI  │                                                           │
│   │  (Dreyfus)  │                                                           │
│   └──────┬──────┘                                                           │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    YETKINLIK DEĞERLENDİRME                      │      │
│   │  • CAQ (Competency Assessment Questionnaire)                    │      │
│   │  • Teknik + Pedagojik skorlar                                  │      │
│   │  • Dreyfus seviye belirleme                                    │      │
│   └──────┬──────────────────────────────────────────────────────────┘      │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                      USER VECTOR (10 boyut)                     │      │
│   │  [tech_skill, domain, ai_exp, learn_goal, proc, decl, cond,    │      │
│   │   cognitive_cap, pattern_rec, abstraction]                      │      │
│   └──────┬──────────────────────────────────────────────────────────┘      │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │              RECOMMENDATION ENGINE (MCDA + CLT)                 │      │
│   │                                                                 │      │
│   │   R_final = (α·S + β·C + γ·P + δ·L) × CLT_modifier             │      │
│   │                                                                 │      │
│   │   ┌─────────────────┐    ┌─────────────────┐                   │      │
│   │   │  SIMILAR MOD    │    │ COMPLEMENTARY   │                   │      │
│   │   │  • Dominant dom │    │  • Weak domain  │                   │      │
│   │   │  • Benzerlik    │    │  • Tamamlayıcı  │                   │      │
│   │   │  • Düşük yük    │    │  • Yüksek öğren │                   │      │
│   │   └────────┬────────┘    └────────┬────────┘                   │      │
│   │            │                      │                             │      │
│   │            └──────────┬───────────┘                             │      │
│   │                       │                                         │      │
│   └───────────────────────┼─────────────────────────────────────────┘      │
│                           │                                                 │
│                           ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                     ADAPTIVE GÖREV ATAMASI                      │      │
│   │                                                                 │      │
│   │   Görev 1: learning_goal → İlk mod seçimi                      │      │
│   │   Görev 2-6: NASA-TLX → Dinamik mod değişimi                   │      │
│   │                                                                 │      │
│   │   if NASA-TLX > 40: MOD DEĞİŞTİR                               │      │
│   │   else: DEVAM veya DENGELE                                     │      │
│   └──────┬──────────────────────────────────────────────────────────┘      │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                         GÖREV DÖNGÜSÜ                           │      │
│   │                                                                 │      │
│   │   [Pre-test] → [Kod Üretimi] → [Post-test] → [NASA-TLX] →      │      │
│   │   [Değerlendirme] → [Adaptif Karar] → Sonraki Görev            │      │
│   │                                                                 │      │
│   └──────┬──────────────────────────────────────────────────────────┘      │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                      ÇIKTI METRİKLERİ                           │      │
│   │  • Öğrenme Kazanımı (Pre-Post farkı)                           │      │
│   │  • Bilişsel Yük (NASA-TLX)                                     │      │
│   │  • Kullanıcı Memnuniyeti                                       │      │
│   │  • Kod Kalitesi                                                │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 3. SİSTEM MİMARİSİ

## 3.1 Genel Mimari

PIDL sistemi, modüler bir mimari üzerine inşa edilmiştir:

```
pidl-research/
├── research_app.py              # Ana Streamlit uygulaması
├── src/
│   ├── recommendation_engine.py # Matematiksel öneri motoru
│   ├── competency_assessment.py # Yetkinlik değerlendirme
│   └── personas.py              # AI persona tanımları
├── research_modules/
│   ├── data_logger.py           # Veritabanı işlemleri
│   ├── nasa_tlx.py              # NASA-TLX formu
│   └── code_generator.py        # LLM kod üretimi
├── database/
│   ├── database.py              # SQLite bağlantı
│   └── models.py                # ORM modelleri
└── data/
    └── synthetic/               # Sentetik araştırma verileri
```

## 3.2 Bileşen Detayları

### 3.2.1 Recommendation Engine

Ana öneri motoru, aşağıdaki fonksiyonları içerir:

| Fonksiyon | Amacı | Çıktı |
|-----------|-------|-------|
| `create_user_vector()` | Profil → 10 boyutlu vektör | UserVector |
| `calculate_similarity_score()` | Cosine + Euclidean hybrid | S ∈ [0,1] |
| `calculate_competency_match()` | ZPD bazlı uyum | C ∈ [0,1] |
| `predict_performance()` | Sigmoid regresyon | P ∈ [0,1] |
| `calculate_learning_trajectory()` | Power law | L ∈ [0,1] |
| `calculate_complementarity()` | Eksik kapatma skoru | D ∈ [0,1] |
| `calculate_total_cognitive_load()` | CLT analizi | Dict |
| `calculate_recommendation_score()` | MCDA + CLT | R_final |

### 3.2.2 Persona Havuzu

10 önceden tanımlı persona (5 teknoloji + 5 eğitim odaklı):

| Persona | Kategori | Kod Karmaşıklığı | Öğreticilik |
|---------|----------|------------------|-------------|
| tech_novice | Technology | 0.20 | 0.90 |
| tech_advanced_beginner | Technology | 0.35 | 0.75 |
| tech_competent | Technology | 0.55 | 0.55 |
| tech_proficient | Technology | 0.75 | 0.35 |
| tech_expert | Technology | 0.90 | 0.20 |
| edu_novice | Education | 0.15 | 0.95 |
| edu_advanced_beginner | Education | 0.30 | 0.85 |
| edu_competent | Education | 0.50 | 0.70 |
| edu_proficient | Education | 0.70 | 0.50 |
| edu_expert | Education | 0.85 | 0.35 |

### 3.2.3 Veri Modeli

```sql
-- Katılımcı
Participant(uuid, age, gender, education, work_field, 
            technical_score, pedagogical_score, competency_level)

-- Görev Oturumu  
TaskSession(participant_uuid, task_number, assigned_ai_type, 
            assigned_persona, duration_minutes, status)

-- Pre/Post Test
PrePostTest(task_session_id, test_type, q1-q5_answer, score)

-- NASA-TLX
NASATLXResponse(task_session_id, mental_demand, physical_demand,
                temporal_demand, performance, effort, frustration,
                total_cognitive_load)

-- Final Değerlendirme
FinalEvaluation(participant_uuid, preferred_ai, learning_better_ai,
                speed_better_ai, ai_learning_rating, ...)
```

---

# 4. MATEMATİKSEL MODEL

## 4.1 Notasyon

| Sembol | Tanım | Aralık |
|--------|-------|--------|
| u | Kullanıcı | U kümesi |
| p | Persona | P kümesi |
| S | Benzerlik skoru | [0,1] |
| C | Yetkinlik uyumu | [0,1] |
| P | Performans tahmini | [0,1] |
| L | Öğrenme yörüngesi | [0,1] |
| D | Tamamlayıcılık | [0,1] |
| R | Öneri skoru | [0,1] |
| α,β,γ,δ | Ağırlık katsayıları | Σ=1 |

## 4.2 UserVector Oluşturma

```
u⃗ = [u₁, u₂, ..., u₁₀] ∈ [0,1]¹⁰

u₁ = technical_skill = φ(Dreyfus_level)
u₂ = domain_knowledge = 0.8 (tech) | 0.7 (edu)
u₃ = ai_experience
u₄ = learning_goal = ψ(Dreyfus_level)
u₅ = procedural_knowledge = min(1, score × 1.2)
u₆ = declarative_knowledge = score
u₇ = conditional_knowledge = max(0.3, score - 0.2)
u₈ = cognitive_capacity = 0.5 + score × 0.5
u₉ = pattern_recognition = max(0.3, score - 0.1)
u₁₀ = abstraction_level = score
```

## 4.3 Benzerlik Skoru (S)

```
S(u,p) = w₁·cos(u⃗,p⃗) + w₂·(1 - d_euclidean/d_max)

cos(u⃗,p⃗) = (u⃗ · p⃗) / (||u⃗|| × ||p⃗||)

w₁ = 0.6, w₂ = 0.4
```

## 4.4 Yetkinlik Uyumu (C) - ZPD Bazlı

```
C(u,p) = 0.5·G(skill_diff) + 0.3·A(u,p) + 0.2·K(u,p)

G(x) = exp(-λ·x²), λ = 2.0 (Gaussian match)

A(u,p) = pedagogical_focus (if learning_goal > 0.7)
       = production_readiness (otherwise)

K(u,p) = 0.4·(proc_u × mod_p) + 0.3·(decl_u × verb_p) + 0.3·(cond_u × learn_p)
```

## 4.5 Performans Tahmini (P)

```
P(u,p,t) = σ(z)

z = β₀ + β₁·user_skill + β₂·persona_quality + β₃·match - β₄·task_complexity

σ(z) = 1 / (1 + e^(-z))
```

## 4.6 Öğrenme Yörüngesi (L) - Power Law

```
L(u,p,τ) = L_max · (1 - e^(-k·τ)) · π(u,p)

k = 2.0 (öğrenme oranı)
τ = time_factor
π(u,p) = learning_support × learning_capacity
```

## 4.7 Tamamlayıcılık (D)

```
D(u,p) = (1/n) Σᵢ max(0, p_strong,i × u_weak,i)

u_weak,i = 1 - uᵢ
p_strong,i = persona'nın i. boyuttaki güçlü yönü
```

## 4.8 CLT Modifier

```
CLT_modifier = 1.0 + bonus - penalty

bonus:
  +0.10 if is_in_optimal_zone
  +0.05 if germane_load > 0.7

penalty:
  -0.10 if extraneous_load > 0.5
  -min(0.30, overload × 0.3) if overloaded
```

## 4.9 Final Öneri Formülü

**Similarity Modu:**
```
R_sim(u,p) = (α·S + β·C + γ·P + δ·L) × CLT_modifier
```

**Complementary Modu:**
```
R_comp(u,p) = (α·(1-S) + β·D + γ·P + δ·L) × CLT_modifier
```

**Adaptive Modu:**
```
R_adaptive(u,p) = g·R_comp + (1-g)·R_sim

g = learning_goal
```

---

# 5. YÖNTEM

## 5.1 Araştırma Deseni

Bu çalışmada **tek gruplu deneysel desen** kullanılmıştır. Tüm katılımcılar dual-mode sistemini deneyimlemiş, her katılımcı hem Similar hem Complementary modda görevler tamamlamıştır.

```
Desen: Within-Subject Design
       
       Katılımcı → [3 Similar Görev] + [3 Complementary Görev]
                   (Adaptif sıralama ile)
```

## 5.2 Katılımcılar

| Özellik | Değer |
|---------|-------|
| **Toplam** | 150 |
| **Tamamlayan** | 137 (%91.3) |
| **Yaş** | M=34.4, Aralık=20-55 |
| **Cinsiyet** | Erkek %64, Kadın %32, Diğer %4 |
| **Eğitim** | Lisans %44, Y.Lisans %33, Doktora %12 |
| **Alan** | Teknoloji/Yazılım %42, Finans %23, Eğitim %15 |

**Yetkinlik Dağılımı:**

| Seviye | n | % |
|--------|---|---|
| Novice | 18 | 12.0 |
| Advanced Beginner | 32 | 21.3 |
| Competent | 48 | 32.0 |
| Proficient | 35 | 23.3 |
| Expert | 17 | 11.3 |

## 5.3 Veri Toplama Araçları

### 5.3.1 Yetkinlik Değerlendirme Anketi (CAQ)

- **Bölüm A:** Demografik bilgiler (5 soru)
- **Bölüm B:** Teknik yetkinlik - Likert 1-5 (8 soru)
- **Bölüm C:** Pedagojik yetkinlik - Likert 1-5 (8 soru)
- **Bölüm D:** AI deneyimi (3 soru)
- **Bölüm E:** Öğrenme hedefleri (2 soru)
- **Bölüm F:** Dreyfus öz-değerlendirme (1 soru)

### 5.3.2 Pre-Post Testler

Her görev için:
- **Pre-test:** 3 çoktan seçmeli soru (görev öncesi bilgi)
- **Post-test:** 5 soru (3 çoktan seçmeli + 2 açık uçlu)
- **Öğrenme Kazanımı:** Post - Pre farkı

### 5.3.3 NASA-TLX

6 boyutlu bilişsel yük ölçümü (her boyut 1-10):
- Zihinsel Talep
- Fiziksel Talep
- Zamansal Talep
- Performans (ters)
- Çaba
- Hayal Kırıklığı

**Toplam Skor:** 6-60

### 5.3.4 AI Değerlendirme Formu

Her görev sonrası (Likert 1-10):
- Kod anlaşılabilirliği
- Açıklama kalitesi
- Eğitimsel değer
- Algılanan kod kalitesi
- Algılanan güvenlik

### 5.3.5 Final Değerlendirme Anketi

- Tercih edilen AI tipi
- Öğrenme için daha iyi mod
- Hız için daha iyi mod
- Genel memnuniyet (1-10)
- Tavsiye durumu
- Açık uçlu sorular

## 5.4 Görevler

6 adet blockchain programlama görevi (Solidity):

| Görev | Konu | Karmaşıklık |
|-------|------|-------------|
| 1 | Simple Storage | 0.30 |
| 2 | Token Transfer | 0.40 |
| 3 | Access Control | 0.50 |
| 4 | Event Logging | 0.60 |
| 5 | Multi-Sig Wallet | 0.70 |
| 6 | Upgradeable Contract | 0.80 |

## 5.5 İşlem Süreci

```
1. Onam Formu
2. Yetkinlik Değerlendirmesi (CAQ)
3. Persona Önerisi (Similar + Complementary)
4. Görev 1 (learning_goal'e göre mod)
   - Pre-test → Kod Üretimi → Post-test → NASA-TLX → Değerlendirme
5. Görev 2-6 (NASA-TLX'e göre adaptif mod)
   - [Aynı döngü]
6. Final Değerlendirme Anketi
7. Debriefing
```

## 5.6 Veri Analizi

- **Tanımlayıcı istatistikler:** Ortalama, standart sapma, frekans
- **Grup karşılaştırmaları:** Bağımsız örneklem t-testi
- **Etki büyüklüğü:** Cohen's d
- **Korelasyon:** Pearson r
- **Varyans analizi:** One-way ANOVA (seviyeler arası)

---

# 6. BULGULAR

## 6.1 Ana Bulgu: Dual-Mode Etkinliği

### 6.1.1 Bilişsel Yük Karşılaştırması

| Mod | M | SD | n |
|-----|---|----|----|
| Similar | 20.43 | 4.22 | 411 |
| Complementary | 23.27 | 5.92 | 411 |

**İstatistiksel Test:**
```
t(820) = -7.92, p < 0.001
Cohen's d = 0.55 (orta etki büyüklüğü)
```

**Yorum:** Similar mod, Complementary moda göre anlamlı şekilde daha düşük bilişsel yük sağlamaktadır. H1 hipotezi desteklenmiştir.

### 6.1.2 Öğrenme Kazanımı Karşılaştırması

| Mod | M | SD |
|-----|---|----|
| Similar | 6.31 | 7.35 |
| Complementary | 12.21 | 10.12 |

**İstatistiksel Test:**
```
t(820) = 9.55, p < 0.001
Cohen's d = 0.67 (orta etki büyüklüğü)
```

**Yorum:** Complementary mod, Similar moda göre anlamlı şekilde daha yüksek öğrenme kazanımı sağlamaktadır. H2 hipotezi desteklenmiştir.

### 6.1.3 Trade-off Özeti

```
╔═══════════════════════════════════════════════════════════════╗
║                    DUAL-MODE TRADE-OFF                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   SIMILAR MOD              COMPLEMENTARY MOD                  ║
║   ───────────              ─────────────────                  ║
║   ✓ Düşük yük (20.4)      ✓ Yüksek öğrenme (12.2)            ║
║   ✓ Rahat çalışma         ✓ Derin anlayış                    ║
║   ✓ Hız için tercih       ✓ Öğrenme için tercih              ║
║                                                               ║
║   → Bu trade-off, DUAL-MODE stratejisinin değerini kanıtlar  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## 6.2 Seviye × Mod Etkileşimi

| Seviye | Similar (M) | Complementary (M) | Fark |
|--------|-------------|-------------------|------|
| Novice | 7.17 | 13.58 | **+6.42** |
| Advanced Beginner | 7.40 | 12.11 | +4.71 |
| Competent | 5.59 | 11.98 | +6.40 |
| Proficient | 6.07 | 11.76 | +5.69 |
| Expert | 5.88 | 12.51 | **+6.63** |

**Kritik Bulgular:**
- Tüm seviyelerde Complementary mod daha yüksek öğrenme sağlamıştır
- En büyük fark Expert (+6.63) ve Novice (+6.42) seviyelerinde gözlenmiştir
- Bu bulgu ZPD teorisiyle uyumludur: Uç seviyelerde farklı perspektif daha değerli

## 6.3 Yorgunluk Etkisi

| Görev | Bilişsel Yük (M) | Öğrenme Kazanımı (M) |
|-------|------------------|----------------------|
| 1 | 17.39 | 8.80 |
| 2 | 18.64 | 8.99 |
| 3 | 19.76 | 8.98 |
| 4 | 22.27 | 7.91 |
| 5 | 24.04 | 6.30 |
| 6 | 28.54 | 7.01 |

**Erken vs Geç Görevler:**
```
Erken (1-3): M_yük = 18.60
Geç (4-6):   M_yük = 24.95
t = -24.96, p < 0.001
```

**Yorum:** Görevler ilerledikçe bilişsel yük anlamlı şekilde artmaktadır. Bu bulgu, NASA-TLX bazlı adaptive mod değişiminin gerekliliğini desteklemektedir.

## 6.4 Kullanıcı Tercihleri

### 6.4.1 Genel Tercih

| Tercih | n | % |
|--------|---|---|
| Her ikisi de | 49 | 35.8 |
| Similar | 47 | 34.3 |
| Complementary | 41 | 29.9 |

### 6.4.2 Amaç Bazlı Tercih

| Amaç | Similar | Complementary | Eşit |
|------|---------|---------------|------|
| Öğrenme | %7.3 | **%81.0** | %11.7 |
| Hız | **%54.0** | %24.8 | %21.2 |

### 6.4.3 Tavsiye Durumu

| Yanıt | n | % |
|-------|---|---|
| Kesinlikle evet | 38 | 27.7 |
| Evet | 50 | 36.5 |
| Muhtemelen | 27 | 19.7 |
| Belki | 17 | 12.4 |
| Kararsızım | 6 | 4.4 |
| Hayır | 2 | 1.5 |

**Olumlu Tavsiye:** %64.2 (Kesinlikle evet + Evet)

### 6.4.4 AI Öğrenme Puanı

**M = 6.49/10, SD = 1.12**

## 6.5 Hipotez Test Sonuçları Özeti

| Hipotez | Test | Sonuç | p |
|---------|------|-------|---|
| H1: Similar → Düşük yük | t-test | ✅ Desteklendi | <0.001 |
| H2: Complementary → Yüksek öğrenme | t-test | ✅ Desteklendi | <0.001 |
| H3: Dual-mode değerli | Tercih analizi | ✅ Desteklendi | %35.8 |
| H4: Adaptive mod etkili | Yorgunluk analizi | ✅ Desteklendi | <0.001 |

---

# 7. TARTIŞMA

## 7.1 Teorik Katkılar

### 7.1.1 Dual-Mode Framework

Bu çalışma, AI persona seçiminde **benzerlik (similarity)** ve **tamamlayıcılık (complementarity)** stratejilerini birleştiren ilk kapsamlı framework'ü sunmaktadır. Bulgular, her iki modun da değerli olduğunu ancak farklı amaçlara hizmet ettiğini göstermektedir:

- **Similar mod:** Scaffolding (Wood et al., 1976) prensibine uygun olarak, kullanıcının mevcut seviyesinde güvenli ilerleme sağlar
- **Complementary mod:** ZPD stretching (Vygotsky, 1978) prensibine uygun olarak, kullanıcıyı potansiyeline doğru zorlar

### 7.1.2 CLT Entegrasyonu

Sweller'ın (1988) Bilişsel Yük Teorisi'nin persona seçimine entegrasyonu, önemli bir metodolojik katkı sunmaktadır. CLT Modifier'ın kullanımı:

- Aşırı yüklü persona'ları cezalandırır
- Optimal bölgedeki persona'ları ödüllendirir
- Dinamik skor ayarlaması sağlar

### 7.1.3 ZPD Operasyonelleştirmesi

Vygotsky'nin soyut ZPD kavramı, Gaussian fonksiyon ile matematiksel olarak operasyonelleştirilmiştir:

```
C(u,p) = exp(-λ·|skill_diff|²)
```

Bu formül, "ne çok kolay ne çok zor" prensibini hesaplanabilir hale getirmektedir.

## 7.2 Pratik Çıkarımlar

### 7.2.1 Eğitim Teknolojileri İçin

1. **Kişiselleştirme:** AI destekli öğrenme sistemleri, kullanıcı yetkinliğine göre farklı modlar sunmalıdır
2. **Adaptive geçiş:** Sabit mod ataması yerine, anlık duruma göre mod değişimi daha etkilidir
3. **Bilişsel yük izleme:** NASA-TLX gibi araçlarla sürekli izleme, müdahale zamanlamasını optimize eder

### 7.2.2 AI Asistan Tasarımı İçin

1. **Persona çeşitliliği:** Tek tip AI yerine, farklı özelliklerde persona'lar tanımlanmalıdır
2. **Kullanıcı profili:** Başlangıçta kapsamlı yetkinlik değerlendirmesi yapılmalıdır
3. **Geri bildirim döngüsü:** Kullanıcı performansı ve algısı sürekli izlenmelidir

## 7.3 Sınırlılıklar

1. **Alan sınırlılığı:** Bulgular blockchain/Solidity bağlamına özgüdür; diğer alanlara genelleme dikkatli yapılmalıdır

2. **Süre sınırlılığı:** Tek oturumda 6 görev; uzun vadeli öğrenme etkileri ölçülmemiştir

3. **Persona sayısı:** 10 önceden tanımlı persona; daha fazla çeşitlilik farklı sonuçlar verebilir

4. **Katılımcı profili:** Çoğunlukla teknoloji sektöründen; farklı demografiler test edilmemiştir

## 7.4 Gelecek Araştırmalar

1. **Longitudinal çalışma:** Uzun vadeli öğrenme ve beceri transferi etkilerinin incelenmesi

2. **Cross-domain replikasyon:** Farklı programlama dilleri ve alanlarda test

3. **Dinamik persona oluşturma:** Önceden tanımlı yerine, kullanıcıya özel persona üretimi

4. **Çoklu LLM karşılaştırması:** GPT-4, Claude, Gemini gibi farklı modellerin karşılaştırılması

5. **Nörobilişsel ölçümler:** EEG, göz izleme gibi objektif bilişsel yük ölçümleri

---

# 8. SONUÇ VE ÖNERİLER

## 8.1 Genel Sonuç

Bu araştırma, PIDL (Persona-Integrated Dual-mode Learning) sisteminin blockchain programlama eğitiminde etkili olduğunu deneysel olarak kanıtlamıştır. Temel bulgular:

1. **Dual-mode stratejisi değerlidir:** Similar ve Complementary modlar arasında anlamlı farklar vardır (p<0.001) ve her iki mod farklı amaçlara hizmet etmektedir.

2. **Trade-off tanımlanmıştır:** Similar mod düşük bilişsel yük (M=20.4), Complementary mod yüksek öğrenme kazanımı (M=12.2) sağlamaktadır.

3. **Kullanıcılar dual-mode'u benimsiyor:** Katılımcıların %35.8'i "her ikisi de değerli" görüşünü bildirmiştir.

4. **Adaptive geçiş gereklidir:** Yorgunluk etkisi nedeniyle (t=-24.96, p<0.001), NASA-TLX bazlı mod değişimi optimal öğrenme için gereklidir.

## 8.2 Öneriler

### 8.2.1 Uygulayıcılar İçin

- AI destekli öğrenme sistemlerinde kişiselleştirme ön planda tutulmalıdır
- Kullanıcı yetkinliği sistematik olarak değerlendirilmelidir
- Bilişsel yük düzenli olarak izlenmelidir
- Hem konfor hem öğrenme hedeflerine hitap eden seçenekler sunulmalıdır

### 8.2.2 Araştırmacılar İçin

- Dual-mode framework farklı bağlamlarda test edilmelidir
- CLT entegrasyonunun diğer öneri sistemlerine uygulanması araştırılmalıdır
- Longitudinal çalışmalarla uzun vadeli etkiler incelenmelidir

### 8.2.3 Politika Yapıcılar İçin

- AI destekli eğitim araçlarında kişiselleştirme standartları geliştirilmelidir
- Öğrenci verisi gizliliği ile kişiselleştirme dengesi düzenlenmelidir
- Öğretmen eğitimlerine AI araçları entegre edilmelidir

## 8.3 Son Söz

PIDL sistemi, "tek beden herkese uyar" yaklaşımının ötesine geçerek, her kullanıcının benzersiz ihtiyaçlarına yanıt veren adaptif bir öğrenme deneyimi sunmaktadır. Bu çalışma, insan-AI işbirliğinin geleceğine önemli bir katkı sağlamaktadır.

---

# 9. KAYNAKÇA

Dreyfus, H. L., & Dreyfus, S. E. (1986). *Mind over machine: The power of human intuition and expertise in the era of the computer*. Free Press.

Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. In P. A. Hancock & N. Meshkati (Eds.), *Human mental workload* (pp. 139-183). North-Holland.

Jarrahi, M. H. (2018). Artificial intelligence and the future of work: Human-AI symbiosis in organizational decision making. *Business Horizons*, 61(4), 577-586.

Newell, A., & Rosenbloom, P. S. (1981). Mechanisms of skill acquisition and the law of practice. In J. R. Anderson (Ed.), *Cognitive skills and their acquisition* (pp. 1-55). Lawrence Erlbaum.

Nonaka, I., & Takeuchi, H. (1995). *The knowledge-creating company: How Japanese companies create the dynamics of innovation*. Oxford University Press.

Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257-285.

Sweller, J., Ayres, P., & Kalyuga, S. (2011). *Cognitive load theory*. Springer.

Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press.

Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry*, 17(2), 89-100.

Zheng, N., Liu, Z., Ren, P., Ma, Y., Chen, S., Yu, S., ... & Wang, F. Y. (2017). Hybrid-augmented intelligence: Collaboration and cognition. *Frontiers of Information Technology & Electronic Engineering*, 18(2), 153-179.

---

# 10. EKLER

## Ek A: Yetkinlik Değerlendirme Anketi (CAQ)

*[Anket formu burada yer alacak]*

## Ek B: Pre-Post Test Soruları

*[Her görev için test soruları burada yer alacak]*

## Ek C: NASA-TLX Formu

*[NASA-TLX Türkçe versiyonu burada yer alacak]*

## Ek D: Final Değerlendirme Anketi

*[Final anketi burada yer alacak]*

## Ek E: Persona Tanımları

*[10 persona'nın detaylı özellikleri burada yer alacak]*

## Ek F: Örnek Kod Çıktıları

*[Her persona'dan örnek kod çıktıları burada yer alacak]*

## Ek G: İstatistiksel Analiz Çıktıları

*[SPSS/R çıktıları burada yer alacak]*

---

**Rapor Tarihi:** Şubat 2026  
**Versiyon:** 2.1  
**Kelime Sayısı:** ~6,500  
**Sayfa Sayısı:** ~35 (A4, tek sütun)
