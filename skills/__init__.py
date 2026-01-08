# skills/__init__.py

import importlib

from config import TOOL_MAPPING

# 定义 导出 Skills 工具函数名 -> 内部路径 的映射
_TOOL_MAPPING = {} or TOOL_MAPPING

__all__ = []
tools_list = []

for func_name, module_path in _TOOL_MAPPING.items():
    try:
        # 动态导入模块
        mod = importlib.import_module(module_path, package="skills")
        # 获取函数对象
        func = getattr(mod, func_name)
        # 将函数注入到当前全局命名空间
        globals()[func_name] = func
        # 添加到 __all__
        __all__.append(func_name)
        tools_list.append(func)
    except (ImportError, AttributeError) as e:
        print(f"Warning: Failed to load tool '{func_name}': {e}")
