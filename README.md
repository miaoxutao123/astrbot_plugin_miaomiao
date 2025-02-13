# AstrBot Plugin Miaomiao
# 喵喵的插件

这是一个为 AstrBot 开发的插件，仍然在开发中，提供了一些有趣的功能，如随机推荐食物、扔骰子、生成语音等。


## 安装

通过插件管理安装本仓库链接： 
https://github.com/miaoxutao123/astrbot_plugin_miaomiao

## 依赖库

**安装前确保在控制台的 pip 库安装界面下，安装以下所需库，并确保你的bot所在网络环境能访问huggingface space：**
**确保安装了 `ffmpeg`，并且在系统路径中可用。**

- typing
- pyhub
- gradio

## 功能

### 喵喵喵
发送 `/喵` 指令，机器人会回复 `喵喵喵, {user_name}!`。

### 今天吃什么呀
发送 `/今天吃什么呀` 指令，机器人会随机推荐一种食物。

### 扔个骰子
发送 `/扔个骰子` 指令，机器人会随机生成一个 1 到 6 的数字。

### gpt-sovits
插件核心功能之一，使用gradio调用部署在huggingface space上的tts服务实现大模型自主调用指定角色的 TTS 语音功能，生成语音消息。

### 喜报生成器
发送 `/喜报 {消息}` 指令，生成一张带有指定消息的喜报图片。(copy by https://github.com/Soulter/astrbot_plugin_essential)
