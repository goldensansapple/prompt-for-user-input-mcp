# VSCode Extension Setup Guide

This guide shows how to set up native in-editor input dialogs for the MCP user prompt extension using a custom VSCode extension.

## Overview

Instead of popup console windows, this approach provides:

- ✅ Native VSCode input boxes
- ✅ Stays within the editor
- ✅ Better UX integration
- ✅ Graceful fallback to console
- ✅ Works in both Cursor and VSCode

## Architecture

```flow
AI Model → MCP Server → VSCode Extension → Native Input Dialog → User
```

## Setup Steps

### 1. Build the VSCode Extension

```bash
cd extension
npm install
npm run compile
```

### 2. Install the Extension

#### Option A: Install in Development Mode

1. Open VSCode/Cursor
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Extensions: Install from VSIX..."
4. Navigate to the `extension` folder and package it:

```bash
cd extension
npm install -g vsce
vsce package
```

This creates a `.vsix` file you can install.

#### Option B: Development Mode (Recommended for testing)

1. Open VSCode/Cursor
2. Press `F5` or go to Run > Start Debugging
3. This opens a new Extension Development Host window
4. The extension will be active in that window

### 3. Use the Enhanced MCP Server

Use `mcp_server_vscode.py` instead of the original `mcp_server.py`:

```bash
python mcp_server_vscode.py
```

### 4. Configure Cursor/VSCode

Update your MCP configuration to use the enhanced server:

```json
{
  "mcpServers": {
    "prompt-for-user-input-mcp": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## How It Works

1. **Extension Startup**: VSCode extension starts an HTTP server on port 3001
2. **MCP Tool Call**: When AI calls `prompt_for_user_input`, the MCP server tries VSCode first
3. **Native Dialog**: Extension shows VSCode's native input box
4. **Response**: User types response, it's sent back to MCP server
5. **Fallback**: If extension unavailable, falls back to console popup

## Features

### Native VSCode Input Box

- Appears as a native VSCode input dialog
- Stays focused and modal
- Supports multi-line input
- Proper keyboard shortcuts (Esc to cancel)

### Graceful Fallback

- If VSCode extension isn't available, automatically falls back to console popup
- No disruption to existing workflows

### Cross-Platform Support

- Works in both VSCode and Cursor
- Windows console fallback maintained
- Easy to extend for Linux/macOS

## Extension API

The VSCode extension exposes these endpoints:

### `GET /health`

Health check to verify extension is running:

```bash
curl http://localhost:3001/health
```

### `POST /prompt`

Show input dialog:

```json
{
  "id": "unique-id",
  "title": "Optional Title",
  "prompt": "What would you like me to do?"
}
```

Response:

```json
{
  "response": "User's typed response"
}
```

## Advanced Configuration

### Custom Ports

To change the extension port, edit `extension/src/extension.ts`:

```typescript
const port = 3001; // Change this
```

Then update `mcp_server_vscode.py`:

```python
VSCODE_EXTENSION_URL = "http://localhost:3001" # Match the port
```

### Enhanced Input Types

The extension can be extended to support:

- Multi-line text areas
- Dropdown selections
- File pickers
- Custom forms

## Troubleshooting

### Extension Not Found

1. Verify extension is installed and active
2. Check `http://localhost:3001/health` responds
3. Look at VSCode Developer Console for errors

### Port Conflicts

1. Change extension port in `extension.ts`
2. Update MCP server URL accordingly
3. Restart both extension and MCP server

### Input Dialog Issues

1. Check VSCode focus (dialog might be behind)
2. Try pressing `Esc` and triggering again
3. Check Developer Console for extension errors

## Development

### Adding New Input Types

To add more sophisticated input options:

1. **Multi-line Input**:

```typescript
const result = await vscode.window.showInputBox({
    title: title,
    prompt: prompt,
    placeHolder: 'Enter your response...',
    ignoreFocusOut: true,
    // Add these for multi-line:
    validateInput: (text) => {
        // Custom validation
        return null; // or error message
    }
});
```

2. **Quick Pick (Dropdown)**:

```typescript
const items = ['Option 1', 'Option 2', 'Option 3'];
const result = await vscode.window.showQuickPick(items, {
    title: title,
    placeHolder: prompt
});
```

3. **Custom Webview**:
For complex forms, create a webview panel with HTML/CSS/JS.

### Publishing the Extension

To publish to VSCode Marketplace:

1. Create publisher account at <https://marketplace.visualstudio.com>
2. Get Personal Access Token
3. Package and publish:

```bash
vsce package
vsce publish
```

## Alternative Approaches

### Option 1: Command Palette Integration

Instead of HTTP server, use VSCode commands:

```typescript
vscode.commands.registerCommand('extension.promptUser', async (prompt, title) => {
    return await vscode.window.showInputBox({title, prompt});
});
```

### Option 2: Notification-Based

Use VSCode notifications for non-blocking prompts:

```typescript
const action = await vscode.window.showInformationMessage(
    prompt, 
    { modal: true }, 
    'Respond'
);
```

### Option 3: Webview Panel

Create a dedicated panel for more complex interactions:

```typescript
const panel = vscode.window.createWebviewPanel(
    'userInput',
    title,
    vscode.ViewColumn.Beside,
    { enableScripts: true }
);
```

## Next Steps

1. **Try the basic setup** with the provided extension
2. **Test the flow** with a simple MCP tool call
3. **Customize the UI** based on your needs
4. **Extend functionality** with additional input types
5. **Consider publishing** if it works well for your team

This approach gives you the best of both worlds: native editor integration when available, with reliable console fallback for all scenarios.
