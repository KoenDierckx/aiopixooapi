"""Main module for the aiopixooapi project.

This module demonstrates interacting with Divoom and Pixoo64 devices
using asynchronous API calls.
"""

import asyncio
import logging

from aiopixooapi.divoom import Divoom

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate() -> None:
    """Interact with Divoom and Pixoo64 devices asynchronously."""
    async with Divoom() as divoom:
        # Get dial types
        dial_types = await divoom.get_dial_types()
        logger.info(dial_types)

        # Generate CHANNEL_INDEX_FACES_DICT
        channel_index_faces_dict = {}
        for dial_type in dial_types:
            dial_list = await divoom.get_dials_for_type(dial_type)
            for dial in dial_list:  # Assuming "Dials" contains the list of dials
                channel_index_faces_dict[f"{dial_type} - {dial.name}"] = dial.clockId

        logger.info("Generated CHANNEL_INDEX_FACES_DICT:")
        logger.info(channel_index_faces_dict)

        # Channels
        channel_dict = {
            "Faces": 0,
            "Cloud": 1,
            "Visualizer": 2,
            "Custom": 3,
            "Black": 4,
        }

        # Define additional dictionaries
        channel_index_cloud_dict = {
            "Recommend gallery": 0,
            "Favourite": 1,
            "Subscribe artist": 2,
            "Album": 3,
        }

        # Unofficial list, created by calling with each index from 0, and coming up with a name...
        channel_index_visualizer_dict = {
            "Rainbow line": 0,
            "Worm": 1,
            "Green bottom": 2,
            "Blue bottom": 3,
            "Green rain": 4,
            "EQ": 5,
            "Green mid": 6,
            "Rainbow bottom": 7,
            "Rainbow rain": 8,
            "Blue mirror": 9,
            "Duck": 10,
            "Dog on stage": 11,
        }

        channel_index_custom_dict = {
            "Custom 1": 0,
            "Custom 2": 1,
            "Custom 3": 2,
        }

        # Write the dictionaries to a new file
        with open("src/aiopixooapi/pixoo64_dicts.py", "w") as f:
            f.write('"""Dictionaries of Divoom Pixoo effect names to internal id\'s.\n\n')
            f.write("These were reverse engineered from the different Divoom Pixoo dials, clocks, channels ...\n")
            f.write("We keep them here hard coded for performance reasons.\n\n")
            f.write("These are actually managed by divoom using its online system, so they might need to be updated from time to time.\n\n")
            f.write('"""\n\n')
            f.write("from bidict import frozenbidict\n")

            f.write('\n"""\n')
            f.write("http://docin.divoom-gz.com/web/#/5/31\n")
            f.write('"""\n')
            f.write("CHANNEL_DICT: frozenbidict[str, int] = frozenbidict({\n")
            for key, value in sorted(channel_dict.items()):
                f.write(f"    {repr(key)}: {repr(value)},\n")
            f.write("})\n")

            f.write('\n"""\n')
            f.write("http://docin.divoom-gz.com/web/#/5/27\n")
            f.write("http://docin.divoom-gz.com/web/#/5/28\n")
            f.write('"""\n')
            f.write("CHANNEL_INDEX_FACES_DICT: frozenbidict[str, int] = frozenbidict({\n")
            for key, value in sorted(channel_index_faces_dict.items()):
                f.write(f"    {repr(key)}: {repr(value)},\n")
            f.write("})\n")

            f.write('\n"""\n')
            f.write("http://docin.divoom-gz.com/web/#/5/32\n")
            f.write('"""\n')
            f.write("CHANNEL_INDEX_CUSTOM_DICT: frozenbidict[str, int] = frozenbidict({\n")
            for key, value in sorted(channel_index_custom_dict.items()):
                f.write(f"    {repr(key)}: {repr(value)},\n")
            f.write("})\n")

            f.write('\n"""\n')
            f.write("http://docin.divoom-gz.com/web/#/5/33\n")
            f.write('"""\n')
            f.write("CHANNEL_INDEX_VISUALIZER_DICT: frozenbidict[str, int] = frozenbidict({\n")
            for key, value in sorted(channel_index_visualizer_dict.items()):
                f.write(f"    {repr(key)}: {repr(value)},\n")
            f.write("})\n")

            f.write('\n"""\n')
            f.write("http://docin.divoom-gz.com/web/#/5/34\n")
            f.write('"""\n')
            f.write("CHANNEL_INDEX_CLOUD_DICT: frozenbidict[str, int] = frozenbidict({\n")
            for key, value in sorted(channel_index_cloud_dict.items()):
                f.write(f"    {repr(key)}: {repr(value)},\n")
            f.write("})\n")


asyncio.run(generate())
