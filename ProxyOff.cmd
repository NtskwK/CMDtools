@echo off 
echo ���ڹر�ϵͳ�������Ժ�...
echo=
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f >nul 2>nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f >nul 2>nul

for /l %%i in (3,-1,0) do (
ping 127.1 -n 2 >nul
echo. �ű�����%%i���Զ��رձ����ڡ���
)
exit