#!/bin/bash

# Ntkskwk@github
# 2024/04/07

test_url="https://www.google.com"

declare -A pkg
declare -A mirrors

pkg[npm]="npm"
mirror[npm]="npm config set registry http://mirrors.cloud.tencent.com/npm/"


response=$(curl -s -o /dev/null -w "%{http_code}" "$url" --connect-timeout 3)
if [ "$response" -eq 200 ]; then     
    echo "Google connected successfully!"; 
else     
    echo "Can not connect to Google!"; 
    echo "We will try to set mirror for you."; 
fi

set -eo pipefail

# 检查当前用户是否有sudo权限
if [ "$(id -u)" != "0" ]; then
    echo "错误：请以sudo权限运行此脚本！"
    exit 1
fi

run(){
	echo "$1"
	eval "$1"
}

set_mirror(){
	check_msg_prefix="Set mirror for ... ${pkg[$1]}"
	check_msg_result="\033[92m\033[1m OK\033[0m\033[39m"
	unset not_found
	hash "${pkg[$1]}" 2>/dev/null || not_found=true
    if [[ $not_found ]]; then
        check_msg_result="\033[91m can't find ${pkg[$1]}! Check that the program is installed and that you have added the proper path to the program to your PATH environment variable. If you change your PATH environment variable, remember to close and reopen your terminal. \033[39m"
    else
        run "${mirror[$1]} || sudo ${mirror[$1]}"
	fi
	echo -e "$check_msg_prefix $check_msg_result"
}


for key in "${!pkg[@]}"; do
    set_mirror "$key"
done