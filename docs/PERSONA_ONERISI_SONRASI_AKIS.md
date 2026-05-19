# Persona Önerisi Sonrası Akış – Adım Adım ve Teoriler


## Genel Özet

| Aşama | Ne oluyor? | Kullanılan teori(ler) |
|-------|------------|------------------------|
| 1 | İki persona atanır (Similar + Complementary) | Dual-Mode, ZPD, Dreyfus |
| 2 | Görev–persona eşlemesi (1,3,5 → Similar; 2,4,6 → Complementary) | Deneysel tasarım (within-subject) |
| 3 | Her görevde 5 alt adım | CLT, Öğrenme ölçümü, NASA-TLX |
| 4 | Veri toplama ve final değerlendirme | Araştırma metrikleri |

---

## Adım 1: Persona Önerisi ve Atama (Faz 2 sonu)

**Ne oluyor?**
- Yetkinlik değerlendirmesi bittikten sonra **Recommendation Engine** çalışır.
- **Similar persona:** Dominant alanınızdan (teknik veya eğitimsel), matematiksel skoru en yüksek persona seçilir.
- **Complementary persona:** Zayıf alanınızdan, “eksikleri en iyi tamamlayan” persona seçilir.
- Bu iki persona `st.session_state.similar_persona` ve `st.session_state.complementary_persona` olarak saklanır.
- Katılımcı veritabanına kaydedilir; ekranda 2 persona kartı ve (isteğe açılır) 6 aşamalı skor detayı gösterilir.

**Kullanılan teoriler / kavramlar:**
- **Dreyfus Model:** Persona’lar Dreyfus seviyelerine göre tanımlı; dominant/weak domain ile alan eşlemesi.
- **Zone of Proximal Development (ZPD, Vygotsky):**  
  - Similar → “ZPD içinde” (mevcut seviyeye uyum).  
  - Complementary → “ZPD sınırını zorlama” (gelişim alanı).
- **Dual-Mode Stratejisi (THEORETICAL_FRAMEWORK):**  
  - Similarity mode: R = α·S + β·C + γ·P + δ·L (benzerlik, yetkinlik uyumu, performans, öğrenme).  
  - Complementary mode: R = α·(1−S) + β·D + γ·P + δ·L (farklılık, tamamlayıcılık, performans, öğrenme).
- **Multi-Criteria Decision Analysis (MCDA):** S, C, P, L (ve D) bileşenleri ağırlıklı toplanarak tek skor.

**Kod:** `get_persona_recommendations_from_profile()` → `RecommendationEngine.calculate_recommendation_score(..., mode="similarity" | "complementary")`.

---

## Adım 2: “Görevlere Başla” ve Görev–Persona Eşlemesi

**Ne oluyor?**
- Kullanıcı **“Görevlere Başla”** butonuna basar → `phase = 'tasks'`, `current_task_number = 1`.
- Her görev numarası için **hangi AI (Similar / Complementary)** kullanılacak sabit kurala göre atanır:
  - **Görev 1, 3, 5** → **Similar** AI (dominant alan persona’sı).
  - **Görev 2, 4, 6** → **Complementary** AI (zayıf alan persona’sı).
- Böylece her katılımcı **3 görev Similar, 3 görev Complementary** ile çalışır (dengeli within-subject tasarım).

**Teori:** Deneysel kontrol; Similar vs Complementary etkisini karşılaştırmak için aynı kişi her iki tipi de deneyimler.

**Kod:** `assign_ai_persona_for_task(task_number, similar_persona, complementary_persona)`.

---

## Adım 3: Her Görevde 5 Alt Adım (Faz 3)

Her görev (1–6) için **aynı sayfada** sırayla 5 alt adım uygulanır.

### 3.1 Pre-test (`pre_test`)

**Ne oluyor?**
- Göreve başlamadan önce **görevle ilgili 3 bilgi sorusu** sorulur.
- Cevaplar ve skor kaydedilir; **Task session** başlatılır (veritabanına kayıt).
- Sonra `task_substep = 'task_work'` olur.

**Teori:** **Ön-test–son-test tasarımı**; görev öncesi bilgi seviyesi (baseline) ölçülür, sonra öğrenme kazanımı post-test ile karşılaştırılır.

---

### 3.2 Görev çalışması (`task_work`)

**Ne oluyor?**
- Görev tanımı ve **atanan persona** (Similar veya Complementary) gösterilir.
- Kullanıcı metin alanına **prompt** yazar; **“Kod Üret”** ile OpenAI API çağrılır; persona’nın system prompt’u kullanılarak kod üretilir.
- Üretilen kod, süre ve (varsa) içerik analizi gösterilir.
- **“Sonraki: Post-Test”** ile `task_substep = 'post_test'` olur.

