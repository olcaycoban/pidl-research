# PITL Sistemi - Literatür Taraması Rehberi
## Doktora Tezi: İnsan-Yapay Zeka İşbirliğinde Yetkinlik Tabanlı Persona Eşleştirme

---

## 1. SİSTEMİN GENEL TANIMI

### 1.1 PITL Nedir?
**PITL (Persona In The Loop)** - Döngüde Persona yaklaşımı, kullanıcının yetkinlik profiline göre optimal yapay zeka personası öneren çift modlu uyarlanabilir bir sistemdir.

**Temel Fark:** Geleneksel "Human in the Loop" yaklaşımından farklı olarak, PITL'de yapay zeka tek tip değil, kullanıcıya özel "persona" şeklinde kişiselleştirilmiştir.

### 1.2 Sistemin Çözdüğü Problem
- **Yetkinlik Uyumsuzluğu:** Farklı seviyelerdeki kullanıcılara aynı AI yanıtı verilmesi
- **Tek Modlu Sistemler:** Sadece benzerlik VEYA sadece tamamlayıcılık sunan mevcut sistemler
- **Pedagoji-Teknik Dengesizliği:** Blokzincir eğitim sistemlerinde %73 teknik, sadece %12 pedagojik odak

### 1.3 Çözüm: Çift Modlu Adaptif Sistem
```
┌─────────────────────────────────────────────────────────────┐
│                    PITL SİSTEMİ                            │
├─────────────────────────────────────────────────────────────┤
│  KULLANICI → Yetkinlik Değerlendirmesi → UserVector (10D)  │
│                          ↓                                  │
│  100 PERSONA → PersonaVector (10D) → Matematiksel Eşleşme  │
│                          ↓                                  │
│  ┌─────────────┐    ┌─────────────────┐                    │
│  │ BENZER MOD  │    │ TAMAMLAYICI MOD │                    │
│  │ (Similar)   │    │ (Complementary) │                    │
│  │ CLT Tabanlı │    │ ZPD Tabanlı     │                    │
│  └─────────────┘    └─────────────────┘                    │
│                          ↓                                  │
│  NASA-TLX Geri Bildirim → Adaptif Mod Değişimi             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. TEORİK TEMELLER (Literatür İçin Kritik)

### 2.1 Dreyfus Beş Aşamalı Yetkinlik Modeli
**Kaynak:** Dreyfus, H. L., & Dreyfus, S. E. (1986). *Mind over machine: The power of human intuition and expertise in the era of the computer.*

| Seviye | İngilizce | Türkçe | Karakteristik |
|--------|-----------|--------|---------------|
| 1 | Novice | Acemi | Kurallara bağlı, bağlam-bağımsız |
| 2 | Advanced Beginner | İleri Başlangıç | Pattern tanıma, guideline-based |
| 3 | Competent | Yetkin | Planlama, önceliklendirme, troubleshooting |
| 4 | Proficient | Usta | Bütünsel görüş, sezgisel karar |
| 5 | Expert | Uzman | Kuralları aşar, yenilikçi, akıcı performans |

**Sistemde Kullanımı:**
- 100 persona, bu 5 seviyeye göre dağıtılmıştır
- Kullanıcı yetkinliği bu modelle ölçülür
- Persona-kullanıcı eşleşmesi Dreyfus seviyelerine göre yapılır

**İlgili Literatür:**
- Benner, P. (1984). From novice to expert. *Addison-Wesley.*
- Berliner, D. C. (2004). Describing the behavior and documenting the accomplishments of expert teachers. *Bulletin of Science, Technology & Society.*
- Ericsson, K. A. (2006). The influence of experience and deliberate practice on the development of superior expert performance.

---

### 2.2 Vygotsky'nin Yakınsak Gelişim Alanı (ZPD)
**Kaynak:** Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes.*

```
┌───────────────────────────────────────────────────┐
│                                                   │
│   ┌─────────────────────────────────────────┐    │
│   │                                         │    │
│   │   ┌───────────────────────────────┐    │    │
│   │   │                               │    │    │
│   │   │   BAĞIMSIZ YAPABİLİR         │    │    │ YAPILAMAZ
│   │   │   (Actual Development)        │    │    │ (Frustration Zone)
│   │   │                               │    │    │
│   │   └───────────────────────────────┘    │    │
│   │                                         │    │
│   │   ZPD - REHBERLE YAPABİLİR             │    │
│   │   (Zone of Proximal Development)        │    │
│   │                                         │    │
│   └─────────────────────────────────────────┘    │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Matematiksel Model (PITL'de):**
```
ZPD_Match = exp(-(user_level - persona_level)² / (2σ²))
```
- σ = 2.0 (duyarlılık parametresi)
- Optimal eşleşme: Kullanıcıdan 1-2 seviye yukarıdaki persona

**Sistemde Kullanımı:**
- **Tamamlayıcı Mod** ZPD teorisine dayanır
- Kullanıcının zayıf alanlarında güçlü personalar önerilir
- "Daha bilgili diğeri" (More Knowledgeable Other - MKO) rolü AI persona tarafından üstlenilir

**İlgili Literatür:**
- Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry.*
- Chaiklin, S. (2003). The zone of proximal development in Vygotsky's analysis of learning and instruction.
- Shayer, M. (2003). Not just Piaget; not just Vygotsky, and certainly not Vygotsky as alternative to Piaget.

---

### 2.3 Sweller'in Bilişsel Yük Teorisi (CLT)
**Kaynak:** Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science.*

**Üç Tür Bilişsel Yük:**

| Yük Türü | İngilizce | Açıklama | Örnek |
|----------|-----------|----------|-------|
| İçsel | Intrinsic Load | İçeriğin doğal karmaşıklığı | Solidity syntax öğrenmek |
| Dışsal | Extraneous Load | Kötü sunumdan kaynaklanan | Karmaşık UI, gereksiz bilgi |
| İlgili | Germane Load | Şema oluşturmaya ayrılan | Örüntü tanıma, transfer |

**Matematiksel Model (PITL'de):**
```python
Total_Cognitive_Load = Intrinsic + Extraneous + Germane

# Optimal durum:
# - Intrinsic: Kontrol edilemez (içerik bağımlı)
# - Extraneous: MİNİMİZE edilmeli (≤ 0.3)
# - Germane: MAKSİMİZE edilmeli

CLT_Modifier = {
    "optimal_zone": +0.15 bonus,      # Düşük extraneous, yüksek germane
    "overload": -0.20 penalty,         # Toplam yük > 0.8
    "high_extraneous": -0.10 penalty   # Extraneous > 0.4
}
```

**Sistemde Kullanımı:**
- **Benzer Mod** CLT'ye dayanır - dışsal yükü minimize eder
- NASA-TLX ile bilişsel yük ölçülür
- CLT skoruna göre persona puanı modifiye edilir

**İlgili Literatür:**
- Sweller, J., Van Merrienboer, J. J., & Paas, F. G. (1998). Cognitive architecture and instructional design.
- Paas, F., Renkl, A., & Sweller, J. (2003). Cognitive load theory and instructional design.
- Sweller, J., Ayres, P., & Kalyuga, S. (2011). *Cognitive load theory.* Springer.

---

### 2.4 Nonaka & Takeuchi Bilgi Dönüşüm Modeli (SECI)
**Kaynak:** Nonaka, I., & Takeuchi, H. (1995). *The knowledge-creating company.*

```
           Tacit (Örtük)              Explicit (Açık)
         ┌─────────────────┬─────────────────┐
 Tacit   │  SOCIALIZATION  │ EXTERNALIZATION │
 (Örtük) │  (Sosyalleşme)  │ (Dışsallaştırma)│
         │  Deneyim paylaşım│ Kavramlaştırma  │
         ├─────────────────┼─────────────────┤
Explicit │ INTERNALIZATION │   COMBINATION   │
 (Açık)  │ (İçselleştirme) │   (Birleştirme) │
         │ Uygulama ile    │ Sistemleştirme  │
         │ öğrenme         │                 │
         └─────────────────┴─────────────────┘
```

**Bilgi Türleri (UserVector'da):**
```python
UserVector = {
    "procedural_knowledge": 0.0-1.0,   # "Nasıl" bilgisi (know-how)
    "declarative_knowledge": 0.0-1.0,  # "Ne" bilgisi (know-what)
    "conditional_knowledge": 0.0-1.0   # "Ne zaman" bilgisi (know-when)
}
```

**Sistemde Kullanımı:**
- Kullanıcı ve persona vektörlerinde bilgi türleri ayrıştırılmış
- Similarity ve Competency hesaplamalarında kullanılır
- Tacit→Explicit dönüşümü AI persona ile desteklenir

---

### 2.5 TPACK Çerçevesi (Mishra & Koehler)
**Kaynak:** Mishra, P., & Koehler, M. J. (2006). Technological pedagogical content knowledge: A framework for teacher knowledge.

```
                    ┌───────────┐
                    │   TPACK   │
                    │ (Kesişim) │
                    └─────┬─────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
   │   TK    │      │   PK    │      │   CK    │
   │Teknoloji│      │Pedagoji │      │ İçerik  │
   │ Bilgisi │      │ Bilgisi │      │ Bilgisi │
   └─────────┘      └─────────┘      └─────────┘
```

**Sistemde Kullanımı:**
- **Technical Score** = TK (Teknoloji Bilgisi)
- **Educational Score** = PK (Pedagoji Bilgisi)
- **Blockchain/Solidity** = CK (İçerik Bilgisi)
- Optimal sistem TPACK kesişiminde

**İlgili Literatür:**
- Archambault, L., & Barnett, J. H. (2010). Revisiting technological pedagogical content knowledge.
- Koehler, M. J., & Mishra, P. (2009). What is technological pedagogical content knowledge?

---

## 3. MATEMATİKSEL MODEL

### 3.1 Ana Öneri Formülü (MCDA)
**Multi-Criteria Decision Analysis:**

```
R(u,p) = α·S(u,p) + β·C(u,p) + γ·P(u,p,g) + δ·L(u,t)
```

| Bileşen | Formül | Açıklama | Ağırlık |
|---------|--------|----------|---------|
| S | Similarity Score | Cosine + Euclidean Hybrid | α = 0.30 |
| C | Competency Match | ZPD-based Gaussian | β = 0.35 |
| P | Performance Prediction | Sigmoid Regression | γ = 0.25 |
| L | Learning Trajectory | Power Law of Practice | δ = 0.10 |

### 3.2 Benzerlik Skoru (S)
```
S(u,p) = 0.6 × CosineSimilarity(u,p) + 0.4 × (1 - NormalizedEuclidean(u,p))
```

**Neden Hibrit?**
- Cosine: Yön benzerliği (profil tipi)
- Euclidean: Büyüklük benzerliği (seviye yakınlığı)

### 3.3 Yetkinlik Uyumu (C) / Tamamlayıcılık (D)
```python
# Similar Mode - Competency Match
C(u,p) = ZPD_Gaussian × Knowledge_Match × Level_Alignment

# Complementary Mode - Complementarity Score
D(u,p) = Σᵢ (pᵢ_strong × uᵢ_weak)  # Persona güçlü, kullanıcı zayıf
```

### 3.4 Çift Mod Seçimi
```python
if mode == "similarity":
    final_score = α·S + β·C + γ·P + δ·L
elif mode == "complementary":
    final_score = α·(1-S) + β·D + γ·P + δ·L  # Benzerlik yerine farklılık
```

---

## 4. 100 PERSONA SİSTEMİ

### 4.1 Yapı
```
2 Ana Domain × 10 Alt-Uzmanlık × 5 Dreyfus Seviyesi = 100 Persona
```

Bu yapı, araştırmanın temel **Teknik-Pedagojik ikiliği** temasını doğrudan yansıtır.

### 4.2 Ana Domainler ve Alt-Uzmanlıklar

#### TEKNOLOJİ DOMAINI (50 Persona)
| # | Alt-Uzmanlık | Odak | Teknolojiler |
|---|--------------|------|--------------|
| 1 | Smart Contract Development | Solidity ve EVM | Hardhat, OpenZeppelin |
| 2 | Web3 Frontend | Blockchain-UI entegrasyonu | Ethers.js, Wagmi |
| 3 | DeFi Protocols | Merkezi olmayan finans | AMM, Lending, Staking |
| 4 | Security & Audit | Smart contract güvenliği | Slither, Mythril |
| 5 | NFT & Gaming | NFT ve GameFi | ERC721, ERC1155 |
| 6 | L2 & Scaling | Layer 2 çözümleri | Optimism, Arbitrum |
| 7 | DevOps & Infrastructure | CI/CD, deployment | GitHub Actions, Docker |
| 8 | Testing & QA | Test stratejileri | Foundry, Coverage |
| 9 | Protocol Research | Yeni protokol tasarımı | EIP/ERC, zkSNARK |
| 10 | Enterprise Blockchain | B2B çözümler | Hyperledger |

#### PEDAGOJİ DOMAINI (50 Persona)
| # | Alt-Uzmanlık | Odak | Yöntemler |
|---|--------------|------|-----------|
| 1 | Instructional Design | Öğretim tasarımı | ADDIE, SAM |
| 2 | Curriculum Development | Müfredat geliştirme | Learning Objectives |
| 3 | Learning Analytics | Öğrenme verisi analizi | xAPI, Dashboards |
| 4 | Assessment & Evaluation | Değerlendirme | Rubrics, Portfolios |
| 5 | Gamification | Oyunlaştırma | Badges, Leaderboards |
| 6 | Adaptive Learning | Kişiselleştirilmiş öğrenme | AI Tutors |
| 7 | Accessibility & UX | Erişilebilirlik | WCAG, Universal Design |
| 8 | Educational Research | Eğitim araştırması | Action Research |
| 9 | Teacher Training | Öğretmen eğitimi | TPACK, Microteaching |
| 10 | Content Creation | İçerik üretimi | Video, Interactive |

### 4.3 Persona Vektörü (10 Boyut)
```python
PersonaVector = {
    "code_complexity": 0.0-1.0,      # Kod karmaşıklığı
    "verbosity": 0.0-1.0,            # Açıklayıcılık
    "technical_depth": 0.0-1.0,      # Teknik derinlik
    "pedagogical_focus": 0.0-1.0,    # Pedagojik odak
    "comment_density": 0.0-1.0,      # Yorum yoğunluğu
    "modularity": 0.0-1.0,           # Modülerlik
    "example_richness": 0.0-1.0,     # Örnek zenginliği
    "learning_support": 0.0-1.0,     # Öğrenme desteği
    "production_readiness": 0.0-1.0, # Üretime hazırlık
    "innovation_factor": 0.0-1.0     # Yenilikçilik
}
```

### 4.4 Dreyfus Seviyesine Göre Vektör Örüntüleri

| Özellik | Novice | Advanced Beginner | Competent | Proficient | Expert |
|---------|--------|-------------------|-----------|------------|--------|
| code_complexity | 0.15 | 0.30 | 0.55 | 0.75 | 0.90 |
| verbosity | 0.95 | 0.75 | 0.50 | 0.30 | 0.15 |
| technical_depth | 0.15 | 0.35 | 0.60 | 0.80 | 0.95 |
| learning_support | 0.90 | 0.75 | 0.55 | 0.35 | 0.20 |
| innovation_factor | 0.05 | 0.15 | 0.35 | 0.60 | 0.90 |

---

## 5. ADAPTİF MEKANİZMA

### 5.1 İlk Görev Ataması (Learning Goal Tabanlı)
```python
def calculate_initial_mode(user):
    if user.learning_goal == "Uzmanlaşmak istiyorum":
        return "Complementary"  # Tamamlayıcı - ZPD
    elif user.learning_goal == "Hızlı üretim yapmak istiyorum":
        return "Similar"  # Benzer - CLT
    else:  # Dengeli
        return "Similar"  # Varsayılan güvenli başlangıç
```

### 5.2 Dinamik Mod Değişimi (NASA-TLX Tabanlı)
```python
def calculate_next_mode(previous_nasa_tlx, current_mode):
    total_load = sum(previous_nasa_tlx.values()) / 6  # 0-100 arası
    
    if total_load > 60:  # YÜKSEK YÜK
        return "Similar"  # Rahatlat - CLT odaklı
    elif total_load < 30:  # DÜŞÜK YÜK
        return "Complementary"  # Zorla - ZPD odaklı
    else:  # NORMAL YÜK
        # Denge koru veya değiştir
        return alternate_mode(current_mode)
```

### 5.3 NASA-TLX Ölçeği
**Kaynak:** Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX.

| Boyut | İngilizce | Ölçüm |
|-------|-----------|-------|
| Zihinsel Talep | Mental Demand | 0-100 |
| Fiziksel Talep | Physical Demand | 0-100 |
| Zamansal Talep | Temporal Demand | 0-100 |
| Performans | Performance | 0-100 |
| Çaba | Effort | 0-100 |
| Hayal Kırıklığı | Frustration | 0-100 |

---

## 6. LİTERATÜR BOŞLUKLARI (Tezin Katkısı)

### 6.1 Tespit Edilen Boşluklar

| Boşluk | Mevcut Durum | PITL Katkısı |
|--------|--------------|--------------|
| Kullanıcı yetkinliği ihmal | Model-merkezli araştırmalar | Yetkinlik-tabanlı eşleştirme |
| Tek modlu sistemler | Sadece similarity VEYA complementary | Çift modlu adaptif sistem |
| Pedagoji-Teknik dengesizliği | %73 teknik, %12 pedagojik | Dengeli 100 persona |
| Matematiksel model eksikliği | Nitel veya basit istatistik | 6 katmanlı MCDA formülü |

### 6.2 Kesişim Analizi (Literatür Taraması)
```
Blockchain ∩ Eğitim: N=247
Blockchain ∩ YZ: N=29
Blockchain ∩ Yetkinlik: N=12
Eğitim ∩ YZ ∩ Yetkinlik: N=9
Blockchain ∩ Eğitim ∩ YZ ∩ Yetkinlik: N=0  ← PITL'in alanı
```

---

## 7. İLGİLİ KAVRAMLAR VE TERİMLER

### 7.1 İnsan-Yapay Zeka İşbirliği
- **Human-in-the-Loop (HITL):** İnsan karar sürecinde
- **AI Augmentation:** YZ insan yeteneğini artırır
- **Hybrid Intelligence:** İnsan + YZ tamamlayıcı işbirliği
- **PITL (Persona In The Loop):** Kişiselleştirilmiş YZ etkileşimi

### 7.2 Öneri Sistemleri
- **Collaborative Filtering:** Benzer kullanıcıların tercihleri
- **Content-Based Filtering:** İçerik özelliklerine göre
- **Hybrid Systems:** İkisinin kombinasyonu
- **Knowledge-Based Systems:** Kural tabanlı öneriler

### 7.3 Prompt Engineering
- **Zero-shot:** Örnek olmadan
- **Few-shot:** Birkaç örnek ile
- **Chain-of-Thought:** Adım adım düşünme
- **Role-playing:** Persona/karakter atama (PITL'in kullandığı)

---

## 8. ANAHTAR REFERANSLAR

### 8.1 Temel Teoriler
```
Dreyfus & Dreyfus (1986) - Yetkinlik modeli
Vygotsky (1978) - ZPD teorisi
Sweller (1988, 2011) - Bilişsel yük teorisi
Nonaka & Takeuchi (1995) - SECI modeli
Mishra & Koehler (2006) - TPACK çerçevesi
```

### 8.2 Büyük Dil Modelleri
```
Vaswani et al. (2017) - Transformer mimarisi
Brown et al. (2020) - GPT-3, few-shot learning
Ouyang et al. (2022) - InstructGPT, RLHF
Touvron et al. (2023) - LLaMA
Bubeck et al. (2023) - GPT-4 yetenekleri
```

### 8.3 İnsan-YZ İşbirliği
```
Dellermann et al. (2019) - Hibrit zeka
Jarrahi (2018) - YZ ve insan tamamlayıcılığı
Seeber et al. (2020) - İşbirlikçi zeka
Floridi & Chiriatti (2020) - GPT-3 analizi
Bender et al. (2021) - LLM riskleri ve etik
```

### 8.4 Blokzincir Eğitim
```
Grech & Camilleri (2017) - AB Blokzincir eğitim raporu
Sharples & Domingue (2016) - Blokzincir ve eğitim
Schmidt (2018) - Blockcerts
Chen et al. (2018) - Blokzincir tabanlı sertifikasyon
```

### 8.5 Öneri Sistemleri
```
Ricci et al. (2015) - Recommender systems handbook
Aggarwal (2016) - Recommender systems textbook
Burke (2002) - Hybrid recommender systems
```

---

## 9. LİTERATÜR YAZIMI İÇİN İPUÇLARI

### 9.1 Yapı Önerisi
```
2. LİTERATÜR TARAMASI
   2.1 Teorik Çerçeve
       2.1.1 Yetkinlik Kazanım Modelleri (Dreyfus)
       2.1.2 Öğrenme Teorileri (Vygotsky, Sweller)
       2.1.3 Bilgi Yönetimi (Nonaka & Takeuchi)
       2.1.4 Eğitim Teknolojisi (TPACK)
   
   2.2 Büyük Dil Modelleri ve İnsan-YZ İşbirliği
       2.2.1 BDM Gelişimi (GPT, Claude, Gemini)
       2.2.2 Prompt Engineering
       2.2.3 İnsan-YZ Etkileşim Modelleri
   
   2.3 Blokzincir ve Eğitim
       2.3.1 Blokzincir Teknolojisi
       2.3.2 Eğitimde Blokzincir Uygulamaları
       2.3.3 Teknik-Pedagojik Kesişim
   
   2.4 Öneri Sistemleri
       2.4.1 Collaborative Filtering
       2.4.2 Content-Based Systems
       2.4.3 Adaptif Sistemler
   
   2.5 Literatür Boşluğu ve Araştırmanın Konumu
```

### 9.2 Her Alt Bölüm İçin
1. **Tanım:** Kavramı açıkla
2. **Tarihçe:** Gelişim süreci
3. **Mevcut Çalışmalar:** Kim ne yapmış
4. **Eleştiri:** Eksiklikler neler
5. **PITL Bağlantısı:** Sistemle ilişki

### 9.3 Kritik Bağlantılar
```
Dreyfus → Persona seviyeleri
Vygotsky → Tamamlayıcı mod
Sweller → Benzer mod + NASA-TLX
TPACK → Teknik/Pedagojik denge
Öneri sistemleri → MCDA formülü
```

---

## 10. ÖRNEK LİTERATÜR PARAGRAFLARİ

### 10.1 Dreyfus Modeli Bağlamında
> Dreyfus ve Dreyfus (1986), uzmanlık kazanımını beş aşamalı bir model ile açıklamıştır: acemi (novice), ileri başlangıç (advanced beginner), yetkin (competent), usta (proficient) ve uzman (expert). Bu model, hemşirelik (Benner, 1984), öğretmenlik (Berliner, 2004) ve yazılım geliştirme gibi birçok alanda doğrulanmıştır. Ancak yapay zeka destekli görev performansı bağlamında bu modelin uygulanması henüz araştırılmamıştır. PITL sistemi, hem kullanıcıları hem de yapay zeka personalarını Dreyfus seviyeleriyle sınıflandırarak bu boşluğu doldurmayı hedeflemektedir.

### 10.2 Çift Mod Teorik Temeli
> Mevcut öneri sistemleri genellikle benzerlik tabanlı (similarity-based) yaklaşımı benimser (Ricci et al., 2015). Ancak öğrenme bağlamında, Vygotsky'nin (1978) Yakınsak Gelişim Alanı teorisi, optimal öğrenmenin mevcut seviyenin "biraz üzerinde" gerçekleştiğini öne sürer. Öte yandan Sweller'in (1988) Bilişsel Yük Teorisi, aşırı zorluğun öğrenmeyi engelleyebileceğini vurgular. PITL'in çift modlu yaklaşımı, bu iki teoriyi sentezleyerek kullanıcının durumuna göre optimal stratejiyi seçer.

---

*Bu belge, PITL doktora tezi literatür taraması için referans rehberi olarak hazırlanmıştır.*
*Son güncelleme: Şubat 2026*
