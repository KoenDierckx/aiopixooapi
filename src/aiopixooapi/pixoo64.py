from .base import BasePixoo


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
