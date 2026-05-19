# DUAL-MODE ADAPTIVE RECOMMENDATION FRAMEWORK
## İnsan-AI İşbirliği Modellerinde Yetkinlik Transferi ve Performans Optimizasyonu

**Araştırmacı:** [İsminiz]  
**Kurum:** [Üniversiteniz]  
**Tarih:** Ekim 2025  
**Versiyon:** 2.0

---

## 📋 İÇİNDEKİLER

1. [Teorik Çerçeve](#1-teorik-çerçeve)
2. [Matematiksel Formülasyon](#2-matematiksel-formülasyon)
3. [Dual-Mode Stratejisi](#3-dual-mode-stratejisi)
4. [Hipotez Sistemi](#4-hipotez-sistemi)
5. [Empirik Validasyon](#5-empirik-validasyon)
6. [Akademik Katkı](#6-akademik-katkı)

---

## 1. TEORİK ÇERÇEVE

### 1.1 Kavramsal Model

```
┌─────────────────────────────────────────────────────────────┐
│                  KULLANICI (u)                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Yetkinlik Seviyesi (Dreyfus: Novice → Expert)     │   │
│  │ • Domain Bilgisi (Teknik/Eğitimsel)                 │   │
│  │ • Bilgi Türleri (Procedural/Declarative/Conditional)│   │
│  │ • Öğrenme Amacı (Learning/Production)               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
              ┌─────────────────────────┐
              │  RECOMMENDATION ENGINE  │
              │                         │
              │  Dual-Mode Strategy:    │
              │  • Similarity-Based     │
              │  • Complementary-Based  │
              └─────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  PERSONA (p)                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Kod Karakteristikleri (Complexity, Verbosity)     │   │
│  │ • Pedagojik Odak (Teaching vs Production)           │   │
│  │ • Teknik Derinlik (Skill Level)                     │   │
│  │ • Stil Özellikleri (Comments, Modularity)           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
              ┌─────────────────────────┐
              │   CODE GENERATION       │
              │   (LLM-based)           │
              └─────────────────────────┘
                            ↓
              ┌─────────────────────────┐
              │  PERFORMANCE METRICS    │
              │  • Technical            │
              │  • Pedagogical          │
              └─────────────────────────┘
```

### 1.2 Teorik Temeller

**1.2.1 Cognitive Load Theory (Sweller, 1988, 2011)**
- Intrinsic Load: Görevin doğal karmaşıklığı
- Extraneous Load: Sunumdan kaynaklanan yük
- Germane Load: Öğrenme için kullanılan yük

**Uygulama:**
```
Persona seçimi → Extraneous load'u minimize et
Optimal challenge → Germane load'u maksimize et
```

**1.2.2 Zone of Proximal Development (Vygotsky, 1978)**
- ZPD: Mevcut seviye ile potansiyel seviye arası
- Scaffolding: Uygun destek sağlama

**Uygulama:**
```
Similarity mode → ZPD içinde kalma
Complementary mode → ZPD sınırlarını zorlama
```

**1.2.3 Knowledge Transfer Theory (Nonaka & Takeuchi, 1995)**
- Tacit Knowledge (örtük) vs Explicit Knowledge (açık)
- SECI Model: Socialization, Externalization, Combination, Internalization

**Uygulama:**
```
Persona prompt → Tacit knowledge'ı explicit hale getirme
Kod örneği → Externalization
```

**1.2.4 Human-AI Symbiosis (Zheng et al., 2017; Jarrahi, 2018)**
- Augmentation vs Automation
- Complementary skills hypothesis
- Hybrid intelligence systems

**Uygulama:**
```
Dual-mode → Farklı symbiosis türleri
Similarity → Amplification (güçlendirme)
Complementary → Augmentation (tamamlama)
```

---

## 2. MATEMATİKSEL FORMÜLASYON

### 2.1 Notasyon Sistemi

**Setler:**
- \( U \): Kullanıcılar kümesi, \( u \in U \)
- \( P \): Persona'lar kümesi, \( p \in P \)
- \( T \): Görevler kümesi, \( t \in T \)
- \( M \): LLM modelleri kümesi, \( m \in M \)

**Vektörler:**
- \( \vec{u} \in \mathbb{R}^{10} \): Kullanıcı yetkinlik vektörü
- \( \vec{p} \in \mathbb{R}^{10} \): Persona karakteristik vektörü

**Skalalar:**
- \( s \in [0,1] \): Yetkinlik skoru
- \( \ell \in \{novice, ..., expert\} \): Yetkinlik seviyesi
- \( g \in [0,1] \): Öğrenme amacı (0=production, 1=learning)

### 2.2 Kullanıcı Vektörü

\[
\vec{u} = \begin{bmatrix}
u_{tech} \\
u_{domain} \\
u_{ai} \\
u_{goal} \\
u_{proc} \\
u_{decl} \\
u_{cond} \\
u_{cogn} \\
u_{pattern} \\
u_{abstract}
\end{bmatrix} \in [0,1]^{10}
\]

**Mapping Function (Dreyfus Model):**

\[
\phi: \ell \mapsto s, \quad \phi(novice) = 0.1, ..., \phi(expert) = 0.9
\]

### 2.3 Ana Tavsiye Formülü (Dual-Mode)

#### **Genel Form:**

\[
R_{mode}(u,p) = \sum_{i=1}^{4} w_i \cdot f_i(u,p)
\]

Burada \( \sum w_i = 1 \) (normalize edilmiş ağırlıklar)

#### **Mod 1: Similarity-Based**

\[
R_{sim}(u,p) = \alpha \cdot S(u,p) + \beta \cdot C(u,p) + \gamma \cdot P(u,p,t) + \delta \cdot L(u,p,\tau)
\]

**Bileşenler:**

1. **Benzerlik Skoru (Hybrid Distance):**
   \[
   S(u,p) = w_1 \cdot \text{cos}(\vec{u}, \vec{p}) + w_2 \cdot \left(1 - \frac{d_{euc}(\vec{u}, \vec{p})}{d_{max}}\right)
   \]
   
   \[
   \text{cos}(\vec{u}, \vec{p}) = \frac{\vec{u} \cdot \vec{p}}{||\vec{u}|| \cdot ||\vec{p}||}
   \]

2. **Yetkinlik Uyumu (Gaussian ZPD):**
   \[
   C(u,p) = \exp\left(-\lambda |s_u - d_p|^2\right) \cdot a(u,p)
   \]
   
   - \( s_u \): User skill level
   - \( d_p \): Persona difficulty
   - \( \lambda = 2.0 \): Sensitivity parameter
   - \( a(u,p) \): Alignment factor

3. **Performans Tahmini (Sigmoid Regression):**
   \[
   P(u,p,t) = \sigma\left(\beta_0 + \beta_1 s_u + \beta_2 q_p + \beta_3 S(u,p) + \beta_4 c_t\right)
   \]
   
   \[
   \sigma(z) = \frac{1}{1 + e^{-z}}
   \]

4. **Öğrenme Yörüngesi (Power Law):**
   \[
   L(u,p,\tau) = L_{max} \cdot (1 - e^{-k\tau}) \cdot \pi(u,p)
   \]
   
   - \( \tau \): Time factor
   - \( k = 2.0 \): Learning rate
   - \( \pi(u,p) \): Learning potential

#### **Mod 2: Complementary-Based**

\[
R_{comp}(u,p) = \alpha \cdot (1 - S(u,p)) + \beta \cdot D(u,p) + \gamma \cdot P(u,p,t) + \delta \cdot L(u,p,\tau)
\]

**Yeni Bileşen - Tamamlayıcılık:**

\[
D(u,p) = \frac{1}{n} \sum_{i=1}^{n} \max(0, p_{strong,i} \cdot u_{weak,i})
\]

Burada:
- \( u_{weak,i} = 1 - u_i \): Kullanıcının i. boyuttaki zayıf yönü
- \( p_{strong,i} \): Persona'nın i. boyuttaki güçlü yönü

#### **Mod 3: Adaptive (Hybrid)**

\[
R_{adaptive}(u,p) = g \cdot R_{comp}(u,p) + (1-g) \cdot R_{sim}(u,p)
\]

- \( g = u_{goal} \): Learning goal (0=production, 1=learning)

### 2.4 Ağırlık Katsayıları

**Default Values (Pilot Study'den):**
- \( \alpha = 0.30 \): Similarity/Dissimilarity
- \( \beta = 0.35 \): Competency/Complementarity  
- \( \gamma = 0.25 \): Performance prediction
- \( \delta = 0.10 \): Learning trajectory

**Bayesian Update:**

\[
P(\theta|D) = \frac{P(D|\theta) \cdot P(\theta)}{P(D)}
\]

- \( \theta = \{\alpha, \beta, \gamma, \delta\} \): Parametreler
- \( D \): Feedback data (user ratings)

### 2.5 Persona Ranking

\[
rank(p_i) = \arg\max_{p \in P} R_{mode}(u, p)
\]

**Top-K Selection:**

\[
P_{top-k} = \{p_1, p_2, ..., p_k : R(u,p_1) \geq R(u,p_2) \geq ... \geq R(u,p_k)\}
\]

---

## 3. DUAL-MODE STRATEJİSİ

### 3.1 Teorik Gerekçelendirme

| Aspect | Similarity Mode | Complementary Mode |
|--------|----------------|-------------------|
| **Teorik Temel** | Scaffolding (Wood et al.) | ZPD Stretching (Vygotsky) |
| **Cognitive Load** | Düşük (Sweller) | Orta-Yüksek (Germane) |
| **Öğrenme Tipi** | Incremental | Transformational |
| **Risk** | Düşük | Orta |
| **Gelişim Hızı** | Yavaş, güvenli | Hızlı, riskli |

### 3.2 Mod Seçim Algoritması

```python
def select_mode(user_vector, context):
    """
    Mod seçim decision tree
    """
    if user_vector.learning_goal > 0.7:
        # Öğrenme odaklı
        if user_vector.cognitive_capacity > 0.6:
            return "complementary"  # Kapasitesi var, zorla
        else:
            return "hybrid"  # Dikkatli zorla
    
    elif user_vector.learning_goal < 0.3:
        # Production odaklı
        return "similarity"  # Rahat çalış
    
    else:
        # Kararsız
        return "adaptive"  # Duruma göre
```

### 3.3 Trade-off Analizi

**Pareto Frontier:**

\[
\text{Maximize } \begin{cases}
f_1(p) = \text{Learning Effectiveness} \\
f_2(p) = \text{Production Quality} \\
f_3(p) = \text{User Comfort}
\end{cases}
\]

\[
\text{s.t. } \sum_{i} w_i = 1, \quad w_i \geq 0
\]

---

## 4. HİPOTEZ SİSTEMİ

### 4.1 Ana Hipotezler (Testable)

#### **H1: Mod Effectiveness (Main Effect)**

\[
H_1: \mu_{learning,comp} > \mu_{learning,sim}, \quad p < 0.05
\]

"Learning goal için complementary mod, similarity'den daha etkilidir"

**Test:** Independent t-test

#### **H2: Yetkinlik-Mod Interaction**

\[
H_2: \exists \text{ interaction between } \ell \text{ and mode}
\]

"Yetkinlik seviyesi ile mod effectiveness arasında etkileşim vardır"

**Test:** 2-way ANOVA
- Factor 1: Level (5 seviye)
- Factor 2: Mode (2 mod)
- DV: Performance score

#### **H3: Complementarity Effect Size**

\[
H_3: d_{edu \rightarrow tech} > 0.8, \quad d_{novice \rightarrow expert} > 1.0
\]

"Tamamlayıcılık effect size'ı büyük olacaktır"

**Test:** Cohen's d calculation

\[
d = \frac{\mu_1 - \mu_2}{\sigma_{pooled}}
\]

#### **H4: Learning Trajectory Prediction**

\[
H_4: R^2 > 0.70 \text{ for performance prediction model}
\]

"Model, kullanıcı performansını yüksek doğrulukla tahmin eder"

**Test:** Regression analysis

\[
Performance = \beta_0 + \beta_1 \cdot s_u + \beta_2 \cdot d_p + \beta_3 \cdot R(u,p) + \epsilon
\]

### 4.2 Alt Hipotezler

**H4a:** Similarity mod, cognitive load'u azaltır  
**H4b:** Complementary mod, öğrenme hızını artırır  
**H4c:** Hybrid mod, her ikisinden de üstündür

---

## 5. EMPİRİK VALİDASYON

### 5.1 Veri Toplama Protokolü

**N = 150 katılımcı:**
- 5 yetkinlik seviyesi × 2 domain × 15 kişi

**Deneysel Tasarım:**

\[
\text{Design: } 5 \times 2 \times 2 \times 3 \text{ Factorial}
\]

- **Factor 1:** Yetkinlik (5 seviye)
- **Factor 2:** Domain (Teknik/Eğitim)
- **Factor 3:** Mod (Similarity/Complementary)
- **Factor 4:** Task Complexity (Düşük/Orta/Yüksek)

### 5.2 Ölçüm Araçları

**Bağımsız Değişkenler:**
- \( X_1 \): Yetkinlik seviyesi (ordinal)
- \( X_2 \): Domain türü (categorical)
- \( X_3 \): Recommendation mode (categorical)
- \( X_4 \): Task complexity (continuous, 0-1)

**Bağımlı Değişkenler:**
- \( Y_1 \): Performance score (continuous, 0-100)
- \( Y_2 \): Learning gain (pre-post diff)
- \( Y_3 \): Cognitive load (NASA-TLX)
- \( Y_4 \): User satisfaction (Likert 1-5)

### 5.3 İstatistiksel Analizler

#### **Tanımlayıcı İstatistikler:**

\[
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i, \quad s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2
\]

#### **ANOVA (Çok Faktörlü):**

\[
Y_{ijkl} = \mu + \alpha_i + \beta_j + \gamma_k + (\alpha\beta)_{ij} + (\alpha\gamma)_{ik} + \epsilon_{ijkl}
\]

- \( \alpha_i \): Yetkinlik etkisi
- \( \beta_j \): Domain etkisi
- \( \gamma_k \): Mod etkisi
- \( (\alpha\beta)_{ij} \): Etkileşim terimleri

#### **Regression Model:**

\[
\hat{Y} = \beta_0 + \sum_{i=1}^{p} \beta_i X_i + \epsilon
\]

**Model Fit:**
- \( R^2 \): Explained variance
- \( RMSE = \sqrt{\frac{1}{n}\sum(y_i - \hat{y}_i)^2} \)
- \( AIC = 2k - 2\ln(L) \): Model comparison

#### **Effect Size:**

\[
\eta^2 = \frac{SS_{between}}{SS_{total}}, \quad \omega^2 = \frac{SS_{between} - df_{between} \cdot MS_{error}}{SS_{total} + MS_{error}}
\]

---

## 6. AKADEMİK KATKI

### 6.1 Teorik Katkılar

**1. Dual-Mode Recommendation Framework**
- **Yenilik:** İlk defa similarity VE complementarity'yi birleştiren model
- **Katkı:** Human-AI interaction literature'üne yeni teorik framework
- **Formül:** \( R_{dual}(u,p) = g \cdot R_{comp} + (1-g) \cdot R_{sim} \)

**2. Multi-Dimensional Competency Modeling**
- **Yenilik:** 10 boyutlu yetkinlik vektörü (Dreyfus + bilgi türleri + bilişsel faktörler)
- **Katkı:** Dreyfus Model'in LLM bağlamına uyarlanması
- **Formül:** \( \vec{u} \in \mathbb{R}^{10} \)

**3. Persona-as-Proxy Methodology**
- **Yenilik:** AI persona'ları farklı yetkinlik seviyelerinin proxy'si olarak kullanma
- **Katkı:** Simulated expertise modeling
- **Formül:** \( \vec{p} \sim Expert_{\ell} \)

### 6.2 Metodolojik Katkılar

**1. Hybrid Similarity Metric**
- Cosine + Euclidean kombinasyonu
- \( S = w_1 \cdot \text{cos} + w_2 \cdot (1 - d_{norm}) \)

**2. Complementarity Function**
- User weakness × Persona strength
- \( D(u,p) = \sum (1-u_i) \cdot p_i \)

**3. Bayesian Weight Optimization**
- Feedback-driven parameter update
- \( P(\theta|D) \propto P(D|\theta) \cdot P(\theta) \)

### 6.3 Pratik Katkılar

**1. PIDL Platform**
- Open-source research platform
- Reproducible experiments
- Data collection infrastructure

**2. Dual-Perspective Metrics**
- Technical (Code quality, performance)
- Pedagogical (Learning ease, cognitive load)

**3. Multi-LLM Comparison**
- Cross-model validation
- Provider-agnostic framework

---

## 7. YAYINLANMA POTANSİYELİ

### Hedef Dergiler:

**Tier 1 (Q1):**
- IEEE Transactions on Education (IF: 2.5)
- Computers & Education (IF: 11.2)
- International Journal of Artificial Intelligence in Education (IF: 6.7)

**Tier 2 (Q2):**
- Educational Technology Research and Development
- Journal of Educational Computing Research

### Makale Başlıkları (Öneriler):

1. **"Dual-Mode Recommendation Framework for Human-AI Collaboration in Code Generation: A Competency Transfer Perspective"**

2. **"Similarity vs Complementarity: Mathematical Modeling of Optimal AI Persona Selection in Educational Technology"**

3. **"Multi-Dimensional Competency Modeling for Adaptive AI-Assisted Learning: A Bayesian Approach"**

---

## 8. SONUÇ

Bu framework, **üç ana akademik katkı** sunmaktadır:

1. **Teorik:** Dual-mode recommendation (similarity + complementarity)
2. **Metodolojik:** 10 boyutlu yetkinlik vektörü + Bayesian optimization
3. **Pratik:** PIDL platform + dual-perspective metrics

**Formül Özeti:**

\[
\boxed{
R(u,p) = 
\begin{cases}
\alpha S + \beta C + \gamma P + \delta L & \text{if production} \\
\alpha(1-S) + \beta D + \gamma P + \delta L & \text{if learning} \\
g \cdot R_{comp} + (1-g) \cdot R_{sim} & \text{if adaptive}
\end{cases}
}
\]

---

**SON GÜNCELLEME:** Ekim 2025  
**DURUM:** Pilot test hazır, empirik veri toplama başlayabilir  
**NEXT STEPS:** N=150 ile tam veri toplama, ANOVA, regression, publication

---

## KAYNAKÇA (Seçilmiş)

1. Sweller, J. (1988). Cognitive load during problem solving. *Cognitive Science*, 12(2), 257-285.
2. Vygotsky, L. S. (1978). *Mind in society*. Harvard University Press.
3. Nonaka, I., & Takeuchi, H. (1995). *The knowledge-creating company*. Oxford University Press.
4. Dreyfus, H. L., & Dreyfus, S. E. (1986). *Mind over machine*. Free Press.
5. Jarrahi, M. H. (2018). Artificial intelligence and the future of work: Human-AI symbiosis in organizational decision making. *Business Horizons*, 61(4), 577-586.
6. Zheng, N., et al. (2017). Hybrid-augmented intelligence. *Frontiers of Information Technology & Electronic Engineering*, 18(2), 153-179.


