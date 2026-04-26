#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:14:20 2026

@author: simayarslan
"""

import pandas as pd


def veri_temizle(df):
    if df is None or df.empty:
        print("UYARI: Temizlenecek veri bulunamadi.")
        return pd.DataFrame()

    try:
        print(f"\nTemizleme oncesi: {len(df)} satir")
        df = df.drop_duplicates(subset=["Urun Adi"])
        df = df.dropna(subset=["Urun Adi", "Fiyat (TL)"])
        df = df[df["Fiyat (TL)"] > 0].reset_index(drop=True)
        print(f"Temizleme sonrasi: {len(df)} satir")
        return df
    except KeyError as e:
        print(f"HATA: Veri temizlenirken sutun bulunamadi: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"HATA: Veri temizlenirken beklenmeyen hata: {e}")
        return pd.DataFrame()