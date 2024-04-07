@echo off 
echo 正在关闭系统代理，请稍候...
echo=
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f >nul 2>nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f >nul 2>nul

for /l %%i in (3,-1,0) do (
ping 127.1 -n 2 >nul
echo. 脚本将在%%i后自动关闭本窗口。。
)
exit