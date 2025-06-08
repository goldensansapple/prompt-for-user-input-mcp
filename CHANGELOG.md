# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-26

### Added
- Initial release of the Prompt for User Input MCP Server
- MCP server that enables AI models to prompt users for input through their code editor
- VS Code extension for native input dialogs
- Cursor IDE integration with one-click installation
- Asynchronous HTTP transport for real-time user interaction
- Configurable timeout and port settings
- Health check endpoint for extension availability
- Comprehensive error handling and logging
- Support for custom prompt titles and messages
- Console script entry point for easy installation

### Features
- **MCP Server**: Streamable HTTP transport compatible with Cursor IDE
- **VS Code Extension**: Native input dialogs with keyboard shortcuts
- **Interactive Experience**: Real-time Q&A between AI and users
- **Configuration**: Flexible host, port, and timeout settings
- **Error Handling**: Graceful fallback when extension unavailable
- **Documentation**: Complete setup and usage instructions

### Technical Details
- Python 3.8+ compatibility
- FastMCP framework integration
- Aiohttp for async HTTP operations
- Express.js backend for VS Code extension
- TypeScript extension with proper bundling
- MIT License for open source distribution 