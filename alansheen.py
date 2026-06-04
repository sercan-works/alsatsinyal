import pandas as pd
import yfinance as yf
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Haziran 2026 Güncellenmiş BIST Listesi
hisseler = [
    "A1CAP.IS", "ACSEL.IS", "ADEL.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", 
    "AGROT.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", 
    "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", 
    "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALTNY.IS", "ALVES.IS", "ANELE.IS", "ANGEN.IS", "ANHYT.IS", 
    "ANSGR.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ARTMS.IS", 
    "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAKP.IS", "AVPGY.IS", "AYDEM.IS", 
    "AYCES.IS", "AYGAZ.IS", "AZTEK.IS", "BANVT.IS", "BARMA.IS", "BEGYO.IS", 
    "BERA.IS", "BFREN.IS", "BIENY.IS", "BIGCH.IS", "BIMAS.IS", "BIOEN.IS", "BIZIM.IS", "BOBET.IS", 
    "BORSK.IS", "BOSSA.IS", "BRISA.IS", "BRKVY.IS", "BRSAN.IS", "BRYAT.IS", "BSOKE.IS", 
    "BTCIM.IS", "BUCIM.IS", "BVSAN.IS", "BYDNR.IS", "CANTE.IS", "CATES.IS", "CCOLA.IS", "CEMAS.IS", 
    "CEMTS.IS", "CMENT.IS", "CONSE.IS", "CVKMD.IS", "CWENE.IS", "DAPGM.IS", "DARDL.IS", "DGGYO.IS", 
    "DGNMO.IS", "DOAS.IS", "DOCO.IS", "DOHOL.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDATA.IS", 
    "EGEEN.IS", "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EKGYO.IS", "EKOS.IS", "ELITE.IS", "ENERY.IS", 
    "ENJSA.IS", "ENKAI.IS", "ERBOS.IS", "EREGL.IS", "ESCAR.IS", "ESCOM.IS", "ESEN.IS", "EUPWR.IS", 
    "EUREN.IS", "EYGYO.IS", "FADE.IS", "FENER.IS", "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORTE.IS", 
    "FROTO.IS", "GARAN.IS", "GENTS.IS", "GESAN.IS", "GIPTA.IS", "GLYHO.IS", "GOKNR.IS", "GOLTS.IS", 
    "GOODY.IS", "GOZDE.IS", "GRSEL.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", 
    "HEKTS.IS", "HKTM.IS", "HLGYO.IS", "HTTBT.IS", "HUNER.IS", "IHAAS.IS", "IMASM.IS", 
    "INDES.IS", "INFO.IS", "INGRM.IS", "ISCTR.IS", "ISGYO.IS", "ISMEN.IS", "IZENR.IS", 
    "IZMDC.IS", "JANTS.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KFEIN.IS", 
    "KLGYO.IS", "KLMSN.IS", "KLSER.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", 
    "KRVGD.IS", "KTLEV.IS", "KTSKR.IS", "KUTPO.IS", "KUYAS.IS", "KZBGY.IS", 
    "LIDER.IS", "LINK.IS", "LKMNH.IS", "LMKDC.IS", "LOGO.IS", "MACKO.IS", "MAGEN.IS", "MAVI.IS", 
    "MEDTR.IS", "MEGMT.IS", "MIATK.IS", "MNDRS.IS", "MOBTL.IS", "MOGAN.IS", "MPARK.IS", 
    "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "NATEN.IS", "NETAS.IS", "NTGAZ.IS", "NUHCM.IS", "OBAMS.IS", 
    "OBASE.IS", "ODAS.IS", "OFSYM.IS", "ONCSM.IS", "ORGE.IS", "OTKAR.IS", "OYAKC.IS", "OZATD.IS", 
    "OZKGY.IS", "PEKGY.IS", "PENTA.IS", "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PLTUR.IS", 
    "PNSUT.IS", "POLHO.IS", "QUAGR.IS", "REEDR.IS", "RYSAS.IS", "RYGYO.IS", "SAHOL.IS", 
    "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SELEC.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", 
    "SMART.IS", "SMRTG.IS", "SNGYO.IS", "SNICA.IS", "SUWEN.IS", "TABGD.IS", "TARKM.IS", 
    "TATGD.IS", "TAVHL.IS", "TCELL.IS", "TEZOL.IS", "THYAO.IS", "TLMAN.IS", "TMSN.IS", "TOASO.IS", 
    "TSKB.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "TUREX.IS", "TURSG.IS", "ULKER.IS", 
    "ULUFA.IS", "UNLU.IS", "VAKBN.IS", "VAKKO.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS", "VESBE.IS", 
    "VESTL.IS", "VKGYO.IS", "VRGYO.IS", "YATAS.IS", "YEOTK.IS", "YKBNK.IS", "YUNSA.IS", "YYLGD.IS", 
    "ZEDUR.IS", "ZRGYO.IS"
]

