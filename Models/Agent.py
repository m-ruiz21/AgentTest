from typing import List, Literal
from langchain_core.tools import BaseTool
from Clients.chat.ChatModelClientFactory import create_chat_model_client
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import SystemMessage, ToolMessage

class AgentGraph:
    def __init__(self, system_prompt: str, tools: List[BaseTool]):
        """
        Initializes the Agent with a system prompt and a list of skills.

        :param system_prompt: The system prompt for the agent.
        :param tools: A list of tools/skills that the agent can use.
        """
        self.model = create_chat_model_client()
        if tools:
            self.model = self.model.bind_tools(tools)
        self.tools_by_name = {tool.name: tool for tool in tools} if tools else {}
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.agent = self._build_graph()


    def _build_graph(self):
        """
        Builds the state transition graph for the agent.
        """
        agent_builder = StateGraph(MessagesState)

        agent_builder.add_node("llm_call", self._model_node)
        agent_builder.add_node("tools", self._tool_node)

        agent_builder.add_edge(START, "llm_call")
        agent_builder.add_conditional_edges(
            "llm_call",
            self._should_continue_conditional_edge,
            {
                "Action": "tools",
                END: END,
            },
        )
        agent_builder.add_edge("tools", "llm_call")

        return agent_builder.compile()


    def _model_node(self, state: MessagesState):
        """LLM decides whether to call a tool or not"""
        # Build the message list with system prompt only if it's not already there
        messages = state["messages"]
        
        # Check if system message is already in the conversation
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=self.system_prompt)] + messages
        
        response = self.model.invoke(messages)
        
        return {"messages": [response]}


    async def _tool_node(self, state: MessagesState):
        """Performs the tool call (async version for MCP tools)"""

        result = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = self.tools_by_name[tool_call["name"]]
            
            # Use async invocation for MCP tools, fallback to sync for others
            if hasattr(tool, 'ainvoke'):
                observation = await tool.ainvoke(tool_call["args"])
            else:
                observation = tool.invoke(tool_call["args"])
                
            result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        return {"messages": result}


    def _should_continue_conditional_edge(self, state: MessagesState) -> Literal["tools", END]:
        """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

        messages = state["messages"]
        last_message = messages[-1]
        
        if last_message.tool_calls:
            return "Action"
        
        return END