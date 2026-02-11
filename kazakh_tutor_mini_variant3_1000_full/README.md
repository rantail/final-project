# Kazakh-Tutor MINI — Variant 3 (Mixed) — 1000 words

**What you get**
- Flask Web App + API
- Login/Register
- SQLite DB
- Global dictionary of **1000 words** split by levels: Beginner, A1, A2, B1, B2
- User can choose difficulty level in Settings
- One-click import of **random words** from the global dictionary
- Training selects words from the user's imported list (with ML-based prioritization)
- Stats page generates charts

## Python version
Use **Python 3.10 or 3.11** for easiest installation on Windows.

## Run (Windows)
Double-click `run_windows.bat` or:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open: http://127.0.0.1:5000

## Levels
Files:
- `tutor/data/words_Beginner.json`
- `tutor/data/words_A1.json`
- `tutor/data/words_A2.json`
- `tutor/data/words_B1.json`
- `tutor/data/words_B2.json`
- `tutor/data/global_1000_words.json`
