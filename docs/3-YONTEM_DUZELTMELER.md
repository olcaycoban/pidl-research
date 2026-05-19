# YÖNTEM BÖLÜMÜ - DÜZELTME VE İYİLEŞTİRME RAPORU

Bu belge, `3-Yontem.docx` dosyasının detaylı incelemesi sonucunda tespit edilen düzeltilmesi gereken noktaları içermektedir.

---

## 1. KRİTİK HATALAR (MUTLAKA DÜZELTİLMELİ)

### 1.1. Karakter Kodlama Hatası (Sayfa 13, Aşama 3)

**Mevcut (Hatalı):**
> "Benzer Mod'da yetk}nl}k uyumu, ZPD tabanlı Gauss fonks}yonu ve b}lg} uyumu çarpımı olarak hesaplanmaktadır: C(u,p) = ZPD_Gauss(sev}ye_farkı) × B}lg}_Uyumu(u,p)."

**Düzeltilmiş:**
> "Benzer Mod'da yetkinlik uyumu, ZPD tabanlı Gauss fonksiyonu ve bilgi uyumu çarpımı olarak hesaplanmaktadır: C(u,p) = ZPD_Gauss(seviye_farkı) × Bilgi_Uyumu(u,p)."

**Açıklama:** "ı" ve "i" harfleri "}" olarak görünüyor. Bu bir karakter kodlama (encoding) hatası.

---

### 1.2. Matematiksel Formül Tutarsızlığı

**Mevcut (Sayfa 13, Aşama 3):**
> "Tamamlayıcı Mod'da }se tamamlayıcılık skoru..."

**Düzeltilmiş:**
> "Tamamlayıcı Mod'da ise tamamlayıcılık skoru, personanın güçlü olduğu ve kullanıcının zayıf olduğu boyutların çarpımlarının toplamı olarak hesaplanmaktadır: D(u,p) = Σᵢ (pᵢ_güçlü × uᵢ_zayıf)."

---

## 2. İÇERİK TUTARSIZLIKLARI

### 2.1. NASA-TLX Formülü Eksikliği

**Mevcut (Sayfa 8):**
> "NASA-TLX toplam puanı, altı alt boyutun ortalaması alınarak hesaplanmaktadır. Performans boyutu ters kodlandığından hesaplamaya (100 - Performans) olarak dahil edilmektedir."

**Önerilen Ekleme:**
Formül açıkça yazılmalı:

```
NASA-TLX_Toplam = (Zihinsel_Talep + Fiziksel_Talep + Zamansal_Talep + 
                  (100 - Performans) + Çaba + Hayal_Kırıklığı) / 6
```

---

### 2.2. Birleşik Kod Kalitesi Formülü

**Mevcut (Sayfa 9):**
> "Bu hesaplamada γ parametresi, kullanıcının öğrenme hedefine göre dinamik olarak belirlenmektedir."

**Önerilen Ekleme:**
Formül açıkça yazılmalı:

```
Kod_Kalitesi = γ × Teknik_Kalite + (1-γ) × Pedagojik_Kalite

Burada:
- γ = 0.7 → Üretim odaklı kullanıcılar için
- γ = 0.3 → Öğrenme odaklı kullanıcılar için  
- γ = 0.5 → Varsayılan (dengeli)
```

---

### 2.3. Kullanıcı Vektörü Bileşenleri Eksikliği

**Mevcut (Sayfa 12-13):**
> "Bu vektör; teknik beceri, alan bilgisi, yapay zeka deneyimi, öğrenme hedefi, prosedürel bilgi, deklaratif bilgi, koşullu bilgi, bilişsel kapasite, örüntü tanıma ve soyutlama düzeyi bileşenlerinden oluşmaktadır."

**Önerilen Düzeltme:**
Bileşenler tablo halinde sunulmalı:

| Bileşen | İngilizce | Açıklama | Aralık |
|---------|-----------|----------|--------|
| Teknik Beceri | technical_skill | Kod yazma yetkinliği | 0.0-1.0 |
| Alan Bilgisi | domain_knowledge | Blockchain/eğitim alan bilgisi | 0.0-1.0 |
| AI Deneyimi | ai_experience | Önceki AI araç kullanımı | 0.0-1.0 |
| Öğrenme Hedefi | learning_goal | Production vs Learning odağı | 0.0-1.0 |
| Prosedürel Bilgi | procedural_knowledge | "Nasıl" bilgisi | 0.0-1.0 |
| Deklaratif Bilgi | declarative_knowledge | "Ne" bilgisi | 0.0-1.0 |
| Koşullu Bilgi | conditional_knowledge | "Ne zaman" bilgisi | 0.0-1.0 |
| Bilişsel Kapasite | cognitive_capacity | Zihinsel işlem kapasitesi | 0.0-1.0 |
| Örüntü Tanıma | pattern_recognition | Kalıp algılama becerisi | 0.0-1.0 |
| Soyutlama Düzeyi | abstraction_level | Kavramsal düşünme | 0.0-1.0 |

