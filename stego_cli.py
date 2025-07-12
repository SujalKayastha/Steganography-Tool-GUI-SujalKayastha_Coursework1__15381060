
import argparse
from PIL import Image
import os

EOF_MARKER = '11111110'

def message_to_binary(message):
    return ''.join(format(ord(c), '08b') for c in message) + EOF_MARKER

def binary_to_message(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''
    for byte in chars:
        if byte == EOF_MARKER:
            break
        message += chr(int(byte, 2))
    return message

def encode(image_path, message, output_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    binary = message_to_binary(message)
    pixels = list(img.getdata())
    new_pixels = []
    bit_idx = 0

    for pixel in pixels:
        r, g, b = pixel
        if bit_idx < len(binary):
            r = (r & ~1) | int(binary[bit_idx])
            bit_idx += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)
    print(f"Message encoded and saved to {output_path}")

def decode(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = list(img.getdata())
    binary_data = ''

    for pixel in pixels:
        r, g, b = pixel
        binary_data += str(r & 1)

    message = binary_to_message(binary_data)
    print(f"Decoded message: {message}")
    return message

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI Steganography Tool")
    subparsers = parser.add_subparsers(dest='command')

    encode_parser = subparsers.add_parser('encode')
    encode_parser.add_argument('input', help="Input image path")
    encode_parser.add_argument('output', help="Output image path")
    encode_parser.add_argument('message', help="Message to hide")

    decode_parser = subparsers.add_parser('decode')
    decode_parser.add_argument('input', help="Stego image path")

    args = parser.parse_args()

    if args.command == 'encode':
        encode(args.input, args.message, args.output)
    elif args.command == 'decode':
        decode(args.input)
    else:
        parser.print_help()
