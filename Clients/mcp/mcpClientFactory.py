from fastmcp import Client
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.load_config_obj import load_config_obj

def load_config(path: str) -> dict:
    """Load mcp.json"""
    conf = load_config_obj(path)
    mcp_servers = {
        name: srv_cfg
        for name, srv_cfg in conf.get("mcpServers", {}).items()
    }

    return {"mcpServers": mcp_servers}


def create_mcp_client() -> MultiServerMCPClient | None:
    """
    Create a MultiServerMCPClient using the provided configuration.

    :return: An instance of the MultiServerMCPClient.
    """
    try:
        config = load_config_obj("mcp.json")
        if config:
            return MultiServerMCPClient(config)
        return None
    except FileNotFoundError:
        print("mcp.json not found")
        return None
    except Exception as e:
        print(f"Error creating MCP client: {e}")
        return None
