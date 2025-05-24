# Prompt User Input MCP Server

An MCP (Model Context Protocol) server that allows AI models to prompt users for input during conversations. This server uses **Streamable HTTP** transport for seamless integration with Cursor and other MCP-compatible clients.

## Features

- **Interactive User Prompts**: Allows AI models to request user input via a modern webview interface
- **Streamable HTTP Transport**: Uses HTTP-based communication for reliable client-server integration
- **VSCode Extension Integration**: Beautiful webview interface with state persistence and flexbox layout
- **Cross-Platform Support**: Works on Windows, macOS, and Linux through VSCode/Cursor
- **Robust Error Handling**: Comprehensive logging and graceful error recovery
- **State Persistence**: User input is preserved when webview loses focus
- **Professional UI**: Modern, accessible interface with VSCode theming

## Recent Improvements

### Version 1.1.0 (Latest)

- ✅ **Flexbox Layout**: Modern CSS architecture replacing margin-based positioning
- ✅ **State Persistence**: Text input preserved when webview loses/regains focus
- ✅ **Enhanced Error Handling**: Comprehensive logging and error recovery
- ✅ **Improved UX**: Better keyboard shortcuts and user experience
- ✅ **Security**: XSS protection and input sanitization

## Prerequisites

- Python 3.8+ (use `py --version` to check)
- Cursor IDE or VSCode
- Node.js and npm (for the VSCode extension)

## Quick Start

### 1. Install Python Dependencies

```cmd
py -m pip install "mcp[cli]" requests
```

### 2. Set Up the VSCode Extension

```cmd
# Navigate to the extension directory
cd extension

# Install extension dependencies
npm install

# Compile the extension
npm run compile
```

### 3. Install the Extension in VSCode/Cursor

```cmd
# In the extension directory
npm install -g vsce
vsce package

# This creates a .vsix file you can install via:
# Extensions: Install from VSIX... command in VSCode/Cursor
```

### 4. Start the MCP Server

```cmd
# Default: Run on 127.0.0.1:8000
py mcp_server.py

# Custom port: Run on a different port
py mcp_server.py --port 9000

# Custom host and port
py mcp_server.py --host 0.0.0.0 --port 3000
```

The server will start on `http://127.0.0.1:8000/prompt-for-user-input-mcp` by default.

## Configuration for Cursor

### Method 1: Via Cursor Settings UI

1. **Open Cursor Settings** → Go to **Settings** → **Features** → **MCP Servers**
2. **Add Server Configuration** with these settings:
   - **Name**: `prompt-for-user-input-mcp`
   - **URL**: `http://127.0.0.1:8000/prompt-for-user-input-mcp/` (or your custom host:port)

### Method 2: Configuration File

Copy the contents of `cursor-mcp-config.json` to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "prompt-for-user-input-mcp": {
      "url": "http://127.0.0.1:8000/prompt-for-user-input-mcp/"
    }
  }
}
```

**Important**: Ensure both the MCP server and VSCode extension are running before configuring Cursor.

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

```json
{
  "name": "prompt_for_user_input",
  "arguments": {
    "prompt": "What specific functionality would you like me to implement next?",
    "title": "Implementation Planning"
  }
}
```

This opens a professional webview panel in VSCode/Cursor with:

- Formatted question text (selectable and copyable)
- Large text input area with state persistence
- Submit/Cancel buttons
- Keyboard shortcuts (Enter to submit, Shift+Enter for new line)

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--port` | `-p` | Port to run the server on | `8000` |
| `--host` |  | Host to bind the server to | `127.0.0.1` |
| `--version` | `-v` | Show version information | |
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

