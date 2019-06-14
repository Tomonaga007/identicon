import sys
import hashlib
from PIL import Image


def get_identicon(string):

    hash_string = get_hash_string(string)
    color = get_color(hash_string)
    image = create_image((5, 5), color, hash=hash_string)
    image = image.resize((400, 400))
    image.show()


def get_hash_string(string):
    hash_string = hashlib.md5(str.encode(string.lower()))
    return hash_string.hexdigest()


def get_color(hash):
    return int(hash[0:6][:2], 16), int(hash[0:6][2:4], 16), int(hash[0:6][4:6], 16)


def create_image(image_size, color, hash):

    image = Image.new(mode="RGB", size=image_size, color="white")
    ind = 0
    for x in range(5):
        for y in range(5):
            if int(hash[ind], 16) % 2 == 0:
                image.putpixel((x, y), color)
            ind += 1

    return image


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_identicon(sys.argv[1])
    else:
        get_identicon("test")
