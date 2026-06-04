"""Sayfa ve JSON API uçları."""
from __future__ import annotations

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from . import scanner


def index(request):
    return render(request, "terminal/index.html")


@require_POST
def api_scan(request):
    """Arka plan taramasını başlat (zaten çalışıyorsa no-op)."""
    return JsonResponse(scanner.start_scan())


@require_GET
def api_results(request):
    """Tarama durumu + ilerleme + (canlı dolan) sonuçlar."""
    return JsonResponse(scanner.get_state())


@require_GET
def api_stock(request, symbol):
    """Tek hisse için detaylı analiz (destek/direnç + stratejik yorum)."""
    try:
        detail = scanner.fetch_detail(symbol.upper())
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=502)
    if detail is None:
        return JsonResponse(
            {"error": f"{symbol} için yeterli veri bulunamadı."}, status=404
        )
    return JsonResponse(detail)
