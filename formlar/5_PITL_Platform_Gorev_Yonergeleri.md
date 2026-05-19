# Form 5 — PITL Platformu Görev Yönergeleri
## Eğitim Odaklı Akıllı Sözleşme Görev Seti

**Araştırma:** İnsan-Yapay Zeka İşbirliği Modellerinde Yetkinlik Transferi ve Performans Optimizasyonu: Blokzincir Tabanlı Eğitim Teknolojilerinde PITL Çok Katmanlı Yetkinlik Modellemesi
**Platform:** PITL (Persona In The Loop)

---

## Görev Seti Yapısı

Görev seti **12 görevden** oluşmaktadır ve **iki bloğa** ayrılmıştır:

| Blok | Mod | Görev | Mekanizma |
|------|-----|-------|-----------|
| **Blok 1 — Adaptif** | NASA-TLX bazlı dinamik | Görev 1–6 | Her görev sonrası bilişsel yüke göre Benzer/Tamamlayıcı mod otomatik atanır |
| **Blok 2 — Sabit** | Counterbalanced | Görev 7–12 | Katılımcının UUID paritesine göre tüm blok boyunca **tek bir mod** sabit kalır |

Görev sırası tüm katılımcılar için aynıdır; karmaşıklık düzeyi düşük-orta-yüksek
biçiminde dalgalı bir sıra izler (bilişsel yorgunluk etkisini azaltmak için).

---

## BLOK 1 — Adaptif Görevler (Görev 1–6)

### Görev 1: Diploma Doğrulama Sistemi *(Düşük karmaşıklık)*

**Amaç:** Üniversite için blockchain tabanlı diploma doğrulama sistemi geliştirmek.

**Gereksinimler:**
- Yalnızca üniversite yönetimi (yetkili adres) diploma ekleyebilir.
- Diploma hash'i, öğrenci bilgisi ve mezuniyet tarihi zincirde saklanır.
- Herkes diploma doğrulayabilir; iptal edilebilir diploma özelliği bulunur.

**Beklenen Fonksiyonlar:**
```solidity
addDiploma(address student, bytes32 diplomaHash, string studentName, uint256 graduationDate)
verifyDiploma(address student) returns (bool, bytes32, string, uint256)
revokeDiploma(address student)
isDiplomaValid(address student) returns (bool)
```

**Değerlendirme Kriterleri (100 puan):**
- [ ] Yetki kontrolü (`onlyOwner` veya benzeri) — 25
- [ ] Diploma ekleme ve hash saklama — 25
- [ ] Doğrulama fonksiyonu — 25
- [ ] İptal mekanizması — 25

---

### Görev 2: Öğrenci Başarı NFT Sistemi *(Düşük-Orta karmaşıklık)*

**Amaç:** Öğrenci başarılarını NFT (ERC-721 veya Soulbound) olarak ödüllendiren bir sistem.

**Gereksinimler:**
- Her başarı kategorisi için benzersiz NFT bas (mint).
- Yalnızca öğretmen yetkili adresleri mint edebilir.
- Öğrencinin tüm NFT'leri listelenebilir.
- Transfer kısıtlaması (öğrenciden öğrenciye devredilemez) opsiyonel olarak eklenmelidir.

**Değerlendirme Kriterleri (100 puan):**
- [ ] NFT veri yapısı ve mapping — 25
- [ ] Mint fonksiyonu yetki kontrolü — 25
- [ ] Öğrenci NFT listeleme — 25
- [ ] Transfer kısıtlaması — 25

---

### Görev 3: Eğitim Materyali Erişim Kontrolü *(Orta karmaşıklık)*

**Amaç:** Ücretli eğitim içerikleri için ödeme + zaman bazlı erişim sözleşmesi.

**Gereksinimler:**
- İçerik fiyatlandırması yöneticisi tarafından belirlenir.
- Kullanıcı `payable` fonksiyon ile abonelik satın alır (belirli süre).
- Süre dolduğunda erişim otomatik kapanır (`block.timestamp` ile).
- İçerik satıcısı bakiyeyi çekebilir (withdraw).

