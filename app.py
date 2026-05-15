import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz", layout="wide")

st.title("📊 GME-AI: Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 Listesi
bist_100 = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS",
    "YKBNK.IS", "EREGL.IS", "PGSUS.IS", "TCELL.IS", "ARCLK.IS", "TOASO.IS", "FROTO.IS", "ASTOR.IS", "SASA.IS", "KONTR.IS",
    "TUKAS.IS", "MIATK.IS", "EGEEN.IS", "DOAS.IS", "MGROS.IS", "PETKM.IS", "HALKB.IS", "VAKBN.IS", "ALARK.IS", "HEKTS.IS"
]

if st.button('🚀 ANALİZİ BAŞLAT'):
    with st.spinner('Veriler çekiliyor...'):
        sonuclar = []
        basarili = []
        
        for h in bist_100:
            try:
                t = yf.Ticker(h)
                # Veri çekme hatasını engellemek için kontrol
                df_g = t.history(period="2d")
                df_a = t.history(period="3d", interval="15m")
                
                if df_g.empty or df_a.empty or len(df_g) < 2:
                    continue
                
                su_an = df_a['Close'].iloc[-1]
                dun = df_g['Close'].iloc[-2]
                zirve = df_g['High'].iloc[-1]
                
                # RSI Hesaplama
                delta = df_a['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs.iloc[-1]))

                # Strateji
                alis = round(su_an * 0.998, 2)
                satis = round(su_an * 1.035, 2)
                
                if rsi < 38: sinyal = "🔥 AL"
                elif rsi > 72: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ TUT"

                h_ad = h.replace(".IS", "")
                if zirve >= satis:
                    basarili.append(h_ad)

                sonuclar.append({
                    "HİSSE": h_ad,
                    "DÜNKÜ KAPAN": round(dun, 2),
                    "BUGÜNKÜ KAPAN": round(su_an, 2),
                    "ALIŞ": alis,
                    "SATIŞ": satis,
                    "SİNYAL": sinyal
                })
            except Exception as e:
                continue
        
        if sonuclar:
            df_final = pd.DataFrame(sonuclar)
            st.dataframe(df_final, use_container_width=True)
            
            st.divider()
            toplam = len(sonuclar)
            oran = (len(basarili) / toplam) * 100 if toplam > 0 else 0
            
            st.metric("BAŞARI ORANI", f"%{round(oran, 2)}")
            st.info(f"Hedefe Ulaşanlar: {', '.join(basarili)}")
        else:
            st.error("Şu an veri çekilemiyor, bağlantını kontrol edip tekrar dene.")

st.sidebar.write("850 TL bütçe ile analizleri takip et.")
