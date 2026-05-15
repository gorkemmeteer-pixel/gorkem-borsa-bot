import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz Sistemi", layout="wide")

st.title("📊 GME-AI: Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ {tr_saati().strftime('%H:%M:%S')}")

# BIST Listesi
bist_liste = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS",
    "YKBNK.IS", "EREGL.IS", "PGSUS.IS", "TCELL.IS", "ARCLK.IS", "TOASO.IS", "FROTO.IS", "ASTOR.IS", "SASA.IS", "KONTR.IS",
    "TUKAS.IS", "MIATK.IS", "EGEEN.IS", "DOAS.IS", "MGROS.IS", "PETKM.IS", "HALKB.IS", "VAKBN.IS", "ALARK.IS", "HEKTS.IS"
]

if st.button('🚀 ANALİZİ BAŞLAT'):
    with st.spinner('Piyasa
