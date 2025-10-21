import logging
import os
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger(__name__)

# Generate or load authentication token
AUTH_TOKEN = os.environ.get("PROMPT_FOR_USER_INPUT_MCP_AUTH_TOKEN")
if not AUTH_TOKEN:
    raise ValueError(
        "No PROMPT_FOR_USER_INPUT_MCP_AUTH_TOKEN environment variable found."
    )


class AuthMiddleware:
    """Middleware to validate authentication token."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # Construct request to access headers
        request = Request(scope, receive=receive)

        # Check for Bearer token in Authorization header
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            response = JSONResponse(
                {"error": "Missing or invalid Authorization header"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return

        token = auth_header[7:]  # Remove "Bearer " prefix

        if token != AUTH_TOKEN:
            response = JSONResponse(
                {"error": "Invalid authentication token"}, status_code=403
            )
            await response(scope, receive, send)
            return

        # Token is valid, continue
        await self.app(scope, receive, send)


auth_middleware = Middleware(AuthMiddleware)

mcp = FastMCP(
    "prompt-for-user-input-mcp",
    port=4444,
    middleware=auth_middleware,
)


class PromptForUserInputResponse(BaseModel):
    response: str = Field(description="The user's response to the prompt.")


@mcp.tool()
async def prompt_for_user_input(prompt: str, ctx: Context[ServerSession, None]) -> str:
    """Prompt the user for input."""
    try:
        result = await ctx.elicit(message=prompt, schema=PromptForUserInputResponse)
        if result.action == "accept" and result.data:
            if result.data.response:
                return result.data.response
            else:
                return "The user did not provide a response."
        return "The user did not provide a response."
    except Exception as error:
        error_message = f"[Error retrieving user input: {error}. The user will provide the input shortly. End the generation.]"
        logger.error(f"Returning error message to MCP client: {error_message}")
        return error_message


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
