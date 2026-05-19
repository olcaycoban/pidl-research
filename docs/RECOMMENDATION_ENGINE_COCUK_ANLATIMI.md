# Tavsiye Motoru – 9 Yaşındaki Birine Anlatır Gibi 🧒

Bu yazıda, bilgisayarın “hangi AI arkadaşını seninle eşleştireceğine” nasıl karar verdiğini **oyun ve günlük hayattan örneklerle** anlatıyorum.

---

## 1. Ne Yapıyor Bu Sistem? (Genel Fikir)

**Analoji: Okulda oyun arkadaşı seçmek**

Düşün ki okulda **6 farklı oyun arkadaşı** var. Biri legoda süper, biri resimde, biri futbolda… Sen de bazı şeylerde iyisin, bazılarında öğrenmek istiyorsun.  
Bilgisayar şunu yapıyor: **Seni tanıyor** (neyi sevdiğin, neyi bilmediğin), sonra **“Bu çocukla oynarsan hem eğlenirsin hem öğrenirsin”** veya **“Bu çocuk tam sana göre, ikiniz de aynı şeyleri seviyorsunuz”** diye iki tür arkadaş öneriyor.  
Yani: **Sen = kullanıcı**, **arkadaşlar = AI persona’lar**, **tavsiye = hangi persona ile eşleştirileceğin**.

---

## 2. Seni Nasıl “Sayılara” Çeviriyor? (User Vector)

**Analoji: Karakter kartın (oyun karakteri gibi)**

Oyunlarda karakterin güç, hız, zeka gibi **çubuklarla** anlatılır. Burada da sen **10 tane çubukla** anlatılıyorsun:

- **Teknik beceri:** Bilgisayar/kod tarafında ne kadar iyisin (0 = hiç bilmiyorum, 1 = çok iyiyim).
- **Alan bilgisi:** Konuyu (blokzincir, eğitim vb.) ne kadar biliyorsun.
- **AI deneyimi:** Daha önce ChatGPT gibi şeyler kullandın mı?
- **Hedef:** “Öğrenmek istiyorum” mu, “Hızlıca işimi bitirmek istiyorum” mu?
- **Nasıl bilgisi:** Bir şeyi “nasıl yapılır” diye anlayabiliyor musun?
- **Ne bilgisi:** “Bu ne?” diye kavramları biliyor musun?
- **Ne zaman bilgisi:** “Bu ne zaman kullanılır?” diye biliyor musun?
- **Kafanın kapasitesi:** Çok karmaşık bir şeyi taşıyabiliyor musun (yorulmadan)?
- **Örüntü görme:** Benzer şeyleri fark edebiliyor musun (pattern)?
- **Soyutlama:** Basit örneklerle mi rahatsın, yoksa formüller/kurallarla mı?

**Kısaca:** Sen bir **10 kutucuklu form** gibi düşünülüyorsun; her kutucuk 0 ile 1 arası. Bilgisayar “Bu çocuk böyle” diyor.

---

## 3. AI Arkadaşları Nasıl Tanımlanıyor? (Persona Vector)

**Analoji: Her arkadaşın bir “profil kartı”**

Her AI’ın da bir kartı var: **Ne tür oyunlar oynar, ne kadar zor konuşur, ne kadar örnek verir** gibi.

- **Kod karmaşıklığı:** Verdiği cevap basit mi (küçük çocuk gibi), karmaşık mı (büyük gibi)?
- **Açıklayıcılık:** Çok mu konuşuyor, az mı?
- **Teknik derinlik:** Konuyu ne kadar derin biliyor?
- **Pedagojik odak:** “Öğretmek” mi istiyor, “hızlı iş çıkarmak” mı?
- **Yorum yoğunluğu:** Her adımı açıklıyor mu?
- **Modülerlik:** Anlatırken parça parça mı anlatıyor (modüler), tek blok mu?
- **Örnek zenginliği:** Bol örnek veriyor mu?
- **Öğrenme desteği:** Yeni öğrenen biri için uygun mu?
- **Production hazırlığı:** “Gerçek işe” yarar şey mi üretiyor?
- **Yenilikçilik:** Hep aynı tarz mı, yoksa farklı fikirler mi sunuyor?

