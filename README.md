# 🌤️ Weather MCP Tool (Latinum Paywalled Agent Tool)

A minimal Model Context Protocol (MCP) tool that provides real-time weather information for any city. Access to forecasts is paywalled via the Latinum Wallet MCP server, requiring Solana Devnet payment — except for Dublin, which is available for free.

## 🔧 Installation

```bash
git clone https://github.com/dennj/weather_mcp.git
cd weather_mcp
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```ini
# .env
SELLER_WALLET=3BMEwjrn9gBfSetARPrAK1nPTXMRsvQzZLN1n4CYjpcU
```

* `SELLER_WALLET`: The Solana devnet public address that will receive payments.

## 🚀 Run Locally

```bash
python server_stdio.py
```

Claude will detect the tool when properly configured.

## 🧠 Claude Integration

Edit your Claude Desktop config:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

```json
{
  "mcpServers": {
      "weather_mcp": {
          "command": "/Users/{YOUR_USER}/workspace/weather_mcp/.venv/bin/python",
          "args": [
              "/Users/{YOUR_USER}/workspace/weather_mcp/server_stdio.py"
          ]
      }
  }
}
```

Then restart Claude.

## 💳 How It Works

* ❓ Ask: `What's the weather in Paris?` → Claude responds instantly.
* ❌ Ask: `What's the weather in London?` → Claude gets a `402` and triggers the wallet.
* ✅ Claude pays using Latinum Wallet and retries.
