@echo off
set INITIAL_PATH=%cd%
echo This Script is responsible for creating project's build-system, building main.c and uploading to rp2350
set BUILD_PATH=C:\Users\brd5clj\Desktop\UltrasonicProject\project\build
if exist %BUILD_PATH% (
    cd /d %BUILD_PATH%
) else (
    mkdir %BUILD_PATH%
    cd /d %BUILD_PATH%
)


set empty=true

for %%f in ("*") do (
    set empty = false
)
IF %empty% == "false" (
cmake -G "MinGW Makefiles" ./ || goto :error
) else (
cmake -G "MinGW Makefiles" ../ || goto :error
)
cd app || goto :error
mingw32-make || goto :error

echo Firmware was built!
echo Upload firmware on rp2350

pause
picotool reboot -f -u
timeout /t 2
picotool load ./main.uf2
timeout /t 2
picotool reboot
::picotool reboot 

echo main.uf2 uploaded!
cd  %INITIAL_PATH%

goto :eof

:error
echo ERROR occurred during build!
cd %INITIAL_PATH%

