@echo off
echo Starting CloudPhoneBook Backend API on http://localhost:8000...
set PYTHONPATH=services\api;packages\shared
python -m uvicorn app.main:app --reload --port 8000
pause
