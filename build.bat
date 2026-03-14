@echo off
REM Build package only (no upload to PyPI)

echo Cleaning old builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info
if exist echorev\*.egg-info rmdir /s /q echorev\*.egg-info

echo Building package...
python -m build

echo Build complete. Files in dist\
dir dist\