# Show version and help
py mcp_server.py --version
py mcp_server.py --help
```

## Architecture & Components

### Core Components

- **`mcp_server.py`**: FastMCP-based Streamable HTTP server with comprehensive error handling
- **`extension/src/extension.ts`**: VSCode extension with modern webview interface
- **Webview Interface**: Professional UI with flexbox layout and state persistence
- **HTTP Communication**: Reliable request/response between MCP server and extension

### Communication Flow

1. **Extension Startup**: VSCode extension starts HTTP server on port 3001
2. **Server Startup**: FastMCP server starts with Streamable HTTP transport on port 8000
3. **Client Connection**: Cursor connects to MCP server endpoint
4. **Tool Call**: AI model calls `prompt_for_user_input` with question
5. **Extension Communication**: MCP server sends HTTP request to extension
6. **User Interface**: Extension creates webview with formatted question and input
7. **User Interaction**: User types response (preserved via state persistence)
8. **Response Return**: Extension returns response to MCP server → AI model

### Security Features

- **Input Sanitization**: XSS protection via HTML escaping
- **Secure Communication**: Localhost-only HTTP endpoints
- **Content Security**: Webview with restricted capabilities
- **Error Isolation**: Graceful error handling and recovery

## Testing & Verification

### Test the MCP Server

```cmd
# Start the server
py mcp_server.py

# Test the endpoint
curl -i http://127.0.0.1:8000/prompt-for-user-input-mcp/
```

Expected response:

- `HTTP/1.1 200 OK`
- Valid MCP server response

### Test the VSCode Extension

```cmd
# Check extension health
curl http://localhost:3001/health
```

Expected response:

```json
{"status":"ok","timestamp":"2024-01-15T10:30:00.123Z"}
```

### Integration Test

1. Start both MCP server and VSCode extension
2. Configure Cursor with the MCP server
3. Use the system prompt with an AI model
4. Verify the webview appears and responds correctly

## Troubleshooting

### Common Issues

#### "Tool prompt_for_user_input not found"

- Ensure MCP server is running: `py mcp_server.py`
- Check Cursor MCP configuration
- Verify server responds: `curl http://127.0.0.1:8000/prompt-for-user-input-mcp/`

#### "Server not connecting"

- Check if port 8000 is in use: `netstat -an | grep 8000`
- Try different port: `py mcp_server.py --port 9000`
- Check firewall settings

#### "Extension unavailable" or User input dialog not appearing

- Verify extension is active in VSCode Extensions panel
- Test extension health: `curl http://localhost:3001/health`
- Check VSCode Developer Console (Help > Toggle Developer Tools)
- Ensure extension compiled successfully: `npm run compile`

#### State not persisting" or Input lost on focus change

- Check browser console for JavaScript errors
- Verify extension is using latest version with state persistence
- Try refreshing the webview panel

### Debug Commands

```cmd
# Check MCP server status
curl -s http://127.0.0.1:8000/prompt-for-user-input-mcp/ | jq

# Check extension status
curl -s http://localhost:3001/health | jq

# Test with verbose logging
py mcp_server.py --host 127.0.0.1 --port 8000

# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :3001
```

### Log Locations

- **MCP Server**: Console output with timestamps
- **VSCode Extension**: VSCode Developer Console
- **Cursor**: Cursor Developer Console (Help > Toggle Developer Tools)

## Platform Compatibility

| Platform | Support |
|----------|---------|
| **Windows** | Full |
| **macOS** | Full |
| **Linux** | Full |

All platforms work through the VSCode extension interface with identical functionality.

## Files Overview

- **`mcp_server.py`**: Main MCP server with FastMCP and error handling
- **`extension/`**: VSCode extension directory
  - **`src/extension.ts`**: Main extension code with webview management
  - **`package.json`**: Extension manifest and dependencies
  - **`tsconfig.json`**: TypeScript configuration
- **`cursor-mcp-config.json`**: Example Cursor configuration
- **`requirements.txt`**: Python dependencies
- **`pyproject.toml`**: Python project configuration
- **`README.md`**: This comprehensive documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper error handling and logging
4. Test thoroughly on multiple platforms
5. Update documentation as needed
6. Submit a pull request

## Version History

- **v1.1.0**: Flexbox layout, state persistence, enhanced error handling
- **v1.0.0**: Initial release with basic functionality

## License

This project is licensed under the MIT License. See LICENSE file for details.
