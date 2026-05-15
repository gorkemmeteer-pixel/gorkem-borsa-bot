import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

# TR Saati Ayarı
def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME-AI Pro Terminal", layout="wide")

st.title("🎖️ GME-AI: BIST 100 Komutanı (Pro Test)")
st.write(f"Komuta Merkezi: Görkem Mete | ⏰ Seans Saati: {tr_saati().strftime('%H:%M:%S')}")

# Portföyündeki ve takibindeki elit liste
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

if st.button('🚀 TÜM LİSTEYİ TEST ET VE TARA'):
    with st.spinner('Yapay zeka dünkü verilerle bugünü kıyaslıyor...'):
        sonuclar = []
        basari_sayaci = 0
        
        for h in bist_100_elit:
            try:
                t = yf.Ticker(h)
                # Hem dünkü hem bugünkü veriyi çek
                df = t.history(period="5d", interval="15m")
                if df.empty: continue
                
                fiyat = df['Close'].iloc[-1]
                onceki_kapanis = t.history(period="2d")['Close'].iloc[-2]
                gunluk_degisim = ((fiyat - onceki_kapanis) / onceki_kapanis) * 100
                
                # RSI Analizi
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]

                if rsi < 38: 
                    karar = "🔥 AL"
                    basari_sayaci += 1
                elif rsi > 72: karar = "🚨 SAT"
                else: karar = "⚖️ TUT"

                sonuclar.append({
                    "HİSSE": h.replace(".IS", ""),
                    "ANLIK FİYAT": round(fiyat, 2),
                    "GÜNLÜK %": f"%{round(gunluk_degisim, 2)}",
                    "HEDEF SATIM": round(fiyat * 1.035, 2),
                    "DURUM": karar,
                    "GÜÇ": "Yüksek" if rsi < 30 or rsi > 75 else "Orta"
                })
            except: continue
        
        df_sonuc = pd.DataFrame(sonuclar)
        st.dataframe(df_sonuc, use_container_width=True)
        
        # Test Özeti Paneli
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Taranan Hisse", len(sonuclar))
        col2.metric("Fırsat Sayısı (AL)", basari_sayaci)
        col3.metric("Borsa Yönü", "⬆️ Pozitif" if gunluk_degisim > 0 else "⬇️ Negatif")
        
        st.success(f"Görkem, şu an {basari_sayaci} hissede 'Düşüş Bitti, Yükseliş Yakın' sinyali var. Bu rakamları bugün seans sonuna kadar takip et!")

st.sidebar.warning("⚠️ NOT: Bu terminal sadece teknik analiz yapar. Önemli haberleri (KAP bildirimi gibi) mutlaka kontrol et.")
