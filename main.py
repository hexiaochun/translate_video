import openai
from conf.config import *
import sys
from moviepy.editor import *
import os
from tts import convert_subtitles_to_speech
from subtitle_audio_merge import create_audio_from_subtitles
from audio import * 
from gpt import *
import subprocess



# 合成新视频
def add_audio_to_video(video_path, voiceover_path, music_path, output_path):
    # 加载视频文件，不带原音轨
    video_clip = VideoFileClip(video_path).without_audio()

    # 加载配音
    voiceover_clip = AudioFileClip(voiceover_path)

    # 加载背景音乐并设置与视频相同的持续时间
    music_clip = AudioFileClip(music_path).set_duration(video_clip.duration)

    # 创建一个组合音频剪辑，将背景音乐和配音放在一起
    # 如果需要调整音量，可以在这里使用volumex()函数
    composite_audio = CompositeAudioClip([music_clip.volumex(0.6), voiceover_clip.volumex(2.0)])
    # 将组合音频添加到视频
    final_clip = video_clip.set_audio(composite_audio)
    # 输出文件
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # 释放资源
    final_clip.close()
    video_clip.close()
    voiceover_clip.close()
    music_clip.close()

# 挂载字幕
def burn_subtitles_to_video(video_path, subtitles_path, output_video_path):
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vf', 'subtitles=' + subtitles_path,
        '-c:a', 'copy',
        '-c:v', 'libx264',
        '-crf', '23',   # 你可以根据需要调整CRF值
        '-preset', 'veryfast',  # 选择一个预设来平衡编码速度和质量
        output_video_path
    ]
    subprocess.run(command, check=True)


def video_main(video_path):
    
    # 分离音频
    mp3_path =  extract_audio_from_video(video_path)
    print(mp3_path,'path')

    # # 分离人声
    separated_files = separate_audio(mp3_path)
    print("Separated files:", separated_files)
    
    # # 转换格式    
    persion_mp3 =  convert_to_mp3(separated_files[0])
    print('persion_mp3:',persion_mp3)
        
    # # 提取字幕
    srt_path =  transcribe_audio_to_srt(persion_mp3)
    print(srt_path)
        
    # 翻译字幕 ./test/output_separator/malaxiya/vocals.srt
    tr_srt_path = translate_subtitle_file(srt_path)
    
    # 翻译成音频
    audio_files =  convert_subtitles_to_speech(tr_srt_path)
    
    # 合并长音频
    # 加载音频文件到一个数组中
    audio_segments = [AudioSegment.from_file(file) for file in audio_files]
    # 创建音频
    final_audio_path = create_audio_from_subtitles(tr_srt_path, audio_segments)
    # 导出音频
    print("Final audio created at:", final_audio_path)
    
    ts_video_output_name = video_path.replace('.mp4','_ts.mp4')
    add_audio_to_video(video_path,final_audio_path,separated_files[1],ts_video_output_name)
    
    sub_ts_video_output_name = ts_video_output_name.replace('.mp4','_sub.mp4')
    burn_subtitles_to_video(ts_video_output_name,tr_srt_path,sub_ts_video_output_name)
    
    print('done:',sub_ts_video_output_name)
    
    pass


if __name__ == '__main__':
    # 分离音频
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_video>")
        sys.exit(1)
    
    video_path = sys.argv[1]  # 获取命令行参数作为视频路径
    video_main(video_path)
    
    
    
        

    


