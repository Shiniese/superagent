QUERY = input("请输入您的问题：")

from util_tools import *
from util_middlewares import *
from util_models import *
from util_prompts import *

import asyncio

from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware, ContextEditingMiddleware, ClearToolUsesEdit, LLMToolSelectorMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


from rich.console import Console
from rich.markdown import Markdown


# Set up memory
checkpointer = InMemorySaver()


# Async function to run the agent
async def run_agent():
    global QUERY

    agent = create_agent(
        model=model_instruct,
        system_prompt= DEFAULT_PROMPT,
        tools=[tool_get_current_datetime, tool_web_search, tool_get_current_weather], 
        middleware=[
            ToolMonitoringMiddleware(),
            TodoListMiddleware(),
            LLMToolSelectorMiddleware(
                model=model_instruct,
                max_tools=3,
            ),
        ], 
        checkpointer=checkpointer, 
    )
    config = {"configurable": {"thread_id": 1}}

    while True:
        print(f'\n\n✅ 开始执行 Agent: "{QUERY}"')
        print("──────────────────────")

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": QUERY}]},
            config=config,
        )

        # Print final response, 将Markdown文本转换为Rich对象, 创建一个Console对象, 打印Markdown对象到控制台
        console = Console()
        markdown = Markdown(response['messages'][-1].content)
        console.print(markdown)

        print("──────────────────────")
        print(f'✅ Agent: "{QUERY}" 已完成\n\n')

        user_input = input('请继续询问，如需开启新话题请输入 "new"，如需停止请输入 "quit"：')
        if user_input == "new":
            print("=" * 100)
            QUERY = input("\n\n请输入您的新问题：")
            config["configurable"]["thread_id"] += 1
        elif user_input == "quit":
            break
        else:
            QUERY = user_input


# Run the async function
if __name__ == "__main__":
    asyncio.run(run_agent())
