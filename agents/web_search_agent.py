from mcp_use import MCPClient, MCPAgent
from langchain_groq import ChatGroq
import os

def load_mcp_client():
    client = MCPClient.from_config_file("browser_mcp.json")
    return client

async def verify_news_web(title: str) -> str:
    try:
        client = load_mcp_client()
        llm = ChatGroq(
            model="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
        agent = MCPAgent(llm=llm, client=client, max_steps=3)
        result = await agent.run(
            f"Search: {title}. Return 1 sentence about this news."
        )
        return result
    except Exception as e:
        print(f"MCP error: {e}")
        return ""