**Kısaca:** Her AI = **farklı bir “arkadaş tipi”**; biri sakin ve öğretici, biri hızlı ve teknik vb.

---

## 4. “Benzerlik” Ne Demek? (Cosine + Euclidean)

**Analoji: İki çocuğun “ne kadar aynı” olduğuna bakmak**

İki şeyi karşılaştırıyoruz: **senin 10 kutucuğun** ile **AI’ın 10 kutucuğu**.

- **Yön (cosine):** İkiniz de **aynı şeylerde mi** yüksek/düşük?  
  Örnek: İkiniz de “çok konuşkan, az soyut” iseniz **yön benzer**.  
  = **Aynı tipte misiniz?** (ikisi de teknik, ikisi de öğrenmeye açık vb.)

- **Uzaklık (Euclidean):** Sayılar **birbirine ne kadar yakın?**  
  Sen 0.8, o 0.7 ise yakın; sen 0.9, o 0.2 ise uzak.  
  = **Seviye olarak ne kadar yakınsınız?**

Bilgisayar ikisini birleştiriyor: **%60 yön + %40 uzaklık** → tek bir “benzerlik puanı”.  
Yüksek puan = “Bu AI sana çok benziyor” (similar). Düşük = “Farklı tip” (complementary için iyi olabilir).

**Neden tam %60 ve %40?** Projede bu sayılar deneyle ölçülmüş değil; **tasarım tercihi**. Mantık: “Ne tip” bir AI (yön) seninle eşleşmede en önemli bilgi; o yüzden biraz daha ağır (%60). “Ne seviyede?” (uzaklık) da önemli ama yardımcı (%40). İstersen bu oranlar değiştirilip deneylerle ayarlanabilir.

---

## 5. “Yetkinlik Uyumu” Ne? (Competency Match – ZPD)

**Analoji: Puzzle zorluğu – ne çok kolay ne çok zor**

Vygotsky’nin **Yakınsal Gelişim Alanı** = “Biraz zor ama yapabileceğin şey”.

- **Çok kolay:** Sıkılırsın, öğrenmezsin.
- **Çok zor:** “Yapamıyorum” deyip bırakırsın.
- **Tam yerinde:** “Biraz zorladım ama yaptım!” → en iyi öğrenme.

Bilgisayar: **Senin seviyen** ile **AI’ın zorluk seviyesi** arasındaki mesafeye bakıyor.  
Mesafe **çok büyük değilse** (ne çok kolay ne imkansız) → **yüksek uyum**.  
Ayrıca: Sen “öğrenmek istiyorum” diyorsan **öğretici** AI’a, “iş bitirmek” diyorsan **hızlı/üretken** AI’a daha çok puan veriyor.

**Kısaca:** “Bu AI sana ne çok kolay ne çok zor; tam öğrenebileceğin yerde.”

---

## 6. “Performans Tahmini” Ne? (Performance Prediction)

**Analoji: Maç öncesi “Kazanır mıyız?” tahmini**

Takımın gücü + rakip + saha… Bir formül ile **“Bu maçı kazanma ihtimalimiz %70”** gibi bir şey söylenir.  
Burada da: **Senin becerin + AI’ın kalitesi + ikinizin uyumu + görevin zorluğu** → **“Bu AI ile bu görevde başarılı olma ihtimalin”** tahmin ediliyor.  
Yüksek tahmin = “Bu ikili iyi gider” deniyor.

**Kısaca:** “Sen bu AI ile çalışırsan işin iyi bitebilir” puanı.

---

## 7. “Öğrenme Yörüngesi” Ne? (Learning Trajectory)

**Analoji: Zamanla ne kadar gelişirsin?**

“Bu arkadaşla 1 ay oynarsan biraz, 1 yıl oynarsan çok gelişirsin” gibi.  
Bilgisayar: **Zaman faktörü** (ne kadar süre) × **AI’ın öğretme gücü** × **senin öğrenmeye açıklığın** → **“Bu eşleşmeden ne kadar öğrenme çıkabilir?”** puanı.  
Yüksek = “Bu AI ile uzun vadede çok şey öğrenirsin.”

**Kısaca:** “Bu arkadaşla oynarsan zamanla ne kadar gelişirsin?” puanı.

