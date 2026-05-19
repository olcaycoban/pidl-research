# PITL DOKTORA TEZİ - GİRİŞ BÖLÜMÜ YAZIM REHBERİ

Bu belge, Claude'a verilerek tezin GİRİŞ bölümünün yazılması için hazırlanmıştır.

---

## GÖREV

Aşağıdaki bilgileri kullanarak bir doktora tezinin **1. GİRİŞ** bölümünü yaz.

**Gereksinimler:**
- Akademik Türkçe, formal dil
- APA 7 atıf formatı
- 15-20 sayfa uzunluğunda
- Alt başlıklar: Problem, Amaç, Önem, Varsayımlar, Sınırlılıklar, Tanımlar

---

## TEZİN KİMLİĞİ

| Alan | Değer |
|------|-------|
| **Başlık** | İnsan-Yapay Zeka İşbirliğinde Yetkinlik Tabanlı Persona Eşleştirme: Blokzincir Eğitim Teknolojileri Bağlamında Çift Modlu Uyarlanabilir Öneri Sistemi |
| **İngilizce Başlık** | Competency-Based Persona Matching in Human-AI Collaboration: A Dual-Mode Adaptive Recommendation System in Blockchain Education Technology Context |
| **Sistem Adı** | PITL (Persona In The Loop) |
| **Alan** | Eğitim Teknolojileri / İnsan-Bilgisayar Etkileşimi |
| **Bağlam** | Blokzincir tabanlı eğitim sistemleri geliştirme |

---

## ARAŞTIRMA PROBLEMİ

### Ana Problem
Farklı yetkinlik seviyelerindeki kullanıcıların (eğitimciler ve yazılım geliştiriciler), yapay zeka sistemleriyle etkileşimde **optimal persona eşleşmesi** nasıl sağlanır?

### Alt Problemler
1. Kullanıcı yetkinlik profili ile AI persona arasındaki uyum nasıl matematiksel olarak modellenir?
2. Benzerlik tabanlı (similarity) ve tamamlayıcılık tabanlı (complementary) stratejiler hangi durumlarda tercih edilmeli?
3. Bilişsel yük (NASA-TLX) geri bildirimine göre persona modu nasıl dinamik olarak adapte edilmeli?
4. Teknik ve pedagojik uzmanlık alanları arasındaki denge nasıl optimize edilmeli?

### Mevcut Durum ve Eksiklikler
- Mevcut AI sistemleri **tek tip** yanıt üretir (kullanıcı yetkinliğini dikkate almaz)
- Öneri sistemleri genellikle **sadece benzerlik** odaklı (tamamlayıcılık ihmal)
- Blokzincir-eğitim araştırmalarının **%73'ü teknik**, sadece **%12'si pedagojik** odaklı
- İnsan-AI işbirliği literatürü **matematiksel modelleme** eksik

---

## PITL SİSTEMİ AÇIKLAMASI

### Temel Konsept
PITL, kullanıcının yetkinlik profiline göre **100 farklı AI personasından** en uygun olanı öneren çift modlu adaptif bir sistemdir.

### Sistem Mimarisi
```
KULLANICI
    ↓
[Yetkinlik Değerlendirmesi] → UserVector (10 boyutlu)
    ↓
[100 Persona Havuzu] → PersonaVector (10 boyutlu her biri)
    ↓
[6 Aşamalı Matematiksel Hesaplama]
    ↓
┌─────────────────┬─────────────────┐
│   BENZER MOD    │  TAMAMLAYICI MOD │
│   (Similar)     │  (Complementary) │
│                 │                  │
│ • CLT Tabanlı   │ • ZPD Tabanlı    │
│ • Konfor alanı  │ • Öğrenme alanı  │
│ • Düşük yük     │ • Optimal zorluk │
└─────────────────┴─────────────────┘
    ↓
[Görev Tamamlama]
    ↓
[NASA-TLX Geri Bildirim]
    ↓
[Adaptif Mod Değişimi] → Sonraki görev
```

### Çift Mod Açıklaması

| Mod | Teori | Ne Zaman | Fayda |
|-----|-------|----------|-------|
| **Benzer (Similar)** | Sweller CLT | Yüksek bilişsel yük, üretim odaklı | Konfor, hız, düşük stres |
| **Tamamlayıcı (Complementary)** | Vygotsky ZPD | Düşük bilişsel yük, öğrenme odaklı | Gelişim, yeni beceri, kapasite artışı |

