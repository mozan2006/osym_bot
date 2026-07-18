import requests
from bs4 import BeautifulSoup
import json
import os

# --- GITHUB SECRETS'TEN BİLGİLERİ ALIYORUZ ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

URL = "https://osym.gov.tr"
VERI_DOSYASI = "osym_duyurular.json"

def telegram_mesaj_gonder(baslik, link):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram kimlik bilgileri eksik, mesaj gönderilemedi.")
        return
        
    mesaj = f"🚨 <b>YENİ EKPSS DUYURUSU!</b> 🚨\n\n📌 <b>Başlık:</b> {baslik}\n🔗 <a href='{link}'>Detaya Git</a>"
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "HTML"
    }
    requests.post(api_url, data=payload, timeout=10)

def main():
    # Eski verileri oku
    kayitli_duyurular = {}
    if os.path.exists(VERI_DOSYASI):
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            kayitli_duyurular = json.load(f)
            
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    duyuru_ögeleri = soup.find_all("a", class_="duyuru-link") or soup.find_all("a")
    yeni_duyuru_var_mi = False

    for öge in duyuru_ögeleri:
        baslik = öge.get_text(strip=True)
        link = öge.get("href")

        if not baslik or not link: continue
        if not link.startswith("http"): link = "https://osym.gov.tr" + link

        if "ekpss" in baslik.lower() or "engelli" in baslik.lower() or "kura" in baslik.lower():
            if link not in kayitli_duyurular:
                print(f"Yeni Duyuru Bulundu: {baslik}")
                telegram_mesaj_gonder(baslik, link)
                kayitli_duyurular[link] = baslik
                yeni_duyuru_var_mi = True

    # Eğer yeni bir şey bulduysa JSON'ı güncelle
    if yeni_duyuru_var_mi:
        with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(kayitli_duyurular, f, ensure_ascii=False, indent=4)
        print("Veriler güncellendi ve kaydedildi.")
    else:
        print("Yeni duyuru bulunamadı.")

if __name__ == "__main__":
    main()
