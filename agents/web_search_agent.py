from mcp_use import MCPClient, MCPAgent
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

# Load MCP Client
def load_mcp_client():
    client = MCPClient.from_config_file("browser_mcp.json")
    return client

# Verify News Using Web Search
async def verify_news_web(title: str) -> str:
    try:
        # Load MCP tools
        client = load_mcp_client()
        
        # Load Groq LLM
        llm = ChatGroq(model="openai/gpt-oss-120b",api_key=os.getenv("GROQ_API_KEY"))

        # Create MCP Agent
        agent = MCPAgent(llm=llm, client=client, max_steps=3)

        result = await agent.run(f"Search: {title}. Return 1 sentence about this news.")

        return result
    except Exception as e:
        print(f"MCP error: {e}")
        return ""