### 100 Persona Yapısı
```
2 Ana Domain × 10 Alt-Uzmanlık × 5 Dreyfus Seviyesi = 100 Persona

TEKNOLOJİ DOMAINI (50 Persona):
├── Smart Contract Development (5 seviye)
├── Web3 Frontend (5 seviye)
├── DeFi Protocols (5 seviye)
├── Security & Audit (5 seviye)
├── NFT & Gaming (5 seviye)
├── L2 & Scaling (5 seviye)
├── DevOps & Infrastructure (5 seviye)
├── Testing & QA (5 seviye)
├── Protocol Research (5 seviye)
└── Enterprise Blockchain (5 seviye)

PEDAGOJİ DOMAINI (50 Persona):
├── Instructional Design (5 seviye)
├── Curriculum Development (5 seviye)
├── Learning Analytics (5 seviye)
├── Assessment & Evaluation (5 seviye)
├── Gamification (5 seviye)
├── Adaptive Learning (5 seviye)
├── Accessibility & UX (5 seviye)
├── Educational Research (5 seviye)
├── Teacher Training (5 seviye)
└── Content Creation (5 seviye)

Dreyfus Seviyeleri (her alt-domain için):
1. Novice (Acemi)
2. Advanced Beginner (İleri Başlangıç)
3. Competent (Yetkin)
4. Proficient (Usta)
5. Expert (Uzman)
```

**Yapının Teorik Temeli:**
Bu yapı, araştırmanın temel ikiliği olan **Teknik-Pedagojik** ayrımını doğrudan yansıtır:
- TEKNOLOJİ personaları: Yüksek technical_depth, düşük pedagogical_focus
- PEDAGOJİ personaları: Yüksek pedagogical_focus, düşük technical_depth
- Bu ortogonallik TPACK çerçevesi (Mishra & Koehler, 2006) ile uyumludur

---

## TEORİK ÇERÇEVE

### 1. Dreyfus Beş Aşamalı Yetkinlik Modeli
**Kaynak:** Dreyfus, H. L., & Dreyfus, S. E. (1986). Mind over machine.

- Uzmanlık gelişimi 5 aşamada gerçekleşir
- Her aşamanın kendine özgü davranış kalıpları var
- PITL'de hem kullanıcılar hem personalar bu modelle sınıflandırılır

**Aşamalar:**
| Seviye | Karakteristik |
|--------|---------------|
| Novice | Kural-bağımlı, bağlam-bağımsız |
| Advanced Beginner | Pattern tanıma, guideline-based |
| Competent | Planlama, önceliklendirme |
| Proficient | Bütünsel görüş, sezgisel |
| Expert | Kuralları aşar, yenilikçi |

### 2. Vygotsky - Yakınsak Gelişim Alanı (ZPD)
**Kaynak:** Vygotsky, L. S. (1978). Mind in society.

- Optimal öğrenme, mevcut seviyenin "biraz üzerinde" gerçekleşir
- "Daha Bilgili Diğeri" (MKO) kavramı - PITL'de AI persona bu rolü üstlenir
- **Tamamlayıcı mod** bu teoriye dayanır

**Matematiksel Model:**
```
ZPD_Match = exp(-(user_level - persona_level)² / (2σ²))
σ = 2.0 → Optimal eşleşme: 1-2 seviye yukarı
```

### 3. Sweller - Bilişsel Yük Teorisi (CLT)
**Kaynak:** Sweller, J. (1988). Cognitive load during problem solving.

**Üç Yük Türü:**
- **İçsel (Intrinsic):** İçeriğin doğal karmaşıklığı
- **Dışsal (Extraneous):** Kötü sunumdan kaynaklanan (minimize edilmeli)
- **İlgili (Germane):** Şema oluşturmaya ayrılan (maximize edilmeli)

- **Benzer mod** dışsal yükü minimize eder
- NASA-TLX ile ölçülür

### 4. Nonaka & Takeuchi - SECI Modeli
**Kaynak:** Nonaka, I., & Takeuchi, H. (1995). The knowledge-creating company.

