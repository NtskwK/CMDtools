@echo off
setlocal EnableDelayedExpansion

rem 将控制台修改为UTF-8
chcp 65001

rem 删除tc字幕
del *.ts.ass

rem 将.sc.ass后缀改为.ass
powershell -Command "Get-ChildItem -Path "." -Filter "*.sc.ass" | Rename-Item -NewName { $_.Name -replace '\.sc\.ass$','.ass' }"

rem 将ass都转化为UTF-8
for /f "delims=" %%a in ('dir /b *.ass') do (
    chcp 65001>nul
    type "%%a" > "%%~na_utf8.ass"
    del "%%a"
)

rem 将_utf8.ass后缀改为.ass
powershell -Command "Get-ChildItem -Path "." -Filter "*_utf8.ass" | Rename-Item -NewName { $_.Name -replace '_utf8\.ass$','.ass' }"

rem 遍历输入目录下的所有mkv文件
for %%a in (*.mkv) do (
    set filename=%%~na
    ffmpeg -i "%%a" -vf "ass=%%~na.ass" -c:v libx264 -b:v 4M -maxrate 4M -bufsize 8M -preset slow -crf 23 -c:a aac -b:a 192k "!filename!RERIP.mkv"
)

# :charenc=UTF-8