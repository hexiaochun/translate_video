
# 视频翻译工具

## 介绍

这个项目旨在将视频中的语音内容翻译成指定的语言，并生成一个包含新语音配音和字幕的新视频文件。它结合了OpenAI的语音识别和翻译服务，以及微软的语言服务，实现高质量的视频语言转换。


## input video
https://github.com/hexiaochun/translate_video/assets/3852922/c2876083-55a3-4994-9aa1-c1f9bafc198d

## output video
https://github.com/hexiaochun/translate_video/assets/3852922/55e8f74e-7b3a-41f4-a3ce-42b66a6fbd05



## 项目依赖

- `ffmpeg`: 用于处理视频和音频流。
- `spleeter`: 用于音频源分离。
- `openai`: 提供语音识别和翻译服务。

在启动项目之前，您需要配置以下API密钥：

- `conf.config.open_api_key`: OpenAI的API密钥。
- `conf.config.tts_subscription_key`: 微软语音服务的订阅密钥。
- `conf.config.tts_service_region`: 微软语音服务的服务区域。

## 启动使用方法

1. 安装所需依赖：

   ```shell
   pip install -r requirements.txt
   ```

2. 运行程序：

   ```shell
   python main.py test/malaxiya.mp4
   ```

确保您的`conf.config`文件已正确设置所有必需的API密钥和配置信息。



# Video Translation Tool

## Introduction

This project aims to translate the speech within videos into a specified language and generate a new video file complete with new voiceover and subtitles. It leverages OpenAI's speech recognition and translation services, along with Microsoft's language services, to perform high-quality video language conversion.

## Project Dependencies

- `ffmpeg`: For handling video and audio streams.
- `spleeter`: For audio source separation.
- `openai`: To provide speech recognition and translation services.

Before starting the project, you need to configure the following API keys:

- `conf.config.open_api_key`: Your OpenAI API key.
- `conf.config.tts_subscription_key`: Your Microsoft speech service subscription key.
- `conf.config.tts_service_region`: Your Microsoft speech service region.

## How to Start

1. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

2. Run the program:

   ```shell
   python main.py test/malaxiya.mp4
   ```

Make sure your `conf.config` file has been correctly set up with all necessary API keys and configuration information.

Both READMEs provide a brief introduction to the project, a list of dependencies, configuration instructions, and a quick-start guide. You should make sure to include any additional instructions or information as needed.



