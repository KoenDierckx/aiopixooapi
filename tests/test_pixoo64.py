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
                payload={"ReturnCode": 0, "ReturnMessage": "Success"},
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
                    "Settings": {"Brightness": 50, "Volume": 20},
                },
            )
            response = await pixoo64.get_all_settings()
            assert response["ReturnCode"] == 0
            assert "Settings" in response
            assert response["Settings"]["Brightness"] == 50
            assert response["Settings"]["Volume"] == 20


@pytest.mark.asyncio
async def test_set_clock_select_id():
    """Test the set_clock_select_id method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_clock_select_id(42)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_get_clock_info():
    """Test the get_clock_info method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"ClockId": 12, "Brightness": 100},
            )
            response = await pixoo64.get_clock_info()
            assert response["ClockId"] == 12
            assert response["Brightness"] == 100


@pytest.mark.asyncio
async def test_set_channel():
    """Test the set_channel method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_channel("Visualizer")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_custom_page_index():
    """Test the set_custom_page_index method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_custom_page_index(1)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_custom_page_index_invalid():
    """Test the set_custom_page_index method with an invalid index."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Invalid custom page index: 3. Must be between 0 and 2."):
            await pixoo64.set_custom_page_index(3)


@pytest.mark.asyncio
async def test_set_visualizer_position():
    """Test the set_visualizer_position method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_visualizer_position(3)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_visualizer_position_invalid():
    """Test the set_visualizer_position method with an invalid position."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Invalid visualizer position: -1. Must be 0 or greater."):
            await pixoo64.set_visualizer_position(-1)
