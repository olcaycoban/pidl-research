# 🔬 6 Aşamalı Matematiksel İçerik Analizi Sistemi

## 📋 Genel Bakış

PIDL Araştırma Sistemi artık **iki farklı 6 aşamalı matematiksel model** içeriyor:

### 1. **PERSONA SEÇİMİ için 6 Aşama** (Zaten vardı ✅)
- Kullanıcı vektörü oluşturma
- Persona vektörleri eşleştirme
- Benzerlik skoru (S)
- Yetkinlik uyumu (C)
- Performans tahmini (P)
- Öğrenme yörüngesi (L)

### 2. **İÇERİK ANALİZİ için 6 Aşama** (YENİ EKLENDI! 🆕)
- Prompt özellik çıkarımı
- Prompt benzerlik analizi (Cosine Similarity)
- Kod yapısı analizi
- Kod karmaşıklık analizi
- Kod kalite değerlendirmesi
- Komparatif analiz (Persona karşılaştırması)

---

## 🆕 YENİ: İçerik Analizi Modülü

### Dosya: `content_analyzer.py`

Bu modül, AI personaları tarafından üretilen **prompt'lar** ve **kodlar** için bilimsel analiz yapar.

---

## 📊 AŞAMA 1: Prompt Özellik Çıkarımı

### Hesaplanan Metrikler:

| Metrik | Açıklama | Formül |
|--------|----------|--------|
| **length** | Karakter sayısı | `len(prompt)` |
| **word_count** | Kelime sayısı | `len(prompt.split())` |
| **sentence_count** | Cümle sayısı | `len(re.split(r'[.!?]+', prompt))` |
| **technical_term_count** | Teknik terim sayısı | Blockchain, Solidity vb. |
| **clarity_score** | Netlik skoru (0-100) | `100 - (avg_sentence_length - 10) × 2` |
| **specificity_score** | Özgüllük skoru (0-100) | `(technical_terms / words) × 1000` |

### Örnek Çıktı:

```
Kelime Sayısı: 45
Cümle Sayısı: 3
Teknik Terim: 8
Netlik Skoru: 85/100
Özgüllük Skoru: 72/100
```

---

## 🔄 AŞAMA 2: Prompt Benzerlik Analizi

### Cosine Similarity Hesaplaması:

```python
# TF-IDF vektörleri oluştur
tfidf_matrix = vectorizer.fit_transform([prompt1, prompt2])

# Cosine benzerliği hesapla
cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
```

### 3 Farklı Benzerlik Metriği:

1. **Cosine Similarity** (TF-IDF bazlı)
   - Formül: `cos(θ) = (A · B) / (||A|| × ||B||)`
   - Aralık: 0.0 (tamamen farklı) → 1.0 (identik)

2. **Jaccard Similarity** (Kelime kümesi)
   - Formül: `J(A,B) = |A ∩ B| / |A ∪ B|`
   - Aralık: 0.0 → 1.0

3. **Overlap Ratio** (Ortak kelime oranı)
   - Formül: `|A ∩ B| / min(|A|, |B|)`
   - Aralık: 0.0 → 1.0

### Yorum Tablosu:

| Skor | Yorum |
|------|-------|
| ≥ 0.8 | Çok Yüksek - Neredeyse İdentik |
| 0.6 - 0.8 | Yüksek - Önemli Benzerlik |
| 0.4 - 0.6 | Orta - Kısmi Benzerlik |
| 0.2 - 0.4 | Düşük - Az Benzerlik |
| < 0.2 | Çok Düşük - Minimal Benzerlik |

### Örnek Çıktı:

```
Cosine Similarity: 0.742 - Yüksek - Önemli Benzerlik
Jaccard Similarity: 0.635
Overlap Ratio: 0.815
```

**💡 Araştırma Değeri:**
- Farklı görevlerde aynı kişinin prompt'ları ne kadar benzer?
- Similar AI vs Complementary AI prompt farkları

---

## 🏗️ AŞAMA 3: Kod Yapısı Analizi

### Hesaplanan Metrikler:

