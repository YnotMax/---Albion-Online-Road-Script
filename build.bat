@echo off
echo Otimizando e isolando módulos do controlador I/O...
echo.
echo Compilacao segura em andamento. Aguarde...
python -m PyInstaller --noconsole --onefile --name "AudioHD_Monitor" main.py
echo.
echo Processo completo! Gerenciador exportado na pasta "dist".
pause
