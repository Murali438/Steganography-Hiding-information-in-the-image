from PIL import Image

def encode_text_in_image(input_image_path, output_image_path, secret_text):
    img = Image.open(input_image_path)
    binary_secret = ''.join(format(ord(i), '08b') for i in secret_text + '#####')  # '#####' is end marker
    pixels = list(img.getdata())

    new_pixels = []
    binary_index = 0

    for pixel in pixels:
        new_pixel = list(pixel)
        for n in range(3):  # RGB
            if binary_index < len(binary_secret):
                new_pixel[n] = new_pixel[n] & ~1 | int(binary_secret[binary_index])
                binary_index += 1
        new_pixels.append(tuple(new_pixel))

    img.putdata(new_pixels)
    img.save(output_image_path)
    print("Encoding complete. Saved as:", output_image_path)