| Metrik | Açıklama |
|--------|----------|
| **total_lines** | Toplam satır sayısı |
| **code_lines** | Kod satırı (boş ve yorum hariç) |
| **comment_lines** | Yorum satırı |
| **blank_lines** | Boş satır |
| **comment_ratio** | Yorum oranı (%) |
| **function_count** | Fonksiyon sayısı (Solidity) |
| **avg_line_length** | Ortalama satır uzunluğu |

### Formüller:

```python
comment_ratio = (comment_lines / total_lines) × 100

function_count = len(re.findall(r'function\s+\w+', code))
```

### Örnek Çıktı:

```
Toplam Satır: 156
Kod Satırı: 98
Yorum Satırı: 42
Yorum Oranı: 26.9%
Fonksiyon Sayısı: 8
```

**💡 Araştırma Değeri:**
- Hangi persona daha çok yorum yazıyor?
- Kod uzunluğu ile öğrenme arasındaki ilişki

---

## 🔬 AŞAMA 4: Kod Karmaşıklık Analizi

### McCabe Cyclomatic Complexity:

```
CC = decision_points + 1

decision_points = if + require + assert + for + while
```

### Hesaplanan Metrikler:

| Metrik | Açıklama |
|--------|----------|
| **cyclomatic_complexity** | Döngüsel karmaşıklık |
| **nesting_depth** | Maksimum iç içe geçme |
| **variable_count** | Değişken sayısı |
| **conditional_count** | Koşul sayısı (if, require) |
| **loop_count** | Döngü sayısı (for, while) |
| **complexity_score** | Genel karmaşıklık (0-100) |

### Karmaşıklık Skoru Formülü:

```python
complexity_score = min(100,
    cyclomatic × 5 +
    nesting_depth × 10 +
    loop_count × 3
)
```

### Karmaşıklık Seviyeleri:

| Skor | Seviye |
|------|--------|
| 80-100 | Çok Yüksek - Refactoring Önerilir |
| 60-80 | Yüksek - Karmaşık |
| 40-60 | Orta - Kabul Edilebilir |
| 20-40 | Düşük - İyi |
| 0-20 | Çok Düşük - Basit |

### Örnek Çıktı:

```
Cyclomatic Complexity: 12
Nesting Depth: 3
Değişken Sayısı: 15
Koşul Sayısı: 8
Döngü Sayısı: 2
Karmaşıklık Skoru: 42/100 - Orta - Kabul Edilebilir
```

**💡 Araştırma Değeri:**
- Similar AI daha basit mi kod yazıyor?
- Karmaşıklık ile bilişsel yük ilişkisi

---

## ⭐ AŞAMA 5: Kod Kalite Değerlendirmesi

### 4 Ana Kalite Boyutu:

#### 1. **Okunabilirlik** (Readability)

```python
readability = base_score

# Yorum oranı bonusu
if comment_ratio >= 20%:
    readability += 20
elif comment_ratio >= 10%:
    readability += 10

# Satır uzunluğu bonusu
if avg_line_length <= 80:
    readability += 30
elif avg_line_length <= 120:
    readability += 15
```

#### 2. **Sürdürülebilirlik** (Maintainability)

```python
maintainability = 100 - (complexity_score × 0.5)

# Modülerlik bonusu
if function_count >= 3:
    maintainability += 10
```

#### 3. **Dokümantasyon** (Documentation)

```python
documentation = min(100, comment_ratio × 3)
```

#### 4. **En İyi Pratikler** (Best Practices)

```python
best_practices = base_score

if 'require(' in code:
    best_practices += 15  # Güvenlik kontrolü
if 'modifier' in code:
    best_practices += 15  # Kod yeniden kullanımı
if 'event' in code:
    best_practices += 10  # Olay yayını
if 'revert' or 'assert' in code:
    best_practices += 10  # Hata yönetimi
```

### Genel Kalite Skoru:

```python
overall_quality = (
    readability × 0.25 +
    maintainability × 0.35 +
    documentation × 0.20 +
    best_practices × 0.20
)
```

