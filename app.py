import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME BIST 100", layout="wide")

st.title("📊 GME-AI: BIST 100 Tam Analiz")
st.write(f"Kullanıcı: Görkem Mete | ⏰ {tr_saati().strftime('%H:%M:%S')}")

# BIST 100 TAM LİSTE (100 HİSSE)
bist_full = [
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

if st.button('🚀 100 HİSSEYİ TARAMAYI BAŞLAT'):
    with st.spinner('BIST 100 radarı çalışıyor...'):
        sonuclar = []
        basarili = []
        beklemede = []
        
        for h in bist_full:
            try:
                t = yf.Ticker(h)
                # Hata almamak için sadece 2 günlük veriyi tek seferde çekiyoruz
                hist = t.history(period="2d")
                if hist.empty or len(hist) < 2: continue

                # Temettü Verimi
                dy = t.info.get('dividendYield', 0)
                temettu = f"%{round(dy * 100, 2)}" if dy else "%0.0"

                su_an = hist['Close'].iloc[-1]
                zirve = hist['High'].iloc[-1]
                
                # RSI Basitleştirilmiş (Hız için)
                delta = hist['Close'].diff()
                rsi_val = 50 # Veri yetersizse nötr kalsın
                if len(delta) > 1:
                    gain = delta.where(delta > 0, 0).mean()
                    loss = -delta.where(delta < 0, 0).mean()
                    if loss > 0:
                        rs = gain / loss
                        rsi_val = 100 - (100 / (1 + rs))

                alis = round(su_an * 0.998, 2)
                satis = round(su_an * 1.035, 2)
                h_ad = h.replace(".IS", "")

                # Sinyal & Başarı
                if rsi_val < 40: sinyal = "🔥 AL"
                elif rsi_val > 65: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ İZLE"

                if zirve >= satis:
                    durum = "✅ BAŞARILI"
                    basarili.append(h_ad)
                else:
                    durum = "⏳ BEKLEMEDE"
                    beklemede.append(h_ad)

                sonuclar.append({
                    "HİSSE": h_ad,
                    "GÜNCEL": round(su_an, 2),
                    "ALIŞ": alis,
                    "HEDEF SATIŞ": satis,
                    "KÂR PAYI": temettu,
                    "SİNYAL": sinyal,
                    "DURUM": durum
                })
            except: continue

        if sonuclar:
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
            st.divider()
            st.metric("📊 TOPLAM TARANAN", len(sonuclar))
            st.success(f"✅ Başarılı Olanlar: {', '.join(basarili)}")
            st.error(f"⏳ Beklemede Olanlar: {', '.join(beklemede[:30])}...")
        else:
            st.error("Bağlantı koptu, tekrar dene.")

st.sidebar.info("850 TL sermaye ile sinyal bekle!")
