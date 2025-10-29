@echo off
setlocal enabledelayedexpansion

REM Set your Perforce server and workspace information
set P4_SERVER=ssl:nrs-p4-ext-euwe2.netherrealm.com:1666
set P4_USER=x.denys.oligov
set P4_WORKSPACE=SwitchDevMinNSA


REM Set the changelist number for querying
set CHANGE_NUMBER=930068

REM Set the output text files
set OUTPUT_FILE=output.txt
set DEBUG_FILE=changelist_info.txt

REM Run p4 describe to get details of the changelist
p4 -p %P4_SERVER% -u %P4_USER% -c %P4_WORKSPACE% describe -s %CHANGE_NUMBER% > %DEBUG_FILE%

REM Extract file paths from the changelist information and save to the text file
(for /f "tokens=2 delims= " %%a in ('findstr /C:"^... ... " %DEBUG_FILE% ^| findstr /v /c:"--"') do (
    set "line=%%a"
    set "filtered_line=!line:#* =!"
    echo !filtered_line!
)) > %OUTPUT_FILE%

echo Done! Output saved to %OUTPUT_FILE% and %DEBUG_FILE%