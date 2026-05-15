import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz", layout="wide")

st.title("📊 GME-AI: Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 Listesi (Hata payını azaltmak için ana kağıtlar)
bist_liste = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS",
    "YKBNK.IS", "EREGL.IS", "PGSUS.IS", "TCELL.IS", "ARCLK.IS", "TOASO.IS", "FROTO.IS", "ASTOR.IS", "SASA.IS", "KONTR.IS",
    "TUKAS.IS", "MIATK.IS", "EGEEN.IS", "DOAS.IS", "MGROS.IS", "PETKM.IS", "HALKB.IS", "VAKBN.IS", "ALARK.IS", "HEKTS.IS"
]

if st.button('🚀 ANALİZİ BAŞLAT'):
    with st.spinner('Veriler toplanıyor...'):
        sonuclar = []
        basarili_hisseler = []
        
        for h in bist_liste:
            try:
                t = yf.Ticker(h)
                df_g = t.history(period="2d")
                df_a = t.history(period="3d", interval="15m")
                
                if df_g.empty or df_a.empty or len(df_g) < 2:
                    continue
                
                anlik = df_a['Close'].iloc[-1]
                dun = df_g['Close'].iloc[-2]
                zirve = df_g['High'].iloc[-1]
                
                # RSI Hesaplama
                delta = df_a['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 1e-9))))

                # Strateji Rakamları
                alis = round(anlik * 0.998, 2)
                satis = round(anlik * 1.035, 2)
                
                if rsi < 38: sinyal = "🔥 AL"
                elif rsi > 72: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ TUT"

                h_adi = h.replace(".IS", "")
                if zirve >= satis:
                    basarili_hisseler.append(h_adi)

                sonuclar.append({
                    "HİSSE": h_adi,
                    "DÜNKÜ KAPAN": round(dun, 2),
                    "GÜNCEL FİYAT": round(anlik, 2),
                    "ALIŞ": alis,
                    "SATIŞ": satis,
                    "SİNYAL": sinyal
                })
            except:
                continue
        
        if sonuclar:
            # Tabloyu göster
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
            
            # Başarı Bölümü
            st.divider()
            toplam = len(sonuclar)
            oran = (len(basarili_hisseler) / toplam) * 100 if toplam > 0 else 0
            
            st.metric("📊 BAŞARI ORANI", f"%{round(oran, 2)}")
            st.success(f"Hedefi Vuranlar: {', '.join(basarili_hisseler)}")
        else:
            st.error("Veri çekilemedi, butona tekrar bas.")

st.sidebar.write("850 TL sermaye için sinyalleri izle.")
