import argparse
import os
import tempfile

import yt_dlp
from faster_whisper import WhisperModel

def download_audio(video_url: str) -> str:
    """
    从 YouTube 视频 URL 下载音频文件，保存为 M4A 格式。

    功能：
        该函数使用 yt-dlp 作为底层工具，从指定的视频 URL 提取音频，并以 M4A 格式保存到临时文件中。
        下载的音频文件将通过临时文件路径返回，调用者需负责在使用后手动清理该文件，以避免磁盘空间占用。

    参数:
        video_url (str): YouTube 视频的完整 URL（例如：https://www.youtube.com/watch?v=abc123）。

    返回:
        str: 下载完成后的音频文件的临时路径（文件扩展名为 .m4a），路径为系统临时目录下的文件。

    示例:
        audio_path = download_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print(f"Audio downloaded to: {audio_path}")
        # 使用后应手动删除文件
        os.unlink(audio_path)
    """

    try:
        # 创建一个临时文件路径（自动管理，下载后手动清理）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
            tmp_path = tmp_file.name  # 临时文件路径
            os.unlink(tmp_path) # 先删除临时文件，只是为了获取这个临时文件名，临时文件最后再手动自行删除

        ydl_opts = {
            'format': 'worstaudio/worst',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'outtmpl': tmp_path,  # 定义输出文件的路径和名称格式
            'quiet' : True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return tmp_path
        
    except Exception as e:
        raise Exception(f"Error downloading audio: {str(e)}")
    
def audio_to_text(audio_path: str) -> str:
    """
    将音频文件转换为文本内容的函数。

    功能：
        该函数使用 Faster-Whisper 模型对指定路径的音频文件进行语音识别（ASR），并返回转录后的文本。

    参数：
        audio_path (str): 音频文件的路径（支持常见格式如 .wav, .mp3, .flac 等）。

    返回：
        str: 转录后的文本内容，多个语音片段之间以逗号加空格（", "）分隔。

    示例：
        text = audio_to_text("example.wav")
        print(text)  # 输出：这是一个测试音频，内容是"Hello, world!"
    """

    try:
        model_size = "large-v3"
        model = WhisperModel(model_size, device="auto")

        segments, _ = model.transcribe(audio_path)
        texts = ""
        for segment in segments:
            texts += segment.text + ", "

        return texts
    
    except Exception as e:
        raise Exception(f"Error transcribing audio to text: {str(e)}")
    
def get_video_text_content(video_url: str) -> str:
    """
    一个用于获取视频链接内容的工具。  

    Args: 
        video_url (str): 视频的URL地址，支持Bilibili、YouTube等主流平台的视频链接（例如：'https://www.bilibili.com/video/BV1UbUDBLEtX'）  
    Returns: 
        str: 视频的文本内容。  
    """

    try:
        audio_path = ""
        audio_path = download_audio(video_url)
        video_texts = audio_to_text(audio_path)

        return video_texts
    
    except Exception as e:
        print(f"Error summarizing video: {str(e)}")
        return f"Error summarizing video: {str(e)}"
    
    finally:
        if audio_path:
            os.unlink(audio_path)  # 删除临时文件


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text content from a video URL.")
    parser.add_argument("video_url", type=str, help="The URL of the video (e.g., https://www.bilibili.com/video/BV1UbUDBLEtX)")
    args = parser.parse_args()

    result = get_video_text_content(args.video_url)
    print(result)
