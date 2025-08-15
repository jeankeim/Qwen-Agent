import json
from typing import Union
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.utils import json_loads, print_traceback

@register_tool('echo')
class MyLocalTool(BaseTool):
    """一个简单的本地工具，执行回显操作"""
    
    name = 'echo'
    description = '将输入的文本原样返回'
    parameters = {
        'type': 'object',
        'properties': {
            'text': {
                'type': 'string',
                'description': '要回显的文本'
            }
        },
        'required': ['text']
    }
    
    def call(self, params: Union[str, dict], **kwargs) -> str:
        """执行回显操作"""
        if isinstance(params, str):
            params = json.loads(params)
        return params['text']
