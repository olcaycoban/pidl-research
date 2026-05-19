# Platform – Tüm Aşamalar (Fazlar) Detaylı Açıklama

PIDL Araştırma Sistemi **tek bir web sayfası** (Streamlit) üzerinde çalışır. Aynı URL'de kalırsınız; içerik **fazlara (phase)** göre değişir. Bu belge tüm 5 fazı ve görev alt adımlarını tek tek açıklar.

---

## Genel akış

| # | Faz | phase | Ekranda ne var? |
|---|-----|-------|------------------|
| 1 | Onam | `consent` | Bilgilendirilmiş onam formu |
| 2 | Yetkinlik | `competency` | CAQ yetkinlik anketi + persona önerisi |
| 3 | Görevler | `tasks` | 6 görev (her biri 5 alt adım) |
| 4 | Final | `final` | Final anketi |
| 5 | Tamamlandı | `complete` | Teşekkür / bitiş |

---

## Faz 1 – Onam (consent)

**Ne zaman:** Sayfa ilk açıldığında (`phase = 'consent'`).

**Ekranda:**
1. Başlık: "PIDL Araştırma Sistemi" / "1. Bilgilendirilmiş Onam Formu"
2. Araştırma metni: Amaç, süre, ne yapılacak, riskler, faydalar, gizlilik, haklar, iletişim
3. 5 onay kutusu: Okudum/anladım, Sorularım yanıtlandı, Gönüllü katılıyorum, Veri kullanımına izin, Çekilebileceğimi biliyorum
4. Beşi işaretlenince: "Tüm onaylar verildi"
5. Buton: **"Onay Verdim, Devam Et"**

**Buton sonrası:** `phase = 'competency'`, sayfa yenilenir → **Faz 2** açılır.

---

## Faz 2 – Yetkinlik (competency)

**Ne zaman:** Onam verildikten sonra.

**Ekranda:**
1. Başlık: "Yetkinlik Değerlendirmesi" / "2. Dreyfus Model Bazlı Yetkinlik Belirleme"
2. Bilgi kutusu: 10 soruluk yetkinlik + persona önerisi hakkında kısa açıklama
3. **1️⃣ Demografik:** Yaş, cinsiyet, eğitim durumu, mesleki deneyim, sektör (2 sütun)
4. **2️⃣ Teknik yetkinlik (8 soru):**
   - Blockchain Teknolojileri (4 slider 1–5)
   - Genel Programlama (4 slider 1–5)
5. **3️⃣ Pedagojik yetkinlik (8 soru):**
   - Eğitim Teorileri ve Uygulamaları (4 slider 1–5)
   - İletişim ve Sunum Becerileri (4 slider 1–5)
6. **4️⃣ AI araçları:** Hangi AI araçları (multiselect), kullanım sıklığı (selectbox), kullanım amaçları (multiselect)
7. **5️⃣ Öğrenme tercihleri:** 6 Likert slider (1–5)
8. **6️⃣ Kendini değerlendirme:** Dreyfus seviye, blockchain eğitimi ihtiyacı, AI destekli öğrenmede en faydalı özellik (selectbox)
9. Buton: **"Yetkinliğimi Değerlendir"**

**"Yetkinliğimi Değerlendir" sonrası:**
- CompetencyProfile oluşturulur (teknik/pedagojik skor, dominant/weak domain)
- User vector + recommendation engine ile **Similar** ve **Complementary** persona seçilir
- Katılımcı veritabanına kaydedilir
- Ekranda: yetkinlik özeti (skorlar, seviyeler), 2 persona kartı (Benzer AI / Tamamlayıcı AI), 6 aşamalı matematiksel hesaplama expander'ı
10. Buton: **"Görevlere Başla"**

**"Görevlere Başla" sonrası:** `phase = 'tasks'`, `current_task_number = 1`, `task_substep = 'pre_test'` → **Faz 3** açılır.

---

## Faz 3 – Görevler (tasks)

**Ne zaman:** Yetkinlik tamamlanıp "Görevlere Başla" tıklandıktan sonra.

**Genel:** Her görev (1–6) için **aynı sayfada** sırayla 5 alt adım (substep) gösterilir. Alt adım sırası: `pre_test` → `task_work` → `post_test` → `nasa_tlx` → `ai_evaluation`.

**Her görev ekranında üstte:**
- Başlık: "Görev X/6"
- Görev kartı: Başlık, zorluk, kullanılacak AI (Similar veya Complementary), persona adı, yetkinlik dengesi, görev açıklaması

**Görev 1, 3, 5:** Similar AI | **Görev 2, 4, 6:** Complementary AI

---

### Alt adım 1: Pre-test (`pre_test`)

- Başlık: "Pre-Test (3 soru)"
- Bilgi: Göreve başlamadan önce mevcut bilgiyi ölçme
- Görev bazlı 3 pre-test sorusu (PrePostTestForm)
- Buton: **"Pre-Test Tamamlandı"** → Task session başlatılır, pre-test skoru/cevaplar kaydedilir, `task_substep = 'task_work'`

---

### Alt adım 2: Görev çalışması (`task_work`)

- Başlık: "Görev Çalışma Alanı"; AI persona adı ve tipi yazılır
- Görev tanımı (bilgi kutusu)
- Expander: Persona'nın düşünce sistemi (rol, felsefe, güçlü yönler, kod stili, öncelikler, tam system prompt)
- Metin alanı: "AI'a vereceğiniz prompt"
- Buton: **"Kod Üret"** → OpenAI ile persona'ya göre kod üretilir; üretilen kod, süre, prompt detayları, (varsa) 6 aşamalı içerik analizi gösterilir
- Buton: **"Sonraki: Post-Test"** → `task_substep = 'post_test'`

