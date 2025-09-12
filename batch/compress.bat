@REM 用7z压缩dist/sam-geo
@echo off
setlocal enabledelayedexpansion
set "dist_dir=.\dist\sam-geo"
set "output_file=sam-geo.7z"

if not exist "%dist_dir%" (
    echo Directory %dist_dir% does not exist.
    exit /b 1
)

if exist "%output_file%" (
    echo Removing existing %output_file%...
    del "%output_file%"
)

echo Compressing %dist_dir% to %output_file%...
7z a -t7z "%output_file%" "%dist_dir%\*"