# PITL DOKTORA TEZİ - BULGULAR BÖLÜMÜ YAZIM REHBERİ

Bu belge, **1. Giriş** ve **3. Yöntem** bölümlerine dayanarak tezin **4. BULGULAR** bölümünün yazılması için hazırlanmıştır. Claude veya başka bir AI’a verilerek bulgular metninin üretilmesinde kullanılabilir.

---

## GÖREV TANIMI

Araştırmanın toplanan verilerine (veya simüle/örnek verilere) dayanarak **4. BULGULAR** bölümünü yaz. Bulgular bölümünde **yorum yapma**, **neden-sonuç çıkarımı** veya **literatürle tartışma** yok; sadece **ne bulundu** nesnel ve sistematik biçimde raporlanır. Yorum ve tartışma **5. Tartışma** bölümüne bırakılır.

**Dil:** Akademik Türkçe  
**Atıf:** APA 7  
**Ton:** Geçmiş zaman, pasif/aktif dengeli (“veriler analiz edildi”, “fark anlamlı bulundu”)

---

## BÖLÜM YAPISI (Giriş ve Yöntem ile Uyumlu)

```
4. BULGULAR
   4.1. Katılımcılar ve Betimsel Özellikler
   4.2. Varsayım Kontrolleri
   4.3. Araştırma Soruları ve Hipotezlere İlişkin Nicel Bulgular
        4.3.1. Mod Etkisi (Benzer vs Tamamlayıcı)
        4.3.2. Dreyfus Seviyesi ve Domain Etkileri
        4.3.3. Mod × Seviye Etkileşimi
        4.3.4. Adaptif Mod Mekanizması (H4)
   4.4. Regresyon Bulguları
   4.5. Nitel Bulgular
        4.5.1. Persona Deneyimi
        4.5.2. Mod Algısı
        4.5.3. Öğrenme Süreci
        4.5.4. Sistem Değerlendirmesi
   4.6. Karma Yöntem Entegrasyonu (Joint Displays ve Meta-Çıkarımlar)
```

---

## 4.1. KATILIMCILAR VE BETİMSEL ÖZELLİKLER

### Amaç
Çalışma grubunun yapısını, kayıp veriyi ve temel betimsel istatistikleri raporla.

### Raporda Yer Alması Gerekenler

| İçerik | Açıklama | Örnek ifade |
|--------|----------|-------------|
| Hedef ve gerçek N | Kaç kişi davet edildi, kaçı analize alındı | "Hedef örneklem 150 katılımcı idi. Veri toplama sonunda 147 katılımcı tüm görevleri tamamladı. Üç katılımcı verisi eksik veri oranı nedeniyle analiz dışı bırakıldı." |
| Tabakalı yapı | 5 Dreyfus × 2 domain, hücre başına n | Tablo 4.1: Dreyfus seviyesi ve domain’e göre katılımcı sayıları |
| Demografik özet | Yaş (M, SS), cinsiyet (n, %), eğitim (n, %) | Tablo 4.2: Demografik özellikler |
| Yetkinlik dağılımı | Teknik/pedagojik puan (M, SS), Dreyfus dağılımı | "Teknik yetkinlik puanı ortalaması 52.3 (SS=18.2), pedagojik yetkinlik puanı ortalaması 48.7 (SS=16.1) olarak hesaplandı." |
| Kontrol değişkenleri | Önceki AI/blokzincir deneyimi (n, % veya M, SS) | Kısa paragraf veya tablo |
| Attrition | Tamamlayan vs bırakan karşılaştırması (varsa) | "Tamamlayanlar ile bırakanlar arasında yaş, cinsiyet ve ön-test puanları açısından anlamlı fark bulunmadı (p>.05)." |

### Tablo 4.1 Önerilen Format

| Dreyfus Seviyesi | Teknik (n) | Pedagojik (n) | Toplam |
|------------------|------------|---------------|--------|
| Acemi | 15 | 14 | 29 |
| İleri Başlangıç | 14 | 15 | 29 |
| Yetkin | 15 | 15 | 30 |
| Usta | 15 | 14 | 29 |
| Uzman | 14 | 16 | 30 |
| **Toplam** | **73** | **74** | **147** |

---

## 4.2. VARSAYIM KONTROLLERİ

Yöntem bölümünde (3.6.1) belirtilen kontrollerin **sonuçları** kısa ve net raporlanmalı.

