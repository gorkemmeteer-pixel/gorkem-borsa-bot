import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz Pro", layout="wide")

st.title("📊 GME-AI: 100 Hisse & Kâr Payı Analizi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 Listesi
bist_100 = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS",
    "YKBNK.IS", "EREGL.IS", "PGSUS.IS", "TCELL.IS", "ARCLK.IS", "TOASO.IS", "FROTO.IS", "ASTOR.IS", "SASA.IS", "KONTR.IS",
    "TUKAS.IS", "MIATK.IS", "EGEEN.IS", "DOAS.IS", "MGROS.IS", "PETKM.IS", "HALKB.IS", "VAKBN.IS", "ALARK.IS", "HEKTS.IS",
    "ENJSA.IS", "DOCO.IS", "MAVI.IS", "OTKAR.IS", "VESTL.IS", "BRSAN.IS", "ALFAS.IS", "GESAN.IS", "SAYAS.IS", "ZOREN.IS"
] # Örnek olarak 40 tane bıraktım, hepsini ekleyebilirsin.

if st.button('🚀 ANALİZİ PATLAT'):
    with st.spinner('100 Hisse ve Temettü verileri taranıyor...'):
        sonuclar = []
        basarili_isimler = []
        
        for h in bist_100:
            try:
                t = yf.Ticker(h)
                df_g = t.history(period="2d")
                df_a = t.history(period="1d", interval="15m")
                
                if df_g.empty or df_a.empty: continue
                
                # Temettü (Kâr Payı) Verimi
                info = t.info
                kar_payi = info.get('dividendYield', 0)
                if kar_payi is None: kar_payi = 0
                kar_payi_yuzde = f"%{round(kar_payi * 100, 2)}"

                guncel = df_a['Close'].iloc[-1]
                dun = df_g['Close'].iloc[-2]
                zirve = df_g['High'].iloc[-1]
                
                # RSI Hassasiyeti (TUT dememesi için aralıkları daralttık)
                delta = df_a['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 1e-9))))

                alis = round(guncel * 0.998, 2)
                satis = round(guncel * 1.035, 2)
                
                # Sinyal Mantığı Güncellendi
                if rsi < 45: sinyal = "🔥 AL"
                elif rsi > 65: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ İZLE"

                h_adi = h.replace(".IS", "")
                durum = "✅ BAŞARILI" if zirve >= satis else "⏳ BEKLEMEDE"
                if zirve >= satis: basarili_isimler.append(h_adi)

                sonuclar.append({
                    "HİSSE": h_adi,
                    "GÜNCEL": round(guncel, 2),
                    "ALIŞ": alis,
                    "SATIŞ": satis,
                    "KÂR PAYI": kar_payi_yuzde,
                    "SİNYAL": sinyal,
                    "DURUM": durum
                })
            except: continue
        
        if sonuclar:
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
            st.divider()
            st.metric("BAŞARI ORANI", f"%{round((len(basarili_isimler)/len(sonuclar))*100, 2)}")
            st.success(f"Hedefi Vuranlar: {', '.join(basarili_isimler)}")
        else:
            st.error("Veri çekilemedi.")
