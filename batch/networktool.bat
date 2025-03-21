@REM ©2024 NtskwK. All rights reserved.

@REM 改变控制台默认编码
chcp 65001

set "account=123456"
set "password=123456"

@REM 校园网0 电信1 移动2 联通3
set "operator=0"

curl "http://172.16.2.2/drcom/login?callback=dr1003&DDDDD=%account%&upass=%password%&0MKKey=123456&R1=0&R2=&R3=%operator%&R6=0&para=00&terminal_type=1"
@REM 输出 dr1003({"result":1, ... 即为登陆成功

timeout /t 5