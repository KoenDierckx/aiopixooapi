"""Main module for the aiopixooapi project.

This module demonstrates interacting with Divoom and Pixoo64 devices
using asynchronous API calls.
"""

import asyncio
import logging

from aiopixooapi.divoom import Divoom
from aiopixooapi.pixoo64 import Pixoo64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Interact with Divoom and Pixoo64 devices asynchronously.

    This function demonstrates fetching dial types and dial lists from a Divoom device,
    as well as retrieving all settings from a Pixoo64 device.
    """
    async with Divoom() as divoom:
        # Get dial types
        dial_types = await divoom.get_dial_type()
        logger.info(dial_types)

        # Get dial list for a specific type and page
        dial_list = await divoom.get_dial_list("Social", 1)
        logger.info(dial_list)

    async with Pixoo64("10.116.4.238") as pixoo64:
        # Get all settings
        settings = await pixoo64.get_all_settings()
        logger.info(settings)

asyncio.run(main())