---

### 2.4. Teknik Kalite Metrikleri Formülü Eksik

**Mevcut (Sayfa 8):**
Metrikler listelenmiş ancak birleşik formül verilmemiş.

**Önerilen Ekleme:**

```
Teknik_Kalite = 0.20 × (Pylint_Skoru / 10 × 100) +
               0.25 × Güvenlik_Skoru +
               0.20 × (1 - Karmaşıklık_Normalized) × 100 +
               0.20 × Bakım_İndeksi +
               0.15 × Test_Kapsamı
```

---

### 2.5. Pedagojik Kalite Metrikleri Formülü Eksik

**Mevcut (Sayfa 8-9):**
Metrikler listelenmiş ancak birleşik formül verilmemiş.

**Önerilen Ekleme:**

```
Pedagojik_Kalite = 0.25 × Yorum_Kalitesi +
                  0.20 × Örnek_Zenginliği +
                  0.20 × Öğrenme_Kolaylığı +
                  0.20 × CLT_Uygunluğu +
                  0.15 × Açıklanabilirlik
```

---

## 3. EKSİK REFERANSLAR VE ATIFLAR

### 3.1. Dreyfus Modeli Atıfı Eksik

**Mevcut:**
Dreyfus modeli birçok yerde kullanılıyor ancak orijinal kaynak atıfı yok.

**Önerilen Ekleme:**
İlk geçtiği yere eklenecek:
> "...Dreyfus yetkinlik modeli (Dreyfus & Dreyfus, 1980)..."

---

### 3.2. ZPD (Vygotsky) Atıfı Eksik

**Mevcut (Sayfa 15):**
> "Vygotsky'nin (1978) ZPD teorisi"

**Önerilen Düzeltme:**
Tam atıf:
> "Vygotsky'nin (1978) Yakınsal Gelişim Alanı (Zone of Proximal Development - ZPD) teorisi"

---

### 3.3. Bilişsel Yük Teorisi (CLT) Atıfı Eksik

**Mevcut (Sayfa 15):**
> "Sweller'in (1988) CLT'si"

**Önerilen Düzeltme:**
Tam atıf:
> "Sweller'in (1988) Bilişsel Yük Teorisi (Cognitive Load Theory - CLT)"

---

### 3.4. Tematik Analiz Detay Eksikliği

**Mevcut (Sayfa 17):**
> "Braun ve Clarke (2006) tarafından önerilen tematik analiz yöntemiyle"

**Önerilen Ekleme:**
Altı aşama açıkça listelenebilir:
1. Verilerle aşinalık kazanma
2. Başlangıç kodlarının üretilmesi
3. Temaların aranması
4. Temaların gözden geçirilmesi
5. Temaların tanımlanması ve adlandırılması
6. Raporun üretilmesi

---

## 4. YAPI VE FORMAT ÖNERİLERİ

### 4.1. Tablo 3.1 Formatı

**Mevcut:**
Tablo Word'de bozuk görünüyor olabilir.

**Önerilen Format:**

| Dreyfus Seviyesi | Teknik (N) | Pedagojik (N) | Katılımcı Kaynağı |
|------------------|------------|---------------|-------------------|
| Acemi (Novice) | 15 | 15 | Üniversite 1-2. sınıf öğrencileri |
| İleri Başlangıç (Advanced Beginner) | 15 | 15 | Üniversite 3-4. sınıf / yeni mezun |
| Yetkin (Competent) | 15 | 15 | 2-4 yıl deneyimli profesyoneller |
| Usta (Proficient) | 15 | 15 | 5-8 yıl deneyimli kıdemli uzmanlar |
| Uzman (Expert) | 15 | 15 | 10+ yıl deneyimli alan uzmanları |
| **TOPLAM** | **75** | **75** | **N = 150** |

---

### 4.2. Tablo 3.2 Genişletme Önerisi

**Mevcut Tablo 3.2:**
Sadece görev ve karmaşıklık var.

**Önerilen Genişletilmiş Format:**