### Kalite Notlandırması:

| Skor | Not |
|------|-----|
| 90-100 | A+ (Mükemmel) |
| 80-90 | A (Çok İyi) |
| 70-80 | B (İyi) |
| 60-70 | C (Orta) |
| 50-60 | D (Zayıf) |
| 0-50 | F (Yetersiz) |

### Örnek Çıktı:

```
Okunabilirlik: 82/100
Sürdürülebilirlik: 75/100
Dokümantasyon: 81/100
Best Practices: 85/100
⭐ GENEL KALİTE: 80.4/100 - A (Çok İyi)
```

**💡 Araştırma Değeri:**
- Hangi persona daha kaliteli kod üretiyor?
- Kalite ile öğrenme kazanımı ilişkisi

---

## 📈 AŞAMA 6: Komparatif Analiz

### İki Persona Çıktısını Karşılaştırma:

```python
comparison = analyzer.compare_persona_outputs(
    persona1_name="Similar AI",
    code1=previous_code,
    prompt1=previous_prompt,
    persona2_name="Complementary AI",
    code2=current_code,
    prompt2=current_prompt
)
```

### Karşılaştırılan Boyutlar:

#### 1. **Prompt Benzerliği**
- İki persona'nın aynı görev için ürettiği prompt'ların benzerliği

#### 2. **Kalite Karşılaştırması**
```python
quality_comparison = {
    "persona1": overall_quality_1,
    "persona2": overall_quality_2,
    "winner": max_quality_persona,
    "difference": abs(quality_1 - quality_2)
}
```

#### 3. **Karmaşıklık Karşılaştırması**
```python
complexity_comparison = {
    "persona1": complexity_1,
    "persona2": complexity_2,
    "simpler": min_complexity_persona
}
```

#### 4. **Yapısal Benzerlik**
```python
# Normalize edilmiş farklar
metrics = ['code_lines', 'comment_lines', 'function_count']
for metric in metrics:
    similarity = 1 - (abs(val1 - val2) / max(val1, val2))
```

### Örnek Çıktı:

```
🔄 Prompt Benzerliği:
Cosine Similarity: 0.523 - Orta - Kısmi Benzerlik

📊 Kalite Karşılaştırması:
Similar AI: 78.5/100
Complementary AI: 82.3/100
🏆 Kalite Kazananı: Complementary AI (Fark: 3.8 puan)

🔬 Karmaşıklık Karşılaştırması:
Daha Basit Kod: Similar AI

📝 Dokümantasyon Karşılaştırması:
Daha İyi Dokümante: Complementary AI
```

**💡 Araştırma Değeri:**
- Similar vs Complementary: Hangisi ne zaman daha iyi?
- Persona değişiminin öğrenme etkisi
- Kod tutarlılığı analizi

---

## 🎓 Teorik Temel

### Kullanılan Akademik Metrikler:

1. **TF-IDF Cosine Similarity**
   - Metin benzerliği ölçümü
   - Kaynak: Salton & McGill (1983)

2. **McCabe Cyclomatic Complexity**
   - Kod karmaşıklığı metriği
   - Kaynak: McCabe (1976)

3. **Halstead Metrics**
   - Kod hacmi ve zorluk ölçümü
   - Kaynak: Halstead (1977)

4. **Maintainability Index**
   - Sürdürülebilirlik skoru
   - Kaynak: ISO/IEC 25010

5. **Code Readability Research**
   - Okunabilirlik metrikleri
   - Kaynak: Buse & Weimer (2010)

6. **Software Quality Metrics**
   - Genel kalite standartları
   - Kaynak: ISO/IEC 25010

---

## 📁 Dosya Yapısı

```
pidl/
├── content_analyzer.py          # YENİ: İçerik analiz modülü
├── recommendation_engine.py     # MEVCUT: Persona seçim engine
├── research_app.py              # GÜNCELLENDİ: Analiz entegrasyonu
├── requirements.txt             # GÜNCELLENDİ: scikit-learn eklendi
└── 6_ASAMALI_MATEMATIKSEL_ANALIZ.md  # Bu dosya
```

