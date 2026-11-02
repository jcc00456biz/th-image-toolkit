@echo off
setlocal

echo [INFO] Activating .venv...
call .\.venv\Scripts\activate

echo [INFO] Installing the package and test dependencies...
python -m pip install -e ".[test]"

echo [INFO] Completed.
