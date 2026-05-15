import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

# 1. SAAT VE SAYFA AYARI
def tr_saati():
    return datetime.now(timezone.utc) + timedelta(hours=3)

st.set_page_config(page_title="GME Analiz Pro", layout="wide")

st.title("📊 GME-AI: 100 Hisse & Kâr Payı Analiz Sistemi")
st.write(f"Kullanıcı: Görkem Mete | ⏰ Güncel Saat: {tr_saati().strftime('%H:%M:%S')}")

# 2. BIST LİSTESİ (HATA VERMEMESİ İÇİN KONTROLLÜ LİSTE)
bist_liste = [
    "THYAO.IS", "TUPRS.IS", "ASELS.IS", "AKBNK.IS", "KCHOL.IS", "BIMAS.IS", "ISCTR.IS", "GARAN.IS", "SISE.IS", "SAHOL.IS",
    "YKBNK.IS", "EREGL.IS", "PGSUS.IS", "TCELL.IS", "ARCLK.IS", "TOASO.IS", "FROTO.IS", "ASTOR.IS", "SASA.IS", "KONTR.IS",
    "TUKAS.IS", "MIATK.IS", "EGEEN.IS", "DOAS.IS", "MGROS.IS", "PETKM.IS", "HALKB.IS", "VAKBN.IS", "ALARK.IS", "HEKTS.IS",
    "ENJSA.IS", "MAVI.IS", "OTKAR.IS", "VESTL.IS", "BRSAN.IS", "ALFAS.IS", "GESAN.IS", "SAYAS.IS", "ZOREN.IS", "AGHOL.IS",
    "DOCO.IS", "CWENE.IS", "EUPWR.IS", "YEOTK.IS", "SMRTG.IS", "BRYAT.IS", "KAYSE.IS", "ENERY.IS", "BIOEN.IS", "CIMSA.IS"
]

# 3. ANALİZ BUTONU
if st.button('🚀 SİSTEMİ ÇALIŞTIR'):
    with st.spinner('Piyasa taranıyor ve kâr payları hesaplanıyor...'):
        sonuclar = []
        basarili_isimler = []
        basarisiz_isimler = []
        
        for h in bist_liste:
            try:
                t = yf.Ticker(h)
                # Güvenli veri çekme (5 günlük geçmiş ve 15 dakikalık canlı veri)
                df_g = t.history(period="5d")
                
                if df_g.empty or len(df_g) < 2:
                    continue
                
                # Temettü Verimi (Kâr Payı)
                # 'dividendYield' bazen None döner, o yüzden 0'a çekiyoruz
                info = t.info
                dy = info.get('dividendYield', 0)
                kar_payi = f"%{round(dy * 100, 2)}" if dy else "%0.0"

                su_an = df_g['Close'].iloc[-1]
                dun = df_g['Close'].iloc[-2]
                zirve = df_g['High'].iloc[-1]
                
                # RSI GÖSTERGESİ (14 Günlük)
                delta = df_g['Close'].diff()
                up = delta.clip(lower=0)
                down = -1 * delta.clip(upper=0)
                ema_up = up.rolling(window=14).mean()
                ema_down = down.rolling(window=14).mean()
                rs = ema_up / (ema_down + 1e-10)
                rsi = 100 - (100 / (1 + rs.iloc[-1]))

                # HESAPLAMALAR
                alis_noktasi = round(su_an * 0.998, 2)
                hedef_satis = round(su_an * 1.035, 2) # %3.5 Kâr hedefi
                
                # SİNYAL MANTIĞI (TUT dememesi için aralıklar daraltıldı)
                if rsi < 42: sinyal = "🔥 AL"
                elif rsi > 62: sinyal = "🚨 SAT"
                else: sinyal = "⚖️ İZLE"

                h_adi = h.replace(".IS", "")
                
                # BAŞARI KONTROLÜ
                if zirve >= hedef_satis:
                    durum = "✅ BAŞARILI"
                    basarili_isimler.append(h_adi)
                else:
                    durum = "⏳ BEKLEMEDE"
                    basarisiz_isimler.append(h_adi)

                sonuclar.append({
                    "HİSSE": h_adi,
                    "GÜNCEL": round(su_an, 2),
                    "ALIŞ": alis_noktasi,
                    "HEDEF SATIŞ": hedef_satis,
                    "KÂR PAYI": kar_payi,
                    "SİNYAL": sinyal,
                    "DURUM": durum
                })
            except Exception:
                continue # Hata veren hisseyi geç, sistemi durdurma
        
        if sonuclar:
            # TABLO GÖSTERİMİ
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True)
            
            st.divider()
            
            # ÖZET METRİKLER
            toplam = len(sonuclar)
            basarili_sayi = len(basarili_isimler)
            oran = (basarili_sayi / toplam) * 100 if toplam > 0 else 0
            
            st.metric("📊 GÜNLÜK BAŞARI ORANI", f"%{round(oran, 2)}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"✅ HEDEFE ULAŞANLAR ({basarili_sayi})")
                st.write(", ".join(basarili_isimler))
            with col2:
                st.error(f"⏳ BEKLEYENLER ({len(basarisiz_isimler)})")
                st.write(", ".join(basarisiz_isimler[:30]) + "...")
        else:
            st.error("Veri bağlantısı kurulamadı. Lütfen butona tekrar bas.")

st.sidebar.info("850 TL bütçe ile '🔥 AL' verenlere odaklan.")
