#!/usr/bin/env python3
"""
MCP Plexus Stdio Entry Point (Simplified)
Provides stdio transport support for MCP Plexus server.
"""
import asyncio
import logging
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from fastmcp import FastMCP
from mcp_plexus.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s STDIO - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger("mcp_plexus_stdio")

async def main():
    """
    Main entry point for stdio transport.
    Runs the MCP Plexus server using stdio communication.
    """
    logger.info("Starting MCP Plexus server with stdio transport")
    
    # Load environment variables from .env file if it exists
    dotenv_path = project_root / ".env"
    if dotenv_path.exists():
        logger.info(f"Loading .env from {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path, override=True)
    else:
        logger.warning(f".env file not found at {dotenv_path}")
    
    # Create a simple FastMCP instance for stdio
    plexus_mcp = FastMCP(
        name="MCP_Plexus_Stdio",
        instructions="MCP Plexus Server - Simplified stdio mode",
        log_level=settings.plexus_fastmcp_log_level
    )
    
    logger.info(f"FastMCP instance ready: {plexus_mcp.name}")
    
    # Add some example tools
    @plexus_mcp.tool()
    def echo(text: str) -> str:
        """Echo the input text"""
        return f"Echo: {text}"
    
    @plexus_mcp.tool()
    def get_info() -> str:
        """Get information about this MCP server"""
        return "MCP Plexus - Multi-Tenant, OAuth-Enabled MCP Server Framework"
    
    # Run the server with stdio transport
    try:
        await plexus_mcp.run_stdio_async()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())