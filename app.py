import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

# TR Saati Ayarı (Güncellenmiş Hatalı Olmayan Versiyon)
def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME-AI Terminal", layout="wide")

st.title("🎖️ GME-AI: BIST 100 Komutanı")
st.write(f"Hoş geldin Görkem Mete! | ⏰ TR Saati: {tr_saati().strftime('%H:%M')}")

# Piyasayı sürükleyen en sağlam 100 hisse
bist_100_elit = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS",
    "YKBNK.IS", "EREGL.IS", "PGSUS.IS", "TCELL.IS", "ARCLK.IS", "TOASO.IS", "FROTO.IS", "ASTOR.IS", "SASA.IS", "KONTR.IS",
    "ALARK.IS", "HEKTS.IS", "PETKM.IS", "DOAS.IS", "ENKAI.IS", "MGROS.IS", "KARDM.IS", "AEFES.IS", "HALKB.IS", "VAKBN.IS",
    "DOHOL.IS", "TAVHL.IS", "GUBRF.IS", "KOZAL.IS", "SOKM.IS", "ULKER.IS", "CANTE.IS", "ENJSA.IS", "OYAKC.IS", "TKFEN.IS",
    "VESTL.IS", "EUPWR.IS", "MIATK.IS", "YEOTK.IS", "SMRTG.IS", "BRSAN.IS", "SDTTR.IS", "ALFAS.IS", "CWENE.IS", "GESAN.IS",
    "SAYAS.IS", "ZOREN.IS", "AGHOL.IS", "DOCO.IS", "MAVI.IS", "TUKAS.IS", "OTKAR.IS", "KORDS.IS", "TKNSA.IS", "LOGOS.IS",
    "TATGD.IS", "GOZDE.IS", "VAKKO.IS", "BRISA.IS", "CCOLA.IS", "TURSG.IS", "ANSGR.IS", "AKSA.IS", "BERA.IS", "QUAGR.IS",
    "KZBGY.IS", "SKBNK.IS", "TSKB.IS", "ISGYO.IS", "REEDR.IS", "TABGD.IS", "BORLS.IS", "EBEBK.IS", "KLSER.IS", "EGEEN.IS",
    "BRYAT.IS", "BMSCH.IS", "INVEO.IS", "SNGYO.IS", "ASUZU.IS", "TMSN.IS", "KMPUR.IS", "GENIL.IS", "ECILC.IS", "TRGYO.IS",
    "KAYSE.IS", "ENERY.IS", "BIOEN.IS", "CIMSA.IS", "AFYON.IS", "GWIND.IS", "AKFYE.IS", "AHGAZ.IS", "PENTA.IS", "TTKOM.IS"
]

if st.button('🚀 100 HİSSEYİ ANLIK TARA'):
    with st.spinner('Midas için elit fırsatlar süzülüyor...'):
        sonuclar = []
        for h in bist_100_elit:
            try:
                t = yf.Ticker(h)
                df = t.history(period="3d", interval="15m")
                if df.empty: continue
                fiyat = df['Close'].iloc[-1]
                
                # Karar Mantığı (RSI/Trend)
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]

                if rsi < 38: karar = "🔥 AL"
                elif rsi > 72: karar = "🚨 SAT"
                else: karar = "⚖️ TUT"

                sonuclar.append({
                    "HİSSE": h.replace(".IS", ""),
                    "FİYAT": round(fiyat, 2),
                    "HEDEF ALIM": round(fiyat * 0.985, 2),
                    "HEDEF SATIM": round(fiyat * 1.035, 2),
                    "DURUM": karar
                })
            except: continue
        
        st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
        st.success("Tarama Bitti! Bol Kazançlar Görkem!")

st.sidebar.info("Midas'ta işlem yapmadan önce buradan teyit al.")
