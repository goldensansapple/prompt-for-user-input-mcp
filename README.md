# Prompt User Input MCP Server

An MCP (Model Context Protocol) server that allows AI models to prompt users for input during conversations. This server uses **Streamable HTTP** transport for seamless integration with Cursor and other MCP-compatible clients.

## Features

- **Single Tool**: Exposes `prompt_for_user_input` tool for models to use
- **Streamable HTTP Transport**: Uses streamable HTTP for reliable client-server communication
- **VS Code Extension**: Attempts to use VS Code extension

## Install

### Prerequisites

- Python 3.8+ (use `py --version` to check)
- Cursor IDE

### Step 1: Install Dependencies

```cmd
py -m pip install "mcp[cli]"
```

### Step 2: Start the Server

```cmd
# Default: Run on 127.0.0.1:8000
py mcp_server.py

# Custom port: Run on a different port
py mcp_server.py --port 9000

# Custom host and port
py mcp_server.py --host 0.0.0.0 --port 3000

# Show version
py mcp_server.py --version

# Get help
py mcp_server.py --help
```

The server will start on `http://127.0.0.1:8000/prompt-for-user-input-mcp` by default

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--port` | `-p` | Port to run the server on | `8000` |
| `--host` |  | Host to bind the server to | `127.0.0.1` |
| `--version` |  | Show version information | |
| `--help` | `-h` | Show help message | |

### Examples

```cmd
# Run on default port 8000
py mcp_server.py

# Run on port 9000
py mcp_server.py --port 9000
py mcp_server.py -p 9000

# Run on all interfaces, port 3000
py mcp_server.py --host 0.0.0.0 --port 3000

# Show version
py mcp_server.py --version
```

## Configuration for Cursor

### Method 1: Via Cursor Settings UI

1. **Open Cursor Settings** → Go to **Settings** → **Features** → **MCP Servers**
2. **Add Server Configuration** with these settings:
   - **Name**: `prompt-for-user-input-mcp`
   - **URL**: `http://127.0.0.1:8000/prompt-for-user-input-mcp` (or your custom host:port)

### Method 2: Configuration File

Copy the contents of `cursor-mcp-config.json` to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "prompt-for-user-input-mcp": {
      "url": "http://127.0.0.1:8000/prompt-for-user-input-mcp"
    }
  }
}
```

**Important**: Make sure the MCP server is running before configuring Cursor.

## Usage

### System Prompt for Models

Use this system prompt to ensure the model uses the MCP tool instead of finishing responses:

```text
IMPORTANT - Do not finish responding until explicitly told to do so, instead always use MCP `prompt_for_user_input` and wait for response in all cases. If you feel stuck, have a question or you are finished with the work, always communicate with the user using this MCP.
```

### Tool Parameters

The `prompt_for_user_input` tool accepts:

- **`prompt`** (required): The message/question to show to the user
- **`title`** (optional): A title for the prompt dialog (default: "User Input Required")

### Example Usage

When the model needs user input, it will call:

```json
{
  "name": "prompt_for_user_input",
  "arguments": {
    "prompt": "What specific functionality would you like me to implement next?",
    "title": "Implementation Planning"
  }
}
```

On Windows, this will open a new console window showing:

```text
============================================================
Implementation Planning
============================================================

What specific functionality would you like me to implement next?

Please enter your response: 
```

## Files Overview

- **`mcp_server.py`**: FastMCP-based Streamable HTTP server (main implementation)
- **`cursor-mcp-config.json`**: Cursor configuration for Streamable HTTP connection
- **`README.md`**: This documentation

## Testing the Server

### Test the server independently

```cmd
py mcp_server.py
```

This will start the Streamable HTTP server on `http://127.0.0.1:8000/prompt-for-user-input-mcp`. You can test the endpoint:

```cmd
curl -i http://127.0.0.1:8000/prompt-for-user-input-mcp
```

You should see:

- `HTTP/1.1 200 OK`
- Proper MCP server response

## Troubleshooting

### Common Issues

1. **"Tool prompt_for_user_input not found"**:
   - Ensure the MCP server is running: `py mcp_server.py`
   - Check that `http://127.0.0.1:8000/prompt-for-user-input-mcp` is accessible
   - Restart Cursor after updating configuration

2. **"Server not connecting"**:
   - Verify the server is running on the correct port (8000)
   - Check Windows firewall isn't blocking the connection
   - Ensure no other service is using port 8000

3. **"Error getting user input"**:
   - This is normal on non-Windows systems (not yet implemented)
   - On Windows, check if console popups are being blocked

### Debug Tips

- Check if server is running: `curl http://127.0.0.1:8000/prompt-for-user-input-mcp`
- Check Cursor's developer console for MCP-related messages
- Verify your system prompt includes the `prompt_for_user_input` instruction

## How It Works

1. **Server Startup**: FastMCP server starts with Streamable HTTP transport on port 8000
2. **Client Connection**: Cursor connects to `http://127.0.0.1:8000/prompt-for-user-input-mcp`
3. **Tool Call**: When the AI model needs user input, it calls `prompt_for_user_input`
4. **User Prompt**: On Windows, a new console window opens for input (or VS Code extension if available)
5. **Response Collection**: User types response, which is captured and returned
6. **Model Continues**: The model uses the user's response to continue the conversation

## Platform Compatibility

- **Windows**: Full support with console popup dialogs
- **Linux/macOS**: Not yet implemented (contributions welcome!)

## Architecture

This implementation uses:

- **FastMCP**: High-level MCP server framework
- **Streamable HTTP Transport**: HTTP-based communication for web integration
- **Subprocess**: Separate console windows for user input on Windows
- **Temporary Files**: For passing data between processes
- **VS Code Extension**: Primary method for user input (with console fallback)
