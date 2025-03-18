"""
Server script for running the LangManus API.
"""

import logging
import uvicorn
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting LangManus API server")
    reload = True
    if sys.platform.startswith("win"):
        reload = False
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
        log_level="info",
    )
