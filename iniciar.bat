@echo off
echo Iniciando o Gravador de Macros...
cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Aviso: Ambiente virtual .venv nao encontrado. Tentando python global...
)

python main.py

if %errorlevel% neq 0 (
    echo.
    echo O programa fechou com erro. Veja a mensagem acima.
    pause
)