---

### Alt adım 3: Post-test (`post_test`)

- Başlık: "Post-Test (5 soru)"
- Bilgi: Görev sonrası öğrenme kazanımını ölçme
- Görev bazlı 5 post-test sorusu; cevaplar ve skor kaydedilir
- Buton: **"Post-Test Tamamlandı"** → `task_substep = 'nasa_tlx'`

---

### Alt adım 4: NASA-TLX (`nasa_tlx`)

- Başlık: "Bilişsel Yük Değerlendirmesi (NASA-TLX)"
- Bilgi: Bu görevdeki zihinsel yükü değerlendirme
- NASA-TLX formu (NASATLXForm); yanıtlar kaydedilir
- Buton: **"Değerlendirme Tamamlandı"** → `task_substep = 'ai_evaluation'`

---

### Alt adım 5: AI değerlendirme (`ai_evaluation`)

- Başlık: "AI Kod Değerlendirmesi"
- AI değerlendirme formu (AIEvaluationForm)
- **Görev 1:** Sadece görev zorluğu değerlendirmesi (slider)
- **Görev 2–6:** "Bu görev için diğer AI daha uygun olur muydu?" (radio), neden (text_area), görev zorluğu (slider)
- Buton: **"Görev Değerlendirmesini Tamamla"** / **"AI Değerlendirmesi ve Karşılaştırmayı Tamamla"**

**Bu buton sonrası:**
- AI değerlendirme ve karşılaştırma verileri kaydedilir
- Task session tamamlanır (süre kaydedilir)
- `current_task_number` 1 artırılır, `task_substep = 'pre_test'`
- **Eğer** `current_task_number > 6` **ise:** `phase = 'final'` → **Faz 4** açılır
- **Değilse:** Bir sonraki görevin pre-test ekranı açılır (aynı sayfada)

---

## Faz 4 – Final (final)

**Ne zaman:** 6 görev tamamlandığında otomatik geçiş.

**Ekranda:**
1. Başlık: "Final Değerlendirme" / "4. Genel Değerlendirme ve Geri Bildirim"
2. Bilgi kutusu: "Tüm görevleri tamamladınız! Son olarak genel deneyiminizi değerlendirin."
3. **Final anketi (FinalSurveyForm):**
   - **AI Persona karşılaştırması:** Hangi AI'yı tercih ettiniz (Benzer / Tamamlayıcı / Duruma göre), neden (metin), öğrenme açısından hangisi daha faydalı, hızlı üretim için hangisi daha uygun (radio)
   - **Likert (1–5):** Benzer AI ile rahatlık, Tamamlayıcı AI ile gelişim, Benzer AI'nın açıklığı, Tamamlayıcı AI'nın kod kalitesi, iki AI'yı birlikte kullanmanın ideal olması (select_slider)
   - (Varsa) Ek sorular ve serbest metin
4. Buton: **"Araştırmayı Tamamla"**

**Buton sonrası:** Final cevapları ve toplam oturum süresi kaydedilir, katılımcı "tamamlandı" işaretlenir, `phase = 'complete'` → **Faz 5** açılır.

---

## Faz 5 – Tamamlandı (complete)

**Ne zaman:** "Araştırmayı Tamamla" tıklandıktan sonra.

**Ekranda:**
1. Başlık: "Tebrikler!"
2. Mesaj: "Araştırmayı başarıyla tamamladınız!"
3. Metin: Teşekkür, verilerin anonim ve araştırma amaçlı kullanımı, sonuçlar için e-posta bilgilendirmesi, hediye kartı çekilişi, katılım sertifikası
4. Katılımcı ID (UUID kısa hali)
5. İletişim: research@pidl.edu

**Buton yok;** kullanıcı sadece bilgi görür. Oturum aynı sayfada kalır.

---

## Akış özeti (tek sayfada)

```
[Sayfa açılır]           → phase = consent     → Onam + 5 onay + "Onay Verdim, Devam Et"

[Onay Verdim, Devam Et]  → phase = competency  → CAQ anketi → "Yetkinliğimi Değerlendir" → persona → "Görevlere Başla"

[Görevlere Başla]        → phase = tasks      → Görev 1..6 × (Pre-test → Kod üret → Post-test → NASA-TLX → AI değerlendirme)
                                                        → 6. görev bitince phase = final

[6 görev bitti]          → phase = final      → Final anketi → "Araştırmayı Tamamla"

[Araştırmayı Tamamla]    → phase = complete   → Teşekkür, katılımcı ID, iletişim (buton yok)
```

---

## Kısa özet: Tüm aşamalar

- **Faz 1 (Onam):** Metin + 5 onay + "Onay Verdim, Devam Et"
- **Faz 2 (Yetkinlik):** CAQ anketi (demografik + teknik + pedagojik + AI + öğrenme + kendini değerlendirme) → "Yetkinliğimi Değerlendir" → persona önerisi → "Görevlere Başla"
- **Faz 3 (Görevler):** 6 görev × (Pre-test → Kod üret → Post-test → NASA-TLX → AI değerlendirme); 6. bittikten sonra otomatik Final'e geçiş
- **Faz 4 (Final):** Final anketi (AI tercihi + Likert) → "Araştırmayı Tamamla"
- **Faz 5 (Tamamlandı):** Teşekkür, katılımcı ID, iletişim; ek işlem yok

Hepsi **aynı URL'de**, **sidebar** ile ilerleme takip edilerek sunulur.
