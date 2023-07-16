@echo off
setlocal EnableDelayedExpansion

rem 将控制台修改为UTF-8
chcp 65001

rem 遍历输入目录下的所有mkv文件
for %%a in (*.MP4) do (
    set filename=%%~na
    ffmpeg -i "%%a" -c:v hevc_qsv -rc vbr_hq -cq 26 -preset slow -profile:v main "!filename!RERIP.mp4"
)

# :charenc=UTF-8