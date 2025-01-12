@echo off

:: Check if a Python interpreter is installed
where python >nul 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo "zryte-cli.cmd: Could not find a Python interpreter"
    exit 127
)

python zryte-cli.py %*
