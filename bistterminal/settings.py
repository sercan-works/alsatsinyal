"""BIST Algo Terminal — Django ayarları (sade, DB modeli gerektirmez)."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Geliştirme amaçlı sabit anahtar — üretimde değiştir.
SECRET_KEY = "dev-bist-algo-terminal-secret-key-change-me"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "terminal",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "bistterminal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "bistterminal.wsgi.application"

# Veritabanı kullanılmıyor (sonuçlar bellekte tutulur). Yine de Django'nun
# DATABASES anahtarı tanımlı olmalı; SQLite dosyası oluşturulmaz çünkü
# hiçbir model/sorgu yapılmıyor.
DATABASES = {}

LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
