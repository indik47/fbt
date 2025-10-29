@echo off
REM Batch script to run cleanup and other Python scripts sequentially

REM Check if Python is installed and available in PATH
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not available in PATH.
    pause
    exit /b 1
)

REM Run the cleanup Python script: cleanup_images.py
echo Running cleanup_images.py...
python cleanup_images.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to run cleanup_images.py.
    pause
    exit /b 1
)

REM Run the first Python script: process_mask.py
echo Running process_mask.py...
python process_mask.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to run process_mask.py.
    pause
    exit /b 1
)

REM Run the second Python script: apply_mask.py
echo Running apply_mask.py...
python apply_mask.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to run apply_mask.py.
    pause
    exit /b 1
)

REM Run the third Python script: resize_and_crop.py
echo Running resize_and_crop.py...
python resize_and_crop.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to run resize_and_crop.py.
    pause
    exit /b 1
)

echo All scripts ran successfully.
pause
exit /b 0