#!/bin/bash

# Clear the dist folder
rm -rf ./dist/*

# Build the executable using PyInstaller
python -m PyInstaller --onefile ./*.py

# Copy the executable to the destination folder
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sudo cp ./dist/updatemodel /usr/local/bin/
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    xcopy /Y .\dist\updatemodel.exe "C:\Users\zhuqi\AppData\Local\Arduino15\packages\realtek\tools\ameba_pro2_tools\1.1.5\"
elif [ "$(uname)" == "Darwin" ]; then
    sudo cp ./dist/updatemodel /usr/local/bin/
else
    echo "Unsupported operating system"
fi
