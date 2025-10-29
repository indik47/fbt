@echo off
echo Killing processes...

taskkill /F /IM NintendoTargetManager2.exe
taskkill /F /IM InputDirector.exe
taskkill /F /IM NintendoSdkDaemon.exe
taskkill /F /IM LLGDHost.exe
taskkill /F /IM SwitchInputSender.exe

echo Processes killed successfully.

timeout /t 1 /nobreak >nul

rem change path to absolute path in your system
start "" "C:\Nintendo\14.3.0\LowLevelGraphicsDebugger\Llgd\LLGDHost.exe"
start "" "C:\Nintendo\SDK_15.3.2\NintendoSDK\Resources\Firmwares\NX\NintendoTargetManager2\NintendoTargetManager2.exe"
start "" "C:\SwitchDevMinNSA\Engine\Platforms\Switch\Binaries\Win64\SwitchInputSender.exe"


pause