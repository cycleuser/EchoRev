@echo off
REM Build and publish EchoRev to PyPI

echo Cleaning old builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info
if exist echorev\*.egg-info rmdir /s /q echorev\*.egg-info

echo Building package...
python -m build

echo Uploading to PyPI...
python -m twine upload dist\*

echo Done!
pause