# BIST Algo Terminal — Web Arayüzü

`alansheen.py`'deki BIST algoritmik tarama mantığını (rejim, Parkinson
volatilitesi, pivot, hacim Z-skoru, RSI, strateji matrisi) bir **Django** web
panosunda gösterir. ~240 hisse arka planda taranır; sonuçlar canlı dolan,
filtrelenebilir, sıralanabilir bir tabloda görüntülenir. Bir satıra tıklayınca
destek/direnç (R1/R2/S1/S2) seviye haritası ve stratejik yorum açılır.

> ⚠️ Veriler yfinance üzerinden gecikmeli olabilir. Yatırım tavsiyesi değildir.

## Kurulum

```bash
cd /Users/codezzium/Development/alsatsinyal

# Sanal ortam
python3 -m venv venv
source venv/bin/activate

# Bağımlılıklar
pip install -r requirements.txt
```

## Çalıştırma

```bash
source venv/bin/activate
python manage.py runserver
```

Tarayıcıda aç: **http://127.0.0.1:8000**

- **Taramayı Başlat**'a bas → ilerleme çubuğu dolar, satırlar canlı akar.
- Üstteki filtreler: hisse arama, rejim (Boğa/Ayı/Yatay), "sadece aksiyon
  sinyalleri", "sadece balina girişi".
- Sütun başlıklarına tıkla → sıralama.
- Bir satıra tıkla → detay paneli (seviyeler + stratejik yorum).

> Not: Veritabanı kullanılmaz; sonuçlar bellekte tutulur. Sunucu yeniden
> başlatılınca tekrar taramak gerekir. `migrate` çalıştırmaya gerek yoktur.

## Yapı

| Dosya | Görev |
|-------|-------|
| `terminal/analysis.py` | Hesaplama çekirdeği (`alansheen.py` mantığının JSON refactoru) |
| `terminal/scanner.py`  | Arka plan tarama + ilerleme durumu (thread + bellek) |
| `terminal/views.py`    | Sayfa + `/api/scan`, `/api/results`, `/api/stock/<symbol>` |
| `terminal/templates/`, `terminal/static/` | Koyu temalı frontend |
| `alansheen.py`         | Orijinal script (referans, dokunulmadı) |
