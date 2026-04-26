# 🛍️ Hepsiburada Kozmetik Analizi

Python ile Hepsiburada'dan kozmetik ürün verilerini otomatik olarak toplayan, temizleyen, analiz eden ve görselleştiren bir veri analizi projesi.

## 📌 Proje Hakkında

Bu proje, Hepsiburada'nın kozmetik kategorilerindeki ürünleri web scraping yöntemiyle toplayarak fiyat, puan ve yorum verilerini analiz etmektedir. Sonuçlar hem Excel raporu hem de interaktif Streamlit dashboard üzerinden sunulmaktadır.

## 🚀 Özellikler

- **Web Scraping** — Selenium ile Hepsiburada'dan otomatik veri toplama
- **Veri Temizleme** — Duplicate ve eksik verilerin temizlenmesi
- **Veri Analizi** — Kategori bazlı fiyat ortalamaları, en yüksek puanlı markalar
- **Excel Raporu** — Formatlı, grafikli Excel çıktısı (openpyxl)
- **Streamlit Dashboard** — İnteraktif web arayüzü ile görselleştirme

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|-----------|---------------|
| Python 3 | Ana programlama dili |
| Selenium | Web scraping |
| BeautifulSoup | HTML parsing |
| Pandas | Veri işleme |
| Streamlit | Dashboard |
| openpyxl | Excel raporu |
| Matplotlib / Seaborn | Görselleştirme |

## ⚙️ Kurulum

```bash
pip install selenium beautifulsoup4 pandas streamlit openpyxl matplotlib seaborn webdriver-manager
python main.py
streamlit run app.py
```

## 📊 Analiz Çıktıları

- Kategori bazlı ortalama fiyat karşılaştırması
- En yüksek puanlı markalar (Top 10)
- Marka bazlı yorum sayısı analizi

---
*Marmara Üniversitesi — Yönetim Bilişim Sistemleri | Veri Analizi Projesi*
