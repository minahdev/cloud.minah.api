from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hendricks")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 헨드릭스 CEO입니다."