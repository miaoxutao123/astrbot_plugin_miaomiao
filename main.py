from astrbot.api.all import *
import base64
import random
from typing import AsyncGenerator
from .tts_test import generate_audio 
from .ttp import generate_image
from .office import *
import os
from PIL import Image as PILImage, ImageDraw as PILImageDraw, ImageFont as PILImageFont
import time
import matplotlib.font_manager as fm
from .get_song import search_song
import requests
from .file_send_server import send_file
from astrbot.api.event import filter, AstrMessageEvent
import re

def get_valid_font(font_name, default_font="Arial"):
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    if font_name in available_fonts:
        return font_name
    else:
        return default_font

@register("miaomiao", "miaomiao", "喵喵开发的第一个插件", "1.2.3","https://github.com/miaoxutao123/astrbot_plugin_miaomiao")
class miaomiao(Star):
    def __init__(self, context: Context,config: dict):
        super().__init__(context)
        self.api_key = config.get("api_key")
        self.huggingface_api_url = config.get("huggingface_api_url")
        self.model = config.get("model")
        self.image_size = config.get("image_size")
        self.nap_server_address = config.get("nap_server_address")
        self.nap_server_port = config.get("nap_server_port")
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
        When the user wants to hear a specific character's voice, or wants to engage in a voice conversation or ask questions to a specific character, call this function.
        When the user initiates a voice conversation with a character, first search online and consider how the character would respond to the query, then generate a response in Chinese exclusively. The response must be in Chinese (to ensure compatibility with the TTS service), as concise as possible, and must not exceed 100 words. The response should be narrated in the first person, as if the character is speaking. If the request fails, inform the user of the reason for the failure.
        Available characters are limited to:派蒙、神里绫华（龟龟）、琴、空（空哥）、丽莎、荧（荧妹）、
        芭芭拉、凯亚、迪卢克、雷泽、安柏、温迪、香菱、北斗、行秋、魈、凝光、可莉、钟离、
        菲谢尔（皇女）、班尼特、达达利亚（公子）、诺艾尔（女仆）、七七、重云、甘雨（椰羊）、
        阿贝多、迪奥娜（猫猫）、莫娜、刻晴、砂糖、辛焱、罗莎莉亚、胡桃、枫原万叶（万叶）、
        烟绯、宵宫、托马、优菈、雷电将军（雷神）、早柚、珊瑚宫心海（心海，扣扣米）、
        五郎、九条裟罗、荒泷一斗（一斗）、埃洛伊、申鹤、八重神子（神子）、神里绫人（绫人）、
        夜兰、久岐忍、鹿野苑平藏、提纳里、柯莱、多莉、云堇、纳西妲（草神）、深渊使徒、妮露、赛诺
        Args:
            Character_Name (string): The name of the TTS character to invoke 
            tts_message (string): The text to be converted (must be in Chinese)
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

    # @llm_tool("duckduckgo_web_search")
    # async def search_from_search_engine(self, event: AstrMessageEvent, query: str) -> str:
    #     '''Search the web for answers to the user's query
        
    #     Args:
    #         query(string): A search query which will be used to fetch the most relevant snippets regarding the user's query
    #     '''
    #     return await search_from_search_engine(query)
    
    @llm_tool(name="pic-gen")
    async def pic_gen(self, event: AstrMessageEvent, prompt: str) -> str:
        '''
        When a user requires image generation or drawing, and asks you to create an image, Or when you need to create a drawing to demonstrate or present something to the user.
        call this function. If the image description provided by the user is not in English, 
        translate it into English and reformat it to facilitate generation by the stable-diffusion model.
        Enrich the prompt with additional details to achieve better results, the more detailed the better.
        Args:
            prompt(string): image description
        '''
        api_key = self.api_key
        model = self.model
        image_size = self.image_size
        image_url, image_path = generate_image(prompt,api_key,model=model,image_size=image_size)
        chain = [Image.fromURL(image_url)]
        yield event.chain_result(chain)
    
    @llm_tool(name="music_search")
    async def music_search(self, event: AstrMessageEvent, music_name: str, singer: str, search_type: str = "qq") -> str:
        '''
        Use this tool when you think it's needed or users need. Search for songs by song name and singer.
        Note: The song must be a real, existing song to avoid search errors.
        Args: 
            music_name (string): The name of the song
            singer (string): The name of the singer
            search_type (string): The search engine to use (default: "qq", choose from "qq", "neteasy", "kugou", "kuwo")
        '''
        try:
            # 调用 search_song 函数进行歌曲搜索
            json_data = search_song(music_name, singer, search_type)
            
            if not json_data:
                yield event.plain_result("未找到相关歌曲信息。")
                return
            
            # 获取歌曲信息
            songs = json_data.get("data", [])
            if not songs:
                yield event.plain_result("未找到相关歌曲信息。")
                return
            
            # 构建返回消息
            result_message = "找到以下歌曲信息：\n"
            song = songs[0]
            title = song.get("title", "未知歌曲")
            author = song.get("author", "未知作者")
            link = song.get("link", "无链接")
            lrc = song.get("lrc", "无歌词")
            download_url = song.get("url", "无下载链接")
            pic = song.get("pic", "无封面图")
            
            # 本地文件路径
            file_path = "downloaded_song.m4a"

            # 发送 GET 请求下载文件
            response = requests.get(download_url, stream=True)

            # 检查请求是否成功
            if response.status_code == 200:
                # 打开本地文件进行写入
                with open(file_path, 'wb') as file:
                    # 分块写入文件
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"歌曲已成功下载并保存到 {file_path}")
            else:
                print(f"下载失败，状态码: {response.status_code}")

            chain = [
                Plain(f"歌曲标题: {title}\n"),
                Plain(f"作者: {author}\n"),
                Image.fromURL(pic),
                Record(file = file_path),
                ]
            yield event.chain_result(chain)
        except Exception as e:
            yield event.plain_result(f"搜索歌曲时出错: {str(e)}")
        
    @llm_tool(name="office")
    async def office_tool(self, event: AstrMessageEvent, doc_type: str, action: str, file_path: str, 
                        title: str = "", subtitle: str = "", content: str = "", 
                        title_font: str = "", title_color: str = "0,0,0", subtitle_font: str = "", subtitle_color: str = "0,0,0",
                        content_font: str = "", content_color: str = "0,0,0", sheet_name: str = "", data: str = "[]",
                        title_size: int = 0, subtitle_size: int = 0, content_size: int = 0) -> str:
        '''
        Avatar
            If the user requests that you generate or process an Office file, such as a Word or Excel document, 
            you must strictly adhere to the specified parameters to call the office processing function. Do not pass in any additional parameters beyond those provided,
            as the font service has not been successfully built.
            Therefore, do not include any font-related parameters.
            Additionally, ensure that all content is generated in a single batch to avoid partial outputs or multiple iterations.
        Args:
            doc_type (string): Document type (required, 'word' or 'excel')
            action (string): Operation type (required, 'create' or 'modify')
            file_path (string): File path (required, format: /data/plugins/astrbot_plugin_miaomiao/gen_doc/filename.extension)
            title (string): Title
            subtitle (string): Subtitle(required)
            content (string): Content
            title_font (string): Title font
            title_size (number): Title font size
            title_color (string): Title color (format: "R,G,B")
            subtitle_font (string): Subtitle font
            subtitle_size (number): Subtitle font size
            subtitle_color (string): Subtitle color (format: "R,G,B")
            content_font (string): Content font
            content_size (number): Content font size
            content_color (string): Content color (format: "R,G,B")
            sheet_name (string): Sheet name (only for Excel)
            data (string): Data (only for Excel), JSON string format
        '''
        try:
            # 检查并创建文件夹
            folder_path = os.path.dirname(file_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # 检查并获取有效的字体
            title_font = get_valid_font(title_font, "Arial")
            subtitle_font = get_valid_font(subtitle_font, "Arial")
            content_font = get_valid_font(content_font, "Arial")

            # 将颜色字符串解析为元组
            title_color = tuple(map(int, title_color.split(',')))
            subtitle_color = tuple(map(int, subtitle_color.split(',')))
            content_color = tuple(map(int, content_color.split(',')))
            if data:
                # 将 JSON 字符串解析为列表
                data = json.loads(data)

            # 根据文档类型过滤参数
            if doc_type == 'word':
                # # 去掉前面的data/plugins/astrbot_plugin_miaomiao/部分
                # file_path = file_path.replace("data/plugins/astrbot_plugin_miaomiao/", "")
                kwargs = {
                    'file_path': file_path,
                    'title': title,
                    'subtitle': subtitle,
                    'content': content,
                    'title_font': title_font,
                    'title_size': title_size,
                    'title_color': title_color,
                    'subtitle_font': subtitle_font,
                    'subtitle_size': subtitle_size,
                    'subtitle_color': subtitle_color,
                    'content_font': content_font,
                    'content_size': content_size,
                    'content_color': content_color
                }
            elif doc_type == 'excel':
                # # 去掉前面的data/plugins/astrbot_plugin_miaomiao/部分
                # file_path = file_path.replace("data/plugins/astrbot_plugin_miaomiao/", "")
                kwargs = {
                    'file_path': file_path,
                    'sheet_name': sheet_name,
                    'title': title,
                    'data': data,
                    'title_font': title_font,
                    'title_size': title_size,
                    'title_color': title_color
                }
            print("正在处理文档...")
            handle_document(doc_type, action, **kwargs)
            if self.nap_server_address !="localhost":
                print("文档处理完成！正在尝试发送文件到服务端...")
                nap_file_path = send_file(file_path, HOST=self.nap_server_address, PORT=self.nap_server_port)
                print(nap_file_path)
                file_name = os.path.basename(file_path)
                file_dir = os.path.dirname(file_path)
                print(f"文件名: {file_name}")
                print(f"文件目录: {file_dir}")
            else :
                print("文档处理完成！")
                nap_file_path = file_path
                file_name = os.path.basename(file_path)
                file_dir = os.path.dirname(file_path)
                print(f"文件名: {file_name}")
                print(f"文件目录: {file_dir}")
            file = File(name=file_name, file=nap_file_path)
            yield event.chain_result([file])
            print("文件发送完成！")
            rrr = doc_type +"文档已成功!" + action
            yield rrr
        except Exception as e:
            rrr = "处理 "+doc_type+"文档时出错:" + str(e)
            print(rrr)
            yield rrr
            
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

