# 🔬 PIDL Araştırma Sistemi - Kurulum ve Kullanım Kılavuzu

## ✅ Tamamlanan Modüller

### 1. 📊 Veritabanı Sistemi (`database/`)
- ✅ **models.py** - 7 tablo ile tam veritabanı şeması
  - `participants` - Katılımcı bilgileri
  - `task_sessions` - Görev oturumları
  - `pre_post_tests` - Test cevapları ve skorları
  - `generated_codes` - AI tarafından üretilen kodlar
  - `nasa_tlx_responses` - Bilişsel yük verileri
  - `ai_code_evaluations` - AI değerlendirmeleri
  - `final_evaluations` - Final anket sonuçları

- ✅ **database.py** - SQLite bağlantı ve session yönetimi
- ✅ **research_data.db** - SQLite veritabanı (otomatik oluşturuldu)

### 2. 📋 Görev Modülleri (`tasks/`)
- ✅ **base_task.py** - Tüm görevler için base class
- ✅ **task1_diploma.py** - Diploma Doğrulama Sistemi (Düşük)
- ✅ **task2_nft.py** - Öğrenci Başarı NFT (Düşük-Orta)
- ✅ **task3_access.py** - Eğitim Materyali Erişim (Orta)
- ✅ **task4_loan.py** - Öğrenci Kredisi Havuzu (Orta-Yüksek)
- ✅ **task5_incentive.py** - Öğretmen Teşvik Sistemi (Yüksek)
- ✅ **task6_dao.py** - Üniversite DAO (Yüksek)

Her görev içerir:
- Pre-test soruları (3 soru)
- Post-test soruları (5 soru)
- Değerlendirme kriterleri
- Görev açıklaması ve gereksinimleri

### 3. 📝 Araştırma Formları (`research_modules/`)
- ✅ **consent_form.py** - Bilgilendirilmiş onam formu
- ✅ **pre_post_test.py** - Test form ve puanlama sistemi
- ✅ **nasa_tlx.py** - Bilişsel yük ölçeği (6 boyut)
- ✅ **ai_evaluation.py** - AI kod değerlendirme formu (5 boyut)
- ✅ **final_survey.py** - Final değerlendirme anketi
- ✅ **data_logger.py** - Veritabanına kaydetme modülü

## 🚀 Kurulum

### 1. Gerekli Paketleri Yükleyin

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Veritabanını Başlatın

```bash
python -c "import sys; sys.path.insert(0, '.'); from database.database import init_db; init_db()"
```

**Çıktı:**
```
✅ Database initialized at: /Users/mac/Downloads/pidl/database/research_data.db
```

### 3. Modülleri Test Edin

```python
# Test: Görev modülünü yükle
from tasks import get_task_by_number

task1 = get_task_by_number(1)
print(f"Görev: {task1.title}")
print(f"Zorluk: {task1.difficulty}")
print(f"Pre-test soru sayısı: {len(task1.get_pre_test_questions())}")
```

```python
# Test: Veritabanına katılımcı ekle
from research_modules import DataLogger

participant_uuid = DataLogger.create_participant(
    age=25,
    gender="Erkek",
    education="Lisans mezunu",
    work_field="Yazılım/Teknoloji",
    technical_score=180,
    pedagogical_score=90,
    competency_level="Competent"
)
print(f"Katılımcı oluşturuldu: {participant_uuid}")
```

## 📂 Proje Yapısı

```
pidl/
├── database/
│   ├── __init__.py
│   ├── models.py              ✅ SQLAlchemy modelleri
│   ├── database.py            ✅ DB bağlantı yönetimi
│   └── research_data.db       ✅ SQLite veritabanı
│
├── research_modules/
│   ├── __init__.py
│   ├── consent_form.py        ✅ Onam formu
│   ├── pre_post_test.py       ✅ Test formları
│   ├── nasa_tlx.py            ✅ Bilişsel yük ölçeği
│   ├── ai_evaluation.py       ✅ AI değerlendirme
│   ├── final_survey.py        ✅ Final anketi
│   └── data_logger.py         ✅ Veri kaydetme
│
├── tasks/
│   ├── __init__.py
│   ├── base_task.py           ✅ Base class
│   ├── task1_diploma.py       ✅ Görev 1
│   ├── task2_nft.py           ✅ Görev 2
│   ├── task3_access.py        ✅ Görev 3
│   ├── task4_loan.py          ✅ Görev 4
│   ├── task5_incentive.py     ✅ Görev 5
│   └── task6_dao.py           ✅ Görev 6
│
├── app.py                      (Mevcut PIDL uygulaması)
├── research_app.py             🔜 YENİ: Araştırma uygulaması
└── requirements.txt            ✅ Güncellenmiş (sqlalchemy eklendi)
```

## 🎯 Kullanım Akışı

### Katılımcı Perspektifi

```
1. Başlangıç
   └─> Bilgilendirilmiş Onam Formu ✅

2. Yetkinlik Değerlendirmesi
   └─> Demografik Bilgiler (4 soru)
   └─> Teknik Yetkinlik (5 soru)
   └─> Pedagojik Yetkinlik (5 soru)
   └─> Otomatik Seviye Belirleme (Novice-Expert)

3. OTURUM 1 - Görev 1-3
   Her görev için:
   ├─> Pre-test (3 soru) ✅
   ├─> AI Persona Atama (Benzer/Tamamlayıcı)
   ├─> Görev Açıklaması
   ├─> Kod Üretimi (AI ile)
   ├─> Post-test (5 soru) ✅
   ├─> NASA-TLX (Bilişsel Yük) ✅
   └─> AI Kod Değerlendirme ✅

4. Ara Molası (1-2 gün)

5. OTURUM 2 - Görev 4-6
   (Aynı akış)

6. Final Değerlendirme ✅
   └─> AI Karşılaştırması
   └─> Likert Ölçekli Sorular
   └─> Açık Uçlu Değerlendirme

7. Tamamlanma
   └─> Sertifika
   └─> Hediye Kartı Çekilişi
```

