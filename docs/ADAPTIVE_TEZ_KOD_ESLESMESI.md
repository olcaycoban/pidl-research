# Tezdeki Adaptive Kısmı – Kodda Nerede?

Bu belge, tezdeki **Adaptive (Mod 3)** kavramının kodda **nerede** tanımlı olduğunu ve araştırma uygulamasında **nasıl** kullanıldığını özetler.

---

## 1. Tezdeki Adaptive (THEORETICAL_FRAMEWORK.md)

- **Mod 3: Adaptive (Hybrid)**  
  \[
  R_{adaptive}(u,p) = g \cdot R_{comp}(u,p) + (1-g) \cdot R_{sim}(u,p)
  \]  
  \( g = u_{goal} \) (learning_goal: 0 = production, 1 = learning).

- **Mod seçim algoritması (tez):**
  - learning_goal > 0.7 → **complementary** (veya cognitive_capacity’ye göre hybrid)
  - learning_goal < 0.3 → **similarity**
  - arada → **adaptive** (duruma göre)

Yani: Kullanıcının **öğrenme hedefine** göre otomatik olarak Similar / Complementary / Hybrid skoru kullanılır.

---

## 2. Kodda Adaptive Nerede? (recommendation_engine.py)

### 2.1 Varsayılan mod = "adaptive"

**Dosya:** `src/recommendation_engine.py`  
**Fonksiyon:** `calculate_recommendation_score(..., mode: str = "adaptive")`

- **Satır ~883:** `mode` parametresi varsayılan olarak **"adaptive"**.
- Yani bu fonksiyon **mode verilmeden** çağrıldığında tezdeki adaptive mantığı devreye girer.

### 2.2 Mod belirleme (learning_goal’a göre)

**Satır ~916–924:**

```python
if mode == "adaptive":
    if user.learning_goal > 0.7:
        actual_mode = "complementary"
    elif user.learning_goal < 0.3:
        actual_mode = "similarity"
    else:
        actual_mode = "hybrid"
else:
    actual_mode = mode
```

- **learning_goal > 0.7** → tezdeki “öğrenme odaklı” → **complementary**.
- **learning_goal < 0.3** → tezdeki “production odaklı” → **similarity**.
- **Arada (0.3–0.7)** → **hybrid**.

Bu blok, tezdeki “Mod seçim algoritması”nın kod karşılığıdır.

### 2.3 Hybrid skoru = tezdeki R_adaptive formülü

**Satır ~948–965 (else: hybrid):**

```python
else:  # hybrid
    similarity_score = α·S + β·C + γ·P + δ·L
    complementary_score = α·(1-S) + β·D + γ·P + δ·L
    total_score = user.learning_goal * complementary_score + (1 - user.learning_goal) * similarity_score
```

Burada:
- `total_score = g · R_comp + (1-g) · R_sim`, \( g = \texttt{user.learning\_goal} \).

Yani **hybrid** durumunda kullanılan skor, tezdeki **R_adaptive** formülüyle aynıdır.

### 2.4 Adaptive’in kullanıldığı yer: rank_personas

**Fonksiyon:** `rank_personas(user_vector, task_complexity, top_k)`  
**Satır ~1021–1026:** `calculate_recommendation_score(user_vector, persona_vec, task_complexity)` çağrılır; **mode verilmez** → varsayılan **"adaptive"** kullanılır.

Yani: **Tüm persona’ları tek bir skorla sıralarken** (top_k liste için) tezdeki **adaptive** mantığı kullanılıyor: learning_goal’a göre otomatik similarity / complementary / hybrid seçiliyor.

---

## 3. Araştırma Uygulamasında (research_app.py) Neden “Adaptive” Görünmüyor?

**Dosya:** `research_app.py`  
**Fonksiyon:** `get_persona_recommendations_from_profile(profile, use_math_engine=True)`

Burada **iki ayrı** persona seçiliyor:

- **Similar persona:** dominant alandan, **mode="similarity"** ile skorlanıp en yüksek skorlu seçiliyor (satır ~147–151).
- **Complementary persona:** zayıf alandan, **mode="complementary"** ile skorlanıp en yüksek skorlu seçiliyor (satır ~167–171).

Yani uygulama, **her zaman** iki sabit mod kullanıyor:  
“Similar için sadece similarity skoru, Complementary için sadece complementary skoru.”  
Bu tasarım, **deneysel kontrol** için: her katılımcıya hem Similar hem Complementary persona atanıp 3+3 görevle karşılaştırılıyor. Bu yüzden **adaptive mod burada açıkça kullanılmıyor**; modlar bilinçli olarak **similarity** ve **complementary** olarak sabitleniyor.

Özet:

- **Adaptive, motor içinde var:** `calculate_recommendation_score(..., mode="adaptive")` ve `rank_personas(...)`.
- **Araştırma akışında sabit mod:** Similar = `mode="similarity"`, Complementary = `mode="complementary"`.

---

## 4. Özet Tablo

| Tez kavramı | Kod yeri | Araştırma uygulamasında kullanım |
|-------------|----------|----------------------------------|
| Mod 3: Adaptive | `recommendation_engine.py` → `calculate_recommendation_score(..., mode="adaptive")` (varsayılan) | Kullanılmıyor; Similar/Complementary için mod açıkça `"similarity"` / `"complementary"` |
| Mod seçimi (learning_goal > 0.7 vb.) | Aynı fonksiyon, satır ~916–924 | Sadece `rank_personas` veya mode verilmeden yapılan çağrılarda geçerli |
| R_adaptive = g·R_comp + (1−g)·R_sim | Aynı fonksiyon, satır ~948–965 (hybrid bloğu) | Sadece `actual_mode == "hybrid"` olduğunda (yani mode="adaptive" ve 0.3 ≤ learning_goal ≤ 0.7) |
| Toplu sıralama (adaptive ile) | `rank_personas(...)` → içeride `calculate_recommendation_score` (mode verilmez → adaptive) | `get_persona_recommendations_from_profile` içinde `rank_personas` kullanılmıyor; her iki persona ayrı modla skorlanıyor |

---

## 5. Doğrulama: Adaptive Gerçekten Çalışıyor mu?

**Test dosyası:** `src/test_adaptive.py`  
**Çalıştırma:** `python3 -m src.test_adaptive` (proje kökünden)

Test şunları kontrol eder: learning_goal > 0.7 → complementary; learning_goal < 0.3 → similarity; 0.3–0.7 → hybrid; mode verilmeden varsayılan adaptive; rank_personas mode vermediği için adaptive kullanır. Tüm adımlar geçti → **adaptive kodda doğru çalışıyor**.

---

## 6. Sonuç

- **Tezdeki adaptive kısmı** kodda **recommendation_engine.py** içinde, **calculate_recommendation_score** fonksiyonunda (varsayılan `mode="adaptive"`) ve **hybrid** skor formülünde tam karşılığını buluyor.
- **rank_personas** bu fonksiyonu mode vermeden çağırdığı için adaptive’i kullanıyor.
- **research_app.py** ise deneysel tasarım gereği **her zaman** Similar için `mode="similarity"`, Complementary için `mode="complementary"` verdiği için adaptive bu akışta **açıkça görünmüyor**; ama motor tarafında tanımlı ve istenirse başka çağrılarda (ör. doğrudan `rank_personas` veya `mode="adaptive"` ile skorlama) kullanılabilir.
