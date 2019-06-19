import hashlib
from PIL import Image, ImageOps
import argparse
import string
import random
import os


def get_identicon(string, color=None, background=(255, 255, 255), image_size=400, num_blocks=5, border=0, symetrical=True):
    """Get identicon based on  provided string

    Parameters
    ----------
    string : string
        String to be hashed
    color : tuple
        Tuple of 3 or 4 integers as a color representation
        Default is None, which implies color based on hashed string
    background : tuple
        Tuple of 3 or 4 integers as a color representation
        Default is white
    image_size : int
        Output image size in pixels. Default is 400
    num_blocks : int
        Number of blocks per row used to create identicon. Default is 5
    border : int
        Integer representing border around image in pixels
    symertical : bool
        Default is True, which implies symmetric along y axis

    Returns
    -------
    image
        Created identicon resized to image_size with optional border
    """
    hash_string = get_hash_string(string)
    color = color if color else get_color(hash_string)
    image = create_image(hash=hash_string, num_blocks=num_blocks,
                         color=color, background=background,
                         symmetrical=symetrical)
    image = image.resize((image_size - 2 * border, image_size - 2 * border))
    image = ImageOps.expand(image, border=border, fill=background)
    return image


def save(identicon, filename):
    '''Save identicon in as filename in current directory
    Allowed filename extensions: png, jpg, jpeg
    '''
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
    '''Returns tuple of 3 integers within range 0-255 '''
    return int(hash[0:2], 16), int(hash[2:4], 16), int(hash[4:6], 16)


def create_image(hash, num_blocks, color, background, symmetrical=True):
    """Create RGB identicon image based on hash string

    Parameters
    ----------
    hash : string
        String of hexadecimal characters
    num_blocks : int
        Number of blocks per row used to create identicon.
    color : tuple
        Tuple of 3 or 4 integers as a color representation
    background : tuple
        Tuple of 3 or 4 integers as a color representation
    symertical : bool
        Default is True, which implies symmetric along y axis

    Returns
    -------
    image
        RGB identicon image
    """
    # create empty white initial image of size num_blocks*num_blocks
    image = Image.new(mode="RGB", size=(
        num_blocks, num_blocks), color=background)
    ind = 0
    # width demends on weather image supposed to be symertical or not
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
    """Returns random string with specified length containing
       letters and digits  """
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
                        help='specify color as 3 or 4 integer values')
    parser.add_argument('--background', default=None, type=int, nargs="+",
                        help='specify background color as 3 or 4 integer values')
    parser.add_argument('--border', default=0, type=int,
                        help='specify border in pixels')
    parser.add_argument('--not_symetrical', default=True, action='store_false',
                        help='use for not symetrical identicon')
    parser.add_argument('--save', default=None,
                        help='filename for save')
    args = parser.parse_args()

    input_string = args.string if args.string else generate_random_string()
    size = args.size
    blocks = args.blocks
    symetrical = args.not_symetrical
    color = args.color and tuple(args.color)
    background = tuple(args.background) if args.background else (255, 255, 255)
    border = args.border

    try:
        image = get_identicon(string=input_string, image_size=size, color=color,
                              background=background, num_blocks=blocks,
                              border=border, symetrical=symetrical)
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
