#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:18:16 2026

@author: simayarslan
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Kozmetik Analizi", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
CSV_YOL  = BASE_DIR / "kozmetik.csv"

# Temanın özelleştirilmesi

st.markdown("""
<style>
.stApp { background-color: #f8f9fb; }
div[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #e0e4ea;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
div[data-testid="metric-container"] label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #1f2937;
    font-size: 26px;
    font-weight: 700;
}
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e0e4ea;
}
</style>
""", unsafe_allow_html=True)

# Renk paletleri ve grafik stilleri

PALET      = ["#c2185b","#e91e8c","#f06292","#f48fb1","#fce4ec","#880e4f","#ad1457","#d81b60"]
PALET_MAVI = ["#1565c0","#1976d2","#1e88e5","#42a5f5","#90caf9","#bbdefb","#0d47a1","#1a237e"]
PALET_SET  = "Set2"


def grafik_stili():
    sns.set_theme(style="whitegrid", rc={
        "axes.spines.top"  : False,
        "axes.spines.right": False,
        "axes.grid.axis"   : "y",
        "grid.color"       : "#e5e7eb",
        "grid.linewidth"   : 0.8,
    })


def etiket_ekle_yatay(ax, fmt="{:.0f}"):
    for bar in ax.patches:
        deger = bar.get_width()
        if deger > 0:
            ax.text(
                deger + ax.get_xlim()[1] * 0.01,
                bar.get_y() + bar.get_height() / 2,
                fmt.format(deger),
                va="center", ha="left", fontsize=9, color="#374151",
            )


def etiket_ekle_dikey(ax, fmt="{:.0f}"):
    for bar in ax.patches:
        deger = bar.get_height()
        if deger > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                deger + ax.get_ylim()[1] * 0.01,
                fmt.format(deger),
                ha="center", va="bottom", fontsize=9, color="#374151",
            )


# Veri yükleme ve ön işleme

@st.cache_data
def veri_yukle():
    try:
        return pd.read_csv(CSV_YOL, encoding="utf-8-sig")
    except FileNotFoundError:
        st.error("HATA: 'kozmetik.csv' bulunamadı. Önce main.py'i çalıştırın.")
        return None
    except Exception as e:
        st.error(f"HATA: Veri yüklenirken hata oluştu: {e}")
        return None


df = veri_yukle()
if df is None:
    st.stop()

# Sidebarın hazırlanması ve filtreler

st.sidebar.markdown("## Hepsiburada Kozmetik Analizi")
st.sidebar.markdown(
    "Hepsiburada'dan çekilen kozmetik ürün verilerinin "
    "kategori, marka, fiyat ve yorum bazlı analizi."
)
st.sidebar.divider()
st.sidebar.header("Filtreler")

kategoriler  = sorted(df["Kategori"].dropna().unique().tolist())
secilen      = st.sidebar.multiselect("Kategori", kategoriler, default=kategoriler)

fiyat_min, fiyat_max = float(df["Fiyat (TL)"].min()), float(df["Fiyat (TL)"].max())
fiyat_aralik = st.sidebar.slider("Fiyat Aralığı (TL)", fiyat_min, fiyat_max,
                                  (fiyat_min, fiyat_max))
st.sidebar.divider()
st.sidebar.caption("WI2034 OOP Projesi")

try:
    df_f = df[
        df["Kategori"].isin(secilen) &
        df["Fiyat (TL)"].between(*fiyat_aralik)
    ].copy()
except Exception as e:
    st.error(f"HATA: Filtreleme sırasında hata oluştu: {e}")
    st.stop()

if df_f.empty:
    st.warning("Seçilen filtrelerle eşleşen ürün bulunamadı.")
    st.stop()

# Uygulama başlığı ve genel bilgiler

st.title("Hepsiburada Kozmetik Ürün Analizi")
st.caption(f"Toplam {len(df_f):,} ürün analiz ediliyor.")
st.divider()

grafik_stili()

# Sekmelerin oluşturulması

sekme1, sekme2, sekme3, sekme4 = st.tabs([
    "Genel Bakış",
    "Fiyat Analizi",
    "Marka ve Puan",
    "Yorum Analizi",
])

# Sekme 1 — Genel bakış var bu ekranda ham veri ve temel metrikler gösterilecek

with sekme1:
    col1, col2, col3, col4 = st.columns(4)
    try:
        col1.metric("Toplam Ürün",  f"{len(df_f):,}")
        col2.metric("Ort. Fiyat",   f"{df_f['Fiyat (TL)'].mean():,.0f} TL")
        col3.metric("Ort. Puan",    f"{df_f['Puan'].mean():.2f} / 5")
        col4.metric("Toplam Marka", f"{df_f['Marka'].nunique():,}")
    except Exception as e:
        st.error(f"HATA: Metrikler hesaplanamadı: {e}")

    st.divider()
    with st.expander("Ham Veriyi Görüntüle"):
        st.dataframe(df_f, use_container_width=True)

# Sekme 2 — Fiyat analizi var, kategorilere göre fiyat analizi ve segmentlere göre fiyat ve puan analizi olacak

