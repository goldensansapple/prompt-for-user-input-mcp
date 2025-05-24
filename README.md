# Prompt User Input MCP Server

An MCP (Model Context Protocol) server that allows AI models to prompt users for input during conversations. This server uses **Server-Sent Events (SSE)** transport for seamless integration with Cursor and other MCP-compatible clients.

## Features

- **Single Tool**: Exposes `prompt_for_user_input` tool for models to use
- **SSE Transport**: Uses Server-Sent Events for reliable client-server communication
- **Windows Console Popup**: Opens a separate console window for user input on Windows
- **Flexible Prompting**: Supports custom prompts with optional titles
- **Seamless Integration**: Works with Cursor and other MCP-compatible clients
- **Interactive Workflow**: Enables back-and-forth communication between AI and user

## Quick Installation (Windows)

### Prerequisites

- Python 3.8+ (use `py --version` to check)
- Cursor IDE

### Step 1: Install Dependencies

```cmd
py -m pip install "mcp[cli]"
```

### Step 2: Start the Server

```cmd
py mcp_server.py
```

The server will start on `http://localhost:8000/sse`

## Configuration for Cursor

### Method 1: Via Cursor Settings UI

1. **Open Cursor Settings** → Go to **Settings** → **Extensions** → **MCP Servers**
2. **Add Server Configuration** with these settings:
   - **Name**: `prompt-for-user-input-mcp`
   - **URL**: `http://localhost:8000/sse`

### Method 2: Configuration File

Copy the contents of `cursor-mcp-config.json` to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "prompt-for-user-input-mcp": {
      "url": "http://localhost:8000/sse"
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

- **`mcp_server.py`**: FastMCP-based SSE server (main implementation)
- **`cursor-mcp-config.json`**: Cursor configuration for SSE connection
- **`README.md`**: This documentation

## Testing the Server

### Test the server independently

```cmd
py mcp_server.py
```

This will start the SSE server on `http://localhost:8000/sse`. You can test the endpoint:

```cmd
curl -i http://localhost:8000/sse
```

You should see:

- `HTTP/1.1 200 OK`
- `Content-Type: text/event-stream`
- Event stream data

## Troubleshooting

### Common Issues

1. **"Tool input_user_prompt not found"**:
   - Ensure the MCP server is running: `py mcp_server.py`
   - Check that `http://localhost:8000/sse` is accessible
   - Restart Cursor after updating configuration

2. **"Server not connecting"**:
   - Verify the server is running on the correct port (8000)
   - Check Windows firewall isn't blocking the connection
   - Ensure no other service is using port 8000

3. **"Error getting user input"**:
   - This is normal on non-Windows systems (not yet implemented)
   - On Windows, check if console popups are being blocked

### Debug Tips

- Check if server is running: `curl http://localhost:8000/sse`
- Check Cursor's developer console for MCP-related messages
- Verify your system prompt includes the `prompt_for_user_input` instruction

## How It Works

1. **Server Startup**: FastMCP server starts with SSE transport on port 8000
2. **Client Connection**: Cursor connects to `http://localhost:8000/sse`
3. **Tool Call**: When the AI model needs user input, it calls `prompt_for_user_input`
4. **User Prompt**: On Windows, a new console window opens for input
5. **Response Collection**: User types response, which is captured and returned
6. **Model Continues**: The model uses the user's response to continue the conversation

## Platform Compatibility

- ✅ **Windows**: Full support with console popup dialogs
- ❌ **Linux/macOS**: Not yet implemented (contributions welcome!)

## Architecture

This implementation uses:

- **FastMCP**: High-level MCP server framework
- **SSE Transport**: Server-Sent Events for web-based communication
- **Subprocess**: Separate console windows for user input on Windows
- **Temporary Files**: For passing data between processes
