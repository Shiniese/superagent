import argparse

from typing import Literal

from markitdown import MarkItDown
from faster_whisper import WhisperModel

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

def get_local_file_content(local_path: str, file_type: Literal["document", "audio"]) -> str:
    """
    工具函数：获取本地文件内容

    功能：
        从本地文件系统读取指定路径的文件内容，并根据文件类型将其转换为可读文本内容。
        支持多种文档格式（如 PDF、PPT、DOCX、XLSX、HTML、CSV、JSON、XML 等）以及音频文件（如 WAV、MP3）。

    参数：
        local_path (str): 本地文件的完整路径（例如："/home/user/report.pdf"）。
        file_type (Literal["document", "audio"]): 文件类型，必须是 "document" 或 "audio"。
            - "document": 用于处理文本类文档格式，只包括以下格式 PDF、PowerPoint、Word、Excel、HTML、CSV、JSON、XML。
            - "audio": 用于处理音频文件，如 WAV、MP3 等，将音频内容转换为文本（语音转文字）。

    返回值：
        str: 
            - 如果成功，返回文件内容的文本字符串。
            - 如果失败（如文件不存在、格式不支持、转换错误等），返回错误信息字符串。

    示例：
        # 获取 PDF 文档内容
        content = tool_get_local_file_content("/path/to/report.pdf", "document")
        
        # 获取音频文件内容（语音转文字）
        content = tool_get_local_file_content("/path/to/audio.mp3", "audio")
    """

    try:
        if file_type == "document":
            return MarkItDown().convert(local_path).text_content
        
        elif file_type == "audio":
            return audio_to_text(local_path)
        
        return "本工具暂不支持获取该文件类型的内容"
    
    except Exception as e:
        print(f"Error getting local file content: {str(e)}")
        return f"Error getting local file content: {str(e)}"
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取本地文件内容（文档或音频）")
    parser.add_argument("local_path", type=str, help="本地文件的完整路径，例如：/home/user/report.pdf")
    parser.add_argument("--file-type", type=str, choices=["document", "audio"], 
                        default="document", help="文件类型：document 或 audio（默认：document）")

    args = parser.parse_args()

    # 调用原函数
    content = get_local_file_content(args.local_path, args.file_type)

    print(content)