---

## 8. “Tamamlayıcılık” Ne? (Complementarity)

**Analoji: Sen topu iyi atamıyorsun, o iyi yakalıyor – tam takım**

**Benzer** = “İkiniz de aynı şeyde iyisiniz.”  
**Tamamlayıcı** = “Senin eksik olduğun yerde o güçlü.”  
Bilgisayar: Senin **zayıf** olduğun (düşük puanlı) kutucuklara bakıyor; AI’ın o kutucuklarda **güçlü** (yüksek puanlı) olup olmadığına.  
Çok “sen zayıf, o güçlü” eşleşmesi varsa → **yüksek tamamlayıcılık** = “Bu AI senin eksiklerini kapatır.”

**Kısaca:** “Senin yapamadığın şeyleri o yapıyor; birlikte güçlü olursunuz.”

---

## 9. Neden α, β, γ, δ? (Ağırlıklar)

**Analoji: Puanlama kuralları – hangi kural daha önemli?**

Toplam puan = **benzerlik** + **uyum** + **performans tahmini** + **öğrenme**.  
Ama hepsi eşit değil; bazıları daha önemli:

- **β (yetkinlik uyumu) en büyük (0.35):** “Zorluk tam yerinde mi?” en önemli kural.
- **α (benzerlik/farklılık) 0.30:** “Bu AI sana benziyor mu / tamamlayıcı mı?” ikinci.
- **γ (performans) 0.25:** “İş iyi biter mi?” üçüncü.
- **δ (öğrenme) 0.10:** “Uzun vadede ne öğrenirsin?” destekleyici.

Yani: Önce “**Zorluk sana uygun mu?**”, sonra “**Tipi doğru mu?**”, sonra “**Başarı çıkar mı?**”, en sonda “**Ne kadar öğrenirsin?**” diye bakılıyor.

---

## 10. Bilişsel Yük (CLT) – Kafan Yorulur mu?

**Analoji: Çantana ne kadar kitap koyabilirsin?**

- **İçsel yük:** Görevin kendisi ne kadar ağır (zor konu = ağır çanta).
- **Dışsal yük:** Sunum kötüyse (karmaşık anlatım, dağınık sayfa) ekstra yük = **gereksiz çanta**.
- **Faydalı yük:** Öğrenmeye harcadığın enerji = **gerçekten öğrendiğin kitaplar**.

Bilgisayar: **Toplam yük = İçsel + Dışsal − Faydalı**.  
Eğer bu, **senin taşıyabileceğin kapasiteden** fazlaysa = “Bu AI seni yorar, kafan karışır.”  
Az dışsal, çok faydalı, kapasiteni aşmayan = “**Optimal öğrenme bölgesi**” = en iyi eşleşme.

**Kısaca:** “Bu AI ne çok yorar ne çok basit; tam kafanı iyi kullanacak yerde.”

---

## 11. “Similar” ve “Complementary” Seçimi

**Analoji: İki tür arkadaş**

- **Similar (benzer):** Seninle **aynı tipte** – aynı şeylerde iyi, aynı tarz.  
  = “Senin gibi biriyle oynamak – rahat, tanıdık.”

- **Complementary (tamamlayıcı):** Senin **eksik olduğun** yerde güçlü.  
  = “Sen top atamıyorsun, o yakalıyor – birlikte takım oluyorsunuz.”

Bilgisayar: **Güçlü olduğun alandan** “en benzer” AI’ı → **Similar**.  
**Zayıf olduğun alandan** “eksiklerini en iyi kapatan” AI’ı → **Complementary**.  
Araştırmada: 3 görev Similar, 3 görev Complementary ile çalışıyorsun; ikisini de deneyimliyorsun.

**Kısaca:** Biri “sana benzeyen”, biri “seni tamamlayan” iki AI arkadaş seçiliyor.

---

## 12. “Adaptive” Ne Demek? (Kendini Ayarlayan Mod) 🎚️

**Analoji: Otomatın sana sorması – “Öğrenmek mi, hızlı bitirmek mi?”**

