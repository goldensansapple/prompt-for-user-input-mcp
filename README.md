# Prompt for User Input MCP Server

An MCP (Model Context Protocol) server that enables AI models to prompt users for input directly through their code editor. This creates an interactive experience where AI assistants can ask questions, request clarification, or gather information from users in real-time during conversations.

## Quick Start

### Prerequisites

- Python 3
- Cursor IDE (or VSCode)

### Install the MCP Server

```bash
# Clone the repository
git clone https://github.com/goldensansapple/prompt-for-user-input-mcp.git
cd prompt_for_user_input_mcp

# Install Python dependencies
pip install -r requirements.txt
```

### Start the MCP Server

```bash
# From the project root directory
py mcp_server.py

# Or with custom options
py mcp_server.py --host 127.0.0.1 --port 8000 --timeout 900 --vscode-port 3001
```

The server will start on `http://127.0.0.1:8000` by default.

### Configure Cursor/VSCode

Add the MCP server configuration to your Cursor settings with the button below.

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=prompt-for-user-input-mcp&config=eyJ1cmwiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAvcHJvbXB0LWZvci11c2VyLWlucHV0LW1jcC8ifQ%3D%3D)

OR Create or update your MCP configuration file with:

```json
{
  "mcpServers": {
    "prompt-for-user-input-mcp": {
      "url": "http://127.0.0.1:8000/prompt-for-user-input-mcp/"
    }
  }
}
```

For Cursor, you can use the provided `cursor-mcp-config.json` file as a reference, or use the one-click deeplink.

## Configuration Options

### MCP Server Options

- `--host`: Host to run the server on (default: 127.0.0.1)
- `--port`: Port to run the server on (default: 8000)
- `--timeout`: Timeout in seconds for user responses (default: 900)
- `--vscode-port`: Port where the VSCode extension is running (default: 3001)

### VSCode Extension Options

The VSCode extension port can be configured through the extension settings:

1. Open VSCode Settings (Ctrl+,)
2. Search for "Prompt For User Input MCP"
3. Modify the "Server Port" setting to your desired port number
4. Restart VSCode for the changes to take effect

**Important:** Make sure the `--vscode-port` argument matches the port configured in your VSCode extension settings.
