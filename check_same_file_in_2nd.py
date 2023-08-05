
"""
用于检测二级目录是否有某种相同的文件
"""


import os
import json
import re

import logging
handler = logging.FileHandler('2.log', encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 指定目录路径
directory = r'path\to\dir'

dice_list = []

# 遍历目录下的子目录
for second_dirs in os.listdir(directory):
    
    dice_info = {}

    root = os.path.join(directory, second_dirs)
    files = os.listdir(root)
    
    # 检查是否为目标目录
    if not 'main.ps1' in files:
        continue

    # 只检索某类文件
    for file_name in files:
        if re.search(r'^Dice[0-9]*', file_name):
            dice_info[file_name] = os.path.join(root,files)
            dice_list.append(dice_info)

# 记录文件列表
with open('data_origin.json', 'w') as f:
    json.dump(dice_list, f, indent=4)

keys = set()
duplicate_keys = set()
dices = []
duplicate_dice = {}

for dice in dice_list:
    for key in dice.keys():
        if key in keys:
            duplicate_keys.add(key)
        else:
            keys.add(key)

for dice in dice_list:
    duplicate_dice = {}
    for key in dice.keys():
        if key in duplicate_keys:
            duplicate_dice[key] = dice[key]
            dices.append(duplicate_dice)

with open('data.json_duplicate', 'w') as f:
    json.dump(duplicate_dice, f, indent=4)