**Değerlendirme Kriterleri (100 puan):**
- [ ] Ödeme alma ve doğrulama — 30
- [ ] Süreli erişim kontrolü — 30
- [ ] Withdraw mekanizması — 20
- [ ] Güvenlik kontrolleri — 20

---

### Görev 4: Öğrenci Kredisi Havuzu *(Orta-Yüksek karmaşıklık)*

**Amaç:** Merkeziyetsiz bir öğrenci kredisi (lending) havuzu oluşturmak.

**Gereksinimler:**
- Yatırımcılar kontrata ETH yatırır, faiz kazanır.
- Öğrenciler kredi başvurusunda bulunur; başvuru DAO onayı veya skor bazlı otomatik onayla işlenir.
- Geri ödeme planı zincirde tutulur.
- Temerrüt durumunda teminat (varsa) likidite edilir.

**Değerlendirme Kriterleri (100 puan):**
- [ ] Yatırım/withdraw mantığı — 25
- [ ] Kredi tahsis mekanizması — 30
- [ ] Geri ödeme takibi — 25
- [ ] Güvenlik (reentrancy, overflow) — 20

---

### Görev 5: Öğretmen Teşvik ve Ödül Sistemi *(Yüksek karmaşıklık)*

**Amaç:** Kaliteli eğitim içeriği üreten öğretmenler için token bazlı teşvik sözleşmesi.

**Gereksinimler:**
- Öğrenci geri bildirimi (5 yıldız) zincirde toplanır.
- Belirli eşiği aşan öğretmenlere ERC-20 token dağıtılır.
- Spam/sahte oy önleme: yalnızca abone öğrenciler oy verebilir.
- Aylık periyodlarla ödül havuzu yenilenir.

**Değerlendirme Kriterleri (100 puan):**
- [ ] Geri bildirim toplama mekanizması — 25
- [ ] Token dağıtım mantığı — 30
- [ ] Spam koruması — 20
- [ ] Periyodik dağıtım — 25

---

### Görev 6: Merkeziyetsiz Üniversite DAO'su *(Yüksek karmaşıklık)*

**Amaç:** Blockchain tabanlı bir üniversite yönetim DAO'su (müfredat değişiklikleri, akreditasyon vb.).

**Gereksinimler:**
- Üye ekleme/çıkarma (yalnızca DAO kararıyla).
- Önerilerin (proposal) oluşturulması ve oylanması.
- Quorum + zaman bazlı oylama (`block.timestamp`).
- Sonuç hesaplama ve kararın otomatik uygulanması (hash kaydı).

**Değerlendirme Kriterleri (100 puan):**
- [ ] Üye/proposal yönetimi — 25
- [ ] Oylama mekanizması (tek oy hakkı) — 25
- [ ] Quorum ve zaman bazlı kısıtlamalar — 25
- [ ] Karar uygulama mantığı — 25

---

## BLOK 2 — Sabit Mod Görevleri (Görev 7–12)

Blok 2'de aynı altı görev tekrar uygulanır; ancak bu blokta **persona modu değişmez**.
Counterbalancing için:

- **Çift UUID** katılımcıları: Blok 2 boyunca **Benzer Mod**'da çalışır.
- **Tek UUID** katılımcıları: Blok 2 boyunca **Tamamlayıcı Mod**'da çalışır.

Görev içerikleri Blok 1 ile aynıdır ancak parametre değerleri (eşikler, faiz oranları,
abonelik süreleri vb.) farklılaştırılır. Bu sayede:

- H1 (Mod etkisi öğrenme üzerine)
- H2 (Mod etkisi bilişsel yük üzerine)
- H4 (Adaptif geçişin sabit moda kıyasla üstünlüğü)

hipotezleri için karşılaştırmalı veri elde edilir.

