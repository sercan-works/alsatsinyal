"""Kök URL yönlendirmesi."""
from django.urls import include, path

urlpatterns = [
    path("", include("terminal.urls")),
]
