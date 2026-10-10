@echo off
cd /d "%~dp0"
python -m parking_app
if errorlevel 1 pause
