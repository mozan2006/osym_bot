import time
import requests
from bs4 import BeautifulSoup
import json
import os

# --- AYARLAR ---
TELEGRAM_TOKEN = "BURAYA_BOT_TOKEN_GELECEK"
TELEGRAM_CHAT_ID = "BURAYA_CHAT_ID_GELECEK"
URL = "https://osym.gov.tr"
VERI_DOSYASI = "osym_duyurular.json"
KONTROL_PERIYODU = 1800  # 30 dakika

def telegram_mesaj_gonder(baslik, link):
    mesaj = f"🚨 <b>YENİ EKPSS DUYURUSU!</b> 🚨\n\n📌 <b>Başlık:</b> {baslik}\n🔗 <a href='{link}'>Detaya Git</a>"
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "HTML"
    }
    try:
        requests.post(api_url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def verileri_yukle():
    if os.path.exists(VERI_DOSYASI):
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}  # {link: baslik} şeklinde tutacağız

def verileri_kaydet(veri):
    with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

def duyurulari_kontrol_et():
    kayitli_duyurular = verileri_yukle()
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        duyuru_ögeleri = soup.find_all("a", class_="duyuru-link") or soup.find_all("a")
        yeni_duyuru_var_mi = False

        for öge in duyuru_ögeleri:
            baslik = öge.get_text(strip=True)
            link = öge.get("href")

            if not baslik or not link:
                continue

            if not link.startswith("http"):
                link = "https://osym.gov.tr" + link

            if "ekpss" in baslik.lower() or "engelli" in baslik.lower() or "kura" in baslik.lower():
                # Eğer yeni bir duyuruysa
                if link not in kayitli_duyurular:
                    print(f"\nYeni Duyuru: {baslik}")
                    
                    # Telegram'a gönder ve JSON'a kaydet
                    telegram_mesaj_gonder(baslik, link)
                    kayitli_duyurular[link] = baslik
                    yeni_duyuru_var_mi = True

        if yeni_duyuru_var_mi:
            verileri_kaydet(kayitli_duyurular)
        else:
            print(".", end="", flush=True)

    except Exception as e:
        print(f"\nHata oluştu: {e}")

print("ÖSYM Botu Başlatıldı...")
while True:
    duyurulari_kontrol_et()
    time.sleep(KONTROL_PERIYODU)

