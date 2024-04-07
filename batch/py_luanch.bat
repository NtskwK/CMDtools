@REM No license
@REM Enjoy yourself!

@REM 一个为普通用户准备的python启动器
@REM 如果环境中没有python则会让用户选择是否自动安装


@REM 当前会话窗口改为UTF-8编码
chcp 65001

@echo off

REM 检查Python命令是否可用
where python > nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安装或未添加到系统环境变量中
    echo Do you want to install Python? (Y/N):
    set /p choice=

    if not /i "%choice%"=="Y" (
        echo Python installation skipped.
        pause
        exit
    )

    echo 准备下载Python zip包到本地...
    set download_url=https://repo.huaweicloud.com/python/3.10.11/python-3.10.11-amd64.exe
    REM 获取自身所在目录
    set script_dir=%~dp0
    set save_path=%script_dir%python-3.10.11-amd64.exe
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile(\"$env:download_url\", \"$env:save_path\")"
    REM 检查下载是否成功
    if %errorlevel% neq 0 (
        echo Python zip包下载失败
        echo 请尝试重新运行脚本或执行手动安装
        pause
        exit
    )
    

    echo Python 下载成功，准备执行安装
    set installer_path=%script_dir%python-3.10.11-amd64.exe 
    set install_dir=C:\Python                

    REM 检查目标目录是否存在，如果不存在则创建
    if not exist "%install_dir%" (
        mkdir "%install_dir%"
    )

    REM 执行静默安装
    "%installer_path%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir="%install_dir%"

    REM 验证安装是否成功
    if exist "%install_dir%\python.exe" (
        echo Python has been installed successfully.
        echo 再次点击即可启动运行
        pause
        exit
    ) else (
        echo Failed to install Python.
        echo 请尝试重新运行脚本或执行手动安装
        pause
        exit
    )      
)

where python > nul 2>&1
if %errorlevel% neq 0 (
    REM 获取Python版本号
    for /f "tokens=2*" %%A in ('python --version 2^>^&1') do (
        echo 当前Python版本号为: %%A %%B
        python main.py
    )
)