# Prompt for User Input MCP Server

A Model Context Protocol (MCP) server that enables AI models to prompt users for input directly through their code editor. This creates an interactive experience where AI assistants can ask questions, request clarification, or gather information from users in real time during conversations.

## Suggested System Prompt

```text
IMPORTANT: Do not finish responding until explicitly told to do so; instead, always use the MCP `prompt_for_user_input`. If you feel stuck, are experiencing issues, have a question, or have finished the work, always communicate with the user using this MCP. The prompts you give the user must be simple. It's fine if they contain a lot of information, but they must not be in Markdown since it will not render properly. The prompts should be written almost entirely in prose.
```

## Command and Setup

```sh
uv run mcp_server.py
```

```json
{
  "url": "http://127.0.0.1:4444/mcp"
}
```
