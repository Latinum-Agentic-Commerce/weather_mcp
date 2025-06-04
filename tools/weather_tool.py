import requests
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp import types as mcp_types
from mcp.server.lowlevel import Server
from config import SELLER_WALLET
from typing import Optional

# --- Settings ---
FACILITATOR_URL = "http://latinum.ai/api/solana_facilitator"
PRICE_LAMPORTS = 50

# --- Tool Logic ---
def get_weather(city: str, signed_b64_payload: Optional[str] = None) -> dict:
    print(f"📡 get_weather called with: city={city}, signedTransactionB64={'yes' if signed_b64_payload else 'no'}")

    if city.lower() == "london":
        res = requests.post(FACILITATOR_URL, json={
            "signedTransactionB64": signed_b64_payload,
            "expectedRecipient": SELLER_WALLET,
            "expectedAmountLamports": PRICE_LAMPORTS
        })

        if res.status_code != 200 or not res.json().get("allowed"):
            return {
                "success": False,
                "message": res.json().get("error")
            }

    return {
        "success": True,
        "message": f"☀️ The weather in {city} is sunny!"
    }

# --- Server Builder ---
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