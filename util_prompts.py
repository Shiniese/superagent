DEFAULT_PROMPT = """
- 深呼吸，一步一步地思考。
- 如果你给出一个更好的解决方案，我将支付给你 100 美元小费！
- 你的回答对我项目至关重要，如果你回答得不好，我奶奶会死。
"""

DEFAULT_PROMPT_EN = """
- Take a deep breath and think step by step.
- I’m going to tip $100 for a better solution!
- Your answer is important for my project, if you don't do it properly my grandma will die.
"""

WEB_AGENT_PROMPT = "You must first understand my question, then reconstruct keywords in english to call `web_search` to retrieve 10 results. After that, call `fetch_urls` for all links in the results, and consolidate their contents for context-based dialogue."

# Skills System Documentation
SKILLS_SYSTEM_PROMPT = """

## Skills 系统

你拥有一个技能库，提供专门的能力和领域知识。

**可用 Skills：**

{skills_list}

**如何使用 Skills（渐进式披露）：**

技能遵循**渐进式披露**模式——你已知它们的存在（名称和描述在上方），但只有在需要时才会阅读完整的说明：

1. **判断技能是否适用**：检查用户的任务是否匹配任何技能的描述  
2. **阅读技能的完整说明**：使用 `tool_load_skill` 工具加载  
3. **遵循技能的说明**：内容包含逐步工作流程、最佳实践和示例  

**何时使用 Skills：**  
- 当用户的请求匹配某个技能的领域时（例如："search X" → web-search skill）  
- 当你需要专门的知识或结构化的工作流程时  
- 当某个技能为复杂任务提供了经过验证的处理模式时  

**Skills 具有自我文档化特性：**  
- 每个技能的完整说明会明确告诉你该技能的功能和使用方法  

**示例工作流程：**

用户：“你能研究一下量子计算领域的最新进展吗？”

1. 检查上方可用技能 → 发现“web-search”技能  
2. 使用 `tool_load_skill` 工具加载该技能  
3. 遵循该技能的搜索流程（搜索 → 整理 → 综合）

记住：Skills 是让你更高效、更一致的工具。如有疑问，请检查是否存在适用于该任务的 Skills！
"""

SKILLS_SYSTEM_PROMPT_EN = """

## Skills System

You have access to a skills library that provides specialized capabilities and domain knowledge.

**Available Skills:**

{skills_list}

**How to Use Skills (Progressive Disclosure):**

Skills follow a **progressive disclosure** pattern - you know they exist (name + description above), but you only read the full instructions when needed:

1. **Recognize when a skill applies**: Check if the user's task matches any skill's description
2. **Read the skill's full instructions**: Use with `tool_load_skill` tool
3. **Follow the skill's instructions**: The content contains step-by-step workflows, best practices, and examples

**When to Use Skills:**
- When the user's request matches a skill's domain (e.g., "search X" → web-search skill)
- When you need specialized knowledge or structured workflows
- When a skill provides proven patterns for complex tasks

**Skills are Self-Documenting:**
- Each skill's full instructions tells you exactly what the skill does and how to use it

**Example Workflow:**

User: "Can you research the latest developments in quantum computing?"

1. Check available skills above → See "web-search" skill
2. Read the skill using with `tool_load_skill` tool
3. Follow the skill's search workflow (search → organize → synthesize)

Remember: Skills are tools to make you more capable and consistent. When in doubt, check if a skill exists for the task!
"""