| Varsayım | Test | Raporda yazılacak |
|----------|------|-------------------|
| Normallik | Shapiro-Wilk / Kolmogorov-Smirnov | p değeri; normallik ihlali varsa “parametrik olmayan testler kullanıldı” |
| Varyans homojenliği | Levene | p değeri; ihlal varsa Welch ANOVA / Brown-Forsythe |
| Kovaryans matrisleri | Box's M | Karma ANOVA için p |
| Küresellik | Mauchly | İhlal varsa Greenhouse-Geisser ε ve düzeltilmiş p |
| Eksik veri | Little MCAR | Eksik oranı (%), desen (MCAR/MAR/MNAR), uygulanan yöntem (silme/çoklu atama) |
| Aykırı değer | z-skor, Mahalanobis | Kaç gözlem aykırı bulundu, nasıl ele alındı |

**Örnek paragraf:**  
"Bağımlı değişkenlere ilişkin normallik varsayımı Shapiro-Wilk testi ile kontrol edildi. Kod kalitesi (W=.98, p=.12) ve öğrenme kazanımı (W=.97, p=.08) için normallik varsayımı karşılandı; NASA-TLX skorları hafif sağa çarpıktı (W=.95, p=.02). Bu nedenle bilişsel yük analizlerinde parametrik ve parametrik olmayan sonuçlar birlikte raporlandı. Levene testi varyans homojenliğini destekledi (p>.05)."

---

## 4.3. ARAŞTIRMA SORULARI VE HİPOTEZLERE İLİŞKİN NİCEL BULGULAR

Yöntemdeki **dört araştırma sorusu** ve **dört hipotez** ile bire bir eşleşecek şekilde bulguları sun.

### Araştırma Sorusu 1 ve H1, H2

**Soru 1:** PITL’in Benzer ve Tamamlayıcı modları kod kalitesi, öğrenme kazanımı, bilişsel yük ve görev tamamlama süresi üzerinde anlamlı farklı etkiler yaratmakta mıdır?

- **H1:** Tamamlayıcı Mod, Benzer Mod’a göre anlamlı düzeyde daha yüksek öğrenme kazanımı sağlamaktadır.
- **H2:** Benzer Mod, Tamamlayıcı Mod’a göre anlamlı düzeyde daha düşük bilişsel yük üretmektedir.

**Raporlama:**

| Bağımlı değişken | Test | Raporda |
|------------------|------|--------|
| Öğrenme kazanımı (görev bazlı, mod bazlı ortalama) | Eşleştirilmiş t-test (Similar vs Complementary, katılımcı içi) | t(df)=X.XX, p=.XXX, Cohen’s d=X.XX; M_Similar, M_Complementary, SS |
| Bilişsel yük (NASA-TLX) | Eşleştirilmiş t-test | t(df)=X.XX, p=.XXX, Cohen’s d=X.XX; M, SS her mod için |
| Kod kalitesi | Eşleştirilmiş t-test | Aynı format |
| Görev tamamlama süresi | Eşleştirilmiş t-test | Aynı format |

**Tablo 4.3 önerisi:** Benzer ve Tamamlayıcı modlara göre bağımlı değişkenlerin ortalamaları, standart sapmaları, t, p ve Cohen’s d.

**Örnek cümle:**  
"Tamamlayıcı Mod’da öğrenme kazanımı ortalaması (M=X.XX, SS=X.XX), Benzer Mod’a (M=X.XX, SS=X.XX) göre daha yüksekti. Eşleştirilmiş örneklem t-testi farkın istatistiksel olarak anlamlı olduğunu gösterdi (t(146)=X.XX, p=.XXX, Cohen’s d=X.XX). H1 desteklendi."  
(H1 desteklenmezse: "Fark anlamlı değildi (p=.XXX). H1 desteklenmedi.")

---

### Araştırma Sorusu 2 ve H3

**Soru 2:** Dreyfus yetkinlik seviyesi ile öneri modu arasında anlamlı etkileşim var mıdır?

- **H3:** Mod etkisi ile Dreyfus yetkinlik seviyesi arasında anlamlı etkileşim bulunmaktadır.

**Test:** İki yönlü karma ANOVA (Mod: within, Dreyfus seviyesi: between). Bağımlı değişkenler: kod kalitesi, öğrenme kazanımı, NASA-TLX, görev süresi.

**Raporlama:**

- Ana etki Mod: F, df, p, η²
- Ana etki Dreyfus: F, df, p, η²
- **Mod × Dreyfus etkileşimi:** F, df, p, η²
- Etkileşim anlamlıysa: Basit etki analizi (her Dreyfus seviyesinde Mod farkı) veya profil grafiği atıfı

**Tablo 4.4:** Karma ANOVA sonuçları (Mod, Dreyfus, Mod×Dreyfus; hata terimi; η²).

**Örnek:**  
"Mod × Dreyfus seviyesi etkileşimi öğrenme kazanımı için anlamlıydı (F(4, 142)=X.XX, p=.XXX, η²=.XX). Basit etki analizine göre Tamamlayıcı Mod’un avantajı özellikle acemi ve ileri başlangıç seviyelerinde belirgindi. H3 desteklendi."

