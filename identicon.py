import hashlib
from PIL import Image
import argparse
import string
import random
import os


def get_identicon(string, color=None, image_size=400, num_blocks=7, symetrical=True):

    hash_string = get_hash_string(string)
    color = color if color else get_color(hash_string)
    image = create_image(num_blocks, color,
                         hash=hash_string, symmetrical=symetrical)
    image = image.resize((image_size, image_size))
    return image


def save(identicon, filename):
    dir_path, file = os.path.split(filename)
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError("Wrong file extension. Allowed are png, jpg, jpeg")
    elif os.path.isfile(filename):
        raise FileExistsError("File with that name already exists")
    elif dir_path:
        raise ValueError("Provide only filename without directory")
    else:
        identicon.save(filename)


def get_hash_string(string):
    '''Returns md5 hashed string in hex (32 characters)'''
    hash_string = hashlib.md5(str.encode(string.lower()))
    return hash_string.hexdigest()


def get_color(hash):
    '''Returns  '''
    return int(hash[0:2], 16), int(hash[2:4], 16), int(hash[4:6], 16)


def create_image(num_blocks, color, hash, symmetrical=True):
    '''Create identicon of size num_blocks*num_blocks based on hash'''
    image = Image.new(mode="RGB", size=(num_blocks, num_blocks), color="white")
    ind = 0
    width = (num_blocks // 2 + num_blocks % 2) if symmetrical else num_blocks
    height = num_blocks
    for col in range(width):
        for row in range(height):
            if ind >= len(hash):  # in index out of range reset it
                ind = 0
            if int(hash[ind], 16) % 2 == 0:
                image.putpixel((col, row), color)
                if symmetrical:
                    image.putpixel((-(1 + col), row), color)
            ind += 1

    return image


def generate_random_string(lenght=10):
    characters = string.ascii_letters + string.digits
    return "".join([random.choice(characters) for i in range(lenght)])


def main():
    parser = argparse.ArgumentParser(description='Say hello')
    parser.add_argument('--string', default=None,
                        help='string on witch identicon will be based')
    parser.add_argument('--size', default=400, type=int,
                        help='output image size in pixels, provide only one value, output image will be square')
    parser.add_argument('--blocks', default=5, type=int,
                        help='number of identicon blocks in a row')
    parser.add_argument('--color', default=None, type=int, nargs="+",
                        help='specify color as 1,3 or 4 integer values')
    parser.add_argument('--not_symetrical', default=True, action='store_false',
                        help='use for not symetrical identicon')
    parser.add_argument('--save', default=None,
                        help='filename for save')
    args = parser.parse_args()

    input_string = args.string if args.string else generate_random_string()
    size = args.size
    blocks = args.blocks
    symetrical = args.not_symetrical
    color = args.color and (args.color[0] if len(
        args.color) == 1 else tuple(args.color))

    try:
        image = get_identicon(string=input_string, image_size=size, color=color,
                              num_blocks=blocks, symetrical=symetrical)
        if args.save:
            save(image, args.save)
        else:
            image.show()
    except TypeError as e:
        print("color must be single integer or tuple of 3 or 4 integers")
    except ValueError as e:
        print(e)
    except FileExistsError as e:
        print(e)


if __name__ == '__main__':
    main()
