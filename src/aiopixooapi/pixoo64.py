from enum import Enum

from . import PixooCommandError
from .base import BasePixoo


class ChannelSelectIndex(Enum):
    """Enum for valid channel IDs with meaningful names."""
    FACES = 0          # Faces
    CLOUD_CHANNEL = 1  # Cloud Channel
    VISUALIZER = 2     # Visualizer
    CUSTOM = 3         # Custom
    BLACK_SCREEN = 4   # Black Screen


class CloudChannelIndex(Enum):
    """Enum for valid cloud channel indices with meaningful names."""
    RECOMMEND_GALLERY = 0  # Recommend gallery
    FAVOURITE = 1          # Favourite
    SUBSCRIBE_ARTIST = 2   # Subscribe artist
    ALBUM = 3              # Album


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
        """Get all settings from the Pixoo64 device.

        Returns:
            Response dictionary containing all settings.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        response = await self._make_command_request("Channel/GetAllConf")
        if response.get("error_code", 0) != 0:
            raise PixooCommandError(f"Failed to get all settings: {response}")
        return response

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
            select_index: The channel to select (as a ChannelSelectIndex enum).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        return await self._make_command_request("Channel/SetIndex", {"SelectIndex": select_index.value})

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

    async def set_cloud_channel(self, index: CloudChannelIndex):
        """Set the device to a specific cloud channel.

        Args:
            index: The cloud channel to select (as a CloudChannelIndex enum).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        return await self._make_command_request("Channel/CloudIndex", {"Index": index.value})

    async def get_current_channel(self):
        """Get the current channel the device is on.

        Returns:
            Response dictionary containing SelectIndex.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        response = await self._make_command_request("Channel/GetIndex")
        return response

    async def set_brightness(self, brightness: int):
        """Set the brightness of the device.

        Args:
            brightness: The brightness level to set (0~100).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the brightness is out of range.
            PixooCommandError: If the API returns an error or invalid response.
        """
        if brightness < 0 or brightness > 100:
            raise ValueError(f"Invalid brightness value: {brightness}. Must be between 0 and 100.")
        return await self._make_command_request("Channel/SetBrightness", {"Brightness": brightness})

    async def set_weather_area(self, longitude: str, latitude: str):
        """Set the weather area by specifying longitude and latitude.

        Args:
            longitude: The longitude value as a string.
            latitude: The latitude value as a string.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If longitude or latitude is not provided.
            PixooCommandError: If the API returns an error or invalid response.
        """
        if not longitude or not latitude:
            raise ValueError("Longitude and Latitude must be provided.")
        return await self._make_command_request("Sys/LogAndLat", {"Longitude": longitude, "Latitude": latitude})

    async def set_time_zone(self, time_zone_value: str):
        """Set the time zone of the device.

        Args:
            time_zone_value: The time zone value (e.g., "GMT-5").

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the time_zone_value is not provided.
            PixooCommandError: If the API returns an error or invalid response.
        """
        if not time_zone_value:
            raise ValueError("TimeZoneValue must be provided.")
        return await self._make_command_request("Sys/TimeZone", {"TimeZoneValue": time_zone_value})

    async def set_system_time(self, utc: int):
        """Set the system time of the device.

        Args:
            utc: The UTC time as a Unix timestamp.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the UTC time is not valid.
            PixooCommandError: If the API returns an error or invalid response.
        """
        if utc < 0:
            raise ValueError("UTC time must be a positive integer.")
        return await self._make_command_request("Device/SetUTC", {"Utc": utc})

    async def set_screen_switch(self, on_off: int):
        """Switch the screen on or off.

        Args:
            on_off: 1 to turn the screen on, 0 to turn it off.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If on_off is not 0 or 1.
            PixooCommandError: If the API returns an error or invalid response.
        """
        if on_off not in (0, 1):
            raise ValueError("OnOff must be 0 (off) or 1 (on).")
        return await self._make_command_request("Channel/OnOffScreen", {"OnOff": on_off})

    async def get_device_time(self):
        """Get the device system time.

        Returns:
            Response dictionary containing error_code, UTCTime, and LocalTime.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
        """
        response = await self._make_command_request("Device/GetDeviceTime")
        if response.get("error_code", 0) != 0:
            raise PixooCommandError(f"Failed to get device time: {response}")
        return response
