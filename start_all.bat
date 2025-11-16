@echo off
echo Starting PR Review Agent...
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate && python run_server.py"

echo Waiting 5 seconds for server to start...
timeout /t 5 /nobreak >nul

echo Starting Streamlit UI...
start "Streamlit UI" cmd /k "cd /d %~dp0 && venv\Scripts\activate && streamlit run ui/streamlit_app.py"

echo.
echo Both servers are starting!
echo Backend: http://localhost:8000
echo UI: http://localhost:8501
echo.
echo Press any key to exit this window (servers will keep running)...
pause >nul

