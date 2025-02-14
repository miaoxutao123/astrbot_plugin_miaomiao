from astrbot.api.all import *
import base64
import random
from typing import AsyncGenerator
from .tts_test import generate_audio 
from .ttp import generate_image
import os
from PIL import Image as PILImage, ImageDraw as PILImageDraw, ImageFont as PILImageFont

@register("miaomiao", "miaomiao", "喵喵开发的第一个插件", "1.0","https://github.com/miaoxutao123/astrbot_plugin_miaomiao")
class miaomiao(Star):
    def __init__(self, context: Context,config: dict):
        super().__init__(context)
        self.api_key = config.get("api_key")
        self.huggingface_api_url = config.get("huggingface_api_url")
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @command("喵")
    async def miaomiaomiao(self, event: AstrMessageEvent):
        '''喵喵喵喵喵'''
        user_name = event.get_sender_name()
        yield event.plain_result(f"喵喵喵, {user_name}!") # 发送一条纯文本消息

    @command("今天吃什么呀")
    async def eat(self, event: AstrMessageEvent):
        '''随机推荐一种食物'''
        user_name = event.get_sender_name()
        foods = [
        "红烧肉", "西红柿炒鸡蛋", "青椒土豆丝", "鱼香肉丝", "宫保鸡丁", 
        "麻婆豆腐", "清炒菠菜", "酸辣土豆丝", "糖醋排骨", "蒜蓉空心菜", 
        "回锅肉", "干煸四季豆", "红烧茄子", "清蒸鲈鱼", "可乐鸡翅", 
        "香菇炒青菜", "蒜蓉西兰花", "酱爆茄子", "水煮肉片", "酸菜鱼", 
        "红烧鸡翅", "清炒豆角", "鱼头豆腐汤", "凉拌黄瓜", "炒三丝", 
        "蒜蓉粉丝蒸扇贝", "红烧狮子头", "清炒芦笋", "糖醋里脊", "葱爆羊肉", 
        "蚝油生菜", "红烧带鱼", "清炒虾仁", "干锅花菜", "酸辣白菜", 
        "酱牛肉", "蒜蓉蒸茄子", "红烧排骨", "清炒西葫芦", "鱼香茄子", 
        "干锅土豆片", "蒜蓉蒸虾", "红烧鸡腿", "清炒芥蓝", "糖醋鲤鱼", 
        "凉拌木耳", "炒鸡蛋", "蒜蓉蒸排骨", "红烧牛腩", "清炒油麦菜", 
        "干锅肥肠", "蒜蓉蒸鲍鱼", "红烧猪蹄", "清炒茼蒿", "糖醋鸡块", 
        "凉拌海带丝", "炒牛肉", "蒜蓉蒸豆腐", "红烧鱼块", "清炒莴笋", 
        "干锅鸡翅", "蒜蓉蒸扇贝", "红烧鸭块", "清炒芹菜", "糖醋虾仁", 
        "凉拌豆腐皮", "炒鸡肉", "蒜蓉蒸南瓜", "红烧羊肉", "清炒小白菜", 
        "干锅排骨", "蒜蓉蒸生蚝", "红烧鸡爪", "清炒韭菜", "糖醋带鱼", 
        "凉拌金针菇", "炒猪肉", "蒜蓉蒸丝瓜", "红烧猪肝", "清炒苋菜", 
        "干锅牛蛙", "蒜蓉蒸蛤蜊", "红烧鸡心", "清炒豆苗", "糖醋鱿鱼", 
        "凉拌黄豆芽", "炒鸭肉", "蒜蓉蒸冬瓜", "红烧猪肚", "清炒苦瓜", 
        "干锅虾", "蒜蓉蒸蟹", "红烧鸡胗", "清炒南瓜", "糖醋鳕鱼", 
        "凉拌菠菜", "炒鹅肉", "蒜蓉蒸豆腐皮", "红烧猪耳", "清炒莲藕",
        # 外国菜品
        "意大利面", "披萨", "寿司", "天妇罗", "咖喱饭", 
        "牛排", "炸鱼薯条", "墨西哥卷饼", "法式蜗牛", "西班牙海鲜饭", 
        "泰式冬阴功汤", "越南春卷", "韩式烤肉", "石锅拌饭", "日式拉面", 
        "印度咖喱鸡", "希腊沙拉", "土耳其烤肉", "德国香肠", "瑞士奶酪火锅", 
        "美式汉堡", "夏威夷披萨", "巴西烤肉", "阿根廷牛排", "秘鲁酸橘汁腌鱼", 
        "摩洛哥塔吉锅", "黎巴嫩鹰嘴豆泥", "俄罗斯罗宋汤", "瑞典肉丸", "挪威三文鱼", 
        "比利时华夫饼", "荷兰煎饼", "奥地利炸猪排", "葡萄牙蛋挞", "匈牙利炖牛肉", 
        "波兰饺子", "捷克烤猪肘", "丹麦开放式三明治", "芬兰驯鹿肉", "冰岛发酵鲨鱼肉"
        ]
        choice = random.choice(foods)
        yield event.plain_result(f"喵喵喵{user_name}, 今天吃{choice}吧!") # 发送一条纯文本消息

    @command("扔个骰子")
    async def random(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        touzi_num = random.randint(1,6)
        yield event.plain_result(f"{user_name}扔出了{touzi_num}!") # 发送一条纯文本消息
        

    @llm_tool(name="gpt-sovits")
    async def gptsovits(self, event: AstrMessageEvent, Character_Name: str, tts_message: str):
        '''
        当用户想要听某一个角色的语音时，或者用户想要和某一个角色语音对话或者提问时，调用这个函数，
        当用户想要和一个角色语音对话时，先联网搜索并思考角色会怎样回答这个问题，然后生成回答，回答越简单越好，
        不可超过100字，如果请求失败，告诉用户失败原因。
        角色只包含以下几个：派蒙、神里绫华（龟龟）、琴、空（空哥）、丽莎、荧（荧妹）、
        芭芭拉、凯亚、迪卢克、雷泽、安柏、温迪、香菱、北斗、行秋、魈、凝光、可莉、钟离、
        菲谢尔（皇女）、班尼特、达达利亚（公子）、诺艾尔（女仆）、七七、重云、甘雨（椰羊）、
        阿贝多、迪奥娜（猫猫）、莫娜、刻晴、砂糖、辛焱、罗莎莉亚、胡桃、枫原万叶（万叶）、
        烟绯、宵宫、托马、优菈、雷电将军（雷神）、早柚、珊瑚宫心海（心海，扣扣米）、
        五郎、九条裟罗、荒泷一斗（一斗）、埃洛伊、申鹤、八重神子（神子）、神里绫人（绫人）、
        夜兰、久岐忍、鹿野苑平藏、提纳里、柯莱、多莉、云堇、纳西妲（草神）、深渊使徒、妮露、赛诺
        Args:
            Character_Name(string): 需要调用的tts角色名称
            tts_message(string): 需要转换的文本
        '''
        url = self.huggingface_api_url
        yield event.plain_result(f"喵喵人正在给{Character_Name}打电话，请稍等片刻。")
        try:
            result = await generate_audio(
                url=url,
                text=tts_message,  # 不超过100字的文本
                language="中文",  # 语言代码
                speaker=Character_Name  # 说话者名称
                # 以下参数可选，保持None则使用API默认值
                # noise_scale=0.5,
                # noise_scale_w=0.6,
                # length_scale=1.0
            )
            print(f"generate_audio 返回结果: {result}")
            if result is None or "audio_data" not in result:
                raise ValueError("generate_audio 返回了无效的结果")
            audio_file = result["audio_file"]
            chain = [
                At(qq=event.get_sender_id()),  # At 消息发送者
                Record(file=audio_file)  # 发送语音消息
            ]
            yield event.chain_result(chain)
            msg = Character_Name + "来信啦"
            yield event.plain_result(msg)
            # 删除语音文件
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except Exception as e:
            yield event.plain_result(f"请求失败: {str(e)}")
    
    @llm_tool(name="pic-gen")
    async def pic_gen(self, event: AstrMessageEvent, prompt: str):
        '''
        When a user requires image generation or drawing, and asks you to create an image, Or when you need to create a drawing to demonstrate or present something to the user.
        call this function. If the image description provided by the user is not in English, 
        translate it into English and reformat it to facilitate generation by the stable-diffusion model.
        Args:
            prompt(string): image description
        '''
        api_key = self.api_key
        yield event.plain_result(f"喵喵人正在用魔法画画，请稍等片刻。")
        image_url, image_path = generate_image(prompt,api_key)
        chain = [Image.fromURL(image_url)]
        yield event.chain_result(chain)
        
    @command("喜报")
    async def congrats(self, message: AstrMessageEvent):
        '''喜报生成器'''
        msg = message.message_str.replace("喜报", "").strip()
        for i in range(20, len(msg), 20):
            msg = msg[:i] + "\n" + msg[i:]

        path = os.path.abspath(os.path.dirname(__file__))
        bg = path + "/congrats.jpg"
        img = PILImage.open(bg)
        draw = PILImageDraw.Draw(img)
        font = PILImageFont.truetype(path + "/simhei.ttf", 65)

        # Calculate the width and height of the text
        text_width, text_height = draw.textbbox((0, 0), msg, font=font)[2:4]

        # Calculate the starting position of the text to center it.
        x = (img.size[0] - text_width) / 2
        y = (img.size[1] - text_height) / 2

        draw.text(
            (x, y),
            msg,
            font=font,
            fill=(255, 0, 0),
            stroke_width=3,
            stroke_fill=(255, 255, 0),
        )

        img.save("congrats_result.jpg")
        return CommandResult().file_image("congrats_result.jpg")