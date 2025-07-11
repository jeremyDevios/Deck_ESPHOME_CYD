from PIL import Image
import numpy as np

def rgb565_to_rgb888(rgb565):
    """Convert a single BGR565 value to RGB888."""
    b = (rgb565 >> 11) & 0x1F  # Blue is in the high bits
    g = (rgb565 >> 5) & 0x3F   # Green in the middle bits
    r = rgb565 & 0x1F          # Red in the low bits
    
    # Scale to 8-bit values
    r = (r << 3) | (r >> 2)
    g = (g << 2) | (g >> 4)
    b = (b << 3) | (b >> 2)
    return (r, g, b)

def render_rgb565_to_image(header_file, width, height, output_file):
    """Render an RGB565 header file to an image."""
    # Read the header file
    with open(header_file, "r") as f:
        lines = f.readlines()

    # Extract the RGB565 data
    data = []
    for line in lines:
        if "0x" in line:  # Look for hex values
            data.extend([int(x, 16) for x in line.split(",") if "0x" in x])

    # Convert RGB565 to RGB888
    rgb888_data = [rgb565_to_rgb888(pixel) for pixel in data]

    # Create an image
    img = Image.new("RGB", (width, height))
    img.putdata(rgb888_data)

    # Save the image
    img.save(output_file)
    print(f"Image saved to {output_file}")

# Example usage
render_rgb565_to_image("Room_rgb565.h", 320, 240, "Room_output.png")