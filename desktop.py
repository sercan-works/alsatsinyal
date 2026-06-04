"""Masaüstü başlatıcı — yerel web sunucusunu açar ve tarayıcıyı yönlendirir.

PyInstaller ile `.exe`'ye paketlenir. Çift tıklayınca:
  1. Django uygulamasını `waitress` ile 127.0.0.1 üzerinde başlatır,
  2. ~1 sn sonra varsayılan tarayıcıda arayüzü açar,
  3. Konsol penceresi açık kaldığı sürece sunucu çalışmaya devam eder.

Yerelde çalıştığı için tarama (arka plan thread + bellek state) sorunsuz işler;
serverless ortamındaki "taranıyorda kalma" sorunu burada yoktur.
"""
import os
import socket
import sys
import threading
import webbrowser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bistterminal.settings")

# PyInstaller ile dondurulmuş (frozen) çalışırken çalışma dizinini bundle
# köküne sabitle ki Django app/template/static yolları çözülebilsin.
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

import django  # noqa: E402

django.setup()

# WhiteNoise'ın "STATIC_ROOT yok" uyarısını sustur (finder'larla servis ediyoruz).
from django.conf import settings  # noqa: E402

if getattr(settings, "STATIC_ROOT", None):
    os.makedirs(settings.STATIC_ROOT, exist_ok=True)

from waitress import serve  # noqa: E402

from bistterminal.wsgi import application  # noqa: E402


def _find_free_port(preferred: int = 8000) -> int:
    """Tercih edilen porttan başlayarak boş bir port bulur."""
    for port in (preferred, 8001, 8080, 8501, 0):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("127.0.0.1", port))
            return sock.getsockname()[1]
        except OSError:
            continue
        finally:
            sock.close()
    return preferred


def main() -> None:
    port = _find_free_port(8000)
    url = f"http://127.0.0.1:{port}/"

    # Sunucu ayağa kalkınca tarayıcıyı aç (kısa gecikmeyle).
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()

    print("=" * 52)
    print("  BIST ALGO TERMINAL")
    print(f"  Arayuz: {url}")
    print("  Kapatmak icin bu pencereyi kapatin (veya Ctrl+C).")
    print("=" * 52)

    try:
        serve(application, host="127.0.0.1", port=port, threads=8)
    except KeyboardInterrupt:
        print("\nKapatiliyor...")


if __name__ == "__main__":
    main()
