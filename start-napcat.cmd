@echo off
chcp 65001 >nul
cd /d "%~dp0napcat\NapCat.44498.Shell"
echo ==============================
echo  Starting QQ + NapCatQQ...
echo ==============================
echo.
echo NapCat 启动后:
echo 1. QQ 登录窗口会出现, 登录 3694319759
echo 2. 登录后在浏览器打开 http://localhost:6099/webui
echo 3. 确认 WebUI 中已启用正向WS端口3001
echo 4. 然后双击 start-nonebot.cmd 启动机器人
echo ==============================
echo.
.\NapCatWinBootMain.exe
pause
