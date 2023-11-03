import os
from moviepy.editor import *
from spleeter.separator import Separator
from pydub import AudioSegment
import re

# 分离音频
def extract_audio_from_video(video_path):
    # 获取文件名和目录
    dir_name = os.path.dirname(video_path)
    base_name = os.path.basename(video_path)
    file_name, _ = os.path.splitext(base_name)

    # 使用moviepy提取音频
    video = VideoFileClip(video_path)
    audio = video.audio

    # 定义导出的音频文件路径
    mp3_path = os.path.join(dir_name, file_name + '.mp3')

    # 导出音频为mp3格式
    audio.write_audiofile(mp3_path, codec='mp3')
    print(f"Audio saved as {file_name}.mp3 in {dir_name}")
    return mp3_path


# 分离人声
def separate_audio(input_path):
    """
    Separate an audio file into stems using Spleeter and save the separated files
    in the same directory as the input file with added suffixes.

    :param input_path: The path to the input MP3 file.
    :return: A list of paths to the separated audio files.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")

    # 初始化Spleeter的分离器
    separator = Separator('spleeter:2stems')

    # 获取输入文件的目录和文件名
    file_directory = os.path.dirname(input_path)
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    # 准备输出目录，与输入文件在同一目录下
    output_directory = os.path.join(file_directory, 'output_separator')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 进行音轨分离
    separator.separate_to_file(input_path, output_directory)

    # 构造分离后的文件路径
    vocals_path = os.path.join(output_directory, file_name , 'vocals.wav')
    accompaniment_path = os.path.join(output_directory, file_name , 'accompaniment.wav')

    # 检查文件是否生成
    if not os.path.isfile(vocals_path) or not os.path.isfile(accompaniment_path):
        raise Exception("Spleeter failed to separate the audio.")

    # 返回分离出的音轨文件路径
    return [vocals_path, accompaniment_path]

# 格式转换
def convert_to_mp3(audio_path):
    """
    Converts an audio file to MP3 format.

    :param audio_path: Path to the input audio file.
    :return: Path to the output MP3 file.
    """
    # 确定输出文件的路径
    base, ext = os.path.splitext(audio_path)
    output_path = f"{base}.mp3"

    # 如果输入文件已经是MP3格式，并且文件已存在，就没有转换的必要
    if ext.lower() == '.mp3' and os.path.exists(output_path):
        print(f"File is already in MP3 format: {output_path}")
        return output_path

    # 载入原始音频文件
    audio = AudioSegment.from_file(audio_path)

    # 导出为MP3
    audio.export(output_path, format='mp3')

    return output_path

