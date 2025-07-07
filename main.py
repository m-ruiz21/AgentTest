import asyncio
from langchain_core.messages import HumanMessage
from Clients.mcp.mcpClientFactory import create_mcp_client
from Models.Agent import AgentGraph

async def main():
    mcp_client = create_mcp_client()
    tools = None

    if mcp_client:
        tools = await mcp_client.get_tools()
        print("Tools loaded successfully, grabbed total of", len(tools), "tools.")
        tools = tools if tools else None

    graph = AgentGraph(
        system_prompt="You are a helpful agent that can use tools to assist the user. Before doing tasks, make sure you're getting as much information as possible from the user. If the tool fails or you need more information, make sure to come back and ask for feedback.",
        tools=tools 
    )

    messages = []

    human_msg_tag = "================================= Human Message =================================\n"
    print(human_msg_tag)
    user_input = input("User: ")

    curr_message_idx = 1
    while user_input.lower() != "exit":
        try:
            messages.append(HumanMessage(content=user_input))
            new_state = await graph.agent.ainvoke({"messages": messages})
            messages = new_state["messages"]
            curr_message_idx = len(messages) - 1
            for m in new_state["messages"][curr_message_idx:]:
                m.pretty_print()

            print(human_msg_tag)
            user_input = input("User: ")

        except Exception as e:
            print(f"An error occurred, error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