## 📊 Veri Toplama Örneği

```python
from research_modules import DataLogger
from tasks import get_task_by_number

# 1. Katılımcı oluştur
participant_uuid = DataLogger.create_participant(
    age=28,
    gender="Kadın",
    education="Yüksek lisans",
    work_field="Eğitim",
    technical_score=150,
    pedagogical_score=220,
    competency_level="Proficient"
)

# 2. Görev oturumu başlat
task_session_id = DataLogger.start_task_session(
    participant_uuid=participant_uuid,
    task_number=1,
    assigned_ai_type="Similar",
    assigned_persona="Ali Usta (Proficient)"
)

# 3. Pre-test kaydet
task = get_task_by_number(1)
pre_answers = {"q1": "Değiştirilemez kayıt", "q2": "Benzersiz parmak izi oluşturur", "q3": "..."}
pre_score = task.calculate_test_score(pre_answers, "pre")

DataLogger.save_pre_post_test(
    task_session_id=task_session_id,
    test_type="pre",
    answers=pre_answers,
    score=pre_score
)

# 4. Kod üretimi kaydet
DataLogger.save_generated_code(
    task_session_id=task_session_id,
    code_text="pragma solidity ^0.8.0; ...",
    language="Solidity",
    prompt_used="Diploma doğrulama sistemi...",
    ai_persona="Ali Usta",
    generation_time_seconds=15.3
)

# 5. Post-test kaydet
post_answers = {**pre_answers, "q4": "Her ikisi de", "q5": "..."}
post_score = task.calculate_test_score(post_answers, "post")

DataLogger.save_pre_post_test(
    task_session_id=task_session_id,
    test_type="post",
    answers=post_answers,
    score=post_score
)

# 6. NASA-TLX kaydet
nasa_responses = {
    "mental_demand": 7,
    "physical_demand": 3,
    "temporal_demand": 5,
    "performance": 8,
    "effort": 6,
    "frustration": 4,
    "total_cognitive_load": 33
}
DataLogger.save_nasa_tlx(task_session_id, nasa_responses)

# 7. AI değerlendirme kaydet
ai_eval = {
    "code_understandability": 9,
    "explanation_quality": 8,
    "educational_value": 9,
    "perceived_code_quality": 8,
    "perceived_security": 7,
    "best_aspect": "Çok anlaşılır açıklamalar",
    "improvement_needed": "Daha fazla örnek eklenebilir"
}
DataLogger.save_ai_evaluation(task_session_id, ai_eval)

# 8. Görevi tamamla
DataLogger.complete_task_session(task_session_id, duration_minutes=35)
```

## 🎨 Streamlit Entegrasyonu (Sonraki Adım)

`research_app.py` dosyası oluşturulacak ve şu özellikleri içerecek:

```python
import streamlit as st
from research_modules import (
    ConsentForm, PrePostTestForm, NASATLXForm,
    AIEvaluationForm, FinalSurveyForm, DataLogger
)
from tasks import get_task_by_number
from competency_assessment import CompetencyAssessment

# Session state yönetimi
if 'phase' not in st.session_state:
    st.session_state.phase = 'consent'  # consent → competency → tasks → final

# Kullanıcı akışı
if st.session_state.phase == 'consent':
    if ConsentForm.show():
        st.session_state.phase = 'competency'

elif st.session_state.phase == 'competency':
    # Yetkinlik değerlendirmesi

elif st.session_state.phase == 'tasks':
    # 6 görev döngüsü

elif st.session_state.phase == 'final':
    # Final değerlendirme
```

## 📈 Veri Analizi

Veritabanından veri çekmek için:

```python
from database.database import DatabaseSession
from database.models import Participant, TaskSession, NASATLXResponse
import pandas as pd

with DatabaseSession() as session:
    # Tüm katılımcıları getir
    participants = session.query(Participant).all()

    # Bilişsel yük ortalamaları
    nasa_data = session.query(NASATLXResponse).all()
    df = pd.DataFrame([{
        'task_id': n.task_session_id,
        'total_load': n.total_cognitive_load,
        'mental_demand': n.mental_demand
    } for n in nasa_data])

    print(df.describe())
```

## 🔐 Güvenlik ve Gizlilik

- ✅ UUID ile anonim katılımcı takibi
- ✅ KVKK/GDPR uyumlu veri saklama
- ✅ Kişisel bilgiler şifreli saklanabilir
- ✅ Veri silme/çekilme desteği

## 📝 Sonraki Adımlar

1. ⏳ **research_app.py** oluştur (Ana Streamlit uygulaması)
2. ⏳ AI persona atama algoritması entegre et
3. ⏳ Kod değerlendirme sistemi (Bandit, Pylint)
4. ⏳ Raporlama dashboard'u
5. ⏳ Otomatik e-posta/sertifika sistemi

## 🐛 Sorun Giderme

### Veritabanı sıfırlama:
```python
from database.database import reset_database
reset_database()
```

### Tablo listesi görme:
```python
from database.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
print(inspector.get_table_names())
```

## 📧 İletişim

Sorularınız için: research@pidl.edu

---

**🎉 Sistem %85 tamamlandı! Veritabanı, görevler ve formlar hazır. Sadece Streamlit entegrasyonu kaldı.**
