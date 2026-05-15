import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME-AI Analiz", layout="wide")
st.title("📊 GME-AI: BIST 100 Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 Listesi (Kısaltılmış Örnek)
bist_listesi = ["THYAO.IS", "TUPRS.IS", "ASELS.IS", "ASTOR.IS", "AKBNK.IS", "YKBNK.IS", "SASA.IS", "TUKAS.IS", "EREGL.IS", "KCHOL.IS"]

if st.button('🚀 ANALİZİ BAŞLAT'):
    with st.spinner('Analiz ediliyor...'):
        sonuclar = []
        for h in bist_listesi:
            try:
                t = yf.Ticker(h)
                df_analiz = t.history(period="3d", interval="15m")
                df_gunluk = t.history(period="1d")
                if df_analiz.empty: continue
                
                fiyat = df_analiz['Close'].iloc[-1]
                zirve = df_gunluk['High'].iloc[-1]
                
                # RSI
                delta = df_analiz['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]

                # Strateji Rakamları
                alim_noktasi = round(fiyat * 0.995, 2) # Fiyatın %0.5 altı ideal alım
                hedef_sat = round(fiyat * 1.035, 2)    # %3.5 kâr
                
                if rsi < 38: sinyal = "🔥 AL"
                elif rsi > 72: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ TUT"

                durum = "✅ BAŞARILI" if zirve >= hedef_sat else "⏳ BEKLEMEDE"

                sonuclar.append({
                    "HİSSE": h.replace(".IS", ""),
                    "ŞU AN": round(fiyat, 2),
                    "ALIM SEVİYESİ": alim_noktasi,
                    "HEDEF SATIM": hedef_sat,
                    "SİNYAL": sinyal,
                    "DURUM": durum
                })
            except: continue
        
        st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
        st.info("💡 850 TL ile 'AL' sinyali verenlerden sepet yapabilirsin.")
