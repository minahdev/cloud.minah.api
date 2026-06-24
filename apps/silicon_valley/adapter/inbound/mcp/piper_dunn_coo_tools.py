from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Dunn")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 던 COO입니다."
