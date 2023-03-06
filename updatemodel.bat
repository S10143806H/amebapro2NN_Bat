@echo off
setlocal EnableDelayedExpansion
set "nbfile_path=%~dp0%"
for /f "delims=" %%i in ('dir /b /s "%nbfile_path%\*.nb" ') do set "nbFiles=!nbFiles!%%i"

set "targetDir=C:\Users\%USERNAME%\AppData\Local\Arduino15\packages\realtek\hardware\AmebaPro2"

set "variantFolder="
for /d %%i in ("%targetDir%\*") do (
    if exist "%%i\variants\common_nn_models" (
        set "variantFolder=%%i"
        goto :breakLoop
    )
)
:breakLoop

if not defined variantFolder (
    echo Variant folder does not exist. Exiting...
    exit /b
)

cd /d "%variantFolder%\variants\common_nn_models"

set "fileName=yolov4_tiny.nb"
echo "%variantFolder%\variants\common_nn_models"
if not exist "%fileName%" (
    echo %fileName% does not exist in target directory. Exiting...
    exit /b
)

set "dateStr=!DATE:/=-!"
set "dateStr=!dateStr:~0,-4!"
set "timeStr=!TIME::=-!"
set "timeStr=!timeStr:,=!"
set "timeStr=!timeStr:~0,-2!"

ren "%fileName%" "yolov4_tiny_backup_%timeStr%nb"
echo "%nbFiles%"
echo copy to
echo "%variantFolder%\variants\common_nn_models\yolov4_tiny.nb"
copy /y "%nbFiles%" "%variantFolder%\variants\common_nn_models\yolov4_tiny.nb"

echo Files copied and renamed successfully.