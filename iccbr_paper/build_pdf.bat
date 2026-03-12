@echo off
REM Build ICCBR paper PDF. Double-click to run.
cd /d "%~dp0"
python build_pdf.py
if errorlevel 1 pause
