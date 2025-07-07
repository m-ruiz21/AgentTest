import asyncio
import sys
sys.path.append("/home/mateoruiz/AgentTest")
from Clients.mcp.mcpClientFactory import create_mcp_client
from langchain_mcp_adapters.client import MultiServerMCPClient

async def print_tools(mcp_client: MultiServerMCPClient):
    print("Entering print_tools...")
    print("Calling get_tools...")
    tools = await mcp_client.get_tools()
    print("get_tools completed.")
    for tool in tools:
        print(f"Tool Name: {tool.name}")
        print(f"Tool Description: {tool.description}")
        print()


async def main():
    print("Starting main...")
    mcp_client = create_mcp_client()
    if mcp_client:
        await print_tools(mcp_client)
    else:
        print("No MCP client available.")

if __name__ == "__main__":
    asyncio.run(main())