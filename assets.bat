@echo off
echo Installing required Python packages...

python.exe -m pip install --upgrade pip

pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Fehler bei der Installation von Pip.
) else (
    echo Pip wurde erfolgreich geupdateted.
)

echo.

pip install customtkinter
if %errorlevel% neq 0 (
    echo Fehler bei der Installation von customtkinter.
) else (
    echo customtkinter wurde erfolgreich installiert.
)

echo.

pip install pywin32
if %errorlevel% neq 0 (
    echo Fehler bei der Installation von pywin32.
) else (
    echo pywin32 wurde erfolgreich installiert.
)

echo.


pip install psutil
if %errorlevel% neq 0 (
    echo Fehler bei der Installation von psutil.
) else (
    echo psutil wurde erfolgreich installiert.
)

echo.


pip install keyboard
if %errorlevel% neq 0 (
    echo Fehler bei der Installation von keyboard.
) else (
    echo keyboard wurde erfolgreich installiert.
)

echo.

pip install Pillow
if %errorlevel% neq 0 (
    echo Fehler bei der Installation von Pillow.
) else (
    echo Pillow wurde erfolgreich installiert.
)

echo.



echo All dependencies installed successfully!
pause
