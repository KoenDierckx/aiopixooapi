import asyncio

from aiopixooapi.divoom import Divoom
from aiopixooapi.pixoo64 import Pixoo64


async def main():
    async with Divoom() as divoom:
        # Get dial types
        dial_types = await divoom.get_dial_type()
        print(dial_types)

        # Get dial list for a specific type and page
        dial_list = await divoom.get_dial_list("Social", 1)
        print(dial_list)

    async with Pixoo64("10.116.4.238") as pixoo64:
        # Get all settings
        settings = await pixoo64.get_all_settings()
        print(settings)


asyncio.run(main())
