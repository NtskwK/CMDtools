@echo off
setlocal EnableDelayedExpansion

rem ������̨�޸�ΪUTF-8
chcp 65001

rem ɾ��tc��Ļ
del *.ts.ass

rem ��.sc.ass��׺��Ϊ.ass
powershell -Command "Get-ChildItem -Path "." -Filter "*.sc.ass" | Rename-Item -NewName { $_.Name -replace '\.sc\.ass$','.ass' }"

rem ��ass��ת��ΪUTF-8
for /f "delims=" %%a in ('dir /b *.ass') do (
    chcp 65001>nul
    type "%%a" > "%%~na_utf8.ass"
    del "%%a"
)

rem ��_utf8.ass��׺��Ϊ.ass
powershell -Command "Get-ChildItem -Path "." -Filter "*_utf8.ass" | Rename-Item -NewName { $_.Name -replace '_utf8\.ass$','.ass' }"

rem ��������Ŀ¼�µ�����mkv�ļ�
for %%a in (*.mkv) do (
    set filename=%%~na
    ffmpeg -i "%%a" -vf "ass=%%~na.ass" -c:v libx264 -b:v 4M -maxrate 4M -bufsize 8M -preset slow -crf 23 -c:a aac -b:a 192k "!filename!RERIP.mkv"
)

# :charenc=UTF-8