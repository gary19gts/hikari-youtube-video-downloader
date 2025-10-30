@echo off
title Hikari Youtube Video Downloader - by Gary19gts
color 0B

echo ========================================
echo   Hikari Youtube Video Downloader
echo   Developed by Gary19gts
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Por favor instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detectado
echo.

REM Verificar dependencias
echo Verificando dependencias...
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo [!] Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo [*] Iniciando Hikari Youtube Video Downloader...
echo.

REM Ejecutar el programa
python hikari-youtube-video-downloader.py

if errorlevel 1 (
    echo.
    echo [ERROR] El programa termino con errores
    pause
)