print("🏛️ KURUMSAL ALGO TERMİNALİ v4.3 (GÜNCEL SÜRÜM)")
print("🔒 Model: Parkinson Volatilitesi & Kurumsal Hacim Güven Sınırı Süzgeci\n")

print(f"{'HİSSE':<10} | {'ANLIK':<8} | {'PİYASA YÖNÜ':<11} | {'HACİM GÜCÜ':<13} | {'ALGO STRATEJİSİ':<23} | {'DENGE/PİVOT':<11} | {'MUTLAK STOP'}")
print("-" * 115)

for hisse in hisseler:
    try:
        df = yf.download(hisse, period="1y", interval="1d", progress=False)
        if df.empty or len(df) < 150:
            continue
            
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        df.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
        
        c = df['Close'].values.flatten()
        h = df['High'].values.flatten()
        l = df['Low'].values.flatten()
        v = df['Volume'].values.flatten()
        
        guncel_fiyat = float(c[-1])
        
        # --- 1. KURUMSAL REJİM FİLTRESİ ---
        ma200_series = df['Close'].rolling(window=200).mean().values.flatten() if len(df) >= 200 else df['Close'].rolling(window=100).mean().values.flatten()
        ma50_series = df['Close'].rolling(window=50).mean().values.flatten()
        
        ma200 = ma200_series[-1]
        ma50 = ma50_series[-1]
        
        if guncel_fiyat > ma200 and ma50 > ma200:
            regime = "🟢 BOĞA"
            is_bull = True
        elif guncel_fiyat < ma200 and ma50 < ma200:
            regime = "🔴 AYI"
            is_bull = False
        else:
            regime = "🟡 YATAY"
            is_bull = None

        # --- 2. PARKINSON VOLATİLİTE MODELİ ---
        log_hl = np.log(h[-20:] / l[-20:])
        parkinson_vol = np.sqrt((1 / (4 * np.log(2))) * np.mean(log_hl ** 2))
        vol_buffer = guncel_fiyat * parkinson_vol * 1.5 
        
        # --- 3. HARMONİK PİVOT HARİTASI ---
        prev_h, prev_l, prev_c = float(h[-2]), float(l[-2]), float(c[-2])
        pivot = (prev_h + prev_l + prev_c) / 3.0
        
        # --- 4. INSTITUTIONAL VOLUME Z-SCORE ---
        v_mean = np.mean(v[-21:-1])
        v_std = np.std(v[-21:-1]) + 1e-10
        volume_zscore = (v[-1] - v_mean) / v_std
        
        hacim_etiket = "⚡ BALİNA GİRİŞ" if volume_zscore > 1.645 else "💤 KÜÇÜK YAT."

        # --- 5. İNDİKATÖR SENTEZİ VE AKSİYON MATRİSİ ---
        delta = df['Close'].diff().values.flatten()
        gains = np.where(delta > 0, delta, 0)
        losses = np.where(delta < 0, -delta, 0)
        
        gain = np.mean(gains[-14:])
        loss = np.mean(losses[-14:])
        rsi = 100 - (100 / (1 + (gain / (loss + 1e-10))))

        strategy = "İZLE / NÖTR"
        stop_loss = guncel_fiyat - vol_buffer
        
        if is_bull:
            if volume_zscore > 1.645 and guncel_fiyat >= np.max(c[-21:-1]):
                strategy = "🚀 HACİMLİ KIRILIM AL"
                stop_loss = guncel_fiyat - (vol_buffer * 0.8)
            elif rsi < 38 and guncel_fiyat <= pivot:
                strategy = "🎯 DESTEKTEN PUSU AL"
                stop_loss = pivot - vol_buffer
        elif is_bull is False:
            if guncel_fiyat <= np.min(c[-21:-1]):
                strategy = "💀 TEHLİKE TABAN RİSKİ"
                stop_loss = guncel_fiyat + vol_buffer
            elif rsi > 65:
                strategy = "❌ MAL BOŞALTMA/KAÇIŞ"
                stop_loss = guncel_fiyat + (vol_buffer * 0.5)

        if strategy == "İZLE / NÖTR":
            continue
            
        hisse_clean = hisse.replace('.IS', '')
        print(f"{hisse_clean:<10} | {guncel_fiyat:<8.2f} | {regime:<11} | {hacim_etiket:<13} | {strategy:<23} | {pivot:<11.2f} | {stop_loss:.2f}")
        
    except:
        continue

print("\n🎯 Akıllı Süzgeç Çalışmayı Bitirdi.")
print("=" * 115)

