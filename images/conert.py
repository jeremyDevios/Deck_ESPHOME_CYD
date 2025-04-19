from PIL import Image

def convert_image_to_rgb565(image_path, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    rgb565_data = []

    for pixel in img.getdata():
        r, g, b = pixel
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)  # Conversion à RGB565
        rgb565_data.append(f'0x{rgb565:04X},')  # Formatage en hexadécimal

    with open(output_path, 'w') as f:
        f.write("const uint16_t Room_data[] = {\n")
        f.write('\n'.join(rgb565_data))
        f.write("\n};")

# Utilisation
convert_image_to_rgb565('output.bmp', 'output.c')
