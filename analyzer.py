#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:14:54 2026

@author: simayarslan
"""

import pandas as pd


def analiz_olustur(df):
    tablolar = {}

    try:
        tablolar["G1_Kat_Fiyat"] = (
            df.groupby("Kategori")["Fiyat (TL)"].mean().round(2)
            .sort_values(ascending=False).reset_index()
            .rename(columns={"Fiyat (TL)": "Ort_Fiyat_TL"})
        )

        tablolar["G2_En_Yuksek_Puan"] = (
            df.groupby("Marka").filter(lambda x: len(x) >= 3)
            .groupby("Marka")["Puan"].mean().nlargest(10).round(2)
            .sort_values().reset_index()
            .rename(columns={"Puan": "Ort_Puan"})
        )

        tablolar["G3_Marka_Yorum"] = (
            df.dropna(subset=["Yorum Sayisi"])
            .groupby("Marka")["Yorum Sayisi"].mean().nlargest(10).round(0)
            .sort_values().reset_index()
            .rename(columns={"Yorum Sayisi": "Ort_Yorum"})
        )

        tablolar["G4_Kat_Ozet"] = (
            df.groupby("Kategori").agg(
                Urun_Sayisi =("Urun Adi",   "count"),
                Min_Fiyat   =("Fiyat (TL)", "min"),
                Ort_Fiyat   =("Fiyat (TL)", "mean"),
                Max_Fiyat   =("Fiyat (TL)", "max"),
                Ort_Puan    =("Puan",       "mean"),
            ).round(2).reset_index()
        )

        tablolar["G5_Fiyat_Segment"] = (
            df.assign(Segment=pd.cut(
                df["Fiyat (TL)"],
                bins  =[0, 200, 750, float("inf")],
                labels=["Ucuz (0-200 TL)", "Orta (200-750 TL)", "Pahali (750+ TL)"],
            ))
            .groupby("Segment", observed=True)
            .agg(
                Urun_Sayisi=("Urun Adi",    "count"),
                Ort_Fiyat  =("Fiyat (TL)",  "mean"),
                Ort_Puan   =("Puan",        "mean"),
                Ort_Yorum  =("Yorum Sayisi","mean"),
            ).round(2).reset_index()
        )

        tablolar["G6_Kat_Yorum"] = (
            df.dropna(subset=["Yorum Sayisi"])
            .groupby("Kategori")["Yorum Sayisi"].mean()
            .sort_values(ascending=False).round(0)
            .reset_index()
            .rename(columns={"Yorum Sayisi": "Ort_Yorum"})
        )

    except Exception as e:
        print(f"HATA: Analiz olusturulurken hata: {e}")

    return tablolar