# ==========================================
# REZERV ALAN: YEOTK ÖZEL ANALİZ PANELİ
# ==========================================
try:
    print("\n🔍 [ÖZEL ANALİZ PANOSU] >> YEOTK (YEO TEKNOLOJİ)")
    print("-" * 60)
    yeo = yf.download("YEOTK.IS", period="1y", interval="1d", progress=False)
    if isinstance(yeo.columns, pd.MultiIndex):
        yeo.columns = yeo.columns.get_level_values(0)
    
    yeo.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
    
    yc = yeo['Close'].values.flatten()
    yh = yeo['High'].values.flatten()
    yl = yeo['Low'].values.flatten()
    yv = yeo['Volume'].values.flatten()
    
    yfiyat = float(yc[-1])
    
    # Matematiksel Hesaplamalar
    yma50 = np.mean(yc[-50:])
    yma200 = np.mean(yc[-200:]) if len(yc) >= 200 else np.mean(yc[-100:])
    
    # Fibonacci / Pivot Seviyeleri (Destek-Direnç Haritası)
    ph, pl, pc = float(yh[-2]), float(yl[-2]), float(yc[-2])
    ypivot = (ph + pl + pc) / 3.0
    r1 = (2 * ypivot) - pl
    s1 = (2 * ypivot) - ph
    r2 = ypivot + (ph - pl)
    s2 = ypivot - (ph - pl)
    
    # Hacim ve Güç Analizi
    yv_mean = np.mean(yv[-20:])
    yhacim_oran = yv[-1] / (yv_mean + 1e-10)
    
    # RSI Hesaplama
    ydelta = yeo['Close'].diff().values.flatten()
    ygains = np.where(ydelta > 0, ydelta, 0)
    ylosses = np.where(ydelta < 0, -ydelta, 0)
    yrsi = 100 - (100 / (1 + (np.mean(ygains[-14:]) / (np.mean(ylosses[-14:]) + 1e-10))))

    # Ekrana Yazdırma Bloğu
    print(f"• Güncel Fiyat       : {yfiyat:.2f} TL")
    print(f"• 50 Günlük Ortalaması: {yma50:.2f} TL")
    print(f"• 200 Günlük Ortalaması: {yma200:.2f} TL")
    print(f"• Anlık RSI Değeri   : {yrsi:.2f}")
    print(f"• 20 Günlük Ort. Hacim Katı: {yhacim_oran:.2f}x")
    print("-" * 60)
    print(f"🚨 KRİTİK SEVİYELER:")
    print(f"   [Direnç-2] {r2:.2f} TL (Güçlü Satış Bölgesi)")
    print(f"   [Direnç-1] {r1:.2f} TL (Ara Pivot Direnci)")
    print(f"   [PİVOT]    {ypivot:.2f} TL (Denge Eşiği)")
    print(f"   [Destek-1] {s1:.2f} TL (İlk Alım Tepki Noktası)")
    print(f"   [Destek-2] {s2:.2f} TL (Majör Koruma / Kesin Stop)")
    print("-" * 60)
    
    # Algoritmik Strateji Yorumu
    print("📈 STRATEJİK YORUM VE AKSİYON PLANI:")
    if yfiyat > yma50 and yma50 > yma200:
        if yrsi < 40:
            print(" >> YEOTK ana trendi BOĞA rejiminde fakat kısa vadede aşırı satılmış durumda.")
            print(f" >> AL-SAT STRATEJİSİ: {s1:.2f} kademeli alım için ideal pusu bölgesi. Momentum pozitif.")
        elif yrsi > 70:
            print(" >> Trend güçlü fakat RSI aşırı alım (şişme) bölgesine girmiş.")
            print(f" >> AL-SAT STRATEJİSİ: {r1:.2f} ve {r2:.2f} dirençlerinde kar realizasyonu düşünülebilir. Yeni alım riskli.")
        else:
            print(" >> Sağlıklı yükselen trend korunuyor. Kurumsal para tahtayı destekliyor.")
            print(f" >> AL-SAT STRATEJİSİ: Taşımaya devam. {s1:.2f} TL üzerinde kaldıkça yön yukarı.")
    elif yfiyat < yma50 and yma50 < yma200:
        if yrsi < 30:
            print(" >> Tahta net bir AYI rejiminde fakat tepki yükselişi kapıda (Aşırı Satım).")
            print(f" >> AL-SAT STRATEJİSİ: Sadece dipten tepki oynamak isteyenler {s2:.2f} stoplu deneyebilir. Kalıcı alım için erken.")
        else:
            print(" >> Negatif baskı sürüyor, fiyat hareketli ortalamaların altında eziliyor.")
            print(f" >> AL-SAT STRATEJİSİ: NAKİTTE KAL / İZLE. {ypivot:.2f} aşılmadan mala girilmemeli.")
    else:
        print(" >> YEOTK yatay konsolidasyon (mal toplama/dağıtma) evresinde.")
        print(f" >> AL-SAT STRATEJİSİ: {s1:.2f} seviyesinden al, {r1:.2f} seviyesinde sat şeklinde range ticareti uygundur.")
        
except Exception as e:
    print(f"⚠️ YEOTK analizi yapılırken bir hata oluştu: {e}")
print("=" * 115)