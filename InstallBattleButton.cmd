@echo off
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (
    python -m tools.install_battle_button %*
) else (
    py -3 -m tools.install_battle_button %*
)
pause
