#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import time
import logging
import requests
import uuid
import argparse
from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# VSCode extension endpoint
VSCODE_EXTENSION_URL = "http://localhost:3001"


def prompt_via_vscode_extension(prompt: str, title: str) -> str:
    """
    Prompt user via VSCode extension API.

    Args:
        prompt: The message/question to show to the user
        title: Optional title for the prompt dialog

    Returns:
        The user's response as a string
    """
    try:
        health_response = requests.get(f"{VSCODE_EXTENSION_URL}/health", timeout=2)
        if health_response.status_code != 200:
            raise Exception("Extension health check failed")

        prompt_data = {"id": str(uuid.uuid4()), "title": title, "prompt": prompt}

        response = requests.post(
            f"{VSCODE_EXTENSION_URL}/prompt",
            json=prompt_data,
            timeout=3600,  # 1 hour timeout
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "[Error: No response from extension]")
        else:
            raise Exception(f"Request failed with status {response.status_code}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")
    except Exception as e:
        raise Exception(f"Extension error: {e}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MCP Server for User Input Prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  py mcp_server.py                          # Run on default port 8000
  py mcp_server.py --port 9000              # Run on port 9000
  py mcp_server.py -p 3000                  # Run on port 3000
  py mcp_server.py --host 0.0.0.0           # Run on all interfaces
  py mcp_server.py --host 0.0.0.0 -p 3000   # Run on all interfaces on port 3000
""",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to run the MCP server on (default: 127.0.0.1)",
    )

    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Port to run the MCP server on (default: 8000)",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s 1.0.0",
        help="Show version information",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    logger.info(f"Starting MCP server for user input prompts")
    logger.info(f"Host: {args.host}")
    logger.info(f"Port: {args.port}")

    mcp = FastMCP(
        "prompt-for-user-input-mcp",
        streamable_http_path="/prompt-for-user-input-mcp",
        host=args.host,
        port=args.port,
    )

    @mcp.tool(
        name="prompt_for_user_input",
        description="Prompt the user for input with an optional title.",
    )
    def prompt_for_user_input(prompt: str, title: str = "User Input Required") -> str:
        """
        Prompt the user for input with an optional title.
        Use this to ask questions, get clarification, or request information from the user.

        Args:
            prompt: The message/question to show to the user
            title: Optional title for the prompt dialog

        Returns:
            The user's response as a string
        """
        try:
            logger.info(f"Attempting VSCode extension prompt: {title[:50]}...")
            return prompt_via_vscode_extension(prompt, title)

        except Exception as e:
            logger.warning(f"VSCode extension unavailable: {e}")
            return f"[Error getting user input: {str(e)}]"

    try:
        # Run the server with Streamable HTTP transport for Cursor integration
        logger.info(
            f"Starting MCP server with Streamable HTTP transport on {args.host}:{args.port}..."
        )
        mcp.run(
            transport="streamable-http",
        )
    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(
                f"Port {args.port} is already in use. Try a different port with --port <number>"
            )
            logger.error(f"Example: python mcp_server.py --port {args.port + 1}")
            sys.exit(1)
        else:
            logger.error(f"Failed to start server: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
