"""Provides functionality specific to the Pixoo64 device."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import PixooCommandError
from .base import BasePixoo
from .pixoo64_dicts import CHANNEL_DICT, CHANNEL_INDEX_CLOUD_DICT, CHANNEL_INDEX_FACES_DICT, CHANNEL_INDEX_CUSTOM_DICT, CHANNEL_INDEX_VISUALIZER_DICT

MAX_CUSTOM_PAGE_INDEX = 2  # Maximum allowed custom page index
MAX_BRIGHTNESS = 100
MAX_RGB_VALUE = 100
MAX_MINUTE = 59
MAX_SECOND = 59
MAX_SCORE = 999
NET_FILE_TYPE = 2
MAX_PIC_NUM = 59
MAX_TEXT_ID = 19
MIN_TEXT_WIDTH = 17
MAX_TEXT_WIDTH = 63
MAX_TEXT_LENGTH = 512
MAX_FONT = 7
MAX_ITEM_TEXT_ID = 39


class ScreenMode(Enum):
    OFF = 0
    ON = 1

class MirrorMode(Enum):
    NORMAL = 0
    MIRRORED = 1

class HourMode(Enum):
    H12 = 0
    H24 = 1

class TemperatureMode(Enum):
    CELSIUS = 0
    FAHRENHEIT = 1

class RotationMode(Enum):
    NORMAL = 0
    RIGHT = 1
    UPSIDE_DOWN = 2
    LEFT = 3

class GalleryMode(Enum):
    OFF = 0
    ON = 1

class GalleryShowTimeMode(Enum):
    OFF = 0
    ON = 1

@dataclass
class Pixoo64Data:
    screen_mode: ScreenMode = ScreenMode.ON
    brightness: int = 0
    channel: CHANNEL_DICT = None
    faces_id: CHANNEL_INDEX_FACES_DICT = None
    mirror_mode: MirrorMode = MirrorMode.NORMAL
    hour_mode: HourMode = HourMode.H24
    temperature_mode: TemperatureMode = TemperatureMode.CELSIUS
    rotation_mode: RotationMode = RotationMode.NORMAL
    gallery_show_time_mode: GalleryShowTimeMode = GalleryShowTimeMode.OFF
    clock_time: int = -1
    gallery_time: int = -1
    single_gallery_time: int = -1
    utc_timestamp: int = 0
    local_time_string: str = None
    # READ-ONLY
    power_on_channel: CHANNEL_DICT = None
    gallery_mode: GalleryMode = GalleryMode.OFF
    weather_string: str = None
    weather_current_temperature: float = 0.0
    weather_min_temperature: float = 0.0
    weather_max_temperature: float = 0.0
    weather_pressure: int = 0
    weather_humidity: int = 0
    weather_visibility: int = 0
    weather_wind_speed: float = 0.0

# NOTE: we can set this but not read it back !!!!
@dataclass
class Pixoo64ConfigData:
    weather_longitude: str = ""
    weather_latitude: str = ""
    time_zone: str = ""
    white_balance: tuple[int, int, int] = (0, 0, 0)


class Pixoo64(BasePixoo):
    """Subclass for handling Pixoo64 device-specific API calls."""

    def __init__(self, host: str, port: int = 80, timeout: int = 10) -> None:
        """Initialize the Pixoo64 device API.

        Args:
            host: IP address of the Pixoo64 device.
            port: Port number (default: 80).
            timeout: Request timeout in seconds (default: 10).

        """
        base_url = f"http://{host}:{port}"
        super().__init__(base_url, timeout)
        self._data = Pixoo64Data()

    async def update_data(self) -> Pixoo64Data:
        """Update the Pixoo64 device data."""
        await self.get_channel()
        await self.get_common_settings()
        await self.get_clock_info()
        await self.get_device_time()
        await self.get_weather_info()
        return self._data

    async def _make_command_request(self, command: str, data: dict | None = None) -> dict:
        """Make a request to the Pixoo64 device with a command.

        Args:
            command: The command to send to the device.
            data: Optional payload for the command.

        Returns:
            Response dictionary.

        Raises:
            PixooCommandError: If the command fails or returns an error.

        """
        if data is None:
            data = {}
        data["Command"] = command
        return await self._make_request("post", data)

    async def _reboot(self) -> dict:
        """Reboot the Pixoo64 device.
        Reference:
            https://docin.divoom-gz.com/web/#/5/26
        """
        return await self._make_command_request("Device/SysReboot")

    async def get_channel(self) -> dict:
        """Get the channel the device is on.

        Returns:
            Response dictionary containing SelectIndex.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/35
        """
        response = await self._make_command_request("Channel/GetIndex")
        self._data.channel = CHANNEL_DICT.get(response["SelectIndex"])
        return response

    async def get_common_settings(self) -> dict:
        """Get settings from the Pixoo64 device.

        Returns:
            Response dictionary containing all common settings:
            * screen switch (light switch)
            * brightness
            * current clock id
            * power on channel id
            * time 24 flag
            * temperature mode
            * gyrate angle
            * mirror flag
            * rotation flag
            * gallery show time flag
            * clock time
            * gallery time
            * single gallery time

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/37
        """
        response = await self._make_command_request("Channel/GetAllConf")

        self._data.screen_mode = ScreenMode(response["LightSwitch"])
        self._data.faces_id = CHANNEL_INDEX_FACES_DICT.get(response["CurClockId"])
        self._data.brightness = int(response["Brightness"])
        self._data.mirror_mode = MirrorMode(response["MirrorFlag"])
        self._data.hour_mode = HourMode(response["Time24Flag"])
        self._data.temperature_mode = TemperatureMode(response["TemperatureMode"])
        self._data.rotation_mode = RotationMode(response["GyrateAngle"])
        self._data.gallery_mode = GalleryMode(response["RotationFlag"])
        self._data.gallery_show_time_mode = GalleryShowTimeMode(response["GalleryShowTimeFlag"])
        self._data.power_on_channel = CHANNEL_DICT.get(response["PowerOnChannelId"])
        self._data.clock_time = int(response["ClockTime"])
        self._data.gallery_time = int(response["GalleryTime"])
        self._data.single_gallery_time = int(response["SingleGalleryTime"])
        return response

    async def get_clock_info(self) -> dict:
        """Get the current working face ID and brightness.

        Returns:
            Response dictionary containing ClockId and Brightness.
            * ClockId
            * Brightness

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/30
        """
        response = await self._make_command_request("Channel/GetClockInfo")
        self._data.clock_id = CHANNEL_INDEX_FACES_DICT.get(response["ClockId"])
        self._data.brightness = response["Brightness"]
        return response

    async def get_device_time(self) -> dict:
        """Get the device system time.

        Returns:
            Response dictionary containing error_code, UTCTime, and LocalTime.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/42
        """
        response = await self._make_command_request("Device/GetDeviceTime")
        self._data.utc_timestamp = response["UTCTime"]
        self._data.local_time_string = response["LocalTime"]
        return response

    async def get_weather_info(self) -> dict:
        """Get the weather information displayed on the device.

        Returns:
            Response dictionary containing weather details such as Weather, CurTemp, MinTemp, MaxTemp, etc.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        response = await self._make_command_request("Device/GetWeatherInfo")
        self._data.weather_string = response["Weather"]
        self._data.weather_current_temperature = float(response["CurTemp"])
        self._data.weather_min_temperature = float(response["MinTemp"])
        self._data.weather_max_temperature = float(response["MaxTemp"])
        self._data.weather_pressure = int(response["Pressure"])
        self._data.weather_humidity = int(response["Humidity"])
        self._data.weather_visibility = int(response["Visibility"])
        self._data.weather_wind_speed = float(response["WindSpeed"])
        return response

    async def set_screen_mode(self, screen_mode: ScreenMode) -> dict:
        """Switch the screen on or off.

        Args:
            ON, OFF

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/41
        """
        return await self._make_command_request("Channel/OnOffScreen", {"OnOff": screen_mode.value})

    async def set_brightness(self, brightness: int) -> dict:
        """Set the brightness of the device.

        Args:
            brightness: The brightness level to set (0~100).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the brightness is out of range.
            PixooCommandError: If the API returns an error or invalid response.
        Reference:
            https://docin.divoom-gz.com/web/#/5/36
        """
        if brightness < 0 or brightness > MAX_BRIGHTNESS:
            msg = f"Invalid brightness value: {brightness}. Must be between 0 and {MAX_BRIGHTNESS}."
            raise ValueError(msg)
        return await self._make_command_request("Channel/SetBrightness", {"Brightness": brightness})

    async def set_channel(self, select_index: CHANNEL_DICT) -> dict:
        """Set the device to the selected channel.

        Args:
            select_index: The channel to select (as a ChannelSelectIndex enum).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/31

        """
        return await self._make_command_request("Channel/SetIndex", {"SelectIndex": select_index.value})

    async def set_face_index(self, face_index: CHANNEL_INDEX_FACES_DICT) -> dict:
        """Set the clock face by selecting the clock ID.

        Args:
            face_index: The ID of the clock face to select.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/29

        """
        return await self._make_command_request("Channel/SetClockSelectId", {"ClockId": face_index.value})

    async def set_custom_page_index(self, custom_page_index: CHANNEL_INDEX_CUSTOM_DICT) -> dict:
        """Set the device to a specific custom page index.

        Args:
            custom_page_index: The custom page index to select (0~2).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/32
        """
        return await self._make_command_request("Channel/SetCustomPageIndex", {"CustomPageIndex": custom_page_index.value})

    async def set_visualizer_index(self, visualizer_index: CHANNEL_INDEX_VISUALIZER_DICT) -> dict:
        """Set the device to a specific visualizer position.

        Args:
            visualizer_index: The visualizer position index (starting from 0).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/33
        """
        return await self._make_command_request("Channel/SetEqPosition", {"EqPosition": visualizer_index.value})

    async def set_cloud_channel_index(self, cloud_channel_index: CHANNEL_INDEX_CLOUD_DICT) -> dict:
        """Set the device to a specific cloud channel.

        Args:
            cloud_channel_index: The cloud channel to select (as a CloudChannelIndex enum).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/34
        """
        return await self._make_command_request("Channel/CloudIndex", {"Index": cloud_channel_index.value})

    async def set_mirror_mode(self, mirror_mode: MirrorMode) -> dict:
        """Set the screen mirror mode.

        Args:
            mirror_mode: NORMAL, MIRRORED

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/45
        """
        return await self._make_command_request("Device/SetMirrorMode", {"Mode": mirror_mode.value})

    async def set_hour_mode(self, hour_mode: HourMode) -> dict:
        """Set the screen hour mode to 24-hour or 12-hour.

        Args:
            hour_mode: H24, H12

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/38
        """
        return await self._make_command_request("Device/SetTime24Flag", {"Mode": hour_mode.value})

    async def set_temperature_mode(self, temperature_mode: TemperatureMode) -> dict:
        """Set the temperature mode to Celsius or Fahrenheit.

        Args:
            CELSIUS, FAHRENHEIT.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/43

        """
        return await self._make_command_request("Device/SetDisTempMode", {"Mode": temperature_mode.value})

    async def set_rotation_mode(self, rotation_mode: RotationMode) -> dict:
        """Set the screen rotation angle.

        Args:
            rotation_mode: The rotation mode (NORMAL, LEFT, RIGHT, UPSIDE_DOWN).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        Reference:
            https://docin.divoom-gz.com/web/#/5/44
        """
        return await self._make_command_request("Device/SetScreenRotationAngle", {"Mode": rotation_mode.value})



    async def set_high_light_mode(self, mode: int) -> dict:
        """Set the screen high light mode.

        Args:
            mode: 0 to close, 1 to open.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the mode is not 0 or 1.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if mode not in (0, 1):
            msg = "Mode must be 0 (close) or 1 (open)."
            raise ValueError(msg)
        return await self._make_command_request("Device/SetHighLightMode", {"Mode": mode})

    async def set_weather_area(self, longitude: str, latitude: str) -> dict:
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
            msg = "Longitude and Latitude must be provided."
            raise ValueError(msg)
        return await self._make_command_request("Sys/LogAndLat", {"Longitude": longitude, "Latitude": latitude})

    async def set_time_zone(self, time_zone_value: str) -> dict:
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
            msg = "TimeZoneValue must be provided."
            raise ValueError(msg)
        return await self._make_command_request("Sys/TimeZone", {"TimeZoneValue": time_zone_value})

    async def set_system_time(self, utc: int) -> dict:
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
            msg = "UTC time must be a positive integer."
            raise ValueError(msg)
        return await self._make_command_request("Device/SetUTC", {"Utc": utc})

    async def set_white_balance(self, r_value: int, g_value: int, b_value: int) -> dict:
        """Set the screen white balance.

        Args:
            r_value: Red value (0~100).
            g_value: Green value (0~100).
            b_value: Blue value (0~100).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If any of the RGB values are out of range.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not (0 <= r_value <= MAX_RGB_VALUE):
            msg = f"RValue must be between 0 and {MAX_RGB_VALUE}. Got: {r_value}"
            raise ValueError(msg)
        if not (0 <= g_value <= MAX_RGB_VALUE):
            msg = f"GValue must be between 0 and {MAX_RGB_VALUE}. Got: {g_value}"
            raise ValueError(msg)
        if not (0 <= b_value <= MAX_RGB_VALUE):
            msg = f"BValue must be between 0 and {MAX_RGB_VALUE}. Got: {b_value}"
            raise ValueError(msg)
        return await self._make_command_request(
            "Device/SetWhiteBalance",
            {"RValue": r_value, "GValue": g_value, "BValue": b_value},
        )

    async def set_countdown_timer(self, minute: int, second: int, status: int) -> dict:
        """Control the countdown tool.

        Args:
            minute: The countdown's minute value.
            second: The countdown's second value.
            status: 1 to start the countdown, 0 to stop it.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If minute or second is out of range, or if status is not 0 or 1.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not (0 <= minute <= MAX_MINUTE):
            msg = f"Minute must be between 0 and {MAX_MINUTE}. Got: {minute}"
            raise ValueError(msg)
        if not (0 <= second <= MAX_SECOND):
            msg = f"Second must be between 0 and {MAX_SECOND}. Got: {second}"
            raise ValueError(msg)
        if status not in (0, 1):
            msg = "Status must be 0 (stop) or 1 (start)."
            raise ValueError(msg)
        return await self._make_command_request(
            "Tools/SetTimer",
            {"Minute": minute, "Second": second, "Status": status},
        )

    async def set_stopwatch(self, status: int) -> dict:
        """Control the stopwatch tool.

        Args:
            status: 2 to reset, 1 to start, 0 to stop.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If status is not 0, 1, or 2.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if status not in (0, 1, 2):
            msg = "Status must be 0 (stop), 1 (start), or 2 (reset)."
            raise ValueError(msg)
        return await self._make_command_request("Tools/SetStopWatch", {"Status": status})

    async def set_scoreboard(self, blue_score: int, red_score: int) -> dict:
        """Control the scoreboard tool.

        Args:
            blue_score: The blue team's score (0~999).
            red_score: The red team's score (0~999).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If blue_score or red_score is out of range.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not (0 <= blue_score <= MAX_SCORE):
            msg = f"BlueScore must be between 0 and {MAX_SCORE}. Got: {blue_score}"
            raise ValueError(msg)
        if not (0 <= red_score <= MAX_SCORE):
            msg = f"RedScore must be between 0 and {MAX_SCORE}. Got: {red_score}"
            raise ValueError(msg)
        return await self._make_command_request(
            "Tools/SetScoreBoard",
            {"BlueScore": blue_score, "RedScore": red_score},
        )

    async def set_noise_tool(self, noise_status: int) -> dict:
        """Control the noise tool.

        Args:
            noise_status: 1 to start the noise tool, 0 to stop it.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If noise_status is not 0 or 1.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if noise_status not in (0, 1):
            msg = "NoiseStatus must be 0 (stop) or 1 (start)."
            raise ValueError(msg)
        return await self._make_command_request("Tools/SetNoiseStatus", {"NoiseStatus": noise_status})

    async def play_gif(self, file_type: int, file_name: str) -> dict:
        """Play a GIF file on the device.

        Args:
            file_type: The type of file (2 for net file; other values are invalid).
            file_name: The URL of the net file to play.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If file_type is not 2 or file_name is not provided.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if file_type != NET_FILE_TYPE:
            msg = f"FileType must be {NET_FILE_TYPE} (net file)."
            raise ValueError(msg)
        if not file_name:
            msg = "FileName must be provided."
            raise ValueError(msg)
        return await self._make_command_request(
            "Device/PlayTFGif",
            {"FileType": file_type, "FileName": file_name},
        )

    async def play_divoom_gif(self, file_id: str) -> dict:
        """Play a Divoom GIF file on the device.

        Args:
            file_id: The FileId of the GIF to play.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If file_id is not provided.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not file_id:
            msg = "FileId must be provided."
            raise ValueError(msg)

        return await self._make_command_request(
            "Draw/SendRemote",
            {"FileId": file_id},
        )

    async def get_http_gif_id(self) -> dict:
        """Get the PicId for the next HTTP GIF animation.

        Returns:
            Response dictionary containing error_code and PicId.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        response = await self._make_command_request("Draw/GetHttpGifId")
        if response.get("error_code", 0) != 0:
            msg = f"Failed to get HTTP GIF ID: {response}"
            raise PixooCommandError(msg)
        return response

    async def reset_http_gif_id(self) -> dict:
        """Reset the HTTP GIF PicId to start from 1.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        response = await self._make_command_request("Draw/ResetHttpGifId")
        if response.get("error_code", 0) != 0:
            msg = f"Failed to reset HTTP GIF ID: {response}"
            raise PixooCommandError(msg)
        return response

    async def send_animation_frame(  # noqa: PLR0913
            self, pic_num: int, pic_width: int, pic_offset: int, pic_id: int, pic_speed: int, pic_data: str,
    ) -> dict:
        """Send a single frame of an animation to the device.

        Args:
            pic_num: Total number of frames in the animation (must be < 60).
            pic_width: Width of the frame in pixels (16, 32, or 64).
            pic_offset: Offset of the current frame (0 to PicNum-1).
            pic_id: Unique ID for the animation (must auto-increment).
            pic_speed: Speed of the animation in milliseconds.
            pic_data: Base64-encoded RGB data for the frame.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If any of the parameters are invalid.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not (1 <= pic_num < MAX_PIC_NUM):
            msg = f"PicNum must be between 1 and {MAX_PIC_NUM}. Got: {pic_num}"
            raise ValueError(msg)
        if pic_width not in (16, 32, 64):
            msg = f"PicWidth must be one of 16, 32, or 64. Got: {pic_width}"
            raise ValueError(msg)
        if not (0 <= pic_offset < pic_num):
            msg = f"PicOffset must be between 0 and PicNum-1. Got: {pic_offset}"
            raise ValueError(msg)
        if pic_id < 1:
            msg = f"PicID must be greater than or equal to 1. Got: {pic_id}"
            raise ValueError(msg)
        if pic_speed < 0:
            msg = f"PicSpeed must be a positive integer. Got: {pic_speed}"
            raise ValueError(msg)
        if not pic_data:
            msg = "PicData must be provided."
            raise ValueError(msg)

        return await self._make_command_request(
            "Draw/SendHttpGif",
            {
                "PicNum": pic_num,
                "PicWidth": pic_width,
                "PicOffset": pic_offset,
                "PicID": pic_id,
                "PicSpeed": pic_speed,
                "PicData": pic_data,
            },
        )

    async def send_text(  # noqa: PLR0913
            self,
            text_id: int,
            x: int,
            y: int,
            direction: int,
            font: int,
            text_width: int,
            text_string: str,
            speed: int,
            color: str,
            align: int = 1,
    ) -> dict:
        """Send text to the device.

        Args:
            text_id: Unique ID for the text (must be < 20).
            x: Start x position.
            y: Start y position.
            direction: 0 for scroll left, 1 for scroll right.
            font: Font type (0~7).
            text_width: Text width (16 < width < 64).
            text_string: UTF-8 string (length < 512).
            speed: Scroll speed in ms per step.
            color: Font color in hex format (e.g., "#FFFF00").
            align: Horizontal alignment (1: left, 2: middle, 3: right).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If any parameter is invalid.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not (0 <= text_id <= MAX_TEXT_ID):
            msg = f"TextId must be between 0 and {MAX_TEXT_ID}. Got: {text_id}"
            raise ValueError(msg)
        if not (MIN_TEXT_WIDTH < text_width < MAX_TEXT_WIDTH):
            msg = f"TextWidth must be between {MIN_TEXT_WIDTH} and {MAX_TEXT_WIDTH}. Got: {text_width}"
            raise ValueError(msg)
        if len(text_string) >= MAX_TEXT_LENGTH:
            msg = f"TextString length must be less than {MAX_TEXT_LENGTH}. Got: {len(text_string)}"
            raise ValueError(msg)
        if direction not in (0, 1):
            msg = f"Direction must be 0 (scroll left) or 1 (scroll right). Got: {direction}"
            raise ValueError(msg)
        if not (0 <= font <= MAX_FONT):
            msg = f"Font must be between 0 and {MAX_FONT}. Got: {font}"
            raise ValueError(msg)
        if align not in (1, 2, 3):
            msg = f"Align must be 1 (left), 2 (middle), or 3 (right). Got: {align}"
            raise ValueError(msg)

        return await self._make_command_request(
            "Draw/SendHttpText",
            {
                "TextId": text_id,
                "x": x,
                "y": y,
                "dir": direction,
                "font": font,
                "TextWidth": text_width,
                "TextString": text_string,
                "speed": speed,
                "color": color,
                "align": align,
            },
        )

    async def clear_text(self) -> dict:
        """Clear all text areas on the device.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        return await self._make_command_request("Draw/ClearHttpText")

    async def send_display_list(self, item_list: list) -> dict:
        """Send a display list to the device.

        Args:
            item_list: A list of dictionaries, each representing a display item with the following keys:
                - TextId: Unique ID for the text (must be < 40).
                - type: Display type (refer to the display type table).
                - x: Start x position.
                - y: Start y position.
                - dir: 0 for scroll left, 1 for scroll right.
                - font: Font ID (from GetTimeDialFontList, Type=0 for scrolling).
                - TextWidth: Text area width.
                - Textheight: Text area height.
                - TextString: Optional UTF-8 string (length < 512).
                - speed: Scroll speed in ms per step.
                - color: Font color in hex format (e.g., "#FFFF00").
                - update_time: Optional URL request interval in seconds.
                - align: Horizontal alignment (1: left, 2: middle, 3: right).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If any item in the list has invalid parameters.
            PixooCommandError: If the API returns an error or invalid response.

        """
        for item in item_list:
            if not (0 <= item.get("TextId", -1) <= MAX_ITEM_TEXT_ID):
                msg = f"TextId must be between 0 and {MAX_ITEM_TEXT_ID}. Got: {item.get('TextId')}"
                raise ValueError(msg)
            if len(item.get("TextString", "")) >= MAX_TEXT_LENGTH:
                msg = f"TextString length must be less than {MAX_TEXT_LENGTH}. Got: {len(item.get('TextString', ''))}"
                raise ValueError(msg)

        return await self._make_command_request("Draw/SendHttpItemList", {"ItemList": item_list})

    async def play_buzzer(self, active_time_in_cycle: int, off_time_in_cycle: int, play_total_time: int) -> dict:
        """Play the buzzer on the device.

        Args:
            active_time_in_cycle: Working time of buzzer in one cycle in milliseconds.
            off_time_in_cycle: Idle time of buzzer in one cycle in milliseconds.
            play_total_time: Total working time of buzzer in milliseconds.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If any parameter is invalid.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if active_time_in_cycle < 0:
            msg = f"ActiveTimeInCycle must be a non-negative integer. Got: {active_time_in_cycle}"
            raise ValueError(msg)
        if off_time_in_cycle < 0:
            msg = f"OffTimeInCycle must be a non-negative integer. Got: {off_time_in_cycle}"
            raise ValueError(msg)
        if play_total_time <= 0:
            msg = f"PlayTotalTime must be a positive integer. Got: {play_total_time}"
            raise ValueError(msg)

        return await self._make_command_request(
            "Device/PlayBuzzer",
            {
                "ActiveTimeInCycle": active_time_in_cycle,
                "OffTimeInCycle": off_time_in_cycle,
                "PlayTotalTime": play_total_time,
            },
        )

    async def run_command_list(self, command_list: list) -> dict:
        """Run a list of commands on the device.

        Args:
            command_list: A list of dictionaries, each representing a command with its parameters.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the command_list is empty or not a list.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not isinstance(command_list, list) or not command_list:
            msg = "CommandList must be a non-empty list."
            raise ValueError(msg)

        return await self._make_command_request("Draw/CommandList", {"CommandList": command_list})

    async def use_http_command_source(self, command_url: str) -> dict:
        """Run commands from a URL on the device.

        Args:
            command_url: The URL containing the command array information.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the command_url is not provided.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if not command_url:
            msg = "CommandUrl must be provided."
            raise ValueError(msg)

        return await self._make_command_request(
            "Draw/UseHTTPCommandSource",
            {"CommandUrl": command_url},
        )
