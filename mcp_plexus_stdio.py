#!/usr/bin/env python3
"""
MCP Plexus Stdio Entry Point
Provides stdio transport support for MCP Plexus server.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from mcp_plexus.mcp_handlers.tenant_mcp_app import shared_fastmcp_server_instance
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
    
    # Check if FastMCP instance is available
    if shared_fastmcp_server_instance is None:
        logger.error("FastMCP server instance not initialized")
        sys.exit(1)
    
    logger.info(f"FastMCP instance ready: {shared_fastmcp_server_instance.name}")
    
    # Run the server with stdio transport
    try:
        await shared_fastmcp_server_instance.run_stdio_async()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())