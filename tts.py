import os
import re
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat, ResultReason, CancellationReason

from conf.config import *


# 文本转语音
def text_to_speech_microsoft(text, output_folder,output_file):
    # 设置语音服务的配置
    speech_config = SpeechConfig(subscription=tts_subscription_key, region=tts_service_region)
    
    # 设置发言人
    speech_config.speech_synthesis_voice_name = tts_voice_name
    
    # 确保输出目录存在
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
        
    # 设置输出音频文件路径
    audio_output_path = os.path.join(output_folder, output_file)
    # 设置音频输出的配置
    audio_config = AudioConfig(filename=audio_output_path)
    # 初始化语音合成器
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    # 进行文本到语音的合成
    result = synthesizer.speak_text_async(text).get()
    
    # 检查结果
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text: [{text}], and the audio was saved to: [{audio_output_path}]")
    elif result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")

    # 返回音频文件的路径
    return audio_output_path


# 字幕生成音频
def convert_subtitles_to_speech(subtitle_path):
    # 验证字幕文件是否存在
    if not os.path.isfile(subtitle_path):
        raise FileNotFoundError(f"The file {subtitle_path} does not exist.")
    
    # 从字幕文件名中获取文件夹名称
    base_name = os.path.splitext(os.path.basename(subtitle_path))[0]
    subtitles_dir = os.path.dirname(subtitle_path)
    audio_output_folder = os.path.join(subtitles_dir, base_name)

    # 如果存储语音的目录不存在，创建它
    if not os.path.exists(audio_output_folder):
        os.makedirs(audio_output_folder)

    # 打开字幕文件
    with open(subtitle_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()

    # 使用正则表达式查找所有字幕
    subtitles = re.finditer(r'(?P<index>\d+)\n(?P<start>\d{2}:\d{2}:\d{2},\d{3}) --> (?P<end>\d{2}:\d{2}:\d{2},\d{3})\n(?P<text>.+?)(?=\n\n|\Z)', content, re.DOTALL)

    # 存储生成的音频文件路径
    audio_file_paths = []

    # 逐条处理字幕
    for match in subtitles:
        index = match.group('index')
        text = match.group('text').replace('\n', ' ')  # 去除字幕中的换行符
        audio_filename = f"{index}.mp3"
        audio_file_path = os.path.join(audio_output_folder, audio_filename)

        # 调用 text_to_speech 方法来转换文本到语音
        text_to_speech_microsoft(
            text,
            audio_output_folder,
            audio_filename
        )

        # 添加到列表中
        audio_file_paths.append(audio_file_path)

    print(f"All subtitles have been converted to audio files in {audio_file_paths}.")
    return audio_file_paths



if __name__ == '__main__':
    pass
    # text_to_speak = "今天天气怎么样"
    # output_folder = "./audio_output"
    # # 调用函数
    # audio_file_path = text_to_speech_microsoft(text_to_speak, output_folder,"output.mp3")
    # print(audio_file_path)
    convert_subtitles_to_speech("./test/output_separator/malaxiya/vocals_translated.srt")
