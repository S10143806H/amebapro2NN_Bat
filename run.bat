@echo off

:: clear dist folder
rmdir /s /q dist
mkdir dist

:: iterate through all the python files in current folder
for %%i in (*.py) do (
  echo Processing %%i
  python -m PyInstaller --onefile "%%i"
  if not errorlevel 1 (
    echo Copying %%~ni.exe to C:\Users\zhuqi\AppData\Local\Arduino15\packages\realtek\tools\ameba_pro2_tools\1.1.5\
    copy "dist\%%~ni.exe" "C:\Users\zhuqi\AppData\Local\Arduino15\packages\realtek\tools\ameba_pro2_tools\1.1.5\"
  ) else (
    echo Failed to build %%i
  )
)

:: grant permission to dist folder (if not Windows)
if not "%OS%"=="Windows_NT" sudo chmod -R 777 ./dist