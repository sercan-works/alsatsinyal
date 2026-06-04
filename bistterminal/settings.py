"""BIST Algo Terminal — Django ayarları (sade, DB modeli gerektirmez)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Üretimde SECRET_KEY ortam değişkeninden gelir; yoksa geliştirme anahtarı.
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-bist-algo-terminal-secret-key-change-me")

# DEBUG yalnızca DEBUG=True ortam değişkeni ile açılır (Vercel'de kapalı).
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "terminal",
]

MIDDLEWARE = [
    # WhiteNoise static dosyaları wsgi/serverless ortamında servis eder.
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise'ın collectstatic'e ihtiyaç duymadan app static'lerini finder'larla
# servis etmesini sağlar (serverless'ta build adımı gerektirmez).
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
