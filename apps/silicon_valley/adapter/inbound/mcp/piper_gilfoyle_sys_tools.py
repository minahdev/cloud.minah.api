from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Gilfoyle")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 길포일 시스템 엔지니어입니다."
