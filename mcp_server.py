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
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# VSCode extension endpoint
VSCODE_EXTENSION_URL = "http://localhost:3001"


def format_log_parameter(
    param: str,
    need_apply_ellipsis: bool = True,
    max_length: int = 50,
) -> str:
    """
    Format individual parameters in log messages with appropriate truncation.

    Args:
        param: The parameter value to format
        max_length: Maximum length before truncation

    Returns:
        Formatted parameter with appropriate truncation
    """

    # Regular parameters: truncate if too long
    if len(param) > max_length and need_apply_ellipsis:
        return param[: max_length - 3] + "..."
    elif len(param) > max_length:
        return param[:max_length]

    return param


def prompt_via_vscode_extension(prompt: str, title: str, timeout: int = 3600) -> str:
    """
    Prompt user via VSCode extension API.

    Args:
        prompt: The message/question to show to the user
        title: Optional title for the prompt dialog
        timeout: Timeout in seconds for waiting for user response

    Returns:
        The user's response as a string
    """
    try:
        logger.info(
            f"Checking VSCode extension health at {VSCODE_EXTENSION_URL}/health..."
        )
        health_response = requests.get(f"{VSCODE_EXTENSION_URL}/health", timeout=2)
        if health_response.status_code != 200:
            raise Exception("Extension health check failed")

        prompt_data = {"id": str(uuid.uuid4()), "title": title, "prompt": prompt}

        logger.info(
            f"Sending prompt to VSCode extension: {format_log_parameter(prompt_data['title'], need_apply_ellipsis=False)}..."
        )
        response = requests.post(
            f"{VSCODE_EXTENSION_URL}/prompt",
            json=prompt_data,
            timeout=timeout,
        )

        if response.status_code == 200:
            result = response.json().get("response")
            if result:
                logger.info(
                    f"Received response from VSCode extension: {format_log_parameter(result)}"
                )
                return result
            else:
                raise Exception("No response from extension")
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
        usage="py mcp_server.py [--host <host>] [--port <port>] [--timeout <seconds>]",
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
        "--timeout",
        "-t",
        type=int,
        default=3600,
        help="Timeout in seconds for user input prompts (default: 3600)",
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

    logger.info("Starting MCP server for user input prompts...")
    logger.info(f"Host: {args.host}")
    logger.info(f"Port: {args.port}")
    logger.info(f"Timeout: {args.timeout} seconds")

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
            logger.info(
                f"Attempting VSCode extension prompt: {format_log_parameter(title, need_apply_ellipsis=False)}..."
            )
            return prompt_via_vscode_extension(prompt, title, args.timeout)

        except Exception as e:
            logger.warning(f"VSCode extension unavailable: {str(e)}")
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
            logger.error(f"Port {args.port} is already in use.")
            sys.exit(1)
        else:
            logger.error(f"Unexpected error: {str(e)}")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
