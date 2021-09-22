#!/usr/bin/env python3

from argparse import ArgumentParser
from os.path import isfile, splitext
from subprocess import PIPE, Popen, run
from sys import exit


def convert_image(image_path, rgb):
    print('Converting image to a datauri')

    proc = Popen([
        'convert',
        '-units', 'PixelsPerInch',
        '-background', 'none',
        '-fill', rgb,
        '-opaque', 'black',
        '-resize', '38x38',
        image_path,
        '-density', '144',
        'INLINE:PNG:-'
    ], stdout=PIPE)

    datauri = proc.communicate()[0].decode().split(',')[1]

    if proc.returncode != 0:
        print('Something went wrong during the conversion')
        exit(1)
    else:
        return datauri


def copy_to_clipboard(datauri):
    print('Copied datauri string to clipboard')
    run('pbcopy', universal_newlines=True, input=datauri)


def hex_to_rgb(hex_color):
    if hex_color is None:
        rgb_str = 'rgb(255,255,255)'
    else:
        hex_color = hex_color.lstrip('#')
        rgb_codes = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb_str = F"rgb({rgb_codes[0]},{rgb_codes[1]},{rgb_codes[2]})"

    print(F"Applying {rgb_str} color")
    return rgb_str


def parse_args():
    p = ArgumentParser()
    p.add_argument('-c', metavar='HEX_COLOR', required=False)
    p.add_argument('-i', metavar='IMAGE_PATH', required=True)
    p.add_argument('-l', metavar='MAX_LINE_LENGTH', type=int, required=False)
    p.add_argument('--copy', action='store_true', required=False)

    return p.parse_args()


def split_at_length(text, length):
    index = 0
    split_datauri = ''

    for char in text:
        split_datauri += char
        index += 1
        if index == length:
            split_datauri += '\n'
            index = 0

    return split_datauri


def validate_image(image_path):
    if not isfile(image_path):
        print('Image does not exist')
        exit(1)

    if splitext(image_path)[1].lower() != '.svg':
        print(F"Image must be a SVG")
        exit(1)

    print('Basic validation of image passed')


def main():
    print('❱❱❱ Make DataURI ❰❰❰')
    args = parse_args()

    validate_image(args.i)
    rgb = hex_to_rgb(args.c)
    datauri = convert_image(args.i, rgb)
    if args.l is not None:
        datauri = split_at_length(datauri, args.l)
    if args.copy:
        copy_to_clipboard(datauri)


if __name__ == '__main__':
    main()
