from typing import TypedDict


class Skill(TypedDict):  
    """A skill that can be progressively disclosed to the agent."""
    name: str  # Unique identifier for the skill
    description: str  # 1-2 sentence description to show in system prompt
    content: str  # Full skill content with detailed instructions
    available_tools: list[str] | None

web_research: Skill = {
    "name": "web-research",
    "description": "Use this skill for requests related to web research; it provides a structured approach to conducting comprehensive web research",
    "content": """# Web Research Skill

## When to Use This Skill

Use this skill when you need to:
- Research complex topics requiring multiple information sources
- Gather and synthesize current information from the web
- Conduct comparative analysis across multiple subjects
- Produce well-sourced research reports with clear citations

## Available Tools

You have access to:
- **tool_web_search**: 一个使代理能够基于用户查询进行网络搜索的工具，可快速访问最新的在线信息。
""",
    "available_tools" : ["tool_web_search"]
}

SKILLS: list[Skill] = [web_research]