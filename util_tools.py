from langgraph.types import Command
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage

from typing import Literal


@tool
def load_skill(skill_name: str, runtime: ToolRuntime) -> Command:
    """Load the full content of a skill into the agent's context.

    Use this when you need detailed information about how to handle a specific
    type of request. This will provide you with comprehensive instructions,
    policies, and guidelines for the skill area.

    Args:
        skill_name: The name of the skill to load (e.g., "expense_reporting", "travel_booking")
    """
    # Find and return the requested skill

    from util_skills import SKILLS
    
    for skill in SKILLS:
        if skill["name"] == skill_name:
            skill_content = f"Loaded skill: {skill_name}\n\n{skill['content']}"

            # Update state to track loaded skill
            return Command(  
                update={  
                    "messages": [  
                        ToolMessage(  
                            content=skill_content,  
                            tool_call_id=runtime.tool_call_id,  
                        )  
                    ],  
                    "available_tools": skill["available_tools"],  
                }  
            )  

    # Skill not found
    available = ", ".join(s["name"] for s in SKILLS)
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Skill '{skill_name}' not found. Available skills: {available}",
                    tool_call_id=runtime.tool_call_id,
                )
            ]
        }
    )

@tool
def tool_get_current_datetime(timezone: str = 'Asia/Shanghai') -> str:
    """
    Get the current date and time in the specified timezone.

    Args:
        timezone: IANA timezone identifier (e.g., 'Asia/Shanghai', 'Europe/Berlin', 'America/New_York')
    """

    from datetime import datetime
    from zoneinfo import ZoneInfo

    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    except Exception as e:
        return f"Error: {str(e)}. Please provide a valid IANA timezone (e.g., 'Asia/Tokyo')."
    

@tool
def tool_get_current_weather(latitude: float, longitude: float) -> str:
    """
    Get the current weather for a given location using Open-Meteo API.

    Args:
        latitude: Latitude of the location (e.g., 52.52)
        longitude: Longitude of the location (e.g., 13.41)
    """

    import requests
    import toon_format

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "weather_code,temperature_2m,wind_speed_10m,relative_humidity_2m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,wind_speed_10m_max",
        "forecast_days": 3,
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return toon_format.encode(data)
    
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"
    

@tool
async def tool_web_search(english_query: str) -> list[str]:
    """
    一个使代理能够基于用户查询进行网络搜索的工具，可快速访问最新的在线信息。
    你必须首先理解我的问题，然后重构成英文关键词来调用此工具。

    Args:
        english_query: English reconstructed keywords derived from my question.
    """

    import zendriver as zd
    import asyncio
    from util_pub_func import get_search_urls, fetch_page_content, RAG

    try:
        search_urls = get_search_urls(english_query)
        browser = await zd.start(
            headless=True,
            browser_args=[
                "--disable-images",
                "--disable-fonts",
                "--disable-features=TranslateUI",
                "--disable-features=Translate"
            ]
        )
        # 并发获取所有页面内容
        tasks = [fetch_page_content(browser, url) for url in search_urls]
        results = await asyncio.gather(*tasks)

        # 打印结果
        md_texts = ""
        for title, url, content in results:
            if title == "NO_TITLE" or len(content) < 500:
                continue
            md_texts += f"# {title}\n\n{content}\n\n"
            print(f"✅ Fetched 「{title}」 {url}: {len(content)} characters")
    
        rag_results = RAG(query=english_query, markdown_text=md_texts)
        rag_results = [rag_result.page_content for rag_result in rag_results]
        return rag_results
    
    except Exception as e:
        print(f"Error web searching: {str(e)}")
        return f"Error web searching: {str(e)}"
    
    finally:
        await browser.stop()
    

@tool
def tool_get_video_text_content(video_url: str) -> str:
    """
    一个用于获取视频链接内容的工具。  

    Args: 
        video_url (str): 视频的URL地址，支持Bilibili、YouTube等主流平台的视频链接（例如：'https://www.bilibili.com/video/BV1UbUDBLEtX'）  
    Returns: 
        str: 视频的文本内容。  
    """

    import os
    from util_pub_func import download_audio, audio_to_text

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

@tool
def tool_get_local_file_content(local_path: str, file_type: Literal["document", "audio"]) -> str:
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
            from markitdown import MarkItDown

            return MarkItDown().convert(local_path).text_content
        
        elif file_type == "audio":
            from util_pub_func import audio_to_text

            return audio_to_text(local_path)
        
        return "本工具暂不支持获取该文件类型的内容"
    
    except Exception as e:
        print(f"Error getting local file content: {str(e)}")
        return f"Error getting local file content: {str(e)}"
    
