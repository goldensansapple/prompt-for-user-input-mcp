#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import time
import logging
import requests
import uuid
from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP("prompt-for-user-input-mcp")

# VSCode extension endpoint
VSCODE_EXTENSION_URL = "http://localhost:3001"


@mcp.tool()
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
    response_file = None

    try:
        # First, try to use VSCode extension (preferred method)
        try:
            logger.info(f"Attempting VSCode extension prompt: {title[:50]}...")
            response = prompt_via_vscode_extension(prompt, title)
            if response and not response.startswith("[Error"):
                return response
            logger.warning("VSCode extension failed, falling back to console")
        except Exception as e:
            logger.warning(f"VSCode extension unavailable: {e}, falling back to console")

        # Fallback to console method
        if os.name == "nt":  # Windows
            logger.info(f"Using console fallback: {title[:50]}...")

            # Clean the strings to avoid encoding issues
            clean_title = title.encode("ascii", "ignore").decode("ascii")
            clean_prompt = prompt.encode("ascii", "ignore").decode("ascii")

            # Create a unique response file
            response_file = f"temp_response_{uuid.uuid4().hex[:8]}.txt"
            logger.info(f"Using response file: {response_file}")

            # Get the path to the user input console script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            console_script = os.path.join(script_dir, "user_input_console.py")
            
            if not os.path.exists(console_script):
                logger.error(f"Console script not found: {console_script}")
                return "[Error: user_input_console.py not found]"

            logger.info(f"Using console script: {console_script}")

            # Run the script in a new console window
            logger.info("Starting console window...")
            process = subprocess.Popen(
                [
                    sys.executable,
                    console_script,
                    clean_title,
                    clean_prompt,
                    response_file,
                ],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )

            # Wait for completion with timeout
            timeout = 300  # 5 minutes
            start_time = time.time()

            while process.poll() is None:
                if time.time() - start_time > timeout:
                    logger.warning("Process timeout reached")
                    process.terminate()
                    return "[Timeout: No response received within 5 minutes]"
                time.sleep(0.5)

            logger.info(f"Process completed with return code: {process.returncode}")

            # Wait a bit more for file to be written
            time.sleep(1)

            # Read the response with multiple attempts
            user_response = None
            for attempt in range(5):
                try:
                    if os.path.exists(response_file):
                        with open(response_file, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            if content:  # Only accept non-empty content
                                user_response = content
                                logger.info(
                                    f"Successfully read response: {user_response[:50]}..."
                                )
                                break
                    else:
                        logger.warning(
                            f"Attempt {attempt + 1}: Response file does not exist"
                        )
                except Exception as e:
                    logger.warning(
                        f"Attempt {attempt + 1}: Error reading response file: {e}"
                    )

                if attempt < 4:  # Don't sleep on last attempt
                    time.sleep(0.5)

            if user_response is None:
                logger.error("Failed to read user response after multiple attempts")
                user_response = (
                    "[Error: Could not read user response - please try again]"
                )

            return user_response

        else:
            raise Exception("Not implemented for non-Windows systems")

    except Exception as e:
        logger.error(f"Error in input_user_prompt: {e}")
        return f"[Error getting user input: {str(e)}]"

    finally:
        # Clean up files
        if response_file and os.path.exists(response_file):
            try:
                os.remove(response_file)
                logger.info(f"Cleaned up response file: {response_file}")
            except Exception as e:
                logger.warning(f"Could not remove response file: {e}")


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
        # First check if extension is available
        health_response = requests.get(f"{VSCODE_EXTENSION_URL}/health", timeout=2)
        if health_response.status_code != 200:
            raise Exception("Extension health check failed")
        
        # Send prompt request
        prompt_data = {
            "id": str(uuid.uuid4()),
            "title": title,
            "prompt": prompt
        }
        
        response = requests.post(
            f"{VSCODE_EXTENSION_URL}/prompt",
            json=prompt_data,
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "[Error: No response received]")
        else:
            raise Exception(f"Request failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")
    except Exception as e:
        raise Exception(f"Extension error: {e}")


if __name__ == "__main__":
    # Run the server with SSE transport for Cursor integration
    logger.info("Starting MCP server with SSE transport on port 8000...")
    mcp.run(transport="sse") 