import base64
from gradio_client import Client
from pydub import AudioSegment
import os
import asyncio

async def generate_audio(url,text, language, speaker, noise_scale=0.5, noise_scale_w=0.5, length_scale=1.0):
    try:
        # 确保 URL 是合法的
        client = Client(url)
    except Exception as e:
        print(f"无法连接到 Hugging Face Space，可能是 URL 无效或网络问题: {e}")
        print("请检查 URL 的合法性，并确保网络连接正常。")
        return {"message": "无法连接到 Hugging Face Space"}

    # 构造符合API要求的请求体
    payload = [
        text,          # 文本输入（可选）
        language,      # 语言选择（必填）
        speaker,       # 说话者选择（必填）
        noise_scale,   # 感情变化程度（必填，提供默认值）
        noise_scale_w, # 音素发音长度（必填，提供默认值）
        length_scale   # 整体语速（必填，提供默认值）
    ]

    try:
        print("发送请求到 Hugging Face Space:", payload)
        result = client.predict(*payload, api_name="/generate")
        
        # 打印调试信息
        print("API响应:", result)
        
        # 解析响应数据
        output_message = result[0]
        audio_file_path = result[1]
        extra_info = result[2]
        duration = None  # 默认值

        # 如果有音频文件路径则读取文件并编码为base64
        audio_base64 = None
        mp3_file_path = None
        if audio_file_path:
            # 转换 WAV 文件为 MP3 文件
            audio = AudioSegment.from_wav(audio_file_path)
            mp3_file_path = audio_file_path.replace(".wav", ".mp3")
            audio.export(mp3_file_path, format="mp3")
            
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            with open(mp3_file_path, "rb") as f:
                audio_data = f.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        return {
            "message": output_message,
            "audio_data": audio_base64,  # 保存为base64编码的字符串，用于前端播放
            "audio_file": mp3_file_path if audio_base64 else None,
            "extra_info": extra_info,
            "duration": duration
        }

    except Exception as e:
        print(f"API请求失败: {e}")
        message = "API请求失败: " + str(e)
        return {"message": message}

# 以下为测试功能时的示例代码

# 使用示例
# if __name__ == "__main__":
#     async def main():
#         result = await generate_audio(
#             text="七七今天想吃椰奶！",  # 不超过100字的文本
#             language="中文",                # 语言代码
#             speaker="七七"  ,     # 说话者名称
#             url = url,  # Hugging Face Space URL
#             # 以下参数可选，保持None则使用API默认值
#             # noise_scale=0.5,
#             # noise_scale_w=0.6,
#             # length_scale=1.0
#         )

#         if result:
#             print(f"输出信息: {result['message']}")
#             print(f"附加信息: {result['extra_info']}")
#             if result['audio_file']:
#                 print(f"音频已保存至: {result['audio_file']}")

#     asyncio.run(main())