**Bilgi Türleri (UserVector'da):**
- Procedural Knowledge (Nasıl bilgisi)
- Declarative Knowledge (Ne bilgisi)
- Conditional Knowledge (Ne zaman bilgisi)

### 5. TPACK Çerçevesi
**Kaynak:** Mishra, P., & Koehler, M. J. (2006). TPACK framework.

- Technological Knowledge (TK) → Technical Score
- Pedagogical Knowledge (PK) → Educational Score
- Content Knowledge (CK) → Blockchain/Solidity
- Optimal = TPACK kesişimi

---

## MATEMATİKSEL MODEL

### Ana Öneri Formülü
```
R(u,p) = α·S(u,p) + β·C(u,p) + γ·P(u,p,g) + δ·L(u,t)
```

| Bileşen | Açıklama | Ağırlık |
|---------|----------|---------|
| S | Benzerlik Skoru (Cosine + Euclidean) | α = 0.30 |
| C | Yetkinlik Uyumu (ZPD Gaussian) | β = 0.35 |
| P | Performans Tahmini (Sigmoid) | γ = 0.25 |
| L | Öğrenme Yörüngesi (Power Law) | δ = 0.10 |

### Çift Mod Formülasyonu
```
# Benzer Mod
R_similar = α·S + β·C + γ·P + δ·L

# Tamamlayıcı Mod
R_complementary = α·(1-S) + β·D + γ·P + δ·L
```

**D = Tamamlayıcılık Skoru:**
```
D(u,p) = Σᵢ (pᵢ_güçlü × uᵢ_zayıf)
```

### Vektör Yapısı (10 Boyut)
```
Vector = [
    code_complexity,      # Kod karmaşıklığı
    verbosity,            # Açıklayıcılık
    technical_depth,      # Teknik derinlik
    pedagogical_focus,    # Pedagojik odak
    comment_density,      # Yorum yoğunluğu
    modularity,           # Modülerlik
    example_richness,     # Örnek zenginliği
    learning_support,     # Öğrenme desteği
    production_readiness, # Üretime hazırlık
    innovation_factor     # Yenilikçilik
]
```

---

## LİTERATÜR BOŞLUKLARI

### Sistematik Tarama Sonuçları
- **Kaynak:** PRISMA guidelines, N=247 makale, Web of Science & Scopus, 2018-2025

### Tespit Edilen Boşluklar

| # | Boşluk | Mevcut Durum | PITL Katkısı |
|---|--------|--------------|--------------|
| 1 | Kullanıcı yetkinliği | Model-merkezli araştırmalar | Yetkinlik-tabanlı eşleştirme |
| 2 | Öneri stratejisi | Tek mod (sadece similarity) | Çift modlu adaptif sistem |
| 3 | Pedagoji-Teknik dengesi | %73 teknik, %12 pedagojik | 100 dengeli persona |
| 4 | Matematiksel modelleme | Nitel veya basit istatistik | 6 katmanlı MCDA |

### Kesişim Analizi
```
Blockchain ∩ Eğitim: N=247
Blockchain ∩ AI: N=29
Blockchain ∩ Yetkinlik: N=12
Eğitim ∩ AI ∩ Yetkinlik: N=9
Blockchain ∩ Eğitim ∩ AI ∩ Yetkinlik: N=0 ← PITL'in alanı
```

---

## ARAŞTIRMA SORULARI

### Ana Soru
Blokzincir tabanlı eğitim teknolojileri bağlamında, kullanıcı yetkinlik profiline dayalı çift modlu (benzerlik ve tamamlayıcılık) uyarlanabilir AI persona öneri sistemi, kod kalitesi ve öğrenme kazanımları üzerinde nasıl bir etki yaratır?

### Alt Sorular
1. Kullanıcı yetkinlik seviyesi (Dreyfus) ile AI persona eşleşmesi arasındaki ilişki nedir?
2. Benzerlik modu vs. tamamlayıcılık modu hangi metriklerde üstünlük sağlar?
3. Bilişsel yük (NASA-TLX) geri bildirimi persona adaptasyonunu nasıl etkiler?
4. Teknik ve pedagojik uzmanlık arasındaki denge kod kalitesini nasıl etkiler?

---

## ARAŞTIRMA HİPOTEZLERİ

### H1: Yetkinlik Eşleşmesi
> Kullanıcı yetkinlik seviyesine uygun AI persona eşleşmesi, rastgele eşleşmeye göre anlamlı düzeyde daha yüksek kod kalitesi sağlar.

### H2: Çift Mod Etkinliği
> Çift modlu adaptif sistem, tek modlu sistemlere göre hem öğrenme kazanımı hem performans metriklerinde üstünlük sağlar.

### H3: Bilişsel Yük Optimizasyonu
> NASA-TLX tabanlı adaptif mod değişimi, sabit mod atamasına göre daha düşük bilişsel yük ve daha yüksek görev tamamlama oranı sağlar.

### H4: Mod-Bağlam Etkileşimi
> Benzerlik modu üretim odaklı görevlerde, tamamlayıcılık modu öğrenme odaklı görevlerde anlamlı düzeyde daha iyi sonuç verir.

---

## VARSAYIMLAR (SAYILTILAR)

### Teorik Varsayımlar
1. **Dreyfus Temsili:** Yetkinlik seviyeleri Dreyfus modeliyle temsil edilebilir
2. **ZPD Ölçülebilirliği:** Yakınsak Gelişim Alanı matematiksel modellenebilir
3. **CLT Uygulanabilirliği:** Bilişsel Yük Teorisi kod üretim bağlamında geçerli
4. **Ortogonallik:** Pedagojik ve teknik uzmanlık bağımsız boyutlar

### Metodolojik Varsayımlar
5. **Persona Geçerliliği:** AI personaları gerçek uzmanları yeterince temsil eder
6. **Öz-bildirim Güvenilirliği:** Katılımcılar dürüst değerlendirme yapar
7. **Platform Kararlılığı:** PITL platformu tutarlı çalışır

### İstatistiksel Varsayımlar
8. **Normallik:** Bağımlı değişkenler normal dağılım gösterir
9. **Varyans Homojenliği:** Gruplar arası varyanslar eşit
10. **Bağımsızlık:** Gözlemler birbirinden bağımsız

---

## SINIRLILIKLAR

### Teknolojik Sınırlılıklar
- **Platform:** Sadece Ethereum (Solana, Cardano vb. hariç)
- **Dil:** Sadece Solidity (Vyper, Rust hariç)
- **Model:** GPT-4o, Claude-3, Gemini, Grok (açık kaynak LLM'ler hariç)

### Metodolojik Sınırlılıklar
- **Tasarım:** Kesitsel (boylamsal takip yok)
- **Örneklem:** N=150 (kolayda örnekleme)
- **Coğrafi:** Sadece Türkiye

### Ölçüm Sınırlılıkları
- **Kod Kalitesi:** Otomatik araçlarla (insan uzman incelemesi sınırlı)
- **Pedagojik Ölçüt:** Kısmen öznel

### Genelleme Sınırlılıkları
- **Alan:** Blokzincir eğitimi (diğer alanlara genellenemeyebilir)
- **Popülasyon:** Üniversite öğrencileri ve EdTech profesyonelleri
- **Zaman:** 2024-2025 dönemi (hızlı teknoloji değişimi)

---

## TANIMLAR

### Temel Kavramlar

| Terim | Tanım |
|-------|-------|
| **PITL** | Persona In The Loop - Kullanıcı yetkinliğine göre AI personası öneren sistem |
| **Çift Modlu Öneri** | Benzerlik ve tamamlayıcılık stratejilerini birleştiren yaklaşım |
| **AI Personası** | Belirli yetkinlik profili ve uzmanlık alanını temsil eden AI ajanı |
| **Benzerlik Modu** | Kullanıcıyla benzer profildeki personayı öneren strateji (CLT tabanlı) |
| **Tamamlayıcılık Modu** | Kullanıcının zayıf alanlarında güçlü personayı öneren strateji (ZPD tabanlı) |

### Matematiksel Terimler

| Terim | Formül/Açıklama |
|-------|-----------------|
| **Öneri Skoru R(u,p)** | α·S + β·C + γ·P + δ·L |
| **Benzerlik Skoru S** | Cosine + Euclidean hibrit |
| **Tamamlayıcılık Skoru D** | Σ(persona_güçlü × user_zayıf) |
| **ZPD Eşleşme** | Gaussian fonksiyon, σ=2.0 |

### Ölçüm Araçları

| Araç | Amaç |
|------|------|
| **NASA-TLX** | Bilişsel yük ölçümü (6 boyut, 0-100) |
| **Pylint/Bandit** | Kod kalitesi (teknik) |
| **Likert Ölçeği** | Pedagojik değerlendirme |

---

## ARAŞTIRMANIN ÖNEMİ

### Teorik Katkı
1. **Yeni Çerçeve:** Dreyfus + Vygotsky + Sweller sentezi
2. **Matematiksel Model:** Çift modlu öneri formülasyonu
3. **Tamamlayıcılık Fonksiyonu:** D(u,p) literatürde ilk kez formüle edildi

### Pratik Katkı
1. **100 Persona Kütüphanesi:** Açık kaynak, kullanıma hazır
2. **PITL Platformu:** Web tabanlı araştırma aracı
3. **Adaptif Algoritma:** NASA-TLX tabanlı mod değişimi

### Metodolojik Katkı
1. **Çoklu Ölçüm:** Teknik + Pedagojik kod değerlendirmesi
2. **Vektör Temsili:** 10 boyutlu yetkinlik vektörü
3. **MCDA Entegrasyonu:** Çok ölçütlü karar analizi

---

## ANAHTAR REFERANSLAR (GİRİŞ İÇİN)

### Yetkinlik Modelleri
```
Dreyfus & Dreyfus (1986) - Mind over machine
Benner (1984) - From novice to expert
Berliner (2004) - Expert teachers
Ericsson (2006) - Deliberate practice
```

### Öğrenme Teorileri
```
Vygotsky (1978) - Mind in society (ZPD)
Sweller (1988, 2011) - Cognitive Load Theory
Wood, Bruner & Ross (1976) - Scaffolding
Nonaka & Takeuchi (1995) - SECI model
```

### Büyük Dil Modelleri
```
Vaswani et al. (2017) - Transformer
Brown et al. (2020) - GPT-3
Ouyang et al. (2022) - InstructGPT
Bubeck et al. (2023) - GPT-4 capabilities
```

### İnsan-AI İşbirliği
```
Dellermann et al. (2019) - Hybrid intelligence
Jarrahi (2018) - AI augmentation
Seeber et al. (2020) - Collaborative intelligence
Floridi & Chiriatti (2020) - GPT-3 analysis
```

### Blokzincir Eğitim
```
Grech & Camilleri (2017) - EU Blockchain education
Nakamoto (2008) - Bitcoin whitepaper
Buterin (2014) - Ethereum whitepaper
```

### Eğitim Teknolojisi
```
Mishra & Koehler (2006) - TPACK framework
Clark (1983) vs Kozma (1994) - Media debate
OECD TALIS (2018) - Teacher competencies
```

### Öneri Sistemleri
```
Ricci et al. (2015) - Recommender systems handbook
Aggarwal (2016) - Recommender systems textbook
Burke (2002) - Hybrid systems
```

---

## YAZI FORMATI TALİMATLARI

### Genel Kurallar
- Akademik Türkçe, üçüncü şahıs anlatım
- APA 7 atıf formatı: (Yazar, Yıl) veya Yazar (Yıl)
- Paragraflar arası mantıksal geçiş
- Her iddia için kaynak

### Bölüm Yapısı Önerisi
```
1. GİRİŞ
   1.1 Araştırmanın Arka Planı ve Bağlamı
   1.2 Problem Durumu
   1.3 Araştırmanın Amacı
   1.4 Araştırma Soruları ve Hipotezler
   1.5 Araştırmanın Önemi
   1.6 Varsayımlar
   1.7 Sınırlılıklar
   1.8 Tanımlar
```

### Uzunluk Hedefi
- Toplam: 15-20 sayfa
- Problem durumu: 4-5 sayfa
- Önem: 3-4 sayfa
- Varsayım + Sınırlılık + Tanım: 5-6 sayfa

---

## ÖRNEK PARAGRAFLAR

### Açılış Paragrafı Örneği
> Yapay zeka teknolojilerinin hızla geliştiği günümüzde, özellikle büyük dil modellerinin (BDM) yaygınlaşması, insan-makine etkileşiminde köklü bir dönüşüm yaratmıştır. OpenAI'ın GPT serisi, Anthropic'in Claude modeli ve Google'ın Gemini sistemi gibi yapay zeka uygulamaları, kod üretiminden problem çözümüne kadar geniş bir yelpazede insan yeteneklerini desteklemektedir (Brown et al., 2020; Bubeck et al., 2023). Ancak bu sistemlerin eğitim alanındaki etkin kullanımı, kullanıcı yetkinliğinin dikkate alınmasını gerektirmektedir.

### Problem Paragrafı Örneği
> Mevcut literatür, yapay zeka sistemlerinin performansını genellikle model-merkezli bir perspektiften incelerken, insan faktörünü ve özellikle kullanıcı yetkinliğinin rolünü büyük ölçüde ihmal etmektedir (Dellermann et al., 2019; Jarrahi, 2018). Sistematik literatür taraması sonuçları (N=247 makale), blokzincir-eğitim araştırmalarının %73'ünün teknik odaklı olduğunu ortaya koymuştur. Buna karşın, pedagojik tasarım perspektifini ele alan çalışmaların oranı yalnızca %12'dir.

---

*Bu rehber, PITL doktora tezi giriş bölümü yazımı için Claude'a verilecek referans belgesidir.*
