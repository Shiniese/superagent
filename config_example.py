# 定义 导出 Skills 工具函数名 -> 内部路径 的映射
TOOL_MAPPING = {
    "get_current_datetime": ".get-current-datetime.scripts.get_current_datetime",
    "get_current_weather": ".get-current-weather.scripts.get_current_weather",
    "get_local_file_content": ".get-local-file-content.scripts.get_local_file_content",
    "get_video_text_content": ".get-video-text-content.scripts.get_video_text_content",
    "web_search": ".web-search.scripts.web_search",
}

# Ollama
OLLAMA_BASE_URL = ""

# ChatGPT Series
ZHIPU_BASE_URL = ""
ZHIPU_API_KEY = ""

QINIU_BASE_URL = ""
QINIU_API_KEY = ""


# 自定义简短 SKILL，具体定义在 util_skills.SkillMetadata
CUSTOM_SKILLS = {
    "summarize-content": {
        "name": "summarize-content",
        "description": "使用指定模板总结内容",
        "content": """
# Template

'''
Summarize the above CONTENT into brief sentences of key points, then provide complete highlighted information in a list, choosing an appropriate emoji for each highlight.
Your output should use the following format: 
### Summary
{brief summary of this content}
### Highlights
- [Emoji] Bullet point with complete explanation
### keyword
Suggest up to a few tags related to the content.
'''
"""
    },
}