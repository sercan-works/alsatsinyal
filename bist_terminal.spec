# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec — BIST Algo Terminal tek dosyalık Windows .exe paketi.

Derleme (Windows):  pyinstaller --noconfirm --clean bist_terminal.spec
Çıktı:              dist\\BIST-Algo-Terminal.exe
"""
from PyInstaller.utils.hooks import collect_all, collect_submodules

datas = []
binaries = []
hiddenimports = []

# Ağır / dinamik paketleri (veri dosyaları + alt modüller) tam topla.
for pkg in ("django", "pandas", "numpy", "yfinance", "whitenoise", "waitress"):
    pkg_datas, pkg_binaries, pkg_hidden = collect_all(pkg)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hidden

# Proje şablonları + statik dosyaları bundle içine kopyala.
datas += [
    ("terminal/templates", "terminal/templates"),
    ("terminal/static", "terminal/static"),
]

# Proje paketlerinin tüm alt modüllerini dahil et.
hiddenimports += collect_submodules("terminal")
hiddenimports += collect_submodules("bistterminal")

a = Analysis(
    ["desktop.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "pytest", "IPython", "notebook"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="BIST-Algo-Terminal",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
