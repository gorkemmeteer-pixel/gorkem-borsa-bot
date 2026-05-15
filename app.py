import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME-AI Skor Terminali", layout="wide")

st.title("🚀 GME-AI: Vur-Kaç Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ Güncel Saat: {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 Elit Liste
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
    with st.spinner('Kâr fırsatları taranıyor...'):
        sonuclar = []
        basarili_listesi = []
        beklemede_listesi = []
        
        for h in bist_100_elit:
            try:
                t = yf.Ticker(h)
                df_gunluk = t.history(period="1d")
                df_analiz = t.history(period="3d", interval="15m")
                
                if df_gunluk.empty or df_analiz.empty: continue
                
                anlik_fiyat = df_analiz['Close'].iloc[-1]
                gun_zirve = df_gunluk['High'].iloc[-1]
                
                # RSI Analizi
                delta = df_analiz['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]

                # Rakamlar
                h_satim = round(anlik_fiyat * 1.035, 2) # %3.5 kâr hedefi
                
                if rsi < 38: sinyal = "🔥 AL"
                elif rsi > 72: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ TUT"

                # Başarı Kontrolü
                hisse_adi = h.replace(".IS", "")
                if gun_zirve >= h_satim:
                    durum = "✅ BAŞARILI"
                    basarili_listesi.append(hisse_adi)
                else:
                    durum = "⏳ BEKLEMEDE"
                    beklemede_listesi.append(hisse_adi)

                sonuclar.append({
                    "HİSSE": hisse_adi,
                    "ANLIK FİYAT": round(anlik_fiyat, 2),
                    "HEDEF SATIŞ (%3.5)": h_satim,
                    "SİNYAL": sinyal,
                    "SONUÇ": durum
                })
            except: continue
        
        # Tablo Gösterimi
        st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
        
        # Başarı Oranı ve Detaylı Listeler
        st.divider()
        toplam = len(sonuclar)
        basarili_sayisi = len(basarili_listesi)
        oran = (basarili_sayisi / toplam) * 100 if toplam > 0 else 0
        
        st.metric("📊 GÜNLÜK HEDEF TUTTURMA ORANI", f"%{round(oran, 2)}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✅ HEDEFE ULAŞANLAR ({basarili_sayisi})")
            st.write(", ".join(basarili_listesi))
        with col2:
            st.error(f"⏳ BEKLEYENLER ({len(beklemede_listesi)})")
            st.write(", ".join(beklemede_listesi[:30]) + "...") # Çok uzun olmasın diye ilk 30'u basar

st.sidebar.info("850 TL ile 🔥 AL veren hisseleri takip et!")
