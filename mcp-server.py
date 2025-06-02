from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("MyAssistantServer")


# Define a tool
@mcp.tool()
def greet(name: str) -> str:
    """Greets the user by name."""
    return f"Hello, {name}!"


# Run the server
if __name__ == "__main__":
    mcp.run()