---

### Araştırma Sorusu 4 ve H4

**Soru 4:** NASA-TLX tabanlı adaptif mod geçiş mekanizması, kullanıcıları optimal bilişsel yük bölgesinde tutmada etkili midir?

- **H4:** Adaptif mod geçiş mekanizması, sabit mod atamasına kıyasla kullanıcıların genel performansını anlamlı düzeyde artırmaktadır.

**Not:** PITL platformunda artık **sabit mod (fixed)** koşulu da vardır. Katılımcılar yetkinlik değerlendirmesini tamamladıktan sonra rastgele **Adaptive** veya **Fixed** koşuluna atanır. Fixed koşulunda görev 1,3,5 → Similar; 2,4,6 → Complementary sabit sıra uygulanır. Böylece H4, Adaptif vs Sabit gruplar karşılaştırılarak test edilebilir.

**Raporlama:** Adaptif (n) vs Sabit (n) için genel performans göstergeleri (ortalama kod kalitesi, öğrenme kazanımı, NASA-TLX, görev süresi) bağımlı değişken; koşul (condition) bağımsız değişken. Bağımsız örneklem t-testi veya ANOVA; etki büyüklüğü (Cohen’s d) raporlanır.

---

## 4.4. REGRESYON BULGULARı

Yöntemdeki üç model (3.6.1) raporlanmalı.

| Model | Bağımlı | Bağımsız | Çıktı |
|-------|---------|----------|--------|
| Model 1 | Kod kalitesi | Mod, Seviye, Domain, Mod×Seviye | R², F, β’lar, p, VIF (çoklu bağlantı) |
| Model 2 | Öğrenme kazanımı | Mod, Seviye, NASA_TLX, Ön_test | Aynı |
| Model 3 | NASA_TLX | Mod, Seviye, Görev_karmaşıklığı, Süre | Aynı |

**Tablo 4.5–4.7:** Her model için regresyon özet tablosu (β, Standart hata β, t, p, VIF; model R², F, p).

**Örnek:**  
"Kod kalitesi regresyon modeli anlamlıydı (F(4, 142)=X.XX, p<.001, R²=.XX). Mod (β=X.XX, p=.XXX), Dreyfus seviyesi (β=X.XX, p=.XXX) ve domain (β=X.XX, p=.XXX) anlamlı yordayıcılardı. Mod×Seviye etkileşim terimi anlamlı değildi (p=.XXX)."

---

## 4.5. NİTEL BULGULAR

Araştırma sorusu 3: Katılımcılar yapay zekâ personasıyla etkileşim deneyimlerini, mod tercihlerini ve algıladıkları öğrenme süreçlerini nasıl tanımlamaktadır?

Yöntemdeki **dört tema** (3.1.2) ile yapılandır.

### 4.5.1. Persona Deneyimi
- Eşleştirilen persona ile etkileşim süreci
- Personanın uzmanlık düzeyi algısı
- İletişim stiline ilişkin izlenimler  
*Tematik kodlardan örnek alıntılar (anonim), tema adları.*

### 4.5.2. Mod Algısı
- Benzer ve Tamamlayıcı modlar arasındaki farkların deneyimi
- Hangi modda daha rahat hissedildiği
- Hangi modda daha fazla öğrenildiği düşüncesi  
*Kod ve alıntılar.*

### 4.5.3. Öğrenme Süreci
- Blokzincir ve akıllı sözleşme konusunda bilgi değişimi
- Personanın öğrenme sürecine katkısı
- Zorlayıcı bulunan noktalar  
*Kod ve alıntılar.*

### 4.5.4. Sistem Değerlendirmesi
- PITL kullanılabilirliği
- Adaptif mod geçişine ilişkin farkındalık ve deneyim
- İyileştirme önerileri  
*Kod ve alıntılar.*

**Raporlama kuralları:**  
- Her tema için kısa tanım + 2–4 alıntı (katılımcı kodu: P1, P2…).  
- Kodlayıcılar arası uyum (Cohen’s κ) bir cümleyle belirtilir.  
- Final anket açık uçlu sorular: içerik analizi özeti, frekans/kategori tablosu veya kelime bulutu atıfı.

---

## 4.6. KARMA YÖNTEM ENTEGRASYONU

Açımlayıcı sıralı desen ve “connecting” stratejisi (3.6.3) gereği:

- **Joint display:** Nicel sonuçlar (örn. “Tamamlayıcı modda öğrenme kazanımı daha yüksek”) ile nitel temalar (örn. “Katılımcılar Tamamlayıcı modda daha çok öğrendiklerini belirtti”) aynı tabloda veya metinde yan yana sunulur.
- **Meta-çıkarım:** Nicel ve nitel bulguların birlikte ne gösterdiği 1–2 paragrafta özetlenir; ancak **yorum/tartışma** (neden böyle, literatürle ilişki) Tartışma bölümüne bırakılır.

