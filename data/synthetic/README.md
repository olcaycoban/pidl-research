# Sentetik veri (v3) – Çift blok, tüm hipotezler destekli

## Tasarım

- **Her katılımcı hem adaptif hem sabit blok** kullanır: toplam 12 görev (6 adaptif + 6 sabit).
- **Adaptif blok:** Mod ataması 3 Similar + 3 Complementary (sıra değişken).
- **Sabit blok:** Görev 1,3,5 Similar; 2,4,6 Complementary.

## Hipotez desteği

| Hipotez | Açıklama | Veriyle nasıl destekleniyor |
|--------|----------|-----------------------------|
| **H1** | Tamamlayıcı > Benzer (öğrenme kazanımı) | Görev düzeyinde Complementary görevlerde daha yüksek learning_gain. |
| **H2** | Benzer < Tamamlayıcı (bilişsel yük) | Görev düzeyinde Similar görevlerde daha düşük cognitive_load (NASA-TLX). |
| **H3** | Mod × Dreyfus etkileşimi | Acemide mod farkı (öğrenme, NASA-TLX, süre) büyük; uzmanda küçük (base_* fonksiyonları level_index kullanıyor). |
| **H4** | Adaptif > Sabit (performans) | Katılımcı düzeyinde adaptive_block ortalamaları > fixed_block; ~%89 katılımcıda adaptif blok öğrenme kazanımında daha yüksek. |

## Dosyalar

- **participant_XXX_&lt;level&gt;.json** – Tek katılımcı: `adaptive_block`, `fixed_block`, birleşik `tasks`, `summary`.
- **all_participants.json** – Özet liste (participant_id, dreyfus_level, adaptive/fixed ortalamalar, h4_adaptive_better).
- **summary_statistics.json** – Seviye bazlı ortalamalar, H4 destek sayısı, tasarım açıklaması.
- **task_level_data.json** – **H1, H2, H3 analizi için** görev düzeyi tablo (1800 satır: 150 × 12). Sütunlar: `participant_id`, `dreyfus_level`, `block`, `task_number`, `mod`, `learning_gain`, `cognitive_load`, `code_quality`, `duration_minutes`. Karma ANOVA (Mod × Dreyfus) ve eşleştirilmiş t-test için kullanılır.

## Yeniden üretmek

```bash
python3 scripts/generate_synthetic_data.py
```

Seed sabit (42); aynı komutla aynı veri seti elde edilir.
