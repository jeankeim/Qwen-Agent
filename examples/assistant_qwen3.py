# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An agent implemented by assistant with qwen3"""
import os  # noqa

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
from qwen_agent.utils.output_beautify import typewriter_print
from typing import List

# from qwen_agent.llm.schema import ASSISTANT, FUNCTION

# TOOL_CALL_S = '[TOOL_CALL]'
# TOOL_CALL_E = ''
# TOOL_RESULT_S = '[TOOL_RESPONSE]'
# TOOL_RESULT_E = ''
# THOUGHT_S = '[THINK]'


# def typewriter_print(messages: List[dict], text: str) -> str:
#     full_text = ''
#     content = []
#     for msg in messages:
#         if msg['role'] == ASSISTANT:
#             if msg.get('reasoning_content'):
#                 assert isinstance(msg['reasoning_content'], str), 'Now only supports text messages'
#                 content.append(f'{THOUGHT_S}\n{msg["reasoning_content"]}')
#             if msg.get('content'):
#                 assert isinstance(msg['content'], str), 'Now only supports text messages'
#                 content.append(msg['content'])
#             if msg.get('function_call'):
#                 content.append(f'{TOOL_CALL_S} {msg["function_call"]["name"]}\n{msg["function_call"]["arguments"]}')
#         elif msg['role'] == FUNCTION:
#             content.append(f'{TOOL_RESULT_S} {msg["name"]}\n{msg["content"]}')
#         else:
#             raise TypeError
#     if content:
#         full_text = '\n'.join(content)
#         print(full_text[len(text):], end='', flush=True)

#     return full_text




def init_agent_service():
    # llm_cfg = {
    #     # Use the model service provided by DashScope:
    #     'model': 'qwen3-235b-a22b',
    #     'model_type': 'qwen_dashscope',

        # 'generate_cfg': {
        #     # When using the Dash Scope API, pass the parameter of whether to enable thinking mode in this way
        #     'enable_thinking': False,
        # },
    # }

    llm_cfg={'model':'qwen3:8b', 
             'model_server': 'http://localhost:11434/v1',  #base_url，也称为 api_base
             'api_key':''}
    # llm_cfg = {
    #     # Use the OpenAI-compatible model service provided by DashScope:
    #     'model': 'qwen3-235b-a22b',
    #     'model_server': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    #     'api_key': os.getenv('DASHSCOPE_API_KEY'),
    #
    #     # 'generate_cfg': {
    #     #     # When using Dash Scope OAI API, pass the parameter of whether to enable thinking mode in this way
    #     #     'extra_body': {
    #     #         'enable_thinking': False
    #     #     },
    #     # },
    # }
    # llm_cfg = {
    #     # Use your own model service compatible with OpenAI API by vLLM/SGLang:
    #     'model': 'Qwen/Qwen3-32B',
    #     'model_server': 'http://localhost:8000/v1',  # api_base
    #     'api_key': 'EMPTY',
    #
    #     'generate_cfg': {
    #         # When using vLLM/SGLang OAI API, pass the parameter of whether to enable thinking mode in this way
    #         'extra_body': {
    #             'chat_template_kwargs': {'enable_thinking': False}
    #         },
    #
    #         # Add: When the content is `<think>this is the thought</think>this is the answer`
    #         # Do not add: When the response has been separated by reasoning_content and content
    #         # This parameter will affect the parsing strategy of tool call
    #         # 'thought_in_content': True,
    #     },
    # }
    tools = [
        {
            'mcpServers': {  # You can specify the MCP configuration file
                'time': {
                    'command': 'uvx',
                    'args': ['mcp-server-time', '--local-timezone=Asia/Shanghai']
                },
                'fetch': {
                    'command': 'uvx',
                    'args': ['mcp-server-fetch']
                }
            }
        }
    ]
    bot = Assistant(llm=llm_cfg,
                    function_list=tools,
                    name='Qwen3 Tool-calling Demo',
                    description="I'm a demo using the Qwen3 tool calling. Welcome to add and play with your own tools!")

    return bot


def test(query: str = 'What time is it?'):
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = [{'role': 'user', 'content': query}]
    response_plain_text = ''
    for response in bot.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        query = input('user question: ')
        messages.append({'role': 'user', 'content': query})
        response = []
        response_plain_text = ''
        for response in bot.run(messages=messages):
            response_plain_text = typewriter_print(response, response_plain_text)
        messages.extend(response)


def app_gui():
    # Define the agent
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            'What time is it?',
            'https://github.com/orgs/QwenLM/repositories Extract markdown content of this page, then draw a bar chart to display the number of stars.'
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()