| Blok 2 Görevi | Eşleniği | Sabit Mod (UUID parite) |
|---|---|---|
| Görev 7 | Görev 1 — Diploma Doğrulama (v2) | Çift: Benzer · Tek: Tamamlayıcı |
| Görev 8 | Görev 2 — NFT Başarı Sistemi (v2) | Çift: Benzer · Tek: Tamamlayıcı |
| Görev 9 | Görev 3 — Materyal Erişim (v2) | Çift: Benzer · Tek: Tamamlayıcı |
| Görev 10 | Görev 4 — Kredi Havuzu (v2) | Çift: Benzer · Tek: Tamamlayıcı |
| Görev 11 | Görev 5 — Teşvik Sistemi (v2) | Çift: Benzer · Tek: Tamamlayıcı |
| Görev 12 | Görev 6 — DAO (v2) | Çift: Benzer · Tek: Tamamlayıcı |

---

## Platform Kullanım Adımları

### Adım 1 — Giriş ve Hazırlık
Size atanan kullanıcı kodu (UUID) ile platforma giriş yapın. Ana sayfada size atanan AI persona ve görev listesini göreceksiniz.

### Adım 2 — CAQ Tamamlama
İlk girişte Yetkinlik Değerlendirme Anketini (Form 1) tamamlayın (10–15 dk). Sistem otomatik olarak kullanıcı vektörünüzü ve uygun personayı belirler.

### Adım 3 — Görev Döngüsü
Her görev için:
1. **Ön-test** (5 çoktan seçmeli soru — 3 dk)
2. **Görev açıklaması ve gereksinimlerin okunması** (2 dk)
3. **AI persona ile etkileşim** (sohbet penceresi) — kod inceleme + Sokratik sorular (10–15 dk)
4. **Kodun teslim edilmesi**
5. **Son-test** (5 çoktan seçmeli soru — 3 dk)
6. **NASA-TLX bilişsel yük ölçeği** (0–100, 2 dk)
7. **Kısa görev değerlendirmesi** (1 dk)

### Adım 4 — Blok Geçişi
Görev 6 sonrasında Blok 2'ye geçilir; sistem otomatik olarak persona modunu sabitler.

### Adım 5 — Final Anket (USQ)
Tüm görevler tamamlandıktan sonra Form 3'teki Kullanıcı Memnuniyet Anketi doldurulur (~15 dk).

### Adım 6 — (Opsiyonel) Görüşme
Seçilen katılımcılarla 30–45 dk yarı yapılandırılmış görüşme (Form 4).

---

## Etik Kurallar ve Dikkat Edilmesi Gerekenler

- **Özgün Çalışma:** AI sadece bir yardımcı/rehberdir. Kodu analiz eden ve onaylayan
  sizsiniz. Üretilen kodu satır satır okuyup anladığınızdan emin olun.
- **Dürüstlük:** Anketleri samimi cevaplayın; yanlış cevap yoktur.
- **Gizlilik:** Gerçek ad, e-posta, telefon vb. kişisel bilgileri AI ile paylaşmayın.
  Platform anonim UUID kullanmaktadır.
- **Süre Yönetimi:** Görev başına ortalama 15–20 dakika yeterlidir. İhtiyaç hâlinde
  araştırmacıyla iletişime geçebilirsiniz.
- **Teknik Destek:** Platform çökmesi, veri kaybı veya başka teknik sorunlarda
  araştırmacıya derhal bildirim yapın.

---

## Veri Toplama Onay Beyanı

Platform kullanımı sırasında aşağıdaki veriler bilimsel araştırma amacıyla toplanır:

- [x] Görev tamamlama süreleri
- [x] Yazılan/onaylanan akıllı sözleşme kodları
- [x] AI ile sohbet kayıtları (sorular ve yanıtlar)
- [x] Test sonuçları (ön/son test puanları)
- [x] Performans metrikleri (teknik + pedagojik kod kalitesi, coverage)
- [x] Anket yanıtları (CAQ, NASA-TLX, USQ)

Onay metni, **Form 3 — Bilgilendirilmiş Onam Formu** üzerinden alınmıştır.
