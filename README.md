# Prompt for User Input MCP Server

An MCP (Model Context Protocol) server that enables AI models to prompt users for input directly through their code editor. This creates an interactive experience where AI assistants can ask questions, request clarification, or gather information from users in real-time during conversations.

## Quick Start

### Prerequisites

- Python 3
- Cursor IDE (or VSCode)
- Node.js (for building the extension)

### 1. Install the MCP Server

```bash
# Clone the repository
git clone <repository-url>
cd prompt_for_user_input_mcp

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install and Activate the Cursor Extension

```bash
# Navigate to the extension directory
cd extension

# Package the extension into a VSIX
vsce package
```

Install the extension in Cursor:

1. Open Cursor
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Extensions: Install from VSIX..."
4. Select the `.vsix` file from the `extension` directory

### 3. Start the MCP Server

```bash
# From the project root directory
py mcp_server.py

# Or with custom options
py mcp_server.py --host 127.0.0.1 --port 8000 --timeout 3600
```

The server will start on `http://127.0.0.1:8000` by default.

### 4. Configure Cursor

Add the MCP server configuration to your Cursor settings. Create or update your MCP configuration file with:

```json
{
  "mcpServers": {
    "prompt-for-user-input-mcp": {
      "url": "http://127.0.0.1:8000/prompt-for-user-input-mcp/"
    }
  }
}
```

For Cursor, you can use the provided `cursor-mcp-config.json` file as a reference.

## Configuration Options

### MCP Server Options

- `--host`: Host to run the server on (default: 127.0.0.1)
- `--port`: Port to run the server on (default: 8000)
- `--timeout`: Timeout in seconds for user responses (default: 3600)