| Görev | Konu | Karmaşıklık | Teknik Odak | Pedagojik Odak |
|-------|------|-------------|-------------|----------------|
| Görev 1 | Diploma Doğrulama Smart Contract | Düşük | Temel Solidity | Doğrulama süreci |
| Görev 2 | Sertifika NFT Sistemi | Orta | ERC-721 standardı | Dijital rozet tasarımı |
| Görev 3 | Öğrenme Kaydı Blockchain | Düşük | Veri yapıları | Öğrenme analitikleri |
| Görev 4 | Çoklu İmza Yönetim Sistemi | Yüksek | Multi-sig patterns | Kurumsal yönetişim |
| Görev 5 | DAO Tabanlı Oylama | Orta | Governance tokens | Katılımcı demokrasi |
| Görev 6 | Token Tabanlı Teşvik Sistemi | Yüksek | Tokenomics | Davranış değişikliği |

---

### 4.3. Prosedür Akış Şeması Önerisi

**Mevcut:**
Metin halinde açıklanmış.

**Önerilen Görsel Ekleme:**

```
┌─────────────────────────────────────────────────────────────┐
│                    VERİ TOPLAMA SÜRECİ                      │
│                    (Yaklaşık 2-2.5 saat)                    │
├─────────────────────────────────────────────────────────────┤
│  HAZIRLIK (5 dk)                                            │
│     └─→ Bilgilendirme + Onam + Teknik kontrol               │
│                          ↓                                  │
│  YETKİNLİK DEĞERLENDİRME (20 dk)                           │
│     └─→ Demografik + Teknik + Pedagojik + Dreyfus           │
│                          ↓                                  │
│  ┌────────────────────────────────────────────┐             │
│  │         GÖREV DÖNGÜSÜ (6 × ~17 dk)         │             │
│  │  ┌──────────────────────────────────────┐  │             │
│  │  │  Her görev için:                     │  │             │
│  │  │  1. Ön-test (3 dk)                   │  │             │
│  │  │  2. Görev açıklaması (2 dk)          │  │             │
│  │  │  3. AI persona ile çalışma (10-15 dk)│  │             │
│  │  │  4. Kod teslimi                      │  │             │
│  │  │  5. Son-test (3 dk)                  │  │             │
│  │  │  6. NASA-TLX (2 dk)                  │  │             │
│  │  │  7. Kısa değerlendirme (1 dk)        │  │             │
│  │  └──────────────────────────────────────┘  │             │
│  │              ↓ (× 6 kez)                   │             │
│  └────────────────────────────────────────────┘             │
│                          ↓                                  │
│  FİNAL DEĞERLENDİRME (15 dk)                               │
│     └─→ Final anketi + Memnuniyet                           │
│                          ↓                                  │
│  KAPANIŞ (5 dk)                                             │
│     └─→ Teşekkür + Çekiliş bilgisi                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. DİL VE ÜSLUP DÜZELTMELERİ

### 5.1. Tutarsız Terim Kullanımları

| Mevcut (Tutarsız) | Önerilen (Tutarlı) |
|-------------------|-------------------|
| "yapay zeka" ve "yapay zekâ" | "yapay zekâ" (tek form kullanılmalı) |
| "blokzincir" ve "blockchain" | "blokzincir" (Türkçe tercih) veya "blockchain" parantez içinde |
| "domain" ve "alan" | "alan" (domain) - ilk geçişte açıklama |
| "frontend" ve "ön yüz" | "ön yüz" (frontend) - tutarlı kullanım |

---

### 5.2. Pasif Yapı Aşırı Kullanımı

**Mevcut:**
> "Veriler toplanmaktadır", "Analiz edilmektedir", "Hesaplanmaktadır"

**Önerilen:**
Bazı yerlerde aktif yapı kullanılabilir:
> "Bu araştırmada veriler... yöntemiyle toplandı"
> "Araştırmacı, verileri... yöntemiyle analiz etti"

**Not:** Akademik yazımda pasif yapı kabul edilebilir, ancak aşırı kullanım okumayı zorlaştırır.

---

### 5.3. Gereksiz Tekrarlar

**Mevcut (Sayfa 1):**
> "Araştırma deseni, çalışma grubu, veri toplama araçları, PITL platformunun teknik mimarisi, veri toplama süreci, veri analizi yöntemleri, geçerlik ve güvenirlik stratejileri ile etik hususlar sistematik bir biçimde açıklanmaktadır."

**Önerilen:**
> "Bu bölümde araştırma deseni, çalışma grubu, veri toplama araçları ve süreci, PITL platformu, veri analizi, geçerlik-güvenirlik ve etik hususlar açıklanmaktadır."

---

## 6. EKSİK BÖLÜMLER / EKLEMELER

### 6.1. PITL Sisteminin Kuramsal Temelleri (Kısa Hatırlatma)

**Önerilen Ekleme (3.4 başlığı öncesine):**

> PITL sistemi, dört temel kuramsal çerçeve üzerine inşa edilmiştir:
> 
> 1. **Dreyfus Beceri Edinim Modeli:** Kullanıcı ve persona yetkinlik sınıflandırması
> 2. **Vygotsky'nin ZPD Teorisi:** Tamamlayıcı Mod'un kuramsal temeli
> 3. **Sweller'in Bilişsel Yük Teorisi:** Benzer Mod'un kuramsal temeli
> 4. **Nonaka & Takeuchi SECI Modeli:** Bilgi türleri (prosedürel, deklaratif, koşullu) temsili

---

### 6.2. Adaptif Mod Seçim Algoritması Detayı

**Önerilen Ekleme (3.4.3 sonuna):**

Algoritma pseudo-code olarak verilebilir:

```python
def adaptif_mod_sec(gorev_no, nasa_tlx_gecmisi, ogrenme_hedefi):
    if gorev_no == 1:
        # İlk görev: öğrenme hedefine göre
        if ogrenme_hedefi > 0.6:
            return "Tamamlayıcı"
        else:
            return "Benzer"
    else:
        # Sonraki görevler: NASA-TLX'e göre
        onceki_yuk = nasa_tlx_gecmisi[-1]["toplam"]
        if onceki_yuk > 60:
            return "Benzer"  # Yükü hafiflet
        elif onceki_yuk < 30:
            return "Tamamlayıcı"  # Öğrenmeyi teşvik et
        else:
            return alternatif_mod()  # Denge
