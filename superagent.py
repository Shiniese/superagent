# readline 库用于修复 input() 接收中文输入时的退格行为与编码问题
import readline

QUERY = input("请输入您的问题：")

from skills import tools_list

from util_middlewares import ToolMonitoringMiddleware, SkillsMiddleware, FinalTranslateMiddleware
from util_models import model_instruct
from util_prompts import DEFAULT_PROMPT

import asyncio

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


from rich.console import Console
from rich.markdown import Markdown


# Async function to run the agent
async def run_agent():
    global QUERY

    # Set up memory
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model_instruct,
        system_prompt=DEFAULT_PROMPT,
        tools=tools_list, 
        middleware=[
            ToolMonitoringMiddleware(),
            SkillsMiddleware(),
            FinalTranslateMiddleware()
        ], 
        checkpointer=checkpointer, 
    )
    config = {"configurable": {"thread_id": 1}}

    while True:
        print(f'\n\n✅ 开始执行 Agent: "{QUERY}"')

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": QUERY}]},
            config=config,
        )
        print("──────────────────────")

        # Print final response, 将Markdown文本转换为Rich对象, 创建一个Console对象, 打印Markdown对象到控制台
        console = Console()
        markdown = Markdown(response['messages'][-1].content)
        console.print(markdown)

        print("──────────────────────")
        print(f'✅ Agent: "{QUERY}" 已完成\n\n')

        user_input = input('请继续询问，如需开启新话题请输入 "new"，如需停止请输入 "quit"：')
        if user_input == "new":
            print("🆕" * 100)
            QUERY = input("\n\n请输入您的新问题：")
            config["configurable"]["thread_id"] += 1
        elif user_input == "quit":
            break
        else:
            QUERY = user_input


# Run the async function
if __name__ == "__main__":
    asyncio.run(run_agent())
