from pydub import AudioSegment
import re
from datetime import datetime

# 音频对齐
def process_audio_to_match_subtitle(subtitle, audio_clip):
    """
    Process the audio clip to match the subtitle duration.

    :param subtitle: A tuple containing the start and end times for the subtitle.
    :param audio_clip: The audio segment corresponding to the subtitle.
    :return: Processed AudioSegment object.
    """
    start_time, end_time = subtitle
    duration = end_time - start_time
    audio_duration = len(audio_clip)

    print(duration ,audio_duration )
    if audio_duration > duration:
        # If audio is longer than subtitle duration, speed up the audio
        ratio = audio_duration / duration
        print(ratio)
        if ratio < 1.01:  # 如果太小会有一个bug，未知原因
            processed_audio = audio_clip
        else:
            processed_audio = audio_clip.speedup(playback_speed=ratio)
    elif audio_duration < duration:
        # If audio is shorter than subtitle duration, add silence
        silence_duration = duration - audio_duration
        silence = AudioSegment.silent(duration=silence_duration)
        processed_audio = audio_clip + silence
    else:
        # If durations match, no processing is needed
        processed_audio = audio_clip

    return processed_audio

# 从字幕创建音频
def create_audio_from_subtitles(subtitle_file_path, audio_clips):
    """
    Create a single audio file from a list of audio segments, matching subtitle timings.

    :param subtitle_file_path: Path to the subtitle file.
    :param audio_clips: List of AudioSegment objects.
    :return: A path to the combined audio file.
    """
    combined_audio = AudioSegment.empty()
    subtitles = parse_subtitles(subtitle_file_path)  # Implement this function based on your subtitle file format.

    for index, (subtitle, audio_clip) in enumerate(zip(subtitles, audio_clips)):
        processed_audio = process_audio_to_match_subtitle(subtitle, audio_clip)
        print(subtitle,processed_audio)
        combined_audio += processed_audio
        
          # 打印当前合并音频的持续时间
        print(f"After processing subtitle {index+1}, combined audio length is: {len(combined_audio)} ms")
        # 可选：导出当前状态的合并音频到临时文件进行检查
        # combined_audio.export(f"temp_combined_audio_{index+1}.mp3", format="mp3")


    output_path = subtitle_file_path.replace('.srt', '_combined_audio.mp3')
    combined_audio.export(output_path, format='mp3')
    return output_path

def srt_time_to_millis(time_str):
    """Convert SRT time format to milliseconds."""
    time_format = '%H:%M:%S,%f'
    dt = datetime.strptime(time_str, time_format)
    return (dt.hour * 3600 + dt.minute * 60 + dt.second) * 1000 + int(dt.microsecond / 1000)

def parse_subtitles(subtitle_file_path):
    """
    Parse an SRT file to get start and end times for each subtitle entry.

    :param subtitle_file_path: Path to the SRT file.
    :return: A list of tuples with start and end times in milliseconds.
    """
    with open(subtitle_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Pattern to find all subtitle entries
    pattern = re.compile(r'\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(content)

    subtitles = []
    for start_str, end_str, _ in matches:
        start_millis = srt_time_to_millis(start_str)
        end_millis = srt_time_to_millis(end_str)
        subtitles.append((start_millis, end_millis))

    return subtitles


if __name__ == '__main__':
    pass
    # convert_subtitles_to_speech("./test/output_separator/malaxiya/vocals_translated.srt")
    
    # 使用示例
    subtitle_file_path = './test/output_separator/malaxiya/vocals_translated.srt'
    audio_files = ['./test/output_separator/malaxiya/vocals_translated/1.mp3', './test/output_separator/malaxiya/vocals_translated/2.mp3', './test/output_separator/malaxiya/vocals_translated/3.mp3', './test/output_separator/malaxiya/vocals_translated/4.mp3', './test/output_separator/malaxiya/vocals_translated/5.mp3', './test/output_separator/malaxiya/vocals_translated/6.mp3']
    
    # 加载音频文件到一个数组中
    audio_segments = [AudioSegment.from_file(file) for file in audio_files]
    # 创建音频
    final_audio_path = create_audio_from_subtitles(subtitle_file_path, audio_segments)
    # 导出音频
    print("Final audio created at:", final_audio_path)
