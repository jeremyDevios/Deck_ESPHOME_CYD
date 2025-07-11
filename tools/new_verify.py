from PIL import Image
import numpy as np

def rgb565_to_rgb888(rgb565):
    """Convert a single RGB565/BGR565 value to RGB888, matching the display config."""
    # For BGR565 (swap_rb=True)
    r = (rgb565 & 0x1F)  
    g = (rgb565 >> 5) & 0x3F
    b = (rgb565 >> 11) & 0x1F
    
    # Scale to 8-bit values
    r = (r << 3) | (r >> 2)
    g = (g << 2) | (g >> 4)
    b = (b << 3) | (b >> 2)
    return (r, g, b)

def read_rgb565_values(file_path):
    """Extract RGB565 values from header file."""
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find all hex values in the format 0xXXXX
    import re
    values = re.findall(r"0x([0-9A-Fa-f]{4})", content)
    return [int(val, 16) for val in values]

def create_image_from_rgb565(rgb565_values, width, height, output_file):
    """Create an image from RGB565 values."""
    rgb888_pixels = [rgb565_to_rgb888(val) for val in rgb565_values]
    
    # Create new image
    img = Image.new("RGB", (width, height))
    img.putdata(rgb888_pixels)
    img.save(output_file)
    print(f"Image saved to {output_file}")

# Example usage
values = read_rgb565_values("Room_rgb565.h")
create_image_from_rgb565(values, 320, 240, "new_output.png")

# Also try alternative RGB/BGR ordering for verification
def rgb565_to_bgr888(rgb565):
    """Convert RGB565 to BGR888 (swap red and blue)."""
    r5 = (rgb565 >> 11) & 0x1F
    g6 = (rgb565 >> 5) & 0x3F
    b5 = rgb565 & 0x1F
    
    # Scale up to 8 bits per channel
    r8 = (r5 * 255 + 15) // 31
    g8 = (g6 * 255 + 31) // 63
    b8 = (b5 * 255 + 15) // 31
    
    return (b8, g8, r8)  # Swap red and blue

bgr888_pixels = [rgb565_to_bgr888(val) for val in values]
img_bgr = Image.new("RGB", (320, 240))
img_bgr.putdata(bgr888_pixels)
img_bgr.save("bgr_output.png")
print("Alternative color ordering saved to bgr_output.png")