Tezdeki **adaptive** şu demek: Bilgisayar **senin hedefini** (öğrenmek mi, işi hızlı bitirmek mi) okuyor ve **buna göre** puanı hesaplıyor. Yani tek bir “sabit kural” yok; **senin durumuna göre kural değişiyor**.

- **“Çok öğrenmek istiyorum”** dersen (hedef öğrenme tarafında) → **Tamamlayıcı** kurala daha çok ağırlık veriyor (seni geliştirecek arkadaş).
- **“Hızlıca işimi bitirmek istiyorum”** dersen (hedef üretim tarafında) → **Benzer** kurala daha çok ağırlık veriyor (sana benzeyen, rahat çalışacağın arkadaş).
- **“İkisi arası”** dersen → İkisini **karıştırıyor**: biraz benzer, biraz tamamlayıcı (hybrid).

**Başka analoji: Öğretmenin seni tanıması**

Öğretmen “Bu çocuk şu an ne istiyor?” diye düşünüyor:  
Öğrenmeye açıksan → “Zorlayıcı ama öğretici” arkadaş (complementary).  
“Sadece ödevimi bitireyim” diyorsan → “Sana benzeyen, rahat” arkadaş (similar).  
Arada bir yerdeysen → İkisinin ortası (hybrid).  
İşte **adaptive** = bilgisayarın bu “senin hedefe göre kuralı seçmesi”.

**Kodda nerede?**

Motorun içinde (recommendation_engine) **varsayılan** ayar bu: “Modu söylemezsen **adaptive** kabul ediyorum.” Yani “senin hedefe göre karar ver” modu açık.  
Araştırma uygulamasında ise **her zaman** iki ayrı arkadaş seçiliyor: biri **similar**, biri **complementary**; ikisini de denemen için sabit. O yüzden adaptive orada “görünmüyor”; ama motorun içinde tanımlı ve başka yerlerde (örneğin tek bir liste sıralarken) kullanılıyor.

**Kısaca:** Adaptive = “Senin hedefin ne? Öğrenmek mi, hızlı bitirmek mi?” diye bakıp **ona göre** benzer mi tamamlayıcı mı (veya ikisinin karışımı mı) puanlaması.

---

## 13. Bilişsel Yük Puanı Etkiliyor mu? (CLT Çarpanı) 🧮

**Analoji: Karne notuna "davranış bonusu/cezası" eklenmesi**

Düşün ki sınav notun var (örnek: 80). Ama öğretmen diyor ki:
- "Derse çok güzel katıldın" → **+10 bonus** → 88 oluyor.
- "Sınıfı rahatsız ettin" → **-10 ceza** → 72'ye düşüyor.

İşte bilgisayar da aynısını yapıyor! Önce **temel puanı** (benzerlik + uyum + performans + öğrenme) hesaplıyor. Sonra **bilişsel yük analizine** bakıp bu puanı **çarpıyor veya düşürüyor**.

### Nasıl Çalışıyor?

| Durum | Ne Oluyor? | Bonus/Ceza |
|-------|-----------|------------|
| **Optimal Zone** (tam yerinde) | "Bu AI seni ne yoruyor ne sıkıyor – mükemmel!" | **+%10 bonus** |
| **Overload** (çok yorucu) | "Bu AI kafanı çok yorar, ezilirsin" | **-%30'a kadar ceza** |
| **High Extraneous** (kötü anlatım) | "Bu AI dağınık anlatıyor, kafa karışır" | **-%10 ceza** |
| **High Germane** (çok öğretici) | "Bu AI çok güzel öğretiyor!" | **+%5 bonus** |

### Örnek

```
Temel puan: 0.70 (benzerlik + uyum + performans + öğrenme)
CLT Çarpanı: ×1.10 (Optimal Zone bonusu)
Final puan: 0.70 × 1.10 = 0.77
```

Veya kötü durumda:
```
Temel puan: 0.70
CLT Çarpanı: ×0.80 (Overload + High Extraneous cezaları)
Final puan: 0.70 × 0.80 = 0.56
```

**Yeni Formül:**
```
Final Puan = Temel Puan × CLT Çarpanı
```

**Kısaca:** Bilişsel yük artık sadece bakılan bir şey değil, **puanı gerçekten etkiliyor**. "Kafanı yoracak mı?" sorusunun cevabı artık sıralamayı değiştiriyor.

