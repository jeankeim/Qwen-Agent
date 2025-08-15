from mcp.server.stdio import stdio_server
from mcp.types import Tool

async def main():
    async with stdio_server() as server:
        @server.tool("local_echo")
        async def echo_tool(params):
            """一个简单的 MCP 工具，执行回显操作"""
            return {
                "content": [{
                    "text": params.get("text", "")
                }]
            }
        
        # 保持服务器运行
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
