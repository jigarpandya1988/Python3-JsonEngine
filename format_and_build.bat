@echo off
setlocal

REM Move to project root
cd /d "%~dp0"

echo -------------------------------------
echo Running isort...
python -m isort .

echo -------------------------------------
echo Running black...
python -m black .

echo -------------------------------------
echo Running flake8...
python -m flake8 .

echo -------------------------------------
echo Building package...
python -m build

echo Done!
endlocal
pause
