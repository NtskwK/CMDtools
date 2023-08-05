import os
import subprocess
import shutil

"""
文件批量复制
"""

source_file = r'C:\Users\natsuu\Desktop\455dices\mx\.git'
# 指定目录路径
directory = r'C:\Users\natsuu\Desktop\455dices\source'

# 遍历目录下的子目录
for root, dirs, files in os.walk(directory):
    for dir_name in dirs:
        if 'main.ps1' in files:
            # 构建文件路径
            target_directory = os.path.join(root, dir_name)

            # 执行文件复制
            shutil.copy(source_file, target_directory)

            print(f"File copied to: {target_directory}")