**Örnek tablo (Joint display):**

| Nicel bulgu | Nitel tema | Bütünleştirici not |
|-------------|------------|---------------------|
| Tamamlayıcı modda öğrenme kazanımı daha yüksek (H1 desteklendi) | “Tamamlayıcı modda daha çok zorlandım ama daha çok öğrendiğimi hissettim” (P12, P23) | Öznel öğrenme algısı ile nesnel kazanım uyumlu |
| Benzer modda NASA-TLX daha düşük (H2 desteklendi) | “Benzer modda işler daha akıcı gitti” (P7, P19) | Düşük bilişsel yük, akıcılık algısı ile örtüşüyor |

---

## HİPOTEZ VE ARAŞTIRMA SORULARI ÖZET TABLOSU

Bulgular bölümü sonunda veya 4.3’ün girişinde kullanılabilecek özet:

| Hipotez / Soru | Test / Analiz | Sonuç (örnek) |
|----------------|---------------|----------------|
| H1: Tamamlayıcı > Benzer (öğrenme kazanımı) | Eşleştirilmiş t | Desteklendi / Desteklenmedi |
| H2: Benzer < Tamamlayıcı (bilişsel yük) | Eşleştirilmiş t | Desteklendi / Desteklenmedi |
| H3: Mod × Dreyfus etkileşimi | Karma ANOVA | Desteklendi / Desteklenmedi |
| H4: Adaptif > Sabit (genel performans) | Grup karşılaştırması veya betimsel | Desteklendi / Sınırlı / Test edilemedi |
| RS3: Deneyim ve mod tercihleri nasıl tanımlanıyor? | Tematik analiz | Tema listesi ve özet |

---

## DİL VE FORMAT KURALLARI

1. **Geçmiş zaman:** “Analiz edildi”, “fark bulundu”, “desteklendi”.
2. **p değeri:** p <.001 veya p = .032; tam p değeri anlamlılık için verilir.
3. **İstatistik semboller:** t, F, df, p, M, SS, η², R², β, Cohen’s d italik (veya kurumun tez kılavuzuna uygun).
4. **Ondalık:** Tutarlı (örn. p ve korelasyonlar 3 hane; M, SS 2 hane).
5. **Tablo/şekil:** Metin içinde “Tablo 4.X’te görüldüğü gibi” şeklinde atıf; tablo başlığı üstte, notlar altta.
6. **Yorum yok:** “Bu sonuç CLT ile uyumludur” gibi ifadeler Tartışma’ya taşınmalı.

---

## OLASI TABLO VE ŞEKİL LİSTESİ

| Numara | İçerik |
|--------|--------|
| Tablo 4.1 | Dreyfus ve domain’e göre katılımcı sayıları |
| Tablo 4.2 | Demografik ve yetkinlik betimsel istatistikleri |
| Tablo 4.3 | Benzer vs Tamamlayıcı mod: Bağımlı değişkenler (M, SS, t, p, d) |
| Tablo 4.4 | Karma ANOVA sonuçları (Mod, Dreyfus, Mod×Dreyfus) |
| Tablo 4.5–4.7 | Regresyon modelleri 1–3 |
| Tablo 4.8 | Joint display (nicel–nitel entegrasyonu) |
| Şekil 4.1 | Mod × Dreyfus etkileşim grafiği (profil) |
| Şekil 4.2 | Nitel temaların şematik gösterimi (isteğe bağlı) |

---

## KISA KONTROL LİSTESİ

- [ ] Katılımcı sayısı, attrition ve tabakalı yapı raporlandı mı?
- [ ] Varsayım kontrolleri (normallik, homojenlik, eksik veri) kısaca yazıldı mı?
- [ ] H1, H2 için eşleştirilmiş t ve etki büyüklüğü verildi mi?
- [ ] H3 için karma ANOVA ve gerekirse basit etki raporlandı mı?
- [ ] H4 için mevcut tasarıma uygun analiz/betimleme yapıldı mı?
- [ ] Üç regresyon modeli (R², β, p, VIF) raporlandı mı?
- [ ] Nitel kısım dört tema ile yapılandı mı? Alıntılar anonim mi?
- [ ] Joint display ve meta-çıkarım (yorum olmadan) eklendi mi?
- [ ] Tablo ve şekiller metin içinde atıf aldı mı?
- [ ] Bulgular bölümünde yorum/tartışma yok mu?

---

*Bu rehber, 1. Giriş ve 3. Yöntem metinleri esas alınarak hazırlanmıştır. Gerçek veriyle yazarken istatistik değerleri analiz çıktılarıyla değiştirin.*
