import streamlit as st
import json
import os

st.set_page_config(page_title="ÖSYM EKPSS Takip", page_icon="🎓")

st.title("🎓 ÖSYM EKPSS ve Engelli Duyuru Paneli")
st.write("Bu panel, Github Actions tarafından belirli aralıklarla çekilen duyuruları gösterir.")

VERI_DOSYASI = "osym_duyurular.json"

if os.path.exists(VERI_DOSYASI):
    with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
        duyurular = json.load(f)
    
    if duyurular:
        st.success(f"Sistemde toplam {len(duyurular)} EKPSS/Engelli duyurusu kayıtlı.")
        
        # En yeni duyurular en üstte olacak şekilde ters çeviriyoruz
        for link, baslik in reversed(list(duyurular.items())):
            st.markdown(f"🔹 **[{baslik}]({link})**")
    else:
        st.info("Veri dosyası mevcut ancak içinde EKPSS kriterlerine uygun duyuru bulunamadı.")
else:
    st.warning("Henüz duyuru verisi çekilmemiş. Arka plan botunun ilk taramasını yapmasını bekleyin.")

