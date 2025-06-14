# run_stdio.py

import asyncio
from mcp.server.models import InitializationOptions
import mcp.server.stdio
from tools.weather_tool import build_weather_mcp
from mcp.server.lowlevel import NotificationOptions

async def run():
    server = build_weather_mcp()
    async with mcp.server.stdio.stdio_server() as (r, w):
        await server.run(
            r, w,
            InitializationOptions(
                server_name=server.name,
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                ),
            )
        )

if __name__ == "__main__":
    asyncio.run(run())