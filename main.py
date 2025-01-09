from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.all import *
import random


@register("miaomiao", "miaomiao", "喵喵开发的第一个插件", "0.0.2")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("喵")
    async def miaomiaomiao(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        yield event.plain_result(f"喵喵喵, {user_name}!") # 发送一条纯文本消息

    @filter.command("今天吃什么呀")
    async def eat(self, event: AstrMessageEvent):
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

    @filter.command("扔个骰子")
    async def random(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        touzi_num = random.randint(1,6)
        yield event.plain_result(f"{user_name}扔出了{touzi_num}!") # 发送一条纯文本消息
    
    @command_group("tts")
    def tts(self):
        pass

    @tts.command("paimeng")
    async def tts(self, event: AstrMessageEvent,message:str):
        #message = event.get_message_str()
        yield event.plain_result(f"派蒙说{message}")