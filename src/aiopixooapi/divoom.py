from .base import BasePixoo


class Divoom(BasePixoo):
    """Subclass for handling online Divoom API calls."""

    def __init__(self, timeout: int = 10):
        """Initialize the online Divoom API.

        Args:
            timeout: Request timeout in seconds (default: 10).
        """
        base_url = "https://app.divoom-gz.com/Channel"
        super().__init__(base_url, timeout)

    async def get_dial_type(self):
        """Fetch the list of dial types from the Divoom API."""
        return await self._make_request("GetDialType")

    async def get_dial_list(self, dial_type: str, page: int):
        """Fetch the list of dials for a specific type and page.

        Args:
            dial_type: The type of dial (e.g., "Social", "Game").
            page: The page number to fetch (30 items per page).

        Returns:
            Response dictionary containing ReturnCode, TotalNum, and DialList.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
            PixooConnectionError: If the request fails.
        """
        data = {"DialType": dial_type, "Page": page}
        return await self._make_request("GetDialList", data)
