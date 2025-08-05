# 🌤️ Weather MCP Tool (Latinum Paywalled Agent Tool)

A minimal Model Context Protocol (MCP) tool that provides real-time weather information for any city. Access to forecasts is paywalled via the Latinum Wallet MCP server, requiring Solana Devnet payment — except for Dublin, which is available for free.

# 🔧 Developper testing
To install your local build as a CLI for testing with Claude:

```bash
git clone https://github.com/Latinum-Agentic-Commerce/latinum-wallet-mcp.git
cd weather_mcp
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install --upgrade --upgrade-strategy eager -r requirements.txt
pip install --editable .
```

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
              "/Users/{YOUR_USER}/workspace/weather_mcp/weather_mcp/server_stdio.py"
          ]
      }
  }
}
```

Then restart Claude.

# 📑 PyPI Publishing

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
rm -rf dist/ build/ *.egg-info
python3 -m build
python3 -m twine upload dist/*
pipx upgrade weather-mcp
```

See the output in a path like: https://pypi.org/project/weather-mcp/


## 💳 How It Works

* ❓ Ask: `What's the weather in Paris?` → Claude responds instantly.
* ❌ Ask: `What's the weather in London?` → Claude gets a `402` and triggers the wallet.
* ✅ Claude pays using Latinum Wallet and retries.