---

## 14. Sistem Senden Öğreniyor (Adaptive Weight Optimization) 🎓

**Analoji: Öğretmenin her çocuktan öğrenmesi**

Düşün ki öğretmen her hafta sana bir arkadaş öneriyor. Sen "Bu arkadaşla çok eğlendim! ⭐⭐⭐⭐⭐" veya "Bu arkadaşla pek iyi olmadı ⭐⭐" diyorsun.

Akıllı bir öğretmen ne yapar? **"Hmm, bu çocuk öğrenmeyi seviyor, demek ki tamamlayıcı arkadaşlar daha iyi gidiyor. Bir dahaki sefere buna daha çok dikkat edeyim."**

İşte bilgisayar da aynısını yapıyor!

### Nasıl Çalışıyor?

1. **Sen geri bildirim veriyorsun:** Her görevden sonra "Bu nasıldı?" diye puanlıyorsun.

2. **Bilgisayar öğreniyor:** 
   - "Bu çocuk öğrenmeyi seviyor ve benzer AI'lardan memnun kalmış → Benzerlik kuralını biraz artırayım"
   - "Bu çocuk üretim odaklı ve performans iyi çıkmış → Performans kuralını artırayım"

3. **Ağırlıklar güncelleniyor:**
   ```
   Önceki: α=0.30, β=0.35, γ=0.25, δ=0.10
   Sonraki: α=0.34, β=0.30, γ=0.20, δ=0.16
   ```

### Örnek: İki Farklı Çocuk

**Öğrenme seven çocuk (Ayşe):**
- Geri bildirim: Tamamlayıcı AI'lardan çok memnun
- Sistem öğreniyor: "Ayşe'ye benzerlik ve öğrenme önemli"
- α ve δ artıyor

**Hızlı iş bitirmek isteyen çocuk (Mehmet):**
- Geri bildirim: Performans odaklı AI'lardan memnun
- Sistem öğreniyor: "Mehmet'e yetkinlik ve performans önemli"
- β ve γ artıyor

**Kısaca:** Sistem **sabit değil**, senin verdiğin puanlara göre **kendini ayarlıyor**. Her kullanıcı için özel bir deneyim.

---

## 15. Tüm Bölümlerin Tek Cümlelik Özeti

| Bölüm | 9 yaşındakine tek cümle |
|--------|--------------------------|
| **User Vector** | Sen 10 kutucukla anlatılıyorsun (güç, bilgi, hedef vb.). |
| **Persona Vector** | Her AI’ın da 10 kutucuklu kartı var (nasıl konuşur, ne kadar zor vb.). |
| **Benzerlik** | İkinizin kutucukları ne kadar aynı yönde ve yakın sayıda? |
| **Yetkinlik uyumu** | Bu AI ne çok kolay ne çok zor; tam öğrenebileceğin yerde mi? |
| **Performans tahmini** | Bu AI ile bu işi iyi yapma ihtimalin ne? |
| **Öğrenme yörüngesi** | Bu AI ile zamanla ne kadar gelişirsin? |
| **Tamamlayıcılık** | Senin eksiklerin, onun güçlü yanları mı? |
| **Ağırlıklar (α,β,γ,δ)** | Hangi kurala daha çok puan veriyoruz? (En çok: zorluk uyumu.) |
| **Bilişsel yük** | Bu AI kafanı ne çok yorar ne çok boş bırakır mı? |
| **Similar / Complementary** | Biri “sana benzeyen”, biri “seni tamamlayan” iki AI seçiliyor. |
| **Adaptive** | "Hedefin ne?" diye bakıp ona göre benzer / tamamlayıcı / karışık puanlaması. |
| **CLT Çarpanı** | Bilişsel yük analizi puana bonus/ceza olarak ekleniyor. |
| **Sistem Öğrenmesi** | Geri bildirimine göre kuralların ağırlıkları değişiyor. |

---

Bu belge, **recommendation_engine**’in her parçasını 9 yaşındaki birine **analojiyle** anlatmak için yazıldı. Orijinal kod ve formüller `recommendation_engine.py` ve `recommendation_engine_ACIKLAMALI.py` içinde; detay için oraya bakılabilir.
