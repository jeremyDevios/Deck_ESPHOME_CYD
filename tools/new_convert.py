from PIL import Image

def convert_to_rgb565(image_path, output_file, swap_rb=True, byte_swap=False):
    # Open the image and convert to RGB
    img = Image.open(image_path).convert("RGB")
    
    # Resize the image to match the display resolution
    img = img.resize((320, 240))
    
    # Create output file
    with open(output_file, 'w') as f:
        # Write header information
        f.write("// RGB565 image data converted from {}\n".format(image_path))
        f.write("// Format: {} swap_rb={} byte_swap={}\n".format(
            "BGR565" if swap_rb else "RGB565", swap_rb, byte_swap))
        f.write("// Resolution: {}x{}\n\n".format(img.width, img.height))
        f.write("const uint16_t image_data[] = {\n")
        
        pixel_values = []
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = img.getpixel((x, y))
                
                # Convert 8-bit RGB to 5-6-5 bit RGB
                r5 = (r & 0xF8) >> 3
                g6 = (g & 0xFC) >> 2
                b5 = (b & 0xF8) >> 3
                
                if swap_rb:
                    # BGR565 format (swap red and blue)
                    rgb565 = (b5 << 11) | (g6 << 5) | r5
                else:
                    # RGB565 format
                    rgb565 = (r5 << 11) | (g6 << 5) | b5
                
                if byte_swap:
                    # Swap the bytes (low byte first, then high byte)
                    rgb565 = ((rgb565 & 0xFF) << 8) | ((rgb565 >> 8) & 0xFF)
                
                pixel_values.append("0x{:04X}".format(rgb565))
        
        # Write pixel values in rows of 16 values
        for i in range(0, len(pixel_values), 16):
            f.write("    " + ", ".join(pixel_values[i:i+16]))
            if i + 16 < len(pixel_values):
                f.write(",")
            f.write("\n")
        
        f.write("};\n")

# Generate all four combinations to test which one works
convert_to_rgb565("Room.jpg", "Room_rgb565_BGR_noswap.h", swap_rb=True, byte_swap=False)  # BGR order, no byte swap
convert_to_rgb565("Room.jpg", "Room_rgb565_BGR_swap.h", swap_rb=True, byte_swap=True)     # BGR order, with byte swap
convert_to_rgb565("Room.jpg", "Room_rgb565_RGB_noswap.h", swap_rb=False, byte_swap=False) # RGB order, no byte swap
convert_to_rgb565("Room.jpg", "Room_rgb565_RGB_swap.h", swap_rb=False, byte_swap=True)    # RGB order, with byte swap