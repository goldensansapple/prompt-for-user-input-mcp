import logging
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

mcp = FastMCP("prompt-for-user-input-mcp", port=4444)


class PromptForUserInputResponse(BaseModel):
    response: str = Field(description="The user's response to the prompt.")


@mcp.tool()
async def prompt_for_user_input(prompt: str, ctx: Context[ServerSession, None]) -> str:
    """Prompt the user for input."""
    try:
        logger.info("Prompting...")
        result = await ctx.elicit(message=prompt, schema=PromptForUserInputResponse)
        logger.info("Successfully obtained user response, returning to MCP client")
        if result.action == "accept" and result.data:
            if result.data.response:
                return result.data.response
            else:
                return "The user did not provide a response."
        return "The user did not provide a response."
    except Exception as error:
        error_message = f"[Error getting user input: {str(error)}. The user will provide the input in a moment. End the generation.]"
        logger.info(f"Returning error message to MCP client: {error_message}")
        return error_message


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
