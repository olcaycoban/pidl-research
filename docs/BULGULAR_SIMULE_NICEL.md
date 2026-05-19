# PITL BULGULAR – SİMÜLE NİCEL VERİ

Bu dosya, 4. BULGULAR bölümünü yazmak için kullanılabilecek **tutarlı simüle istatistikler** içerir. Değerler rehberdeki yapı ve hipotezlerle uyumludur (H1, H2 desteklendi; H3 etkileşim; H4 adaptif > sabit).

---

## 4.1. Katılımcılar ve Betimsel Özellikler

- **Hedef N:** 150  
- **Analize alınan N:** 147 (3 katılımcı eksik veri nedeniyle çıkarıldı)  
- **Deney koşulu:** Adaptive n = 74, Fixed n = 73 (rastgele atama)

### Tablo 4.1. Dreyfus Seviyesi ve Domain’e Göre Katılımcı Sayıları

| Dreyfus Seviyesi     | Teknik (n) | Pedagojik (n) | Toplam |
|----------------------|------------|---------------|--------|
| Acemi                | 15         | 14            | 29     |
| İleri Başlangıç      | 14         | 15            | 29     |
| Yetkin               | 15         | 15            | 30     |
| Usta                 | 15         | 14            | 29     |
| Uzman                | 14         | 16            | 30     |
| **Toplam**           | **73**     | **74**        | **147**|

### Tablo 4.2. Demografik ve Yetkinlik Özeti

| Değişken              | M    | SS   | Min–Max / n (%) |
|-----------------------|------|------|------------------|
| Yaş                   | 28.4 | 6.2  | 19–52            |
| Cinsiyet (Kadın)      | –    | –    | 78 (53.1%)       |
| Eğitim (Lisans)       | –    | –    | 89 (60.5%)       |
| Teknik yetkinlik      | 52.3 | 18.2 | 12–94            |
| Pedagojik yetkinlik   | 48.7 | 16.1 | 10–88            |
| Önceki AI deneyimi (Evet) | – | –   | 91 (61.9%)       |
| Önceki blokzincir (Evet)  | – | –   | 44 (29.9%)       |

---

## 4.2. Varsayım Kontrolleri

- **Normallik (Shapiro-Wilk):** Kod kalitesi W = .98, p = .12; Öğrenme kazanımı W = .97, p = .08; NASA-TLX W = .95, p = .02 (hafif sağa çarpıklık).  
- **Levene:** Tüm bağımlı değişkenlerde p > .05 (varyans homojenliği kabul).  
- **Eksik veri:** %2; Little MCAR p = .18 (MCAR kabul). Liste bazında silme uygulandı.  
- **Aykırı değer:** 2 gözlem |z| > 3.29; analiz hem dahil hem hariç raporlandı, sonuçlar değişmedi.

---

## 4.3. Hipotez Testleri

### H1 – Öğrenme kazanımı (Tamamlayıcı > Benzer)

| Mod            | M    | SS   |
|----------------|------|------|
| Benzer         | 8.2  | 5.1  |
| Tamamlayıcı    | 11.4 | 5.8  |

- Eşleştirilmiş t: **t(146) = 4.82, p < .001, Cohen’s d = 0.58**  
- **H1 desteklendi.**

### H2 – Bilişsel yük / NASA-TLX (Benzer < Tamamlayıcı)

| Mod            | M    | SS   |
|----------------|------|------|
| Benzer         | 38.2 | 12.4 |
| Tamamlayıcı    | 45.6 | 13.1 |

- Eşleştirilmiş t: **t(146) = 4.21, p < .001, Cohen’s d = 0.58**  
- **H2 desteklendi.**

### Kod kalitesi ve görev süresi (betimsel + t-test)

| Bağımlı        | Benzer M (SS) | Tamamlayıcı M (SS) | t(146) | p     | d   |
|----------------|----------------|---------------------|--------|-------|-----|
| Kod kalitesi   | 62.1 (14.2)    | 58.3 (15.0)         | 2.14   | .034  | 0.26 |
| Görev süresi (dk) | 14.2 (4.1)  | 16.8 (4.5)          | -4.02  | < .001| 0.61 |

---

### H3 – Mod × Dreyfus etkileşimi (Karma ANOVA)

**Öğrenme kazanımı (bağımlı değişken):**

- Ana etki Mod: **F(1, 142) = 22.31, p < .001, η² = .14**  
- Ana etki Dreyfus: **F(4, 142) = 8.44, p < .001, η² = .19**  
- **Mod × Dreyfus: F(4, 142) = 3.18, p = .016, η² = .08**  

Etkileşim anlamlı; basit etki: Tamamlayıcı modun avantajı acemi ve ileri başlangıç seviyelerinde daha belirgin.  
- **H3 desteklendi.**

---

### H4 – Adaptif vs sabit mod (genel performans)

**Koşullar:** Adaptive (n = 74), Fixed (n = 73).

| Bağımlı (ortalama/görev) | Adaptive M (SS) | Fixed M (SS) | t(145) | p     | Cohen’s d |
|--------------------------|-----------------|--------------|--------|-------|-----------|
| Öğrenme kazanımı         | 10.1 (4.2)      | 9.2 (4.5)    | 1.98   | .049  | 0.33      |
| Kod kalitesi             | 61.2 (12.8)     | 58.9 (13.4)  | 2.10   | .038  | 0.35      |
| NASA-TLX (ortalama)      | 41.2 (10.1)     | 42.8 (11.2)  | -1.12  | .265  | 0.15 (ns) |
| Görev tamamlama süresi (dk) | 15.2 (3.8)  | 15.8 (4.2)   | -1.02  | .310  | 0.15 (ns) |

- Adaptif grupta öğrenme kazanımı ve kod kalitesi sabit gruba göre daha yüksek (küçük–orta etki).  
- **H4 kısmen desteklendi** (performans göstergelerinde adaptif lehine fark; bilişsel yük ve süre farkı anlamlı değil).

---

## 4.4. Regresyon Bulguları

### Model 1 – Kod kalitesi

- **R² = .28, F(4, 142) = 13.82, p < .001**  
- Mod (β = -.18, p = .012), Dreyfus (β = .22, p = .003), Domain (β = .14, p = .042); Mod×Seviye (β = -.08, p = .312, ns).  
- VIF < 2.0.

### Model 2 – Öğrenme kazanımı

- **R² = .35, F(4, 142) = 19.11, p < .001**  
- Mod (β = .24, p < .001), NASA_TLX (β = -.12, p = .028), Ön_test (β = .38, p < .001).  
- VIF < 2.0.

### Model 3 – NASA-TLX

- **R² = .22, F(4, 142) = 10.02, p < .001**  
- Mod (β = .19, p = .008), Görev_karmaşıklığı (β = .31, p < .001), Süre (β = .18, p = .019).  
- VIF < 2.0.

---

## Kullanım notu

- Bu değerler **simüle**dir; gerçek analiz çıktılarıyla değiştirilmelidir.  
- Bulgular metninde geçmiş zaman ve rehberdeki tablo/paragraf yapısı kullanılabilir.  
- H4 için artık sistemde **sabit mod** koşulu da vardır; gerçek veri toplandığında `condition` (adaptive/fixed) ile bu karşılaştırma yapılabilir.
