"""Arka plan tarama yöneticisi.

Tüm BIST listesini yfinance ile gruplar halinde indirir, her hisseyi
`analysis.analyze_dataframe` ile işler ve sonuçları bellekte (thread-safe)
tutar. Frontend `/api/results`'ı poll'layarak ilerlemeyi ve gelen satırları
canlı görür. Veritabanı kullanılmaz; sunucu yeniden başlayınca durum sıfırlanır.
"""
from __future__ import annotations

import threading
import time

import yfinance as yf

from . import analysis

_BATCH_SIZE = 40

_lock = threading.Lock()
_thread: threading.Thread | None = None

# Toplam lot (sharesOutstanding) cache'i. Lot/float nadiren değişir; sunucu
# ömrü boyunca tutulur, böylece her taramada tekrar tekrar çekilmez.
_lot_cache: dict[str, float | None] = {}


def _fetch_lot(ticker: str) -> float | None:
    """Hissenin toplam lot (sharesOutstanding) değerini döndürür.

    Önce cache'e bakar; yoksa hızlı `fast_info`, olmazsa `.info` fallback dener.
    Veri yoksa/başarısızsa None döner — hisse ASLA atlanmaz. Başarılı sonuç
    (None dahil değil) cache'lenir.
    """
    if ticker in _lot_cache:
        return _lot_cache[ticker]

    lot: float | None = None
    try:
        tk = yf.Ticker(ticker)
        # fast_info hızlıdır ve genelde 'shares' alanını taşır.
        try:
            shares = tk.fast_info.get("shares") if hasattr(tk.fast_info, "get") else None
        except Exception:
            shares = None
        if not shares:
            shares = tk.info.get("sharesOutstanding")
        if shares:
            lot = float(shares)
    except Exception:
        lot = None

    if lot is not None:
        _lot_cache[ticker] = lot  # yalnızca geçerli değeri kalıcı cache'le
    return lot

_state = {
    "status": "idle",          # idle | running | done | error
    "progress": {"done": 0, "total": len(analysis.HISSELER)},
    "results": [],
    "started_at": None,
    "finished_at": None,
    "error": None,
}


def get_state() -> dict:
    """Durumun JSON-güvenli kopyasını döndürür."""
    with _lock:
        return {
            "status": _state["status"],
            "progress": dict(_state["progress"]),
            "results": list(_state["results"]),
            "started_at": _state["started_at"],
            "finished_at": _state["finished_at"],
            "error": _state["error"],
        }


def _extract_single(batch_df, ticker):
    """Toplu indirilen DataFrame'den tek tickerin alt-çerçevesini çıkar."""
    try:
        # group_by="ticker" => üst seviye sütun = ticker
        if hasattr(batch_df, "columns") and ticker in batch_df.columns.get_level_values(0):
            return batch_df[ticker]
    except Exception:
        pass
    return None


def _run_scan():
    tickers = analysis.HISSELER
    try:
        for start in range(0, len(tickers), _BATCH_SIZE):
            with _lock:
                if _state["status"] != "running":
                    return  # iptal
            grup = tickers[start:start + _BATCH_SIZE]
            try:
                batch = yf.download(
                    grup,
                    period="1y",
                    interval="1d",
                    group_by="ticker",
                    threads=True,
                    progress=False,
                    auto_adjust=True,
                )
            except Exception:
                batch = None

            for ticker in grup:
                row = None
                try:
                    sub = _extract_single(batch, ticker) if batch is not None else None
                    if sub is not None:
                        row = analysis.analyze_dataframe(ticker, sub)
                        if row is not None:
                            # Lot çekimi taramayı bozmamalı; hata olsa da satır eklenir.
                            try:
                                row["lot"] = _fetch_lot(ticker)
                            except Exception:
                                row["lot"] = None
                except Exception:
                    row = None

                with _lock:
                    if row is not None:
                        _state["results"].append(row)
                    _state["progress"]["done"] += 1

        with _lock:
            _state["status"] = "done"
            _state["finished_at"] = time.time()
    except Exception as exc:  # beklenmedik hata
        with _lock:
            _state["status"] = "error"
            _state["error"] = str(exc)
            _state["finished_at"] = time.time()


def start_scan() -> dict:
    """Tarama çalışmıyorsa yeni bir arka plan thread başlatır."""
    global _thread
    with _lock:
        if _state["status"] == "running":
            return {"status": "running", "progress": dict(_state["progress"])}
        # durumu sıfırla
        _state["status"] = "running"
        _state["progress"] = {"done": 0, "total": len(analysis.HISSELER)}
        _state["results"] = []
        _state["started_at"] = time.time()
        _state["finished_at"] = None
        _state["error"] = None

    _thread = threading.Thread(target=_run_scan, name="bist-scan", daemon=True)
    _thread.start()
    return {"status": "running", "progress": {"done": 0, "total": len(analysis.HISSELER)}}


def fetch_detail(ticker: str) -> dict | None:
    """Tek hisseyi indirip detaylı analizini döndürür (detay drawer)."""
    if not ticker.endswith(".IS"):
        ticker = f"{ticker}.IS"
    df = yf.download(
        ticker,
        period="1y",
        interval="1d",
        progress=False,
        auto_adjust=True,
    )
    return analysis.detailed_analysis(ticker, df)
