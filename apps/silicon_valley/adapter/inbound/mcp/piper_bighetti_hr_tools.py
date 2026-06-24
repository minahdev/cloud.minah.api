from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Bighetti")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 비게티 HR담당자입니다."
