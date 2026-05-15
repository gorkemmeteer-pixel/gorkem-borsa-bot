import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME-AI Analiz", layout="wide")

st.title("📊 GME-AI: BIST 100 Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ Güncel Saat: {tr_saati().strftime('%H:%M:%S')}")

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

if st.button('🚀 ANALİZİ BAŞLAT'):
    with st.spinner('Veriler analiz ediliyor...'):
        sonuclar = []
        basarili_listesi = []
        basarisiz_listesi = []
        
        for h in bist_100_elit:
            try:
                t = yf.Ticker(h)
                df_gunluk = t.history(period="1d")
                df_analiz = t.history(period="3d", interval="15m")
                
                if df_gunluk.empty or df_analiz.empty: continue
                
                fiyat = df_analiz['Close'].iloc[-1]
                zirve = df_gunluk['High'].iloc[-1]
                
                delta = df_analiz['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]

                # %3.5 Kar Hedefi
                h_sat = fiyat * 1.035
                
                if zirve >= h_sat:
                    durum = "✅ BAŞARILI"
                    basarili_listesi.append(h.replace(".IS", ""))
                else:
                    durum = "⏳ BEKLEMEDE"
                    basarisiz_listesi.append(h.replace(".IS", ""))

                if rsi < 38: sinyal = "🔥 AL"
                elif rsi > 72: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ TUT"

                sonuclar.append({
                    "HİSSE": h.replace(".IS", ""),
                    "ŞU AN": round(fiyat, 3), # Kuruş hassasiyeti için 3 yaptık
                    "HEDEF SATIM": round(h_sat, 3),
                    "GÜNÜN ZİRVESİ": round(zirve, 3),
                    "SİNYAL": sinyal,
                    "DURUM": durum
                })
            except: continue
        
        st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
        st.divider()
        toplam = len(basarili_listesi) + len(basarisiz_listesi)
        oran = (len(basarili_listesi) / toplam) * 100 if toplam > 0 else 0
        st.metric("📊 GÜNLÜK BAŞARI ORANI", f"%{round(oran, 2)}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.success(f"✅ Başarılı ({len(basarili_listesi)})")
            st.write(", ".join(basarili_listesi))
        with c2:
            st.error(f"⏳ Bekleyen ({len(basarisiz_listesi)})")
            st.write(", ".join(basarisiz_listesi[:15]))
