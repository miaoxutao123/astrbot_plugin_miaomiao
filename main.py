from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register

@register("miaomiao", "miaomiao", "喵喵开发的第一个插件", "0.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("喵")
    async def miaomiaomiao(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        yield event.plain_result(f"喵喵喵, {user_name}!") # 发送一条纯文本消息
