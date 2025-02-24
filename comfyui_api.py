import json
import uuid
import requests
import os
import time
import random
import websocket
from PIL import Image
import io

# ComfyUI 服务器地址和端口
server_address = "http://42.193.99.90:5478"  # 确保服务器地址和端口正确

# 客户端 ID（唯一标识）
client_id = str(uuid.uuid4())

# 动态输入的正负面提示词
positive_prompt = "A detailed shot of hands holding an object, with realistic skin texture, veins, and natural lighting to emphasize the sense of touch."
negative_prompt = "blurry, cartoonish, distorted, low quality, pixelated, out of focus, ugly, deformed, bad anatomy, bad composition, Extra limbs, extra fingers"

# 生成随机种子
seed = random.randint(0, 999999999999999)

# 工作流 JSON 数据
prompt = {
    "3": {
        "inputs": {
            "seed": seed,
            "steps": 20,
            "cfg": 8,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1,
            "model": ["10", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0]
        },
        "class_type": "KSampler",
        "_meta": {"title": "K采样器"}
    },
    "5": {
        "inputs": {
            "width": 512,
            "height": 512,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage",
        "_meta": {"title": "空Latent图像"}
    },
    "6": {
        "inputs": {
            "text": positive_prompt,
            "clip": ["10", 1]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "CLIP文本编码"}
    },
    "7": {
        "inputs": {
            "text": negative_prompt,
            "clip": ["10", 1]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "CLIP文本编码"}
    },
    "8": {
        "inputs": {
            "samples": ["3", 0],
            "vae": ["10", 2]
        },
        "class_type": "VAEDecode",
        "_meta": {"title": "VAE解码"}
    },
    "9": {
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": ["8", 0]
        },
        "class_type": "SaveImage",
        "_meta": {"title": "保存图像"}
    },
    "10": {
        "inputs": {
            "ckpt_name": "majic_v7.safetensors"
        },
        "class_type": "CheckpointLoaderSimple",
        "_meta": {"title": "Checkpoint加载器（简易）"}
    }
}

# 发送请求
def queue_prompt(prompt):
    data = {"prompt": prompt, "client_id": client_id}
    response = requests.post(f"{server_address}/prompt", json=data)
    if response.status_code != 200:
        print(f"发送请求失败，状态码：{response.status_code}")
        print(f"响应内容：{response.text}")
    return response.json()

# 获取图片
def get_images(prompt_id):
    ws = websocket.WebSocket()
    ws.connect(f"ws://{server_address.split('http://')[-1]}/ws?clientId={client_id}")
    try:
        while True:
            message = json.loads(ws.recv())
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break
    finally:
        ws.close()

    # 获取历史记录
    history_url = f"{server_address}/history/{client_id}/{prompt_id}"
    print(f"请求历史记录的URL: {history_url}")
    response = requests.get(history_url)
    if response.status_code == 200:
        try:
            history = response.json()
        except json.JSONDecodeError as e:
            print(f"解析历史记录时发生错误：{e}")
            print(f"响应内容：{response.text}")
            return None
    else:
        print(f"获取历史记录失败，状态码：{response.status_code}")
        print(f"响应内容：{response.text}")
        return None

    # 检查是否有图片输出
    for node_id in history.get(prompt_id, {}).get('outputs', {}):
        if 'images' in history[prompt_id]['outputs'][node_id]:
            for image in history[prompt_id]['outputs'][node_id]['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                if image_data:
                    return image_data
    return None

# 获取图片数据
def get_image(filename, subfolder, image_type):
    image_url = f"{server_address}/images/{subfolder}/{filename}.{image_type}"
    print(f"请求图片的URL: {image_url}")
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"获取图片失败，状态码：{response.status_code}")
        print(f"响应内容：{response.text}")
        return None

# 保存图片到本地
def save_image_to_local(image_data, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image_path = os.path.join(output_dir, f"ComfyUI_output.png")
    with open(image_path, "wb") as f:
        f.write(image_data)
    print(f"图片已保存到 {image_path}")

# 调用接口
response = queue_prompt(prompt)
prompt_id = response["prompt_id"]
print(f"任务 ID: {prompt_id}")
print(f"随机种子: {seed}")

# 获取图片并保存
image_data = get_images(prompt_id)
if image_data:
    save_image_to_local(image_data)
else:
    print("图片获取失败")