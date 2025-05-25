from typing import Literal
from .base import BasePixoo

# Define a type for valid channel IDs with meaningful names
ChannelSelectIndex = Literal[
    "Faces",          # 0: Faces
    "CloudChannel",   # 1: Cloud Channel
    "Visualizer",     # 2: Visualizer
    "Custom",         # 3: Custom
    "BlackScreen"     # 4: Black Screen
]

class Pixoo64(BasePixoo):
    """Subclass for handling Pixoo64 device-specific API calls."""

    def __init__(self, host: str, port: int = 80, timeout: int = 10):
        """Initialize the Pixoo64 device API.

        Args:
            host: IP address of the Pixoo64 device.
            port: Port number (default: 80).
            timeout: Request timeout in seconds (default: 10).
        """
        base_url = f"http://{host}:{port}"
        super().__init__(base_url, timeout)

    async def _make_command_request(self, command: str, data: dict = None):
        """Make a request to the Pixoo64 device with a command.

        Args:
            command: The command to send to the device.
            data: Additional data to include in the request.

        Returns:
            Response dictionary.
        """
        if data is None:
            data = {}
        data["Command"] = command
        return await self._make_request("post", data)

    async def sys_reboot(self):
        """Reboot the Pixoo64 device."""
        return await self._make_command_request("Device/SysReboot")

    async def get_all_settings(self):
        """Get all settings from the Pixoo64 device."""
        return await self._make_command_request("Channel/GetAllConf")

    async def set_clock_select_id(self, clock_id: int):
        """Set the clock face by selecting the clock ID.

        Args:
            clock_id: The ID of the clock face to select.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        return await self._make_command_request("Channel/SetClockSelectId", {"ClockId": clock_id})

    async def get_clock_info(self):
        """Get the current working face ID and brightness.

        Returns:
            Response dictionary containing ClockId and Brightness.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        return await self._make_command_request("Channel/GetClockInfo")

    async def set_channel(self, select_index: ChannelSelectIndex):
        """Set the device to the selected channel.

        Args:
            select_index: The channel name to select.
                "Faces": Faces
                "CloudChannel": Cloud Channel
                "Visualizer": Visualizer
                "Custom": Custom
                "BlackScreen": Black Screen

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        # Map meaningful names to their corresponding numeric values
        channel_map = {
            "Faces": 0,
            "CloudChannel": 1,
            "Visualizer": 2,
            "Custom": 3,
            "BlackScreen": 4
        }
        if select_index not in channel_map:
            raise ValueError(f"Invalid channel name: {select_index}")
        return await self._make_command_request("Channel/SetIndex", {"SelectIndex": channel_map[select_index]})

    async def set_custom_page_index(self, custom_page_index: int):
        """Set the device to a specific custom page index.

        Args:
            custom_page_index: The custom page index to select (0~2).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the custom_page_index is out of range.
            PixooCommandError: If the API returns an error or invalid response.
        """
        if custom_page_index < 0 or custom_page_index > 2:
            raise ValueError(f"Invalid custom page index: {custom_page_index}. Must be between 0 and 2.")
        return await self._make_command_request("Channel/SetCustomPageIndex", {"CustomPageIndex": custom_page_index})

    async def set_visualizer_position(self, eq_position: int):
        """Set the device to a specific visualizer position.

        Args:
            eq_position: The visualizer position index (starting from 0).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the eq_position is negative.
            PixooCommandError: If the API returns an error or invalid response.
        """
        if eq_position < 0:
            raise ValueError(f"Invalid visualizer position: {eq_position}. Must be 0 or greater.")
        return await self._make_command_request("Channel/SetEqPosition", {"EqPosition": eq_position})