---

## 🚀 Kullanım

### Araştırma Akışında Gösterim:

1. Kullanıcı prompt girer
2. AI kodu üretir
3. Kod ekranda gösterilir
4. **"🔬 6 Aşamalı Matematiksel İçerik Analizi"** expander'ı açılır
5. Tüm 6 aşama otomatik hesaplanır ve gösterilir

### Manuel Analiz (Kod):

```python
from content_analyzer import ContentAnalyzer

analyzer = ContentAnalyzer()

# Tek analiz
analysis = analyzer.full_analysis(
    prompt="Write a simple NFT contract",
    code=generated_solidity_code
)

# İki çıktıyı karşılaştır
comparison = analyzer.compare_persona_outputs(
    persona1_name="Similar AI",
    code1=code1,
    prompt1=prompt1,
    persona2_name="Complementary AI",
    code2=code2,
    prompt2=prompt2
)
```

---

## 📊 Veri Toplama

### Session State'de Saklanan Veriler:

```python
st.session_state.previous_prompt       # Önceki prompt
st.session_state.previous_code         # Önceki kod
st.session_state.previous_persona_name # Önceki persona
```

### Veritabanına Kaydedilebilecek Metrikler:

- Prompt uzunluğu, netlik, özgüllük
- Prompt benzerlik skorları
- Kod yapısı metrikleri
- Karmaşıklık skorları
- Kalite skorları
- Komparatif analiz sonuçları

---

## 🎯 Araştırma Soruları

Bu analizlerle cevapla anabilecek sorular:

1. **Similar vs Complementary AI:**
   - Hangi persona daha kaliteli kod üretiyor?
   - Hangi persona daha basit/karmaşık kod yazıyor?
   - Hangi persona daha iyi dokümante ediyor?

2. **Öğrenme Etkisi:**
   - Kod kalitesi ile öğrenme kazanımı ilişkisi?
   - Karmaşıklık ile bilişsel yük ilişkisi?
   - Dokümantasyon ile anlaşılırlık ilişkisi?

3. **Prompt Analizi:**
   - Kullanıcılar ne kadar detaylı prompt yazıyor?
   - Prompt kalitesi ile kod kalitesi ilişkisi?
   - İki görev arasında prompt benzerliği?

4. **Persona Karşılaştırması:**
   - İki persona'nın çıktıları ne kadar farklı?
   - Persona değişiminin tutarlılık etkisi?
   - Hangi persona hangi göreve daha uygun?

---

## ✅ Kurulum

### Gerekli Kütüphaneler:

```bash
pip install scikit-learn==1.4.0
pip install numpy==1.26.3
```

### Test:

```python
from content_analyzer import ContentAnalyzer

analyzer = ContentAnalyzer()
print("✅ ContentAnalyzer başarıyla yüklendi!")
```

---

## 📚 Kaynaklar

1. McCabe, T. J. (1976). "A Complexity Measure". IEEE Transactions on Software Engineering.

2. Halstead, M. H. (1977). "Elements of Software Science". Elsevier.

3. Salton, G., & McGill, M. J. (1983). "Introduction to Modern Information Retrieval". McGraw-Hill.

4. Buse, R. P., & Weimer, W. R. (2010). "Learning a Metric for Code Readability". IEEE TSE.

5. ISO/IEC 25010:2011. "Systems and software Quality Requirements and Evaluation (SQuaRE)".

---

## 🎉 Özet

Sistem artık **TAM 6 AŞAMALI MATEMATİKSEL İÇERİK ANALİZİ** yapabiliyor:

✅ Prompt özellik çıkarımı
✅ Cosine similarity ile prompt benzerliği
✅ Kod yapısı analizi (satır, yorum, fonksiyon)
✅ Kod karmaşıklık analizi (McCabe CC)
✅ Kod kalite değerlendirmesi (4 boyut)
✅ Komparatif analiz (persona karşılaştırması)

**Artık sadece persona seçimi değil, üretilen içerik de bilimsel olarak analiz ediliyor! 🔬**
