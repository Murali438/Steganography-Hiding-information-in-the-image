def decode_text_from_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_data = ''

    for pixel in pixels:
        for n in range(3): 
            binary_data += str(pixel[n] & 1)

    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''
    for c in chars:
        character = chr(int(c, 2))
        if message[-5:] == '#####':
            break
        message += character
    return message[:-5] 
