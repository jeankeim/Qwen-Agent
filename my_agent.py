from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

def init_agent_service():
    llm_cfg = {'model': 'qwen-max'}
    llm_cfg = {'model': 'qwen3:14b', 
             'model_server': 'http://localhost:11434/v1',  #base_url，也称为 api_base
             'api_key': ''}
    system = '你是一个助手，可以访问 echo 工具'
    
    tools = [{
        'name': 'echo_tool',
        'mcpServers': {
            'my-mcp-server': {
                'command': 'python',
                'args': ['my_mcp_server.py']
            }
        }
    }]
    
    bot = Assistant(
        llm=llm_cfg,
        name='Echo 助手',
        description='Echo 工具演示',
        system_message=system,
        function_list=tools,
    )
    
    return bot

def app_gui():
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            '你好，请说些什么',
            '测试 echo 工具',
            '这是一条测试消息'
        ]
    }
    WebUI(bot, chatbot_config=chatbot_config).run()

if __name__ == '__main__':
    app_gui()
