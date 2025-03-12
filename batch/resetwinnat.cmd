chcp 65001

openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在获取管理员权限...
    echo Obtaining administrator privileges...
    powershell -Command "Start-Process cmd.exe -ArgumentList '/c %~dpnx0' -Verb RunAs"
    exit /b
)

net stop winnat
net start winnat