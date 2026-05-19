# 🚀 PIDL Araştırma Sistemi - Hızlı Başlangıç

## ✅ Sistem Hazır!

Tüm modüller başarıyla oluşturuldu ve test edildi.

## 📦 Kurulum (İlk Kullanım)

### 1. Gereksinimleri Kontrol Et

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Veritabanını Başlat

```bash
python -c "import sys; sys.path.insert(0, '.'); from database.database import init_db; init_db()"
```

**Beklenen çıktı:**
```
✅ Database initialized at: /Users/mac/Downloads/pidl/database/research_data.db
```

## 🎯 Uygulamayı Çalıştır

### Araştırma Uygulaması

```bash
streamlit run research_app.py
```

Tarayıcınız otomatik açılacak: `http://localhost:8501`

### Ana PIDL Uygulaması (Eski)

```bash
streamlit run app.py
```

## 👥 Kullanıcı Akışı

### 1. Onam Formu (consent)
- Katılımcı bilgilendirme
- 5 onay checkbox'ı
- KVKK/GDPR uyumlu

### 2. Yetkinlik Değerlendirmesi (competency)
- Demografik bilgiler (4 soru)
- Teknik yetkinlik (5 soru)
- Pedagojik yetkinlik (5 soru)
- **Otomatik seviye belirleme:** Novice → Expert
- Veritabanına katılımcı kaydedilir

### 3. Görevler (tasks) - 6 Görev

Her görev için:

```
1. Pre-test (3 soru)
   ↓
2. Görev Açıklaması
   ↓
3. AI ile Kod Üretimi
   - Atanan persona (Similar/Complementary)
   - Prompt girişi
   - Kod üretimi
   ↓
4. Post-test (5 soru)
   ↓
5. NASA-TLX (Bilişsel Yük - 6 boyut)
   ↓
6. AI Kod Değerlendirme (5 boyut + açık uçlu)
   ↓
Sonraki göreve geç
```

**Görevler:**
1. Diploma Doğrulama (Düşük) - Similar AI
2. Öğrenci NFT (Düşük-Orta) - Complementary AI
3. Erişim Kontrolü (Orta) - Similar AI
4. Kredi Havuzu (Orta-Yüksek) - Complementary AI
5. Öğretmen Teşvik (Yüksek) - Similar AI
6. Üniversite DAO (Yüksek) - Complementary AI

### 4. Final Değerlendirme (final)
- AI karşılaştırması
- Likert ölçekli sorular (1-5)
- Genel deneyim (1-10)
- Açık uçlu sorular

### 5. Tamamlanma (complete)
- Teşekkür mesajı
- Sertifika bilgisi
- Hediye kartı çekilişi

## 📊 Veritabanı Kontrolleri

### Katılımcıları Görüntüle

```python
import sys
sys.path.insert(0, '.')

from database.database import DatabaseSession
from database.models import Participant
import pandas as pd

with DatabaseSession() as session:
    participants = session.query(Participant).all()

    data = [{
        'UUID': p.uuid[:8] + '...',
        'Yaş': p.age,
        'Seviye': p.level.value,
        'Teknik': p.technical_score,
        'Pedagojik': p.pedagogical_score,
        'Tamamlandı': '✅' if p.completed else '⏳'
    } for p in participants]

    df = pd.DataFrame(data)
    print(df)
```

### Görev Oturumlarını Görüntüle

```python
from database.models import TaskSession

with DatabaseSession() as session:
    sessions = session.query(TaskSession).all()

    for s in sessions:
        print(f"Görev {s.task_number} - {s.assigned_ai_type.value} - {s.status.value}")
```

### Bilişsel Yük Analizi

```python
from database.models import NASATLXResponse

with DatabaseSession() as session:
    nasa_data = session.query(NASATLXResponse).all()

    total_loads = [n.total_cognitive_load for n in nasa_data]
    avg_load = sum(total_loads) / len(total_loads) if total_loads else 0

    print(f"Ortalama Bilişsel Yük: {avg_load:.1f}/60")
```

## 🗄️ Veritabanı Yönetimi

### Veritabanını Sıfırla

```python
from database.database import reset_database
reset_database()
```

**UYARI:** Tüm veriler silinir!

### Tabloları Listele

```python
from database.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

for table in tables:
    print(f"✓ {table}")
```

## 📈 Veri Analizi Örneği

```python
import pandas as pd
from database.database import DatabaseSession
from database.models import Participant, TaskSession, NASATLXResponse, PrePostTest

with DatabaseSession() as session:
    # Öğrenme kazanımı analizi
    results = session.query(
        PrePostTest.task_session_id,
        PrePostTest.test_type,
        PrePostTest.score
    ).all()

    df = pd.DataFrame(results, columns=['session_id', 'test_type', 'score'])

    # Pre-test ve Post-test karşılaştırması
    pre_scores = df[df.test_type == 'pre']['score']
    post_scores = df[df.test_type == 'post']['score']

    print(f"Pre-test ortalama: {pre_scores.mean():.1f}")
    print(f"Post-test ortalama: {post_scores.mean():.1f}")
    print(f"Öğrenme kazanımı: {(post_scores.mean() - pre_scores.mean()):.1f} puan")
```

## 🎨 Özelleştirme

### AI Persona Atama Stratejisini Değiştir

`research_app.py` dosyasında `assign_ai_persona()` fonksiyonunu düzenleyin:

```python
def assign_ai_persona(task_number: int, competency_level: str) -> dict:
    # Kendi stratejinizi buraya ekleyin
    # Örn: Tüm görevler için Similar AI
    ai_type = "Similar"

    # veya rastgele atama
    import random
    ai_type = random.choice(["Similar", "Complementary"])

    return {"ai_type": ai_type, "persona": "..."}
```

### Görev Sıralamasını Değiştir

`research_app.py` içinde `phase_tasks()` fonksiyonunda:

```python
# Özel sıralama
custom_order = [3, 1, 5, 2, 6, 4]
actual_task_number = custom_order[current_task_number - 1]
task = get_task_by_number(actual_task_number)
```

## 🔧 Sorun Giderme

### Import Hatası

```bash
# PYTHONPATH ayarla
export PYTHONPATH="${PYTHONPATH}:."
streamlit run research_app.py
```

### SQLite Kilidi

```bash
# Veritabanı dosyasını sil ve yeniden oluştur
rm database/research_data.db
python -c "from database.database import init_db; init_db()"
```

### Port Zaten Kullanımda

```bash
# Farklı port kullan
streamlit run research_app.py --server.port 8502
```

## 📧 Destek

Sorularınız için:
- Email: research@pidl.edu
- GitHub Issues: https://github.com/...

## 📝 Lisans

MIT License

---

## ✅ Checklist

Uygulamayı çalıştırmadan önce:

- [x] Virtual environment aktif
- [x] Gereksinimler yüklü (`pip install -r requirements.txt`)
- [x] Veritabanı başlatıldı (`init_db()`)
- [x] `.env` dosyası var (API keys)
- [ ] Uygulamayı çalıştır (`streamlit run research_app.py`)

---

**🎉 Sistem hazır! İyi araştırmalar!**
