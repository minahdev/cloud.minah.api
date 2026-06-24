from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Dinesh")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 디네시 대시보드 개발자입니다."
