@echo off
cd /d %~dp0
if not exist .venv (
  py -3.10 -m venv .venv 2>nul
  if errorlevel 1 python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt
python app.py
pause
