# User Vector Parametrelerinin Hesaplanması

Bu belge, `recommendation_engine.py` içindeki `create_user_vector()` fonksiyonunda **learning_goal**, **bilgi türleri** (procedural, declarative, conditional) ve **bilişsel faktörler** (cognitive_capacity, pattern_recognition, abstraction_level) parametrelerinin nasıl hesaplandığını açıklar.

---

## Girdi: `competency_profile` (Dict)

Fonksiyon şu anahtarları kullanır (yoksa varsayılan):

| Anahtar | Açıklama | Varsayılan | Örnek |
|---------|----------|------------|--------|
| `score` | Genel yetkinlik skoru (0-100) | 0 | 64 |
| `level` | Dreyfus seviyesi (string) | 'novice' | 'competent' |
| `domain` | Dominant domain | 'technical' | 'technical' |
| `responses` | Anket yanıtları dict | {} | {...} |

**Not:** `score` 0-1 aralığına `score / 100` ile normalize edilir. Örnek: 64 → 0.64.

---

## 1. learning_goal (0–1)

**Kod:**
```python
if level in ['novice', 'advanced_beginner']:
    learning_goal = 0.9
elif level == 'competent':
    learning_goal = 0.6
else:  # proficient, expert
    learning_goal = 0.3
```

**Mantık:** Dreyfus seviyesine göre sabit atanır.

| Seviye | learning_goal | Anlamı |
|--------|----------------|--------|
| novice, advanced_beginner | 0.9 | Ağırlıklı öğrenme |
| competent | 0.6 | Öğrenme + üretim arası |
| proficient, expert | 0.3 | Ağırlıklı üretim |

**Teori:** Düşük seviyede öğrenme, yüksek seviyede production odaklı kabul edilir.

---

## 2. Bilgi türleri (Nonaka & Takeuchi, 1995)

Hepsi **normalize skor** `score ∈ [0, 1]` üzerinden hesaplanır (`score = competency_profile['score'] / 100`).

### 2.1 procedural_knowledge ("Nasıl" bilgisi)

**Formül:**
```python
procedural = min(1.0, score * 1.2)
```

- Skor yükseldikçe “nasıl yapılır” bilgisi artar.
- 1.2 katsayısı ile biraz yukarı çekilir; üst sınır 1.0.

**Örnek (score = 0.64):**
- procedural = min(1.0, 0.64 × 1.2) = min(1.0, 0.768) = **0.768** ≈ 0.77

---

### 2.2 declarative_knowledge ("Ne" bilgisi)

**Formül:**
```python
declarative = score
```

- Doğrudan normalize skor; “ne olduğu” bilgisi skorla aynı kabul edilir.

**Örnek (score = 0.64):**
- declarative = **0.64**

---

### 2.3 conditional_knowledge ("Ne zaman" bilgisi)

**Formül:**
```python
conditional = max(0.3, score - 0.2)
```

- Skordan 0.2 çıkarılır; alt sınır 0.3 ile korunur.
- “Ne zaman kullanılır” bilgisi, skor düştükçe 0.3’e yaklaşır.

**Örnek (score = 0.64):**
- conditional = max(0.3, 0.64 - 0.2) = max(0.3, 0.44) = **0.44**

---

## 3. Bilişsel faktörler

Yine **score ∈ [0, 1]** kullanılır.

### 3.1 cognitive_capacity

**Formül:**
```python
cognitive_capacity = 0.5 + (score * 0.5)
```

- Minimum 0.5, maksimum 1.0.
- Skor arttıkça bilişsel kapasite artar.

**Örnek (score = 0.64):**
- cognitive_capacity = 0.5 + (0.64 × 0.5) = 0.5 + 0.32 = **0.82**

---

### 3.2 pattern_recognition

**Formül:**
```python
pattern_recognition = max(0.3, score - 0.1)
```

- Skordan 0.1 çıkarılır; alt sınır 0.3.

**Örnek (score = 0.64):**
- pattern_recognition = max(0.3, 0.64 - 0.1) = max(0.3, 0.54) = **0.54**

---

### 3.3 abstraction_level

**Formül:**
```python
abstraction_level = score
```

- Declarative ile aynı: skor = soyutlama seviyesi.

**Örnek (score = 0.64):**
- abstraction_level = **0.64**

---

## Özet tablo (score = 0.64, level = 'competent')

| Parametre | Formül | Sonuç |
|-----------|--------|--------|
| learning_goal | level → competent ⇒ 0.6 | **0.6** |
| procedural_knowledge | min(1, 0.64×1.2) | **0.77** |
| declarative_knowledge | score | **0.64** |
| conditional_knowledge | max(0.3, 0.64−0.2) | **0.44** |
| cognitive_capacity | 0.5 + 0.64×0.5 | **0.82** |
| pattern_recognition | max(0.3, 0.64−0.1) | **0.54** |
| abstraction_level | score | **0.64** |

---

## research_app ile uyum

`research_app.py` profile_dict’te `score` ve `level` yerine `technical_score`, `educational_score`, `technical_level`, `dominant_domain` gönderiyor. Bu yüzden `create_user_vector` içinde:

- **score:** Yoksa `(technical_score + educational_score) / 2` Likert (1–5) ortalaması alınıp 0–1’e şu şekilde normalize edilir:  
  `(likert_avg - 1) / 4`
- **level:** Yoksa `technical_level` kullanılır.
- **domain:** Yoksa `dominant_domain` kullanılır.

Böylece yukarıdaki tüm formüller, research_app’ten gelen profil ile de aynı mantıkla çalışır.
