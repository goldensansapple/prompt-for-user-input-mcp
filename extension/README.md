# Prompt For User Input MCP

A VSCode extension that enables AI assistants and MCP (Model Context Protocol) servers to interactively request user input through native VSCode dialogs. This creates a seamless experience where AI assistants can ask questions, request clarification, or gather information from users in real-time during conversations.

## Installation

### From VSCode Marketplace

1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Prompt For User Input MCP"
4. Click Install

## Setup with MCP Server

This extension works with the companion MCP server. To set up the complete system:

1. **Install the MCP Server**: Follow the instructions at [prompt-for-user-input-mcp](https://github.com/goldensansapple/prompt-for-user-input-mcp)
2. **Start the Server**: Run the MCP server on your local machine
3. **Configure Your AI Assistant**: Add the MCP server to your AI assistant's configuration
4. **Install This Extension**: Install this VSCode extension
5. **Ready to Go**: Your AI assistant can now prompt for user input!

## Usage

Once installed and configured, the extension works automatically. When an AI assistant needs user input:

1. A dialog will appear in VSCode with the AI's question
2. Type your response in the text area
3. Press Enter or click Submit to send your response
4. The AI assistant will receive your input and continue

### Keyboard Shortcuts

- **Enter**: Submit response
- **Shift+Enter**: Add new line
- **Escape**: Cancel (sends "[Cancelled by user]" to the AI)

## Configuration

The extension runs on port 3001 by default. If you need to change this, you can modify the port in the extension settings or rebuild the extension.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [MCP Server](https://github.com/goldensansapple/prompt-for-user-input-mcp) - The companion MCP server
- [Model Context Protocol](https://github.com/modelcontextprotocol/specification) - The protocol specification
