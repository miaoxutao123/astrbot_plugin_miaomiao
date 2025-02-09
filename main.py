from astrbot.api.all import *
import base64
from gradio_client import Client
import random
from typing import AsyncGenerator


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

    @command_group("math")
    def math(self):
        pass

    @math.command("add")
    async def add(self, event: AstrMessageEvent, a: int, b: int):
        # /math add 1 2 -> 结果是: 3
        yield event.plain_result(f"结果是: {a + b}")

    @math.command("sub")
    async def sub(self, event: AstrMessageEvent, a: int, b: int):
        # /math sub 1 2 -> 结果是: -1
        yield event.plain_result(f"结果是: {a - b}")

    
    @llm_tool(name="gpt-sovits") # 如果 name 不填，将使用函数名
    async def gptsovits(self, event: AstrMessageEvent, Character_Name: str, tts_message: str) ->  MessageEventResult:
        '''
        当用户想要听某一个角色的语音时，或者用户想要和某一个角色语音对话时，调用这个函数，当用户想要和一个角色语音对话时，先联网搜索并思考角色会怎样回答这个问题，然后生成回答，回答越简单宇浩，不可超过100字。
        角色只包含以下几个：特别周、无声铃鹿、东海帝皇（帝宝，帝王）、丸善斯基、富士奇迹、小栗帽、黄金船、伏特加、大和赤骥、大树快车、草上飞、菱亚马逊、目白麦昆、神鹰、好歌剧、成田白仁、鲁道夫象征（皇帝）、气槽、爱丽数码、星云天空、玉藻十字、美妙姿势、琵琶晨光、摩耶重炮、曼城茶座、美浦波旁、目白赖恩、菱曙、雪中美人、米浴、艾尼斯风神、爱丽速子（爱丽快子）、爱慕织姬、稻荷一、胜利奖券、空中神宫、荣进闪耀、真机伶、川上公主、黄金城（黄金城市）、樱花进王、采珠、新光风、东商变革、超级小海湾、醒目飞鹰（寄寄子）、荒漠英雄、东瀛佐敦、中山庆典、成田大进、西野花、春丽（乌拉拉）、青竹回忆、微光飞驹、美丽周日、待兼福来、mr cb（cb先生）、名将怒涛（名将户仁）、目白多伯、优秀素质、帝王光辉、待兼诗歌剧、生野狄杜斯、目白善信、大拓太阳神、双涡轮（两立直，两喷射，二锅头，逆喷射）、里见光钻（萨托诺金刚石）、北部玄驹、樱花千代王、天狼星象征、目白阿尔丹、八重无敌、鹤丸刚志、目白光明、成田拜仁（成田路）、也文摄辉、小林历奇、北港火山、奇锐骏、苦涩糖霜、小小蚕茧、骏川手纲（绿帽恶魔）、秋川弥生（小小理事长）、乙名史悦子（乙名记者）、桐生院葵、安心泽刺刺美、樫本理子、神里绫华（龟龟）、琴、空（空哥）、丽莎、荧（荧妹）、芭芭拉、凯亚、迪卢克、雷泽、安柏、温迪、香菱、北斗、行秋、魈、凝光、可莉、钟离、菲谢尔（皇女）、班尼特、达达利亚（公子）、诺艾尔（女仆）、七七、重云、甘雨（椰羊）、阿贝多、迪奥娜（猫猫）、莫娜、刻晴、砂糖、辛焱、罗莎莉亚、胡桃、枫原万叶（万叶）、烟绯、宵宫、托马、优菈、雷电将军（雷神）、早柚、珊瑚宫心海（心海，扣扣米）、五郎、九条裟罗、荒泷一斗（一斗）、埃洛伊、申鹤、八重神子（神子）、神里绫人（绫人）、夜兰、久岐忍、鹿野苑平藏、提纳里、柯莱、多莉、云堇、纳西妲（草神）、深渊使徒、妮露、赛诺、债务处理人、坎蒂丝、真弓快车、秋人、望族、艾尔菲、艾莉丝、艾伦、阿洛瓦、天野、天目十五、愚人众-安德烈、安顺、安西、葵、青木、荒川幸次、荒谷、有泽、浅川、麻美、凝光助手、阿托、竺子、百识、百闻、百晓、白术、贝雅特丽奇、丽塔、失落迷迭、缭乱星棘、伊甸、伏特加女孩、狂热蓝调、莉莉娅、萝莎莉娅、八重樱、八重霞、卡莲、第六夜想曲、卡萝尔、姬子、极地战刃、布洛妮娅、次生银翼、理之律者%26希儿、理之律者、迷城骇兔、希儿、魇夜星渊、黑希儿、帕朵菲莉丝、不灭星锚、天元骑英、幽兰黛尔、派蒙bh3、爱酱、绯玉丸、德丽莎、月下初拥、朔夜观星、暮光骑士、格蕾修、留云借风真君、梅比乌斯、仿犹大、克莱因、圣剑幽兰黛尔、妖精爱莉、特斯拉zero、苍玄、若水、西琳、戴因斯雷布、贝拉、赤鸢、镇魂歌、渡鸦、人之律者、爱莉希雅、天穹游侠、琪亚娜、空之律者、薪炎之律者、云墨丹心、符华、识之律者、特瓦林、维尔薇、芽衣、雷之律者、断罪影舞、阿波尼亚、榎本、厄尼斯特、恶龙、范二爷、法拉、愚人众士兵、愚人众士兵a、愚人众士兵b、愚人众士兵c、愚人众a、愚人众b、飞飞、菲利克斯、女性跟随者、逢岩、摆渡人、狂躁的男人、奥兹、芙萝拉、跟随者、蜜汁生物、黄麻子、渊上、藤木、深见、福本、芙蓉、古泽、古田、古山、古谷昇、傅三儿、高老六、矿工冒、元太、德安公、茂才公、杰拉德、葛罗丽、金忽律、公俊、锅巴、歌德、阿豪、狗三儿、葛瑞丝、若心、阿山婆、怪鸟、广竹、观海、关宏、蜜汁卫兵、守卫1、傲慢的守卫、害怕的守卫、贵安、盖伊、阿创、哈夫丹、日语阿贝多（野岛健儿）、日语埃洛伊（高垣彩阳）、日语安柏（石见舞菜香）、日语神里绫华（早见沙织）、日语神里绫人（石田彰）、日语白术（游佐浩二）、日语芭芭拉（鬼头明里）、日语北斗（小清水亚美）、日语班尼特（逢坂良太）、日语坎蒂丝（柚木凉香）、日语重云（齐藤壮马）、日语柯莱（前川凉子）、日语赛诺（入野自由）、日语戴因斯雷布（津田健次郎）、日语迪卢克（小野贤章）、日语迪奥娜（井泽诗织）、日语多莉（金田朋子）、日语优菈（佐藤利奈）、日语菲谢尔（内田真礼）、日语甘雨（上田丽奈）、日语（畠中祐）、日语鹿野院平藏（井口祐一）、日语空（堀江瞬）、日语荧（悠木碧）、日语胡桃（高桥李依）、日语一斗（西川贵教）、日语凯亚（鸟海浩辅）、日语万叶（岛崎信长）、日语刻晴（喜多村英梨）、日语可莉（久野美咲）、日语心海（三森铃子）、日语九条裟罗（濑户麻沙美）、日语丽莎（田中理惠）、日语莫娜（小原好美）、日语纳西妲（田村由加莉）、日语妮露（金元寿子）、日语凝光（大原沙耶香）、日语诺艾尔（高尾奏音）、日语奥兹（增谷康纪）、日语派蒙（古贺葵）、日语琴（斋藤千和）、日语七七（田村由加莉）、日语雷电将军（泽城美雪）、日语雷泽（内山昂辉）、日语罗莎莉亚（加隈亚衣）、日语早柚（洲崎绫）、日语散兵（柿原彻也）、日语申鹤（川澄绫子）、日语久岐忍（水桥香织）、日语女士（庄子裕衣）、日语砂糖（藤田茜）、日语达达利亚（木村良平）、日语托马（森田成一）、日语提纳里（小林沙苗）、日语温迪（村濑步）、日语香菱（小泽亚李）、日语魈（松冈祯丞）、日语行秋（皆川纯子）、日语辛焱（高桥智秋）、日语八重神子（佐仓绫音）、日语烟绯（花守由美里）、日语夜兰（远藤绫）、日语宵宫（植田佳奈）、日语云堇（小岩井小鸟）、日语钟离（前野智昭）、杰克、阿吉、江舟、鉴秋、嘉义、纪芳、景澄、经纶、景明、晋优、阿鸠、酒客、乔尔、乔瑟夫、约顿、乔伊斯、居安、君君、顺吉、纯也、重佐、大岛纯平、蒲泽、勘解由小路健三郎、枫、枫原义庆、荫山、甲斐田龍馬、海斗、惟神晴之介、鹿野奈奈、卡琵莉亚、凯瑟琳、加藤信悟、加藤洋平、胜家、茅葺一庆、和昭、一正、一道、桂一、庆次郎、阿贤、健司、健次郎、健三郎、天理、杀手a、杀手b、木南杏奈、木村、国王、木下、北村、清惠、清人、克列门特、骑士、小林、小春、康拉德、大肉丸、琴美、宏一、康介、幸德、高善、梢、克罗索、久保、九条镰治、久木田、昆钧、菊地君、久利须、黑田、黑泽京之介、响太、岚姐、兰溪、澜阳、劳伦斯、乐明、莱诺、莲、良子、李当、李丁、小乐、灵、小玲、琳琅a、琳琅b、小彬、小德、小楽、小龙、小吴、小吴的记忆、理正、阿龙、卢卡、洛成、罗巧、北风狼、卢正、萍姥姥、前田、真昼、麻纪、真、愚人众-马克西姆、女性a、女性b、女性a的跟随者、阿守、玛格丽特、真理、玛乔丽、玛文、正胜、昌信、将司、正人、路爷、老章、松田、松本、松浦、松坂、老孟、孟丹、商人随从、传令兵、米歇尔、御舆源一郎、御舆源次郎、千岩军教头、千岩军士兵、明博、明俊、美铃、美和、阿幸、削月筑阳真君、钱眼儿、森彦、元助、理水叠山真君、理水疊山真君、朱老板、木木、村上、村田、永野、长野原龙之介、长濑、中野志乃、菜菜子、楠楠、成濑、阿内、宁禄、牛志、信博、伸夫、野方、诺拉、纪香、诺曼、修女、纯水精灵、小川、小仓澪、冈林、冈崎绘里香、冈崎陆斗、奥拉夫、老科、鬼婆婆、小野寺、大河原五右卫门、大久保大介、大森、大助、奥特、派蒙、派蒙2、病人a、病人b、巴顿、派恩、朋义、围观群众、围观群众a、围观群众b、围观群众c、围观群众d、围观群众e、铜雀、阿肥、兴叔、老周叔、公主、彼得、乾子、芊芊、乾玮、绮命、杞平、秋月、昆恩、雷电影、兰道尔、雷蒙德、冒失的帕拉德、伶一、玲花、阿仁、家臣们、梨绘、荣江、戎世、浪人、罗伊斯、如意、凉子、彩香、酒井、坂本、朔次郎、武士a、武士b、武士c、武士d、珊瑚、三田、莎拉、笹野、聪美、聪、小百合、散兵、害怕的小刘、舒伯特、舒茨、海龙、世子、谢尔盖、家丁、商华、沙寅、阿升、柴田、阿茂、式大将、清水、志村勘兵卫、新之丞、志织、石头、诗羽、诗筠、石壮、翔太、正二、周平、舒杨、齐格芙丽雅、女士、思勤、六指乔瑟、愚人众小兵d、愚人众小兵a、愚人众小兵b、愚人众小兵c、吴老五、吴老二、滑头鬼、言笑、吴老七、士兵h、士兵i、士兵a、士兵b、士兵c、士兵d、士兵e、士兵f、士兵g、奏太、斯坦利、掇星攫辰天君、小头、大武、陶义隆、杉本、苏西、嫌疑人a、嫌疑人b、嫌疑人c、嫌疑人d、斯万、剑客a、剑客b、阿二、忠胜、忠夫、阿敬、孝利、鹰司进、高山、九条孝行、毅、竹内、拓真、卓也、太郎丸、泰勒、手岛、哲平、哲夫、托克、大boss、阿强、托尔德拉、旁观者、天成、阿大、蒂玛乌斯、提米、户田、阿三、一起的人、德田、德长、智树、利彦、胖乎乎的旅行者、藏宝人a、藏宝人b、藏宝人c、藏宝人d、阿祇、恒雄、露子、话剧团团长、内村、上野、上杉、老戴、老高、老贾、老墨、老孙、天枢星、老云、有乐斋、丑雄、乌维、瓦京、菲尔戈黛特、维多利亚、薇尔、瓦格纳、阿外、侍女、瓦拉、望雅、宛烟、琬玉、战士a、战士b、渡辺、渡部、阿伟、文璟、文渊、韦尔纳、王扳手、武沛、晓飞、辛程、星火、星稀、辛秀、秀华、阿旭、徐刘师、矢部、八木、山上、阿阳、颜笑、康明、泰久、安武、矢田幸喜、矢田辛喜、义坚、莺儿、盈丰、宜年、银杏、逸轩、横山、永贵、永业、嘉久、吉川、义高、用高、阳太、元蓉、玥辉、毓华、有香、幸也、由真、结菜、韵宁、百合、百合华、尤苏波夫、裕子、悠策、悠也、于嫣、柚子、老郑、正茂、志成、芷巧、知易、支支、周良、珠函、祝明
        Args:
            Character_Name(string): 需要调用的tts角色名称
            tts_message(string): 需要转换的文本
        '''
        yield event.plain_result(f"喵喵人正在给{Character_Name}打电话，请稍等片刻。") # 发送一条纯文本消息
        result = generate_audio(
        text = tts_message,  # 不超过100字的文本
        language="中文",                # 语言代码
        speaker=Character_Name       # 说话者名称
        # 以下参数可选，保持None则使用API默认值
        # noise_scale=0.5,
        # noise_scale_w=0.6,
        # length_scale=1.0
        )
        chain = [
        At(qq=event.get_sender_id()), # At 消息发送者
        Record(audio_base64=result["audio_data"]) # 发送语音消息
        ]
        yield event.chain_result(chain)

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