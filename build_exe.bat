@echo off
REM ====================================================================
REM  BIST Algo Terminal - Windows .exe derleyici
REM  Bu dosyayi Windows'ta cift tiklayin. Sonunda:
REM      dist\BIST-Algo-Terminal.exe
REM  olusur. O exe'yi cift tiklayinca arayuz tarayicida acilir.
REM ====================================================================
setlocal

echo [1/4] Sanal ortam hazirlaniyor...
if not exist build-venv (
    python -m venv build-venv
)
call build-venv\Scripts\activate.bat

echo [2/4] Bagimliliklari kuruluyor...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-build.txt

echo [3/4] .exe derleniyor (birkac dakika surebilir)...
pyinstaller --noconfirm --clean bist_terminal.spec

echo [4/4] Tamamlandi.
echo.
echo Cikti: dist\BIST-Algo-Terminal.exe
echo Bu dosyayi cift tiklayinca arayuz acilir.
echo.
pause
