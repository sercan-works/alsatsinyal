"""BIST algo hesaplama çekirdeği.

`alansheen.py` içindeki matematiksel mantığın birebir korunmuş, ancak terminale
basmak yerine JSON-uyumlu sözlükler döndüren refactor'u. Frontend bu sözlükleri
renkli badge / seviye haritası olarak gösterir.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

# Haziran 2026 Güncellenmiş BIST Listesi (alansheen.py'den)
HISSELER = [
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
    "ZEDUR.IS", "ZRGYO.IS",
]

# Strateji etiketleri (frontend renk eşlemesi için "kod" + görsel "label")
NEUTRAL_STRATEGY = "IZLE"


def _f(value):
    """JSON-güvenli float: NaN / Inf -> None."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """yfinance MultiIndex sütunlarını tek seviyeye indir."""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = df.columns.get_level_values(0)
    return df


def _rsi_from_close(close: pd.Series, period: int = 14) -> float:
    delta = close.diff().values.flatten()
    gains = np.where(delta > 0, delta, 0)
    losses = np.where(delta < 0, -delta, 0)
    gain = np.mean(gains[-period:])
    loss = np.mean(losses[-period:])
    return 100 - (100 / (1 + (gain / (loss + 1e-10))))


def analyze_dataframe(symbol: str, df: pd.DataFrame) -> dict | None:
    """Tek hissenin tarama metriklerini hesaplar (alansheen.py:58-134 mantığı).

    Yeterli veri yoksa (< 150 bar) ya da hata olursa None döner.
    """
    if df is None or df.empty:
        return None

    df = _normalize_columns(df)
    needed = ["Open", "High", "Low", "Close", "Volume"]
    if not all(col in df.columns for col in needed):
        return None
    df = df.dropna(subset=needed)
    if len(df) < 150:
        return None

    c = df["Close"].values.flatten()
    h = df["High"].values.flatten()
    l = df["Low"].values.flatten()
    v = df["Volume"].values.flatten()

    guncel_fiyat = float(c[-1])

    # --- 1. KURUMSAL REJİM FİLTRESİ ---
    if len(df) >= 200:
        ma200_series = df["Close"].rolling(window=200).mean().values.flatten()
    else:
        ma200_series = df["Close"].rolling(window=100).mean().values.flatten()
    ma50_series = df["Close"].rolling(window=50).mean().values.flatten()

    ma200 = ma200_series[-1]
    ma50 = ma50_series[-1]

    if guncel_fiyat > ma200 and ma50 > ma200:
        regime, regime_label, is_bull = "BOGA", "🟢 BOĞA", True
    elif guncel_fiyat < ma200 and ma50 < ma200:
        regime, regime_label, is_bull = "AYI", "🔴 AYI", False
    else:
        regime, regime_label, is_bull = "YATAY", "🟡 YATAY", None

    # --- 2. PARKINSON VOLATİLİTE MODELİ ---
    log_hl = np.log(h[-20:] / l[-20:])
    parkinson_vol = np.sqrt((1 / (4 * np.log(2))) * np.mean(log_hl ** 2))
    vol_buffer = guncel_fiyat * parkinson_vol * 1.5

    # --- 3. HARMONİK PİVOT + DESTEK/DİRENÇ HARİTASI ---
    prev_h, prev_l, prev_c = float(h[-2]), float(l[-2]), float(c[-2])
    pivot = (prev_h + prev_l + prev_c) / 3.0
    r1 = (2 * pivot) - prev_l
    s1 = (2 * pivot) - prev_h
    r2 = pivot + (prev_h - prev_l)
    s2 = pivot - (prev_h - prev_l)

    # --- 4. INSTITUTIONAL VOLUME Z-SCORE ---
    v_mean = np.mean(v[-21:-1])
    v_std = np.std(v[-21:-1]) + 1e-10
    volume_zscore = (v[-1] - v_mean) / v_std
    if volume_zscore > 1.645:
        hacim, hacim_label = "BALINA", "⚡ BALİNA GİRİŞ"
    else:
        hacim, hacim_label = "KUCUK", "💤 KÜÇÜK YAT."

    # --- 5. RSI + AKSİYON MATRİSİ ---
    rsi = _rsi_from_close(df["Close"])

    strategy = NEUTRAL_STRATEGY
    strategy_label = "İZLE / NÖTR"
    stop_loss = guncel_fiyat - vol_buffer
    yorum = ""

    if is_bull:
        if volume_zscore > 1.645 and guncel_fiyat >= np.max(c[-21:-1]):
            strategy, strategy_label = "KIRILIM_AL", "🚀 KIRILIM AL"
            stop_loss = guncel_fiyat - (vol_buffer * 0.8)
            yorum = (
                f"Ana trend BOĞA. Güçlü balina hacmiyle direnç kırıldı. "
                f"{guncel_fiyat:.2f} üzerinden momentum hızlanabilir. Stop: {stop_loss:.2f}"
            )
        elif rsi < 38 and guncel_fiyat <= pivot:
            strategy, strategy_label = "PUSU_AL", "🎯 PUSU AL"
            stop_loss = pivot - vol_buffer
            yorum = (
                f"Yükselen trendde sağlıklı düzeltme. İlk alım tepki bölgesi olan "
                f"{s1:.2f} ve Pivot {pivot:.2f} kademeli pusu alanı."
            )
        else:
            strategy, strategy_label = "TRENDI_KORU", "📈 TRENDİ KORU"
            yorum = (
                f"Yükselen ana trend gücünü koruyor. {s1:.2f} ana desteği üzerinde "
                f"kaldığı sürece pozisyonlar orta vade taşınabilir."
            )
    elif is_bull is False:
        if guncel_fiyat <= np.min(c[-21:-1]):
            strategy, strategy_label = "TABAN_RISKI", "💀 TABAN RİSKİ"
            stop_loss = guncel_fiyat + vol_buffer
            yorum = (
                f"Net AYI piyasası. Destekler kırılıyor, yeni dip arayışı aktif. "
                f"{s2:.2f} seviyesine kadar alım yapmak yüksek risk taşır."
            )
        elif rsi > 65:
            strategy, strategy_label = "KACIS", "❌ KAÇIŞ/SAT"
            stop_loss = guncel_fiyat + (vol_buffer * 0.5)
            yorum = (
                f"Düşüş trendinde geçici tepki yükselişi. RSI şişti. "
                f"{r1:.2f} ve {r2:.2f} dirençleri mal boşaltma ve nakde geçiş yeridir."
            )
        else:
            strategy, strategy_label = "ZAYIF_TREND", "🚨 ZAYIF TREND"
            yorum = (
                f"Fiyat hareketli ortalamaların altında eziliyor. {pivot:.2f} direnci "
                f"aşılmadıkça nakitte kalıp izlemek en güvenli aksiyondur."
            )
    else:
        if rsi < 35:
            strategy, strategy_label = "TEPKI_ALIMI", "🛒 TEPKİ ALIMI"
            yorum = (
                f"Yatay bantta konsolide oluyor. RSI aşırı satımda. {s1:.2f} desteğinden "
                f"gelebilecek tepki yükselişi tradable durumdadır."
            )
        else:
            strategy, strategy_label = "KONSOLIDE", "⚖️ KONSOLİDE"
            yorum = (
                f"Belirli bir fiyat aralığında akümülasyon (mal toplama) evresi. "
                f"{s1:.2f} - {r1:.2f} bandı arası git-gel ticareti uygundur."
            )

    return {
        "symbol": symbol.replace(".IS", ""),
        "ticker": symbol,
        "fiyat": _f(guncel_fiyat),
        "regime": regime,
        "regime_label": regime_label,
        "is_bull": is_bull,
        "ma50": _f(ma50),
        "ma200": _f(ma200),
        "parkinson_vol": _f(parkinson_vol),
        "vol_buffer": _f(vol_buffer),
        "pivot": _f(pivot),
        "r1": _f(r1),
        "r2": _f(r2),
        "s1": _f(s1),
        "s2": _f(s2),
        "volume_zscore": _f(volume_zscore),
        "hacim": hacim,
        "hacim_label": hacim_label,
        "rsi": _f(rsi),
        "strategy": strategy,
        "strategy_label": strategy_label,
        # "Aktif sinyal" = doğrudan alım fırsatı (her hisse artık bir strateji alır).
        "is_action": strategy in ("KIRILIM_AL", "PUSU_AL", "TEPKI_ALIMI"),
        "stop_loss": _f(stop_loss),
        "yorum": yorum,
        "lot": None,  # scanner._fetch_lot tarafından doldurulur
    }


def detailed_analysis(symbol: str, df: pd.DataFrame) -> dict | None:
    """Tek hisse için detaylı destek/direnç + stratejik yorum.

    `alansheen.py:142-219`'daki YEOTK panosunun herhangi bir hisseye
    genelleştirilmiş hali. Detay drawer'ı bunu kullanır.
    """
    if df is None or df.empty:
        return None

    df = _normalize_columns(df)
    needed = ["Open", "High", "Low", "Close", "Volume"]
    if not all(col in df.columns for col in needed):
        return None
    df = df.dropna(subset=needed)
    if len(df) < 2:
        return None

    yc = df["Close"].values.flatten()
    yh = df["High"].values.flatten()
    yl = df["Low"].values.flatten()
    yv = df["Volume"].values.flatten()

    yfiyat = float(yc[-1])
    yma50 = np.mean(yc[-50:]) if len(yc) >= 50 else np.mean(yc)
    yma200 = np.mean(yc[-200:]) if len(yc) >= 200 else np.mean(yc[-100:]) if len(yc) >= 100 else np.mean(yc)

    # Fibonacci / Pivot seviyeleri
    ph, pl, pc = float(yh[-2]), float(yl[-2]), float(yc[-2])
    ypivot = (ph + pl + pc) / 3.0
    r1 = (2 * ypivot) - pl
    s1 = (2 * ypivot) - ph
    r2 = ypivot + (ph - pl)
    s2 = ypivot - (ph - pl)

    # Hacim
    yv_mean = np.mean(yv[-20:]) if len(yv) >= 20 else np.mean(yv)
    yhacim_oran = yv[-1] / (yv_mean + 1e-10)

    yrsi = _rsi_from_close(df["Close"])

    # Stratejik yorum (alansheen.py:199-219)
    yorum = []
    if yfiyat > yma50 and yma50 > yma200:
        rejim = "BOGA"
        if yrsi < 40:
            yorum.append(f"{symbol.replace('.IS','')} ana trendi BOĞA rejiminde fakat kısa vadede aşırı satılmış durumda.")
            yorum.append(f"AL-SAT STRATEJİSİ: {s1:.2f} kademeli alım için ideal pusu bölgesi. Momentum pozitif.")
        elif yrsi > 70:
            yorum.append("Trend güçlü fakat RSI aşırı alım (şişme) bölgesine girmiş.")
            yorum.append(f"AL-SAT STRATEJİSİ: {r1:.2f} ve {r2:.2f} dirençlerinde kar realizasyonu düşünülebilir. Yeni alım riskli.")
        else:
            yorum.append("Sağlıklı yükselen trend korunuyor. Kurumsal para tahtayı destekliyor.")
            yorum.append(f"AL-SAT STRATEJİSİ: Taşımaya devam. {s1:.2f} TL üzerinde kaldıkça yön yukarı.")
    elif yfiyat < yma50 and yma50 < yma200:
        rejim = "AYI"
        if yrsi < 30:
            yorum.append("Tahta net bir AYI rejiminde fakat tepki yükselişi kapıda (Aşırı Satım).")
            yorum.append(f"AL-SAT STRATEJİSİ: Sadece dipten tepki oynamak isteyenler {s2:.2f} stoplu deneyebilir. Kalıcı alım için erken.")
        else:
            yorum.append("Negatif baskı sürüyor, fiyat hareketli ortalamaların altında eziliyor.")
            yorum.append(f"AL-SAT STRATEJİSİ: NAKİTTE KAL / İZLE. {ypivot:.2f} aşılmadan mala girilmemeli.")
    else:
        rejim = "YATAY"
        yorum.append(f"{symbol.replace('.IS','')} yatay konsolidasyon (mal toplama/dağıtma) evresinde.")
        yorum.append(f"AL-SAT STRATEJİSİ: {s1:.2f} seviyesinden al, {r1:.2f} seviyesinde sat şeklinde range ticareti uygundur.")

    return {
        "symbol": symbol.replace(".IS", ""),
        "ticker": symbol,
        "fiyat": _f(yfiyat),
        "ma50": _f(yma50),
        "ma200": _f(yma200),
        "rsi": _f(yrsi),
        "hacim_oran": _f(yhacim_oran),
        "rejim": rejim,
        "levels": {
            "r2": _f(r2),
            "r1": _f(r1),
            "pivot": _f(ypivot),
            "s1": _f(s1),
            "s2": _f(s2),
        },
        "yorum": yorum,
    }
