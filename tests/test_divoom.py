import pytest
from aioresponses import aioresponses

from aiopixooapi.divoom import Divoom


@pytest.mark.asyncio
async def test_get_dial_type():
    """Test the get_dial_type method."""
    async with Divoom() as divoom:
        with aioresponses() as mock:
            mock.post(
                "https://app.divoom-gz.com/Channel/GetDialType",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "",
                    "DialTypeList": ["Social", "normal", "financial"],
                },
            )
            response = await divoom.get_dial_type()
            assert response["ReturnCode"] == 0
            assert "DialTypeList" in response
            assert response["DialTypeList"] == ["Social", "normal", "financial"]


@pytest.mark.asyncio
async def test_get_dial_list():
    """Test the get_dial_list method."""
    async with Divoom() as divoom:
        with aioresponses() as mock:
            mock.post(
                "https://app.divoom-gz.com/Channel/GetDialList",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "",
                    "TotalNum": 100,
                    "DialList": [
                        {"ClockId": 10, "Name": "Classic Digital Clock"},
                        {"ClockId": 12, "Name": "US Stock - 2"},
                    ],
                },
            )
            response = await divoom.get_dial_list("Social", 1)
            assert response["ReturnCode"] == 0
            assert response["TotalNum"] == 100
            assert "DialList" in response
            assert len(response["DialList"]) == 2
            assert response["DialList"][0]["ClockId"] == 10
            assert response["DialList"][0]["Name"] == "Classic Digital Clock"
