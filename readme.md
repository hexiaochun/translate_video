

## input video
https://github.com/hexiaochun/translate_video/assets/3852922/c2876083-55a3-4994-9aa1-c1f9bafc198d


## output video
https://github.com/hexiaochun/translate_video/assets/3852922/55e8f74e-7b3a-41f4-a3ce-42b66a6fbd05


### 中文版本

```markdown
# 视频翻译工具

## 介绍

这个项目旨在将视频中的语音内容翻译成指定的语言，并生成一个包含新语音配音和字幕的新视频文件。它结合了OpenAI的语音识别和翻译服务，以及微软的语言服务，实现高质量的视频语言转换。

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
```

### English Version

```markdown
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
```

Both READMEs provide a brief introduction to the project, a list of dependencies, configuration instructions, and a quick-start guide. You should make sure to include any additional instructions or information as needed.

## ffmpeg 安装方法

### Windows

在 Windows 上安装 `ffmpeg`，你可以下载预编译的二进制文件并将其添加到你的系统路径中：

1. 访问 [FFmpeg官方下载页面](https://ffmpeg.org/download.html)。
2. 选择 Windows 对应的链接，通常会被重定向到一个可以下载编译好的 `ffmpeg` 版本的页面。
3. 下载 `ffmpeg` 的 zip 文件。
4. 解压 zip 文件到你希望存放 `ffmpeg` 的地方（例如 `C:\Program Files\ffmpeg`）。
5. 将 `ffmpeg` 的 bin 目录（例如 `C:\Program Files\ffmpeg\bin`）添加到系统环境变量 `Path` 中。
6. 打开命令提示符并输入 `ffmpeg -version` 来检查是否安装成功。

### macOS

在 macOS 上，你可以使用 `brew`（Homebrew），一个包管理器来安装 `ffmpeg`：

1. 打开终端。
2. 如果你还没有安装 Homebrew，使用以下命令来安装它：
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. 安装 `ffmpeg`：
   ```sh
   brew install ffmpeg
   ```
4. 通过输入 `ffmpeg -version` 来检查是否安装成功。

### Ubuntu / Debian

在基于 Debian 的系统上（包括 Ubuntu 和 Linux Mint），你可以通过 `apt` 包管理器来安装 `ffmpeg`：

1. 打开终端。
2. 更新你的包列表：
   ```sh
   sudo apt update
   ```
3. 安装 `ffmpeg`：
   ```sh
   sudo apt install ffmpeg
   ```
4. 验证安装：
   ```sh
   ffmpeg -version
   ```

### CentOS / Fedora / RHEL

在 CentOS、Fedora 或 RHEL 上，你可以使用 `dnf` 或 `yum`（根据你的系统版本）来安装 `ffmpeg`：

对于 CentOS/RHEL 7 和一些旧版本的 Fedora，你可能需要先启用 EPEL 仓库：

```sh
sudo yum install epel-release
```

然后，对于 CentOS/RHEL：

```sh
sudo yum install ffmpeg
```

对于 Fedora：

```sh
sudo dnf install ffmpeg
```

然后，检查 `ffmpeg` 是否安装成功：

```sh
ffmpeg -version
```



