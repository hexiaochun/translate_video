import openai
from conf.config import *
openai.api_key =  open_api_key

import os
import requests
import json
import re


# 识别字幕
def transcribe_audio_to_srt(mp3_path):
    # 打开音频文件
    with open(mp3_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file, response_format="srt")

    # 获取文件名和目录
    dir_name = os.path.dirname(mp3_path)
    base_name = os.path.basename(mp3_path)
    file_name, _ = os.path.splitext(base_name)
    # 定义srt文件的路径
    srt_path = os.path.join(dir_name, file_name + '.srt')
    # 写入srt文件
    with open(srt_path, "w") as srt_file:
        srt_file.write(transcript)

    print(f"Transcript has been saved to {srt_path}")

    return srt_path


# 翻译内容
def fanyi_gpt_text(input_msg,chat_history):
     # 保留 chat_history 的最后6条消息
    history_limit = 6
    if len(chat_history) > history_limit:
        chat_history = chat_history[-history_limit:]

    msg = [{"role": "system", "content": gpt_sys_role_content}]
      # 添加历史消息到消息列表
    msg.extend(chat_history)
    
    msg.append({"role": "user", "content": input_msg})
    print(msg)
    response   = translate_english_to_chinese(msg)
    return response['choices'][0]['message']['content']


def translate_english_to_chinese( msg):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open_api_key}"
    }
    data = {
        "model": gpt_model,
        "messages": msg
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
    return response.json()


def translate_subtitle_file(subtitle_path):
    """
    读取字幕文件，翻译每一条字幕，并写入一个新的字幕文件。

    :param subtitle_path: 字幕文件的路径
    :return: 新字幕文件的路径
    """
    # 确保文件存在
    if not os.path.isfile(subtitle_path):
        raise FileNotFoundError(f"The file {subtitle_path} does not exist.")
    
    # 新文件的路径
    base, ext = os.path.splitext(subtitle_path)
    translated_subtitle_path = f"{base}_translated{ext}"

    # 正则表达式匹配字幕文件中的文本
    subtitle_pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*?)\n\n', re.DOTALL)

    # 读取原字幕文件
    with open(subtitle_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 查找所有的字幕文本
    subtitles = subtitle_pattern.findall(content)


    # 翻译字幕文本并替换
    chat_history = []
    for subtitle_text in subtitles:
        translated_text = fanyi_gpt_text(subtitle_text,chat_history)
        chat_history.append({"role": "user", "content": subtitle_text})
        chat_history.append({"role": "assistant", "content": translated_text})
        content = content.replace(subtitle_text, translated_text)
        

    # 写入新的字幕文件
    with open(translated_subtitle_path, 'w', encoding='utf-8') as file:
        file.write(content)

    return translated_subtitle_path