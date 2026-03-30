@echo off
echo Building PDF Solutions Desktop App...
echo.
echo Installing dependencies (including PyInstaller)...
pip install -r requirements.txt
echo.
echo Building executable...
python build.py
echo.
echo Done! Your executable is in the dist\ folder.
echo Double-click dist\PDF_Solutions.exe to launch the app.
pause
