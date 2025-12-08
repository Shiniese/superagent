from langchain.agents.middleware import AgentMiddleware
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage
from langgraph.types import Command
from typing import Callable

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