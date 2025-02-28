import requests
import json
import sys
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def search_song(music_name, singer, search_type="qq", url="https://music.txqq.pro/"):
    # 请求头部
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
    }

    # 请求的数据
    data = {
        "input": f"{music_name} {singer}",
        "filter": "name",
        "type": search_type,
        "page": 1
    }

    # 添加重试机制
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST", "GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # 发送 POST 请求
    try:
        response = session.post(url, data=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        return None

    # 解析返回的 JSON 数据
    try:
        json_data = response.json()
    except ValueError:
        print("返回的内容不是有效的 JSON 格式")
        return None

    # 检查返回数据是否包含所需字段
    if "data" not in json_data:
        print("返回的数据中没有找到 'data' 字段")
        return None

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'songs_data.json')

    # 将搜索结果保存到 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    
    print("数据已保存到 'songs_data.json' 文件")

    # 打印歌曲信息
    # for song in json_data.get("data", []):
    #     title = song.get("title", "未知歌曲")
    #     author = song.get("author", "未知作者")
    #     link = song.get("link", "无链接")
    #     lrc = song.get("lrc", "无歌词")
    #     download_url = song.get("url", "无下载链接")
    #     pic = song.get("pic", "无封面图")

    #     print(f"歌曲名称: {title}")
    #     print(f"作者: {author}")
    #     print(f"歌曲链接: {link}")
    #     print(f"歌词: {lrc}")
    #     print(f"下载链接: {download_url}")
    #     print(f"封面图: {pic}")
    #     print("-" * 50)

    return json_data

# 示例调用
# if __name__ == "__main__":
#     music_name = "演"
#     singer = "chilichill"
#     search_song(music_name, singer)
