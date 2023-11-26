from PIL import Image
from stegano import lsb

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = "".join(format(ord(char), "08b") for char in message)

    pixels = list(img.getdata())

    for i in range(len(binary_message)):
        pixels[i] = (
            pixels[i][0],
            pixels[i][1],
            pixels[i][2] & ~1 | int(binary_message[i]),
        )

    new_img = Image.new("RGB", img.size)
    new_img.putdata(pixels)

    encoded_image = lsb.hide(image_path, message)
    encoded_image.save(output_path)

def decode_message(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_message = "".join(str(pixel[2] & 1) for pixel in pixels)

    message = "".join(
        chr(int(binary_message[i : i + 8], 2)) for i in range(0, len(binary_message), 8)
    )
    decoded_message = lsb.reveal(image_path)

    return decoded_message


# Example usage
original_message = "Hello, this is a hidden message!"
encode_message(
    "Lenna_(test_image).png", original_message, "image_with_hidden_message.png"
)
print("Original Message:", original_message)

hidden_message = decode_message("image_with_hidden_message.png")
print("Hidden Message:", hidden_message)