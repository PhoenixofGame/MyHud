@echo off
echo ================================
echo Installing required Python packages
echo ================================
echo.

REM Upgrade pip
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Fehler beim Aktualisieren von pip.
    pause
    exit /b
)

echo Pip erfolgreich aktualisiert.
echo.

REM List of required packages
set PACKAGES=customtkinter pywin32 psutil pynput Pillow

for %%P in (%PACKAGES%) do (
    echo Installing %%P ...
    python -m pip install %%P
    if %errorlevel% neq 0 (
        echo Fehler bei der Installation von %%P
    ) else (
        echo %%P erfolgreich installiert.
    )
    echo.
)

echo ================================
echo All dependencies processed.
echo ================================
pause
