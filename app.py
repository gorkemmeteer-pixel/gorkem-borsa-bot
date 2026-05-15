import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz Sistemi", layout="wide")

st.title("📊 GME-AI: BIST 100 Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 Tam Liste
bist_100 = [
    "AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFYE.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS", "ALFAS.IS",
    "ANSGR.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "ASUZU.IS", "AYDEM.IS", "BAGFS.IS", "BERA.IS", "BIENP.IS", "BIMAS.IS",
    "BIOEN.IS", "BOBET.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",
    "DOHOL.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
    "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GESAN.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IPEKE.IS",
    "ISCTR.IS", "ISGYO.IS", "ISMEN.IS", "IZENR.IS", "KARDM.IS", "KAYSE.IS", "KCHOL.IS", "KENT.IS", "KLSER.IS", "KONTR.IS",
    "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KSRAC.IS", "MAVI.IS", "MGROS.IS", "MIATK.IS", "ODAS.IS", "OTKAR.IS",
    "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "QUAGR.IS", "REEDR.IS", "SAHOL.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS",
    "SISE.IS", "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS", "TABGD.IS", "TAVHL.IS", "TCELL.IS", "THYAO.IS", "TKFEN.IS",
    "TMSN.IS", "TOASO.IS", "TSKB.IS", "TUKAS.IS", "TUPRS.IS", "TURSG.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS",
    "YEOTK.IS", "YKBNK.IS", "ZOREN.IS"
]

if st.button('🚀 100 HİSSEYİ ANALİZ ET'):
    with st.spinner('100 hisse taranıyor, bu işlem yaklaşık 30 saniye sürebilir...'):
        sonuclar = []
        basarili_isimler = []
        basarisiz_isimler = []
        
        for h in bist_100:
            try:
                t = yf.Ticker(h)
                df_g = t.history(period="2d")
                df_a = t.history(period="1d", interval="15m")
                
                if df_g.empty or df_a.empty or len(df_g) < 2:
                    continue
                
                guncel = df_a['Close'].iloc[-1]
                dun = df_g['Close'].iloc[-2]
                zirve = df_g['High'].iloc[-1]
                
                # RSI
                delta = df_a['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 1e-9))))

                alis = round(guncel * 0.998, 2)
                satis = round(guncel * 1.035, 2)
                
                if rsi < 38: sinyal = "🔥 AL"
                elif rsi > 72: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ TUT"

                h_adi = h.replace(".IS", "")
                if zirve >= satis:
                    durum = "✅ BAŞARILI"
                    basarili_isimler.append(h_adi)
                else:
                    durum = "⏳ BEKLEMEDE"
                    basarisiz_isimler.append(h_adi)

                sonuclar.append({
                    "HİSSE": h_adi,
                    "DÜNKÜ KAPAN": round(dun, 2),
                    "GÜNCEL FİYAT": round(guncel, 2),
                    "ALIŞ": alis,
                    "SATIŞ": satis,
                    "SİNYAL": sinyal,
                    "DURUM": durum
                })
            except:
                continue
        
        if sonuclar:
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
            
            st.divider()
            toplam = len(sonuclar)
            oran = (len(basarili_isimler) / toplam) * 100 if toplam > 0 else 0
            
            st.metric("📊 BIST 100 GENEL BAŞARI ORANI", f"%{round(oran, 2)}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.success(f"✅ BAŞARILI ({len(basarili_isimler)})")
                st.write(", ".join(basarili_isimler))
            with c2:
                st.error(f"⏳ BEKLEMEDE ({len(basarisiz_isimler)})")
                st.write(", ".join(basarisiz_isimler[:50]) + "...") # Çok uzun olmasın diye kısıtladım
        else:
            st.error("Veri bağlantısı kurulamadı. Tekrar dene.")

st.sidebar.write("850 TL ile 100 hisselik dev radar!")
