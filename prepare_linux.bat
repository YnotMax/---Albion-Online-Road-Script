@echo off
setlocal
echo ========================================================
echo PREPARANDO PACOTE PARA LINUX - Gerenciador HD
echo ========================================================
echo.

set DIST_DIR=dist_linux
set ZIP_FILE=AudioHD_Linux_Version.zip

echo [1/4] Limpando arquivos temporarios...
if exist %DIST_DIR% rd /s /q %DIST_DIR%
if exist %ZIP_FILE% del /f /q %ZIP_FILE%

echo [2/4] Criando estrutura de pastas...
mkdir %DIST_DIR%
mkdir %DIST_DIR%\recordings

echo [3/4] Copiando arquivos fonte e scripts...
copy main.py %DIST_DIR%\ >nul
copy recorder.py %DIST_DIR%\ >nul
copy player.py %DIST_DIR%\ >nul
copy storage_manager.py %DIST_DIR%\ >nul
copy requirements.txt %DIST_DIR%\ >nul
copy install_and_run.sh %DIST_DIR%\ >nul
copy README.md %DIST_DIR%\ >nul

echo [4/4] Compactando para transporte...
powershell -Command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath '%ZIP_FILE%' -Force"

echo.
echo ========================================================
echo PROCESSO CONCLUIDO!
echo Arquivo gerado: %ZIP_FILE%
echo.
echo Instrucoes para o Linux:
echo 1. Transfira o arquivo .zip para o Linux
echo 2. Extraia o conteudo
echo 3. Execute: bash install_and_run.sh
echo ========================================================
pause
