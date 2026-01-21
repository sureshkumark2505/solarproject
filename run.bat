@echo off
REM Solar Edge AI - One-Click Launcher
REM This script starts all three services in separate windows

cls
echo.
echo ============================================================
echo.
echo    ^>  Solar Edge AI - Launching All Services
echo.
echo ============================================================
echo.

REM Get the project directory
set PROJECT_DIR=%~dp0

REM Start API Server in new window
echo Starting API Server...
start "Solar Edge AI - API Server (5000)" cmd /k "cd /d %PROJECT_DIR%api && python server.py"
timeout /t 3 /nobreak

REM Start Edge AI in new window
echo Starting Edge AI Runner...
start "Solar Edge AI - Edge AI Runner" cmd /k "cd /d %PROJECT_DIR%EdgeAI && python edge_runner.py"
timeout /t 3 /nobreak

REM Start Dashboard in new window
echo Starting Dashboard (Streamlit)...
start "Solar Edge AI - Dashboard (8501)" cmd /k "cd /d %PROJECT_DIR%Dashboard && streamlit run dashboard.py"

echo.
echo ============================================================
echo.
echo ^> All services starting...
echo.
echo ^> Dashboard:  http://localhost:8501
echo ^> API:        http://localhost:5000
echo ^> Edge AI:    Running
echo.
echo ^> Close any window to stop that service
echo ^> Close all windows to stop everything
echo.
echo ============================================================
echo.

REM Optional: Open dashboard in browser after a delay
timeout /t 5 /nobreak
start http://localhost:8501

echo Dashboard opened in browser!
