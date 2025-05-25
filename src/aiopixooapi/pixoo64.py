"""Provides functionality specific to the Pixoo64 device."""

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

    async def set_temperature_mode(self, mode: int):
        """Set the temperature mode to Celsius or Fahrenheit.

        Args:
            mode: 0 for Celsius, 1 for Fahrenheit.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the mode is not 0 or 1.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if mode not in (0, 1):
            raise ValueError("Mode must be 0 (Celsius) or 1 (Fahrenheit).")
        return await self._make_command_request("Device/SetDisTempMode", {"Mode": mode})

    async def set_screen_rotation_angle(self, mode: int):
        """Set the screen rotation angle.

        Args:
            mode: The rotation angle mode (0: normal, 1: 90, 2: 180, 3: 270).

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the mode is not one of the valid options.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if mode not in (0, 1, 2, 3):
            raise ValueError("Mode must be 0 (normal), 1 (90), 2 (180), or 3 (270).")
        return await self._make_command_request("Device/SetScreenRotationAngle", {"Mode": mode})

    async def set_mirror_mode(self, mode: int):
        """Set the screen mirror mode.

        Args:
            mode: 0 to disable, 1 to enable.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the mode is not 0 or 1.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if mode not in (0, 1):
            raise ValueError("Mode must be 0 (disable) or 1 (enable).")
        return await self._make_command_request("Device/SetMirrorMode", {"Mode": mode})

    async def set_hour_mode(self, mode: int):
        """Set the screen hour mode to 24-hour or 12-hour.

        Args:
            mode: 1 for 24-hour mode, 0 for 12-hour mode.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            ValueError: If the mode is not 0 or 1.
            PixooCommandError: If the API returns an error or invalid response.

        """
        if mode not in (0, 1):
            raise ValueError("Mode must be 0 (12-hour) or 1 (24-hour).")
        return await self._make_command_request("Device/SetTime24Flag", {"Mode": mode})

    async def set_high_light_mode(self, mode: int):
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
            raise ValueError("Mode must be 0 (close) or 1 (open).")
        return await self._make_command_request("Device/SetHighLightMode", {"Mode": mode})

    async def set_white_balance(self, r_value: int, g_value: int, b_value: int):
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
        if not (0 <= r_value <= 100):
            raise ValueError(f"RValue must be between 0 and 100. Got: {r_value}")
        if not (0 <= g_value <= 100):
            raise ValueError(f"GValue must be between 0 and 100. Got: {g_value}")
        if not (0 <= b_value <= 100):
            raise ValueError(f"BValue must be between 0 and 100. Got: {b_value}")
        return await self._make_command_request(
            "Device/SetWhiteBalance",
            {"RValue": r_value, "GValue": g_value, "BValue": b_value},
        )

    async def get_weather_info(self):
        """Get the weather information displayed on the device.

        Returns:
            Response dictionary containing weather details such as Weather, CurTemp, MinTemp, MaxTemp, etc.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        response = await self._make_command_request("Device/GetWeatherInfo")
        if response.get("error_code", 0) != 0:
            raise PixooCommandError(f"Failed to get weather info: {response}")
        return response

    async def set_countdown_timer(self, minute: int, second: int, status: int):
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
        if not (0 <= minute <= 59):
            raise ValueError(f"Minute must be between 0 and 59. Got: {minute}")
        if not (0 <= second <= 59):
            raise ValueError(f"Second must be between 0 and 59. Got: {second}")
        if status not in (0, 1):
            raise ValueError("Status must be 0 (stop) or 1 (start).")
        return await self._make_command_request(
            "Tools/SetTimer",
            {"Minute": minute, "Second": second, "Status": status},
        )

    async def set_stopwatch(self, status: int):
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
            raise ValueError("Status must be 0 (stop), 1 (start), or 2 (reset).")
        return await self._make_command_request("Tools/SetStopWatch", {"Status": status})

    async def set_scoreboard(self, blue_score: int, red_score: int):
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
        if not (0 <= blue_score <= 999):
            raise ValueError(f"BlueScore must be between 0 and 999. Got: {blue_score}")
        if not (0 <= red_score <= 999):
            raise ValueError(f"RedScore must be between 0 and 999. Got: {red_score}")
        return await self._make_command_request(
            "Tools/SetScoreBoard",
            {"BlueScore": blue_score, "RedScore": red_score},
        )

    async def set_noise_tool(self, noise_status: int):
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
            raise ValueError("NoiseStatus must be 0 (stop) or 1 (start).")
        return await self._make_command_request("Tools/SetNoiseStatus", {"NoiseStatus": noise_status})

    async def play_gif(self, file_type: int, file_name: str):
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
        if file_type != 2:
            raise ValueError("FileType must be 2 (net file).")
        if not file_name:
            raise ValueError("FileName must be provided.")
        return await self._make_command_request(
            "Device/PlayTFGif",
            {"FileType": file_type, "FileName": file_name},
        )

    async def play_divoom_gif(self, file_id: str):
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
            raise ValueError("FileId must be provided.")

        return await self._make_command_request(
            "Draw/SendRemote",
            {"FileId": file_id},
        )

    async def get_http_gif_id(self):
        """Get the PicId for the next HTTP GIF animation.

        Returns:
            Response dictionary containing error_code and PicId.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        response = await self._make_command_request("Draw/GetHttpGifId")
        if response.get("error_code", 0) != 0:
            raise PixooCommandError(f"Failed to get HTTP GIF ID: {response}")
        return response

    async def reset_http_gif_id(self):
        """Reset the HTTP GIF PicId to start from 1.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        response = await self._make_command_request("Draw/ResetHttpGifId")
        if response.get("error_code", 0) != 0:
            raise PixooCommandError(f"Failed to reset HTTP GIF ID: {response}")
        return response

    async def send_animation_frame(
        self, pic_num: int, pic_width: int, pic_offset: int, pic_id: int, pic_speed: int, pic_data: str,
    ):
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
        if not (1 <= pic_num < 60):
            raise ValueError(f"PicNum must be between 1 and 59. Got: {pic_num}")
        if pic_width not in (16, 32, 64):
            raise ValueError(f"PicWidth must be one of 16, 32, or 64. Got: {pic_width}")
        if not (0 <= pic_offset < pic_num):
            raise ValueError(f"PicOffset must be between 0 and PicNum-1. Got: {pic_offset}")
        if pic_id < 1:
            raise ValueError(f"PicID must be greater than or equal to 1. Got: {pic_id}")
        if pic_speed < 0:
            raise ValueError(f"PicSpeed must be a positive integer. Got: {pic_speed}")
        if not pic_data:
            raise ValueError("PicData must be provided.")

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

    async def send_text(
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
    ):
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
        if not (0 <= text_id < 20):
            raise ValueError(f"TextId must be between 0 and 19. Got: {text_id}")
        if not (16 < text_width < 64):
            raise ValueError(f"TextWidth must be between 17 and 63. Got: {text_width}")
        if len(text_string) >= 512:
            raise ValueError(f"TextString length must be less than 512. Got: {len(text_string)}")
        if direction not in (0, 1):
            raise ValueError(f"Direction must be 0 (scroll left) or 1 (scroll right). Got: {direction}")
        if not (0 <= font <= 7):
            raise ValueError(f"Font must be between 0 and 7. Got: {font}")
        if align not in (1, 2, 3):
            raise ValueError(f"Align must be 1 (left), 2 (middle), or 3 (right). Got: {align}")

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

    async def clear_text(self):
        """Clear all text areas on the device.

        Returns:
            Response dictionary containing the error_code.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.

        """
        return await self._make_command_request("Draw/ClearHttpText")

    async def send_display_list(self, item_list: list):
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
            if not (0 <= item.get("TextId", -1) < 40):
                raise ValueError(f"TextId must be between 0 and 39. Got: {item.get('TextId')}")
            if len(item.get("TextString", "")) >= 512:
                raise ValueError(f"TextString length must be less than 512. Got: {len(item.get('TextString', ''))}")

        return await self._make_command_request("Draw/SendHttpItemList", {"ItemList": item_list})

    async def play_buzzer(self, active_time_in_cycle: int, off_time_in_cycle: int, play_total_time: int):
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
            raise ValueError(f"ActiveTimeInCycle must be a non-negative integer. Got: {active_time_in_cycle}")
        if off_time_in_cycle < 0:
            raise ValueError(f"OffTimeInCycle must be a non-negative integer. Got: {off_time_in_cycle}")
        if play_total_time <= 0:
            raise ValueError(f"PlayTotalTime must be a positive integer. Got: {play_total_time}")

        return await self._make_command_request(
            "Device/PlayBuzzer",
            {
                "ActiveTimeInCycle": active_time_in_cycle,
                "OffTimeInCycle": off_time_in_cycle,
                "PlayTotalTime": play_total_time,
            },
        )

    async def run_command_list(self, command_list: list):
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
            raise ValueError("CommandList must be a non-empty list.")

        return await self._make_command_request("Draw/CommandList", {"CommandList": command_list})

    async def use_http_command_source(self, command_url: str):
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
            raise ValueError("CommandUrl must be provided.")

        return await self._make_command_request(
            "Draw/UseHTTPCommandSource",
            {"CommandUrl": command_url},
        )
