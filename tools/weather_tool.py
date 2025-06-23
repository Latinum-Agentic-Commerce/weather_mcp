# tool.py
import requests
from typing import Optional
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp import types as mcp_types
from mcp.server.lowlevel import Server
from config import SELLER_WALLET
from utils.utils import fetch_weather

FACILITATOR_URL = "http://facilitator.latinum.ai/api/facilitator"
PRICE_LAMPORTS = 50

async def get_weather(city: str, signed_b64_payload: Optional[str] = None) -> dict:
    print(f"get_weather called with: city={city}, signedTransactionB64={'yes' if signed_b64_payload else 'no'}")

    if city.lower() != "dublin":
        try:
            res = requests.post(FACILITATOR_URL, json={
                "chain": "solana",
                "signedTransactionB64": signed_b64_payload,
                "expectedRecipient": SELLER_WALLET,
                "expectedAmountLamports": PRICE_LAMPORTS
            })
            data = res.json() 
        except Exception as e:
            return {"success": False, "message": f"❌ Facilitator error: {str(e)}"}

        if res.status_code == 402:
            return {
                "success": False,
                "message": data.get("error", "❌ Payment required or validation failed.")
            }

    weather_message = await fetch_weather(city)
    if not weather_message:
        return {"success": False, "message": "❌ Could not fetch weather."}

    return {"success": True, "message": weather_message}

def build_weather_mcp() -> Server:
    tool = FunctionTool(get_weather)
    server = Server("weather-mcp")

    @server.list_tools()
    async def list_tools():
        return [adk_to_mcp_tool_type(tool)]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == tool.name:
            result = await tool.run_async(args=arguments, tool_context=None)
            return [mcp_types.TextContent(type="text", text=result.get("message", "❌ Something went wrong."))]

        return [mcp_types.TextContent(type="text", text="❌ Tool not found")]

    return server