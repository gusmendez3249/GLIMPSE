@echo off
cd backend
start cmd /k "venv\Scripts\activate && python run.py"
timeout /t 3
cd ..\frontend
start cmd /k "npm start"
