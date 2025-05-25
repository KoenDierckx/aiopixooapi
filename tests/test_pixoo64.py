import pytest
from aioresponses import aioresponses

from aiopixooapi.pixoo64 import Pixoo64


@pytest.mark.asyncio
async def test_sys_reboot():
    """Test the sys_reboot method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "Success"
                },
            )
            response = await pixoo64.sys_reboot()
            assert response["ReturnCode"] == 0
            assert response["ReturnMessage"] == "Success"


@pytest.mark.asyncio
async def test_get_all_settings():
    """Test the get_all_settings method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={
                    "ReturnCode": 0,
                    "Settings": {
                        "Brightness": 50,
                        "Volume": 20
                    },
                },
            )

            response = await pixoo64.get_all_settings()
            assert response["ReturnCode"] == 0
            assert "Settings" in response
            assert response["Settings"]["Brightness"] == 50
            assert response["Settings"]["Volume"] == 20
