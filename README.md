# aiopixooapi
An asynchronous Python library for controlling Divoom Pixoo64 LED display devices.

## Installation

```bash
pip install aiopixooapi
```

## Quick Start

```python
import asyncio
from aiopixooapi import Pixoo

async def main():
    # Connect to your Pixoo64 device
    async with Pixoo("192.168.1.100") as pixoo:  # Replace with your device's IP address
        # Display text
        await pixoo.draw_text("Hello, World!", x=0, y=0, color=(255, 0, 0))

        # Display an image
        await pixoo.draw_image("path/to/image.png")

        # Set brightness
        await pixoo.set_brightness(50)  # 0-100

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

For detailed documentation, please visit our [GitHub repository](https://github.com/KoenDierckx/aiopixooapi).

### Sources used

#### Divoom
* https://divoom.com/apps/help-center#hc-pixoo64developeropen-sourcesdkapiopen-source

That gives us:
* http://doc.divoom-gz.com/web/#/12?page_id=89

Where the contact page:
* http://doc.divoom-gz.com/web/#/12?page_id=143

Send us to
* http://docin.divoom-gz.com/web/#/5/23

OLDER REFERENCES
* http://doc.divoom-gz.com/web/#/12
* http://doc.divoom-gz.com/web/#/7
* http://doc.divoom-gz.com/web/#/5

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the LICENSE file for details. 