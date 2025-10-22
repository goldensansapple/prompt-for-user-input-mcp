import logging
import os
import contextlib
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    SimpleUser,
)
from starlette.routing import Mount

logger = logging.getLogger(__name__)


class NoAuthenticationTokenError(Exception):
    """Exception raised when no authentication token is found."""

    def __init__(self):
        super().__init__(
            "No PROMPT_FOR_USER_INPUT_MCP_AUTH_TOKEN environment variable found."
        )


# Generate or load authentication token
AUTH_TOKEN = os.environ.get("PROMPT_FOR_USER_INPUT_MCP_AUTH_TOKEN")
if not AUTH_TOKEN:
    raise NoAuthenticationTokenError()


class BearerAuthBackend(AuthenticationBackend):
    """Middleware to validate authentication token."""

    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return
        auth_header = conn.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            return
        token = auth_header.split(" ")[1]
        if token != AUTH_TOKEN:
            return
        return AuthCredentials(["authenticated"]), SimpleUser(
            "prompt-for-user-input-mcp"
        )


mcp = FastMCP(
    "prompt-for-user-input-mcp",
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


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield


app = Starlette(
    routes=[
        Mount("/", app=mcp.streamable_http_app()),
    ],
    middleware=[Middleware(AuthenticationMiddleware, backend=BearerAuthBackend())],
    lifespan=lifespan,
)
