"""
 Copyright (c) 2023 ZeyuWu

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """


"""
二级目录批量化处理脚本
"""

import os
import logging
import time
import subprocess

import sys
sys.stdin.reconfigure(encoding='utf-8')

# 设置日志配置
import logging
handler = logging.FileHandler('log.log', encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# 指定目录路径
directory = r'path/to/dir'

def task(cmd:str,waittime:int):
    logging.info(f'start:{cmd}')
    process = subprocess.Popen(cmd, shell=True,stdout=handler.stream, stderr=subprocess.STDOUT)
    try:
        process.wait(timeout=waittime)  # 设置超时时间为15秒
    except subprocess.TimeoutExpired:
        logging.error(f'timeout:{cmd}')
        process.kill()  # 中止进程
    if process.returncode != 0:
        logging.error(f'fail:{cmd}')



# 遍历目录下的子目录
for second_dirs in os.listdir(directory):
    root = os.path.join(directory, second_dirs)
    files = os.listdir(root)
    
    # 检查是否为目标目录
    if 'main.ps1' in files:
        logging.info('找到 main.ps 文件：{}'.format(root))
        
        # 切换到当前目录
        os.chdir(root)

        # git命令的要把 windows path 转换成 unix path
        fp = str(root).replace('\\','/')
        task('git config --global --add safe.directory' + ' ' + fp,15)
        
        task('git pull',15)
        task('java -jar mcl.jar -u',30)

        # 切换回上级目录
        os.chdir('..')

        time.sleep(5)  # 等待15秒后继续下一次循环

logging.info('mission compelet')