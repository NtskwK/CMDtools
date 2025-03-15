import os
import re

target_directory = r"F:\ani-rss\bangumi\彻夜之歌\Season 1"

def rename_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if "Yofukashi no Uta" in file:
                # 使用正则表达式提取集数信息
                episode_match = re.search(r'\s(\d+)\s', file)
                if episode_match:
                    episode_number = episode_match.group(1)
                    new_file_name = f"[XKsub&LoliHouse] Yofukashi no Uta S01E{episode_number} [WebRip 1080p HEVC-10bit AAC ASSx2].mkv"
                    old_file_path = os.path.join(root, file)
                    new_file_path = os.path.join(root, new_file_name)
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed {file} to {new_file_name}")


if __name__ == "__main__":
    rename_files(target_directory)