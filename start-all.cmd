@echo off
echo ============================================
echo  Starting QQ Bot (NapCatQQ + NoneBot2)
echo ============================================
echo.
echo 步骤:
echo 1. QQ 登录窗口会弹出，登录你的账号 3694319759
echo 2. 稍等登录成功后，在浏览器打开 http://localhost:6099/webui
echo 3. 在 WebUI 中确认 OneBot v11 正向WS 端口为 3001
echo 4. 然后按任意键启动 NoneBot2
echo.
echo 按任意键开始...
pause >nul

echo Starting QQ + NapCatQQ...
start "QQ" cmd /k "cd /d %~dp0napcat\NapCat.44498.Shell && QQ.exe"

echo.
echo ============================================
echo QQ 正在启动, 请在 QQ 窗口登录!
echo 等登录成功后, 打开 http://localhost:6099/webui
echo 确认 OneBot 正向WS 端口为 3001, 然后...
echo ============================================
echo.
pause

echo Starting NoneBot2...
start "NoneBot2" cmd /k "cd /d %~dp0nonebot && python bot.py"

echo.
echo ============================================
echo All systems go!
echo NoneBot2 连接 NapCat WebSocket (port 3001)
echo.
echo 测试: 给你自己的 QQ 号发 /ping 命令
echo ============================================
pause