```

---

### 6.3. Sınırlılıklar Bölümü Eksik

**Önerilen Ekleme (3.8 sonuna veya ayrı 3.9 olarak):**

> **3.X. Araştırmanın Sınırlılıkları**
> 
> Bu araştırma bazı sınırlılıklara sahiptir:
> 
> 1. **Örneklem:** Türkiye bağlamıyla sınırlıdır; farklı kültürel bağlamlara genelleme dikkatle yapılmalıdır.
> 2. **Programlama Dili:** Solidity ve blockchain odaklıdır; diğer programlama dilleri ve alanlar için uyarlamalar gerekebilir.
> 3. **AI Modeli:** GPT-4o ile sınırlıdır; farklı LLM'lerin persona davranışları farklılık gösterebilir.
> 4. **Süre:** 2-2.5 saatlik tek oturum, uzun vadeli öğrenme etkilerini ölçmekte yetersiz kalabilir.
> 5. **Çevrimiçi Ortam:** Kontrollü laboratuvar ortamına kıyasla daha fazla dışsal değişkenlik içerir.

---

## 7. SAYISAL DOĞRULAMA

### 7.1. Örneklem Büyüklüğü Hesaplaması ✓

- 5 Dreyfus seviyesi × 2 domain × 15 katılımcı = **150 katılımcı** ✓
- G*Power hesaplaması tutarlı (minimum 107, hedef 150) ✓

### 7.2. Persona Yapısı ✓

- 2 domain × 10 alt uzmanlık × 5 Dreyfus = **100 persona** ✓
- Teknoloji: 50 persona ✓
- Pedagoji: 50 persona ✓

### 7.3. Görev Sayısı ✓

- 6 görev (3 Benzer + 3 Tamamlayıcı) ✓

### 7.4. Süre Hesaplaması

**Mevcut:**
- Hazırlık: 5 dk
- Yetkinlik: 20 dk
- Görevler: 90-120 dk (6 × 15-20 dk)
- Final: 15 dk
- Kapanış: 5 dk
- **Toplam: 135-165 dk = 2.25-2.75 saat**

**Not:** "2-2.5 saat" ifadesi biraz iyimser. "2-2.75 saat" veya "yaklaşık 2.5 saat" daha doğru olabilir.

---

## 8. ŞEKİL VE TABLO LİSTESİ

Metinde referans verilen ancak eksik olan şekiller:

| Referans | Açıklama | Durum |
|----------|----------|-------|
| Şekil 3.3 | Yetkinlik değerlendirme aracı arayüzü | [EKRAN GÖRÜNTÜSÜ EKLENMELİ] |
| Şekil 3.4 | NASA-TLX platformdaki arayüzü | [EKRAN GÖRÜNTÜSÜ EKLENMELİ] |
| Şekil 3.5 | PITL platformu ana ekranı | [EKRAN GÖRÜNTÜSÜ EKLENMELİ] |
| Şekil 3.6 | Sistem mimarisi diyagramı | [DİYAGRAM EKLENMELİ] |
| Şekil 3.7 | Persona kütüphanesi arayüzü | [EKRAN GÖRÜNTÜSÜ EKLENMELİ] |
| Şekil 3.8 | Öneri algoritması çıktı ekranı | [EKRAN GÖRÜNTÜSÜ EKLENMELİ] |
| Şekil 3.9 | AI persona sohbet arayüzü | [EKRAN GÖRÜNTÜSÜ EKLENMELİ] |
| Şekil 3.10 | Görev döngüsü arayüzü | [EKRAN GÖRÜNTÜSÜ EKLENMELİ] |

**Öneri:** Tüm ekran görüntüleri PITL platformundan alınarak eklenmeli.

---

## 9. APA 7 FORMAT KONTROL

### 9.1. Metin İçi Atıf Formatı

**Doğru Kullanımlar:** ✓
- "Creswell ve Plano Clark (2018)"
- "Hart ve Staveland (1988)"
- "Braun ve Clarke (2006)"

**Düzeltilmesi Gerekenler:**
- "Cohen, 1988" → "(Cohen, 1988)" - parantez içinde olmalı

### 9.2. Kaynakça Kontrolü

Metinde geçen tüm kaynakların kaynakçada olduğundan emin olunmalı:
- Creswell & Plano Clark (2018) ✓
- Johnson & Onwuegbuzie (2004) ✓
- Moustakas (1994) ✓
- Patton (2015) ✓
- Hart & Staveland (1988) ✓
- Faul, Erdfelder, Lang & Buchner (2007) ✓
- Braun & Clarke (2006) ✓
- Campbell & Stanley (1963) ✓
- Vygotsky (1978) ✓
- Sweller (1988) ✓
- **Dreyfus & Dreyfus (1980)** - EKLENMELİ
- **Nonaka & Takeuchi (1995)** - EKLENMELİ (SECI modeli için)
- **Hart (2006)** - Kontrol edilmeli (NASA-TLX geçerlilik makalesi)

---

## 10. ÖZET: ÖNCELİKLİ DÜZELTMELER

### Acil (Kritik):
1. ☐ Karakter kodlama hatası düzeltilmeli (}→ı)
2. ☐ Eksik formüller eklenmeli (NASA-TLX, Kod Kalitesi)
3. ☐ Dreyfus & Dreyfus (1980) atıfı eklenmeli

### Yüksek Öncelik:
4. ☐ Tablo formatları düzeltilmeli
5. ☐ Terim tutarlılığı sağlanmalı
6. ☐ Kullanıcı vektörü tablosu eklenmeli
7. ☐ Sınırlılıklar bölümü eklenmeli

### Orta Öncelik:
8. ☐ Şekiller/ekran görüntüleri eklenmeli
9. ☐ Prosedür akış şeması eklenmeli
10. ☐ Süre hesaplaması güncellenmeli

### Düşük Öncelik:
11. ☐ Dil/üslup iyileştirmeleri
12. ☐ Gereksiz tekrarlar azaltılmalı

---

## 11. CLAUDE İÇİN YENİDEN YAZIM TALİMATLARI

Claude'a şu talimatları verebilirsiniz:

> Lütfen yukarıdaki düzeltmeleri uygulayarak 3. YÖNTEM bölümünü yeniden yaz. Özellikle:
> 
> 1. Tüm karakter kodlama hatalarını düzelt (} → ı, } → i)
> 2. Eksik matematiksel formülleri ekle
> 3. Dreyfus & Dreyfus (1980) ve Nonaka & Takeuchi (1995) atıflarını ekle
> 4. Tablo 3.1 ve 3.2'yi düzgün formatla
> 5. Kullanıcı vektörü için detaylı tablo ekle
> 6. "3.X Araştırmanın Sınırlılıkları" bölümü ekle
> 7. Terim tutarlılığını sağla (yapay zekâ, blokzincir)
> 8. APA 7 formatına uy
> 9. [EKRAN GÖRÜNTÜSÜ] yer tutucularını koru
> 10. Prosedür akış şeması ekle
> 
> Toplam uzunluk: ~22-25 sayfa
> Dil: Akademik Türkçe
> Format: APA 7

---

*Bu rapor, 3-Yontem.docx dosyasının detaylı incelemesi sonucunda hazırlanmıştır.*
*Tarih: 31 Ocak 2026*
