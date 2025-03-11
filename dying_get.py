import requests
import json
import os

def parse_douyin_video(video_url):
    """
    解析抖音视频链接，获取无水印视频信息。
    :param video_url: 抖音视频的分享链接
    :return: 解析结果（字典格式）
    """
    api_url = "https://api.xinyew.cn/api/douyinjx?url="
    request_url = api_url + requests.utils.quote(video_url)

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        result = response.json()

        if result["code"] == 200:
            print("解析成功！")
            return result
        else:
            print(f"解析失败：{result['msg']}")
            return None

    except requests.RequestException as e:
        print(f"请求错误：{e}")
        return None

def download_video(video_url, save_path):
    """
    下载视频并保存到指定路径。
    :param video_url: 视频直链地址
    :param save_path: 保存路径
    :return: 视频的绝对地址
    """
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return os.path.abspath(save_path)

    except requests.RequestException as e:
        print(f"下载错误：{e}")
        return None

def process_douyin_video(video_url):
    """
    解析抖音视频并下载保存。
    :param video_url: 抖音视频的分享链接
    :return: 包含视频绝对地址、作者昵称和视频描述的字典
    """
    result = parse_douyin_video(video_url)
    print(result)
    if result:
        video_download_url = result['data']['video_url']
        author_name = result["data"]["additional_data"][0]["nickname"]
        video_description = result["data"]["additional_data"][0]["desc"]
        save_dir = 'data/plugins/astrbot_plugin_miaomiao/download_videos/dy'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'video.mp4')
        video_path = download_video(video_download_url, save_path)
        return {
            "video_path": video_path,
            "author_name": author_name,
            "video_description": video_description
        }
    return None

# if __name__ == "__main__":
#     video_url = input("请输入抖音视频链接：")
#     result = process_douyin_video(video_url)
#     if result:
#         print(f"视频已下载并保存到：{result['video_path']}")
#         print(f"作者昵称：{result['author_name']}")
#         print(f"视频描述：{result['video_description']}")
#     else:
#         print("视频下载失败")