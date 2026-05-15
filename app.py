import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz", layout="wide")

st.title("📊 GME-AI: Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | {tr_saati().strftime('%H:%M:%S')}")

bist_100_elit = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS",
    "YKBNK.IS", "EREGL.IS", "PGSUS.IS", "TCELL.IS", "ARCLK.IS", "TOASO.IS", "FROTO.IS", "ASTOR.IS", "SASA.IS", "KONTR.IS",
    "ALARK.IS", "HEKTS.IS", "PETKM.IS", "DOAS.IS", "
