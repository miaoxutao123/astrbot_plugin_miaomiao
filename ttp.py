import requests
import json
import time
import random
def generate_image(prompt,api_key,model="stabilityai/stable-diffusion-3-5-large",seed=None,image_size = "1024x1024"):
    url = "https://api.siliconflow.cn/v1/images/generations"

    if seed is None:
        seed = random.randint(0, 9999999999)

    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": image_size,
        "seed": seed
    }
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    while True:
        response = requests.request("POST", url, json=payload, headers=headers)
        data = json.loads(response.text)

        if data.get("code") == 50603:
            print("System is too busy now. Please try again later.")
            time.sleep(1)
            continue

        if 'images' in data:
            for image in data['images']:
                image_url = image['url']
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_path = 'downloaded_image.jpeg'
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image downloaded from {image_url}")
                    return image_url, image_path
                else:
                    print(f"Failed to download image from {image_url}")
                    return None, None
        else:
            print("No images found in the response.")
            return None, None


# # 示例调用
# prompt = "A majestic, floating crystal cluster amidst swirling nebulae, bathed in starlight. This is the peak of Aetheria, the Zenith of Starlight, radiating magical energy. The image should have a fantastical, ethereal quality."
# api_key = ""
# image_url, image_path = generate_image(prompt,api_key)
# print(f"Image URL: {image_url}, Image Path: {image_path}")