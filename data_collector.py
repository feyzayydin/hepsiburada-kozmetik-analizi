#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:11:52 2026

@author: simayarslan
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time


KATEGORILER = {
    "Makyaj"        : "https://www.hepsiburada.com/makyaj-urunleri-c-341425",
    "Cilt Bakim"    : "https://www.hepsiburada.com/cilt-bakim-urunleri-c-32000005",
    "Gunes Bakim"   : "https://www.hepsiburada.com/gunes-koruyucu-urunler-c-32010889",
    "Parfum"        : "https://www.hepsiburada.com/parfumler-c-341406",
    "Sac Bakim"     : "https://www.hepsiburada.com/sac-bakim-urunleri-c-26012111",
    "Tiras Urunleri": "https://www.hepsiburada.com/erkek-tiras-urunleri-c-26012116",
    "Agiz Bakim"    : "https://www.hepsiburada.com/agiz-bakim-urunleri-c-26012110",
}


def tarayici_baslat():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0.0.0")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        print("Tarayici baslatildi.")
        return driver
    except ValueError:
        print("HATA: Tarayici seceneklerinde gecersiz bir deger var.")
        return None
    except Exception as e:
        print(f"HATA: Tarayici baslatılamadi: {e}")
        return None


def sayfayi_kaydir(driver):
    try:
        son = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            yeni = driver.execute_script("return document.body.scrollHeight")
            if yeni == son:
                break
            son = yeni
    except Exception as e:
        print(f"  HATA: Sayfa kaydirilamamdi: {e}")


def urun_cikart(kart, kategori):
    try:
        ad_tag = kart.select_one("h3, span[class*='title'], a[class*='title']")
        if not ad_tag:
            return None
        ad = ad_tag.get_text(strip=True)
        if not ad:
            return None

        fiyat_tag = kart.select_one("span[class*='price'], div[class*='price'], ins")
        if not fiyat_tag:
            return None
        fiyat_ham = fiyat_tag.get_text(strip=True)
        eslesme = re.search(r"[\d.,]+", fiyat_ham.replace("\xa0", ""))
        if not eslesme:
            return None

        try:
            fiyat = float(eslesme.group().replace(".", "").replace(",", "."))
        except ValueError:
            print(f"  HATA: Fiyat sayiya donusturulemedi: '{eslesme.group()}'")
            return None

        if fiyat <= 0:
            return None

        marka = ad.split()[0] if ad else None

        puan = None
        puan_tag = kart.select_one("span[class*='rating'], span[class*='score']")
        if puan_tag:
            try:
                puan = float(puan_tag.get_text(strip=True).replace(",", "."))
                if not (0 <= puan <= 5):
                    puan = None
            except ValueError:
                puan = None

        yorum = None
        yorum_tag = kart.select_one("span[class*='review'], span[class*='count']")
        if yorum_tag:
            temiz = re.sub(r"[^\d]", "", yorum_tag.get_text(strip=True))
            try:
                yorum = int(temiz) if temiz else None
            except ValueError:
                yorum = None

        link = None
        link_tag = kart.select_one("a[href]")
        if link_tag:
            href = link_tag.get("href", "")
            link = href if href.startswith("http") else "https://www.hepsiburada.com" + href

        return {
            "Kategori"    : kategori,
            "Urun Adi"    : ad,
            "Marka"       : marka,
            "Fiyat (TL)"  : fiyat,
            "Puan"        : puan,
            "Yorum Sayisi": yorum,
            "Link"        : link,
        }

    except Exception as e:
        print(f"  HATA: Kart islenirken beklenmeyen hata: {e}")
        return None


def veri_cek(sayfa_sayisi=2):
    driver = tarayici_baslat()
    if driver is None:
        return []

    tum_urunler = []
    try:
        for kategori, url in KATEGORILER.items():
            print(f"\n[{kategori}] cekiliyor...")
            for sayfa in range(1, sayfa_sayisi + 1):
                sayfa_url = url if sayfa == 1 else f"{url}?sayfa={sayfa}"
                print(f"  Sayfa {sayfa} yukleniyor...")
                try:
                    driver.get(sayfa_url)
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(3)
                    sayfayi_kaydir(driver)

                    soup    = BeautifulSoup(driver.page_source, "html.parser")
                    kartlar = soup.select(
                        "li[class*='productListContent'], "
                        "div[class*='ProductCard'], "
                        "div[class*='product-card']"
                    )

                    if not kartlar:
                        print(f"  Sayfa {sayfa}: urun bulunamadi.")
                        break

                    for kart in kartlar:
                        urun = urun_cikart(kart, kategori)
                        if urun:
                            tum_urunler.append(urun)

                    print(f"  Sayfa {sayfa}: {len(kartlar)} kart | Toplam: {len(tum_urunler)} urun")
                    time.sleep(2)

                except Exception as e:
                    print(f"  HATA: Sayfa {sayfa} yuklenirken hata: {e}")
                    continue

    finally:
        driver.quit()
        print("\n(Sistem Mesaji: Tarayici baglantisi guvenle kapatildi.)")

    return tum_urunler