# Home Assistant Deck CYD Component

This project is inspired by the CYD Screen (2 USB Version) support component for [HA_Deck](https://github.com/strange-v/ha_deck) by [strange_v](https://github.com/strange-v). It has been updated to be installed on ESP32-2432S024R or ESP32-2432S028.

To launch the application on `ESP32-2432S024R`, use the command:

```bash
esphome run examples/ha_deck_cyd.yaml
```

For `ESP32-2432S028`, use the command:

```bash
esphome run examples/ha_deck_cyd-28.yaml
```

The code has been completely rewritten to display a view and provide control of connected objects on my Home Assistant server (e.g., light control, temperature display, etc.).

### Hardware reference:
[ESP32-2432S028 aka CYD (Cheap Yellow Display) or ESP32-2432S024R ](https://ali.ski/vNTYds)

![](/images/ha-deck-cyd.jpg)


  To convert a JPG image into RGB565 format, you can use an image conversion tool or library. For example, you can use Python with the `Pillow` library to convert the image. Here's how you can do it:

    1. Install Pillow:
        ```bash
        pip install pillow
        ```

    2. Use the following Python script to convert the image:
        ```python
        from PIL import Image
        import numpy as np

        def convert_to_rgb565(image_path, output_path):
             img = Image.open(image_path).convert('RGB')
             arr = np.array(img)

             def rgb888_to_rgb565(r, g, b):
                  return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

             rgb565_array = np.array([[rgb888_to_rgb565(r, g, b) for r, g, b in row] for row in arr], dtype=np.uint16)

             with open(output_path, 'w') as f:
                  f.write('#include <stdint.h>\n\n')
                  f.write(f'const uint16_t Room_width = {img.width};\n')
                  f.write(f'const uint16_t Room_height = {img.height};\n')
                  f.write('const uint16_t Room_data[] = {\n')
                  for row in rgb565_array:
                        f.write(', '.join(f'0x{pixel:04X}' for pixel in row) + ',\n')
                  f.write('};\n')

        # Replace 'Room.jpg' with your image file and 'Room.h' with the output header file
        convert_to_rgb565('Room.jpg', 'Room.h')
        ```

    3. Run the script to generate a header file (`Room.h`) containing the RGB565 data.

    4. Include the generated `Room.h` file in your project and use it in your code:
        ```cpp
        #include "Room.h"

        lcd.pushImage(0, 0, Room_width, Room_height, Room_data);
        ```

    This will display the converted image correctly on your ESP32.