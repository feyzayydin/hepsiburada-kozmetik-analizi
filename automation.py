#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:17:03 2026

@author: simayarslan
"""

import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))

from data_collector import veri_cek
from data_cleaner import veri_temizle
from analyzer import analiz_olustur
from excel_report import excel_raporu_olustur


def pipeline_calistir(csv_yol, excel_yol):
    print("=" * 50)
    print("  HEPSIBURADA KOZMETIK ANALIZI")
    print("=" * 50)

    # Verilerin çekilmesi
    tum_urunler = veri_cek(sayfa_sayisi=2)

    if not tum_urunler:
        print("HATA: Hic veri cekilemedi!")
        return

    # Çekilen verilerin temizlenmesi
    df = pd.DataFrame(tum_urunler)
    df = veri_temizle(df)

    if df.empty:
        print("UYARI: Temizleme sonrasi gecerli veri kalmadi.")
        return

    # Verileri CSV olarakkaydet
    try:
        df.to_csv(csv_yol, index=False, encoding="utf-8-sig")
        print(f"CSV kaydedildi: {csv_yol}")
    except PermissionError:
        print(f"HATA: '{csv_yol}' baska bir program tarafindan acik.")
    except Exception as e:
        print(f"HATA: CSV kaydedilirken hata: {e}")

    # Analiz tablolarını hazırla
    tablolar = analiz_olustur(df)

    # Excel raporunun oluşturulması
    try:
        excel_raporu_olustur(tablolar, csv_yol, excel_yol)
    except Exception:
        return

    print(f"\nTAMAMLANDI! {len(df)} urun kaydedildi.")