**Teoriler:**
- **Cognitive Load Theory (CLT, Sweller):** Persona seçimi extraneous load’u azaltmak, optimal challenge ile germane load’u artırmak için kullanılır; recommendation engine’de CLT skoruna göre persona sıralama seçeneği de vardır.
- **Knowledge Transfer (Nonaka & Takeuchi):** Persona’nın ürettiği kod ve açıklamalar “externalization”; kullanıcı ile etkileşim “socialization” benzeri.
- **Human–AI Symbiosis:** Similar → amplification (mevcut yetkinliği güçlendirme); Complementary → augmentation (zayıf alanı tamamlama).

---

### 3.3 Post-test (`post_test`)

**Ne oluyor?**
- Görev **sonrası** aynı konuda **5 soru** sorulur.
- Cevaplar ve skor kaydedilir.
- Pre–post skor farkı ileride **öğrenme kazanımı** olarak analiz edilir.

**Teori:** **Öğrenme transferi / kazanım ölçümü**; görev ve persona’nın bilgi edinimine etkisi.

---

### 3.4 NASA-TLX (`nasa_tlx`)

**Ne oluyor?**
- **NASA-TLX** (Task Load Index) formu sunulur: zihinsel talep, fiziksel talep, zaman baskısı, başarı hissi, çaba, hayal kırıklığı vb.
- Yanıtlar kaydedilir.

**Teori:** **Bilişsel yük ölçümü** (CLT ile uyumlu); görevin ve persona’nın kullanıcıda oluşturduğu yük nicel olarak toplanır.

---

### 3.5 AI değerlendirme (`ai_evaluation`)

**Ne oluyor?**
- Kullanıcı **AI çıktısını** değerlendirir (kalite, uygunluk vb.).
- **Görev 1:** Sadece görev zorluğu değerlendirmesi.
- **Görev 2–6:** “Bu görev için diğer AI daha uygun olur muydu?” (Similar vs Complementary) + neden + zorluk.
- Bu karşılaştırma verileri **veritabanına** kaydedilir (`save_task_comparison`).
- Task session tamamlanır (süre kaydedilir); `current_task_number` 1 artar; sonraki göreve veya Faz 4’e geçilir.

**Teori:** **Subjektif uygunluk ve tercih**; Similar vs Complementary’nin görev bazında nasıl algılandığı.

---

## Adım 4: 6. Görev Bittikten Sonra – Final (Faz 4)

**Ne oluyor?**
- `current_task_number > 6` olunca `phase = 'final'`.
- **Final anketi** (FinalSurveyForm): Hangi AI’yı tercih ettiniz (Benzer / Tamamlayıcı / Duruma göre), neden, öğrenme/hız açısından hangisi daha uygun, Likert maddeleri vb.
- **“Araştırmayı Tamamla”** → Final cevapları kaydedilir; katılımcı “tamamlandı” işaretlenir; toplam süre kaydedilir; `phase = 'complete'`.

**Teori:** **Genel tercih ve algı**; hipotezlerdeki “Similar vs Complementary” karşılaştırması için birincil anket verisi.

---

## Adım 5: Tamamlanma (Faz 5)

**Ne oluyor?**
- Teşekkür ekranı, katılımcı ID, iletişim bilgisi gösterilir.
- Başka işlem yok; oturum biter.

---

## Teorilerin Kısa Eşlemesi

| Teori / kavram | Nerede kullanılıyor? |
|----------------|----------------------|
| **Dreyfus Model** | Yetkinlik seviyesi, persona seviyeleri, dominant/weak domain. |
| **ZPD (Vygotsky)** | Similar = ZPD içi; Complementary = ZPD sınırı; competency match formülü “optimal challenge”. |
| **Cognitive Load Theory (CLT)** | Persona seçimi (yükü yönetmek); NASA-TLX ile bilişsel yük ölçümü. |
| **Dual-Mode (Similar / Complementary)** | Öneri skoru R(u,p); görev ataması 3+3. |
| **MCDA** | R = α·S + β·C + γ·P + δ·L (ve complementary’de D). |
| **Nonaka & Takeuchi** | Bilgi türleri (procedural, declarative, conditional); persona çıktısı externalization. |
| **Human–AI Symbiosis** | Similar = amplification; Complementary = augmentation. |
| **Ön-test–son-test** | Pre-test / post-test ile öğrenme kazanımı. |
| **NASA-TLX** | Görev sonrası bilişsel yük anketi. |

---

## Veri Akışı Özeti

```
Persona önerisi (Similar + Complementary)
    → Session’da saklanır
    → Her görev için assign_ai_persona_for_task ile persona atanır
    → Görev 1..6: Pre-test → Kod üret (OpenAI + persona) → Post-test → NASA-TLX → AI değerlendirme
    → Her görevde: TaskSession, pre/post skorları, NASA-TLX, karşılaştırma cevapları DB’ye yazılır
    → 6. görev bitince Final anketi → Tamamlanma
```

Bu akış, persona önerisi sonrası **ne olduğunu** ve **hangi teorilerin hangi adımda** devreye girdiğini tek belgede toplar.
