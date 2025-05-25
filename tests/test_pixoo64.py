import pytest
from aioresponses import aioresponses

from aiopixooapi.pixoo64 import Pixoo64, CloudChannelIndex, ChannelSelectIndex


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
                    "error_code": 0,
                    "Brightness": 100,
                    "RotationFlag": 1,
                    "ClockTime": 60,
                    "GalleryTime": 60,
                    "SingleGalleyTime": 5,
                    "PowerOnChannelId": 1,
                    "GalleryShowTimeFlag": 1,
                    "CurClockId": 1,
                    "Time24Flag": 1,
                    "TemperatureMode": 1,
                    "GyrateAngle": 1,
                    "MirrorFlag": 1,
                    "LightSwitch": 1,
                },
            )
            response = await pixoo64.get_all_settings()
            assert response["error_code"] == 0
            assert response["Brightness"] == 100
            assert response["RotationFlag"] == 1
            assert response["ClockTime"] == 60
            assert response["GalleryTime"] == 60
            assert response["SingleGalleyTime"] == 5
            assert response["PowerOnChannelId"] == 1
            assert response["GalleryShowTimeFlag"] == 1
            assert response["CurClockId"] == 1
            assert response["Time24Flag"] == 1
            assert response["TemperatureMode"] == 1
            assert response["GyrateAngle"] == 1
            assert response["MirrorFlag"] == 1
            assert response["LightSwitch"] == 1


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
            response = await pixoo64.set_channel(ChannelSelectIndex.VISUALIZER)
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


@pytest.mark.asyncio
async def test_set_cloud_channel():
    """Test the set_cloud_channel method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_cloud_channel(CloudChannelIndex.FAVOURITE)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_get_current_channel():
    """Test the get_current_channel method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"SelectIndex": 2},
            )
            response = await pixoo64.get_current_channel()
            assert response["SelectIndex"] == 2


@pytest.mark.asyncio
async def test_set_brightness():
    """Test the set_brightness method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_brightness(75)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_brightness_invalid():
    """Test the set_brightness method with an invalid brightness value."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Invalid brightness value: 150. Must be between 0 and 100."):
            await pixoo64.set_brightness(150)


@pytest.mark.asyncio
async def test_set_weather_area():
    """Test the set_weather_area method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_weather_area("30.29", "20.58")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_weather_area_invalid():
    """Test the set_weather_area method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Longitude and Latitude must be provided."):
            await pixoo64.set_weather_area("", "20.58")
        with pytest.raises(ValueError, match="Longitude and Latitude must be provided."):
            await pixoo64.set_weather_area("30.29", "")


@pytest.mark.asyncio
async def test_set_time_zone():
    """Test the set_time_zone method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_time_zone("GMT-5")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_time_zone_invalid():
    """Test the set_time_zone method with an invalid input."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="TimeZoneValue must be provided."):
            await pixoo64.set_time_zone("")


@pytest.mark.asyncio
async def test_set_system_time():
    """Test the set_system_time method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_system_time(1672416000)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_system_time_invalid():
    """Test the set_system_time method with an invalid UTC time."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="UTC time must be a positive integer."):
            await pixoo64.set_system_time(-1)


@pytest.mark.asyncio
async def test_set_screen_switch():
    """Test the set_screen_switch method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_switch(1)
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_switch(0)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_screen_switch_invalid():
    """Test the set_screen_switch method with an invalid input."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="OnOff must be 0 \\(off\\) or 1 \\(on\\)."):
            await pixoo64.set_screen_switch(2)


@pytest.mark.asyncio
async def test_get_device_time():
    """Test the get_device_time method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={
                    "error_code": 0,
                    "UTCTime": 1647200428,
                    "LocalTime": "2022-03-14 03:40:28",
                },
            )
            response = await pixoo64.get_device_time()
            assert response["error_code"] == 0
            assert response["UTCTime"] == 1647200428
            assert response["LocalTime"] == "2022-03-14 03:40:28"
