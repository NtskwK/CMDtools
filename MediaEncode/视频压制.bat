@echo off
setlocal EnableDelayedExpansion

rem ������̨�޸�ΪUTF-8
chcp 65001

rem ��������Ŀ¼�µ�����mkv�ļ�
for %%a in (*.MP4) do (
    set filename=%%~na
    ffmpeg -i "%%a" -c:v hevc_qsv -rc vbr_hq -cq 26 -preset slow -profile:v main "!filename!RERIP.mp4"
)

# :charenc=UTF-8