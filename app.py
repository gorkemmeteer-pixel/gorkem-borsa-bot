import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

# Saat ayarı
def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz", layout="wide")

st.title("📊 GME-AI: Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 Elit Liste (Error vermemesi için en stabil kağıtlar)
bist_liste = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", 
    "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS", "YKBNK.IS", "EREGL.IS", 
    "PGSUS.IS", "TCELL.IS", "ASTOR.IS", "SASA.IS", "TUKAS.IS", "MIATK.IS"
]

if st.button('🚀 ANALİZİ BAŞLAT'):
    with st.spinner('Piyasa taranıyor...'):
        sonuclar = []
        basarili_isimler = []
        beklemede_isimler = []
        
        for h in bist_liste:
            try:
                # Veriyi güvenli çekme
                t = yf.Ticker(h)
                df_g = t.history(period="2d")
                df_a = t.history(period="1d", interval="15m")
                
                if df_g.empty or df_a.empty or len(df_g) < 2:
                    continue
                
                guncel = df_a['Close'].iloc[-1]
                dun_kapanis = df_g['Close'].iloc[-2]
                gun_zirve = df_g['High'].iloc[-1]
                
                # Basit RSI Hesaplama (Error korumalı)
                delta = df_a['Close'].diff()
                up = delta.clip(lower=0)
                down = -1 * delta.clip(upper=0)
                ema_up = up.rolling(window=14).mean()
                ema_down = down.rolling(window=14).mean()
                rs = ema_up / (ema_down + 1e-10)
                rsi = 100 - (100 / (1 + rs.iloc[-1]))

                # Strateji
                alis = round(guncel * 0.998, 2)
                satis = round(guncel * 1.035, 2)
                
                if rsi < 38: sinyal = "🔥 AL"
                elif rsi > 72: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ TUT"

                h_adi = h.replace(".IS", "")
                if gun_zirve >= satis:
                    durum = "✅ BAŞARILI"
                    basarili_isimler.append(h_adi)
                else:
                    durum = "⏳ BEKLEMEDE"
                    beklemede_isimler.append(h_adi)

                sonuclar.append({
                    "HİSSE": h_adi,
                    "DÜNKÜ KAPAN": round(dun_kapanis, 2),
                    "GÜNCEL FİYAT": round(guncel, 2),
                    "ALIŞ": alis,
                    "SATIŞ": satis,
                    "SİNYAL": sinyal,
                    "DURUM": durum
                })
            except Exception:
                continue
        
        if sonuclar:
            # Tablo
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
            
            # Başarı Özeti
            st.divider()
            toplam = len(sonuclar)
            oran = (len(basarili_isimler) / toplam) * 100 if toplam > 0 else 0
            
            st.metric("📊 GENEL BAŞARI ORANI", f"%{round(oran, 2)}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.success(f"✅ BAŞARILI ({len(basarili_isimler)})")
                st.write(", ".join(basarili_isimler) if basarili_isimler else "Henüz yok.")
            with c2:
                st.error(f"⏳ BEKLEMEDE ({len(beklemede_isimler)})")
                st.write(", ".join(beklemede_isimler) if beklemede_isimler else "Hepsi başarılı!")
        else:
            st.error("Veri çekilemedi. Lütfen sayfayı yenileyip tekrar dene.")

st.sidebar.write("850 TL bütçe ile takiptesin.")
