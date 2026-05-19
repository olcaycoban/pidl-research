# Platform 1 Sayfada Ne Yapıyor?

PIDL Araştırma Sistemi **tek bir web sayfası** (Streamlit uygulaması) üzerinde çalışır. Aynı URL’de kalırsınız; içerik **fazlara (phase)** göre değişir. Sidebar’da hangi fazda olduğunuz görünür.

---

## 1. Tek sayfa = 5 faz (ekran)

Uygulama **tek sayfa** ama **5 farklı ekran** (faz) sunar. Hangi ekranın gösterileceği `st.session_state.phase` ile belirlenir:

| Faz | phase değeri | Ekranda ne var? |
|-----|----------------|------------------|
| 1 | `consent` | Bilgilendirilmiş onam formu |
| 2 | `competency` | Yetkinlik değerlendirmesi (CAQ anketi) |
| 3 | `tasks` | 6 görev (pre-test → kod üretimi → post-test → NASA-TLX → AI değerlendirme) |
| 4 | `final` | Final anketi |
| 5 | `complete` | Teşekkür / tamamlandı |

Yani **“1 sayfada”** aslında şu anlama gelir: tek tarayıcı sekmesi, tek adres; içerik fazlara göre değişir.

---

## 2. Sayfa açıldığında (ilk yükleme)

- `init_session_state()` çalışır.
- `phase = 'consent'` atanır.
- `show_sidebar()` ile sol tarafta **“Araştırma İlerlemesi”** ve faz listesi gösterilir.
- Ana alanda **Faz 1: Onam Formu** (`phase_consent()`) çalışır.

Yani **platform 1 sayfada**, ilk etapta **onam ekranını** gösteriyor.

---

## 3. Faz 1 – Onam (consent) ekranında ne yapıyor?

Bu ekranda platform şunları yapar:

1. **Başlık:** “PIDL Araştırma Sistemi” ve “1. Bilgilendirilmiş Onam Formu”.
2. **Metin:** Araştırma adı, amacı, süresi, ne yapılacağı, riskler, faydalar, gizlilik, haklar, iletişim (ConsentForm içeriği).
3. **5 onay kutusu:**
   - Yukarıdaki bilgileri okudum ve anladım  
   - Sorularım yanıtlandı veya sormak istediğim soru yok  
   - Gönüllü olarak katılıyorum  
   - Verilerimin araştırmada kullanılmasına izin veriyorum  
   - İstersem çekilebileceğimi biliyorum  
4. **Kontrol:** Beşi de işaretlenince “Tüm onaylar verildi” mesajı.
5. **Buton:** “Onay Verdim, Devam Et” → tıklanınca `phase = 'competency'` yapılır ve sayfa yenilenir; içerik **Yetkinlik** ekranına geçer.

Özet: **1 sayfada**, ilk açılışta **sadece onam metnini gösterip 5 onay topluyor ve “Devam Et” ile bir sonraki faza geçiriyor.**

---

## 4. Sidebar (aynı sayfada sol panel)

Her fazda, **aynı sayfada** sol tarafta:

- Hangi fazda olduğunuz (→ Onam / Yetkinlik / Görevler / Final / Tamamlandı),
- Tamamlanan fazlar (✅),
- Henüz gelinmeyen fazlar (⏳),
- Görevler fazındaysanız “Görev: X/6” ve ilerleme çubuğu,
- Yetkinlik yapıldıysa kısa yetkinlik özeti (teknik/pedagojik seviye, dominant alan)

gösterilir. Yani **1 sayfada** hem ana içerik hem de bu ilerleme bilgisi birlikte sunulur.

---

## 5. Kısa özet: “Platform 1 sayfada ne yapıyor?”

- **Tek sayfa:** Tek URL, tek Streamlit uygulaması.
- **5 faz:** Onam → Yetkinlik → Görevler → Final → Tamamlandı; içerik `phase`’e göre değişir.
- **İlk açılışta:** Onam metni + 5 onay kutusu + “Onay Verdim, Devam Et” butonu; onaylayınca yetkinlik ekranına geçer.
- **Sidebar:** Hangi fazda olunduğu ve ilerleme hep aynı sayfada, solda gösterilir.

**Sonraki aşamalar (Faz 2–5) detaylı:** Bkz. **docs/PLATFORM_TUM_ASAMALAR.md**

İstersen bir sonraki adımda “Yetkinlik sayfasında 1 sayfada ne yapıyor?” veya “Görevler sayfasında 1 sayfada ne yapıyor?” diye de aynı mantıkla tek tek özetleyebilirim.
