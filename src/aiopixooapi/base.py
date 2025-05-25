"""Provides the `BasePixoo` class, which handles common functionality for interacting with the Pixoo API."""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Type
import types

import aiohttp

from .exceptions import PixooConnectionError, PixooCommandError

logger = logging.getLogger(__name__)


class BasePixoo:
    """Base class for handling common Pixoo API functionality."""

    def __init__(self, base_url: str, timeout: int = 10):
        """Initialize the base Pixoo API class.

        Args:
            base_url: Base URL for API requests.
            timeout: Request timeout in seconds (default: 10).

        """
        self.base_url = base_url
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ):
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Create aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={"Content-Type": "application/json"},
                raise_for_status=True,
            )
            logger.debug("Created new aiohttp session")

    async def _make_request(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the API.

        Args:
            endpoint: API endpoint.
            data: Optional request payload.

        Returns:
            Response dictionary.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
            PixooConnectionError: If the request fails.

        """
        if self._session is None:
            await self.connect()

        try:
            async with self._session.post(
                    f"{self.base_url}/{endpoint}",
                    json=data,
                    timeout=self.timeout,
            ) as response:
                text = await response.text()
                try:
                    result = json.loads(text)
                except json.JSONDecodeError as json_err:
                    logger.error(f"Failed to parse JSON from response: {text}")
                    raise PixooCommandError(
                        f"Failed to parse JSON from response: {text}",
                    ) from json_err
                if result.get("error_code", 0) != 0:
                    raise PixooCommandError(f"API returned error: {result}")
                return result
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.error(f"Error making request to {endpoint}: {e}")
            raise PixooConnectionError(f"Failed to connect to API: {e}") from e

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session:
            await self._session.close()
            await asyncio.sleep(0)  # Graceful shutdown
            self._session = None
            logger.debug("Closed aiohttp session")
