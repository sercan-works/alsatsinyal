from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/scan", views.api_scan, name="api_scan"),
    path("api/results", views.api_results, name="api_results"),
    path("api/stock/<str:symbol>", views.api_stock, name="api_stock"),
]
