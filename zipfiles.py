import os
import subprocess
import re

# 指定目录路径
directory = r'C:\Users\natsuu\Desktop\455dices\source'

for second_dir in os.listdir(directory):
    if not re.search(r'\.7z$', second_dir):
        # 构建压缩文件名
        zip_name = second_dir + '_202307_backup_final' + '.7z'
        zip_path = os.path.join(directory, zip_name)

        # 使用 7-Zip 进行最大压缩
        subprocess.run(['7z', 'a', '-t7z', '-mx9', '-mfb257', '-md256m', zip_path, os.path.join(directory, second_dir)])

        print(f"Created: {zip_path}")
