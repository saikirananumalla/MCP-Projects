import asyncio
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import (
    FunctionAgent,
    ToolCallResult,
    ToolCall
)
from llama_index.core.workflow import Context
from dotenv import load_dotenv
import os
load_dotenv()

# Configure the LLM (served locally via Ollama)
# llm = Ollama(model="llama3.2", request_timeout=120.0)
# Settings.llm = llm

# Configure the LLM (served online via OpenAPI key)
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(model="gpt-4o", api_key=api_key)

SYSTEM_PROMPT = """
You are an AI assistant for Tool Calling.
Before helping, work with our tools to interact
with our database.
"""

# Create a FunctionAgent with MCP tools
async def get_agent(tools: McpToolSpec):
    tools = await tools.to_tool_list_async()
    return FunctionAgent(
        name="Agent",
        description="agent that interacts with our Database",
        tools=tools,
        llm=llm,
        system_prompt=SYSTEM_PROMPT
    )

# Handle user input and print streaming tool call events
async def handle_user_messages(
    message_context: str,
    agent: FunctionAgent,
    agent_context: Context,
    verbose: bool = False,
):
    handler = agent.run(message_context, ctx=agent_context)

    async for event in handler.stream_events():
        if verbose and isinstance(event, ToolCall):
            print(f"[Tool Call] {event.tool_name}")
        elif verbose and isinstance(event, ToolCallResult):
            print(f"[Tool Return] {event.tool_name} → {event.tool_output}")

    response = await handler
    return str(response)

# CLI loop to chat with the agent
async def main():
    mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
    mcp_tool = McpToolSpec(client=mcp_client)

    agent = await get_agent(mcp_tool)
    context = Context(agent)

    while True:
        user_input = input("Enter your message: ")
        if user_input.lower() == "exit":
            break
        response = await handle_user_messages(user_input, agent, context, verbose=True)
        print("Agent:", str(response))

def extract_agent_output(response):
    if hasattr(response, "message"):
        return response.message.content
    if hasattr(response, "content"):
        return response.content
    if isinstance(response, str):
        return response
    return str(response)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