with sekme2:
    st.subheader("Kategoriye Göre Ortalama Fiyat")
    try:
        veri = df_f.groupby("Kategori")["Fiyat (TL)"].mean().sort_values(ascending=False).round(0)
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(x=veri.index, y=veri.values, palette=PALET, ax=ax)
        etiket_ekle_dikey(ax, "{:.0f} TL")
        ax.set_xlabel("")
        ax.set_ylabel("Ortalama Fiyat (TL)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption(f"En yüksek ortalama fiyat: {veri.index[0]} | En düşük: {veri.index[-1]}")
    except Exception as e:
        st.error(f"HATA: Grafik oluşturulamadı: {e}")

    st.divider()

    st.subheader("Kategori Bazlı Özet Tablo")
    try:
        ozet = df_f.groupby("Kategori").agg(
            Urun_Sayisi=("Urun Adi",   "count"),
            Min_Fiyat  =("Fiyat (TL)", "min"),
            Ort_Fiyat  =("Fiyat (TL)", "mean"),
            Max_Fiyat  =("Fiyat (TL)", "max"),
            Ort_Puan   =("Puan",       "mean"),
        ).round(2).reset_index()
        st.dataframe(ozet, use_container_width=True, hide_index=True)
        st.caption("Her kategorinin minimum, ortalama ve maksimum fiyat değerleri ile ortalama puanı.")
    except Exception as e:
        st.error(f"HATA: Tablo oluşturulamadı: {e}")

    st.divider()

    st.subheader("Fiyat Segmentine Göre Karşılaştırma")
    try:
        segment_df = df_f.copy()
        segment_df["Segment"] = pd.cut(
            segment_df["Fiyat (TL)"],
            bins  =[0, 200, 750, float("inf")],
            labels=["Ucuz (0-200 TL)", "Orta (200-750 TL)", "Pahalı (750+ TL)"],
        )
        segment = (
            segment_df.groupby("Segment", observed=True)
            .agg(Ort_Puan=("Puan", "mean"), Ort_Yorum=("Yorum Sayisi", "mean"))
            .round(2).reset_index()
        )
        if segment.empty:
            st.warning("Yeterli veri bulunamadı.")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                fig, ax = plt.subplots(figsize=(5, 4))
                sns.barplot(data=segment, x="Segment", y="Ort_Puan", palette=PALET[:3], ax=ax)
                etiket_ekle_dikey(ax, "{:.2f}")
                ax.set_title("Segment - Ortalama Puan", fontweight="bold")
                ax.set_xlabel("")
                ax.set_ylabel("Ort. Puan")
                ax.set_ylim(0, 5.5)
                plt.xticks(fontsize=8)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            with col_b:
                fig, ax = plt.subplots(figsize=(5, 4))
                sns.barplot(data=segment, x="Segment", y="Ort_Yorum", palette=PALET_MAVI[:3], ax=ax)
                etiket_ekle_dikey(ax, "{:.0f}")
                ax.set_title("Segment - Ortalama Yorum Sayısı", fontweight="bold")
                ax.set_xlabel("")
                ax.set_ylabel("Ort. Yorum Sayısı")
                plt.xticks(fontsize=8)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            st.caption("Ucuz, orta ve pahalı segmentlerin ortalama puan ve yorum yoğunluğu karşılaştırması.")
    except Exception as e:
        st.error(f"HATA: Grafik oluşturulamadı: {e}")

# Sekme 3 — Marka ve puan analizi var, en yüksek puanlı 10 marka ve marka başına ortalama yorum sayısı analizleri olacak

with sekme3:
    st.subheader("En Yüksek Puanlı 10 Marka")
    try:
        veri = (
            df_f.groupby("Marka").filter(lambda x: len(x) >= 3)
            .groupby("Marka")["Puan"].mean()
            .nlargest(10).round(2).sort_values()
        )
        if veri.empty:
            st.warning("Yeterli marka verisi bulunamadı.")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=veri.values, y=veri.index, palette="YlOrRd", ax=ax)
            etiket_ekle_yatay(ax, "{:.2f}")
            ax.set_xlabel("Ortalama Puan")
            ax.set_xlim(0, 5.8)
            ax.set_ylabel("")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.caption(f"En az 3 ürüne sahip markalar arasında en yüksek puan: {veri.index[-1]} ({veri.values[-1]:.2f} / 5)")
    except Exception as e:
        st.error(f"HATA: Grafik oluşturulamadı: {e}")

    st.divider()

    st.subheader("Marka Başına Ortalama Yorum Sayısı (Top 10)")
    try:
        veri = (
            df_f.dropna(subset=["Yorum Sayisi"])
            .groupby("Marka")["Yorum Sayisi"].mean()
            .nlargest(10).round(0).sort_values()
        )
        if veri.empty:
            st.warning("Yorum verisi bulunamadı.")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=veri.values, y=veri.index, palette=PALET_MAVI, ax=ax)
            etiket_ekle_yatay(ax, "{:.0f}")
            ax.set_xlabel("Ortalama Yorum Sayısı")
            ax.set_ylabel("")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.caption(f"En yüksek ortalama yorum sayısına sahip marka: {veri.index[-1]} ({int(veri.values[-1]):,} yorum)")
    except Exception as e:
        st.error(f"HATA: Grafik oluşturulamadı: {e}")

# Sekme 4 — Yorum analizi var, kategorilere göre ortalama yorum sayısı ve en çok yorum alan ürünler olacak

with sekme4:
    st.subheader("Kategoriye Göre Ortalama Yorum Sayısı")
    try:
        veri = (
            df_f.dropna(subset=["Yorum Sayisi"])
            .groupby("Kategori")["Yorum Sayisi"]
            .mean().sort_values(ascending=False).round(0)
        )
        if veri.empty:
            st.warning("Yorum verisi bulunamadı.")
        else:
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(x=veri.index, y=veri.values, palette=PALET_SET, ax=ax)
            etiket_ekle_dikey(ax, "{:.0f}")
            ax.set_xlabel("")
            ax.set_ylabel("Ortalama Yorum Sayısı")
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
            plt.xticks(rotation=20, ha="right")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.caption(f"En çok yorum alan kategori: {veri.index[0]} | En az: {veri.index[-1]}")
    except Exception as e:
        st.error(f"HATA: Grafik oluşturulamadı: {e}")

st.divider()
st.caption("Veri kaynağı: hepsiburada.com | WI2034 OOP Projesi")