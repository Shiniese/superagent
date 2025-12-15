from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
)
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage, AIMessage
from langgraph.types import Command
from typing import Callable, Any

# 引入第三方轻量库
import langid

from util_pub_func import translate_text

class ToolMonitoringMiddleware(AgentMiddleware):
    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        print(f"🔧 Executing tool: {request.tool_call['name']}")
        print(f"📝 Arguments: {request.tool_call['args']}")
        try:
            result = handler(request)
            print(f"✅ '{request.tool_call['name']}' Tool completed successfully")
            return result
        except Exception as e:
            print(f"❌ '{request.tool_call['name']}' Tool failed: {e}")
            raise
    
    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        print(f"🔧 Executing tool: '{request.tool_call['name']}'")
        print(f"📝 Arguments: {request.tool_call['args']}")
        try:
            result = await handler(request)
            print(f"✅ '{request.tool_call['name']}' Tool completed successfully")
            return result
        except Exception as e:
            print(f"❌ '{request.tool_call['name']}' Tool failed: {e}")
            raise


class FinalTranslateState(AgentState):
    user_lang_code: str

class FinalTranslateMiddleware(AgentMiddleware):
    state_schema = FinalTranslateState
    def before_agent(self, state: FinalTranslateState) -> dict[str, Any] | None:
        """
        Agent 开始前：检测用户输入语言
        """
        try:
            last_msg = state["messages"][-1].content
            # detect 返回如 'zh-cn', 'en', 'ja'
            lang_code = langid.classify(last_msg)[0]
            print(f"🕵️ [检测] 用户输入语言: {lang_code}")
            return {"user_lang_code": lang_code}
        except Exception:
            # 如果检测失败（例如纯数字），默认不处理
            return {"user_lang_code": "en"}

    def after_agent(self, state: FinalTranslateState) -> dict[str, Any] | None:
        """
        Agent 结束后：如果语言不通，进行翻译
        """
        target_lang = state.get("user_lang_code", "en")
        last_message = state["messages"][-1]
        
        # 确保只处理 AI 的回复文本
        if not isinstance(last_message, AIMessage) or not last_message.content:
            return None

        response_text = last_message.content

        try:
            # 检测回复的语言
            response_lang = langid.classify(response_text)[0]
            
            # 简单逻辑：如果检测到的语言前缀不一样（例如 'zh-cn' vs 'en'），则翻译
            # 使用 startswith 是为了兼容 zh-cn, zh-tw 等情况
            if not response_lang.startswith(target_lang.split('-')[0]):
                print(f"🔄 [翻译] 发现输出语言不一致，正在翻译 ({response_lang} -> {target_lang}) ...")
                
                # 调用翻译，翻译后的内容并不会加入到整个msgs里，只是单纯作为最后一条msg显示，原msgs不变 
                last_message.content = translate_text(response_text, target_lang)
                # 返回修正后的消息
                return 
                
        except Exception as e:
            print(f"⚠️ 翻译过程出错: {e}")
            
        return None