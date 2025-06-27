from PIL import Image

# Function to encode the message into an image
def encode_image(input_image_path, output_image_path, secret_message):
    image = Image.open(input_image_path)
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message + "#####")  # '#####' is end marker
    data = list(image.getdata())

    if len(binary_message) > len(data) * 3:
        raise ValueError("Message is too long to encode in the image.")

    encoded_pixels = []
    binary_index = 0

    for pixel in data:
        r, g, b = pixel[:3]
        if binary_index < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_index])
            binary_index += 1
        encoded_pixels.append((r, g, b) + pixel[3:] if len(pixel) == 4 else (r, g, b))

    image.putdata(encoded_pixels)
    image.save(output_image_path)
    print(f"Message encoded and saved to {output_image_path}")

# Function to decode the message from an image
def decode_image(encoded_image_path):
    image = Image.open(encoded_image_path)
    data = list(image.getdata())

    binary_message = ''
    for pixel in data:
        for color in pixel[:3]:
            binary_message += str(color & 1)

    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''
    for byte in chars:
        char = chr(int(byte, 2))
        message += char
        if message.endswith("#####"):
            break

    return message[:-5]  # Remove end marker

# CLI usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Encode: python steganography.py encode input.png \"secret message\" output.png")
        print("  Decode: python steganography.py decode encoded.png")
    elif sys.argv[1] == "encode":
        _, _, input_image, message, output_image = sys.argv
        encode_image(input_image, output_image, message)
    elif sys.argv[1] == "decode":
        _, _, encoded_image = sys.argv
        decoded = decode_image(encoded_image)
        print("Decoded message:", decoded)
