import base64
from gradio_client import Client

def generate_audio(text, language, speaker, noise_scale=0.5, noise_scale_w=0.5, length_scale=1.0):
    client = Client("https://miaomiaoren-vits-uma-genshin-honkai.hf.space/")
    
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
        result = client.predict(*payload, api_name="/generate")
        
        # 打印调试信息
        print("API响应:", result)
        
        # 解析响应数据
        output_message = result[0]
        audio_base64 = result[1]
        extra_info = result[2]
        duration = result[3]

        # 如果有音频数据则保存为文件
        if audio_base64:
            audio_data = base64.b64decode(audio_base64.split(",")[-1])
            with open("output_audio.wav", "wb") as f:
                f.write(audio_data)

        return {
            "message": output_message,
            "audio_data": audio_base64,  # 保存为base64编码的字符串，用于前端播放"
            "audio_file": "output_audio.wav" if audio_base64 else None,
            "extra_info": extra_info,
            "duration": duration
        }

    except Exception as e:
        print(f"API请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    result = generate_audio(
        text="你好,这是一个测试文本",  # 不超过100字的文本
        language="中文",                # 语言代码
        speaker="胡桃"       # 说话者名称
        # 以下参数可选，保持None则使用API默认值
        # noise_scale=0.5,
        # noise_scale_w=0.6,
        # length_scale=1.0
    )

    if result:
        print(f"生成耗时: {result['duration']}秒")
        print(f"输出信息: {result['message']}")
        print(f"附加信息: {result['extra_info']}")
        if result['audio_file']:
            print(f"音频已保存至: {result['audio_file']}")