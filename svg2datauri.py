#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#
# ❱❱ SVG2DATAURI
# Easy way to convert a SVG into a PNG DataURI an even apply color.
# =============================================================================

from argparse import ArgumentParser
from os.path import isfile, splitext
from subprocess import PIPE, Popen, run
from sys import exit


def parse_args():
    p = ArgumentParser()

    # Required args.
    p.add_argument('image_path', metavar='IMAGE_PATH')

    # Optional args.
    p.add_argument('-hc',
                   help='Hex color code to apply',
                   default='ffffff',
                   required=False)
    p.add_argument('-mll',
                   help='Max line length for output',
                   default=0,
                   type=int,
                   required=False)
    p.add_argument('--copy',
                   help='Copy datauri output to clipboard',
                   action='store_true',
                   required=False)

    return p.parse_args()


def main():
    print('❱❱❱ SVG2DATAURI ❰❰❰')
    args = parse_args()

    # Validate the image.
    if not isfile(args.image_path):
        print('Image does not exist')
        exit(1)
    if splitext(args.image_path)[1].lower() != '.svg':
        print(F"Image must be a SVG")
        exit(1)

    # Generate the RGB color code from Hex.
    rgb_codes = tuple(int(args.hc.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    rgb_str = F"rgb{str(rgb_codes).replace(' ', '')}"
    print(F"Using color => {rgb_str}")

    # Convert the SVG to de-prefixed datauri.
    print(F"Converting {args.image_path} to datauri")
    proc = Popen(['convert', '-units', 'PixelsPerInch', '-background', 'none',
                  '-fuzz', "75%", '-fill', rgb_str, '-opaque', 'black',
                  '-resize', '38x38', args.image_path, '-density', '144',
                  'INLINE:PNG:-'], stdout=PIPE)
    result = proc.communicate()[0]
    if proc.returncode != 0:
        print('Something went wrong during the conversion')
        exit(1)
    else:
        datauri = result.decode().split(',')[1]

    # Split the output at a specific line length if -mll was passed.
    if args.mll is not None:
        datauri = '\n'.join(
            [datauri[i:i + args.mll] for i in range(0, len(datauri), args.mll)]
        )

    # Copy or output the datauri string.
    if args.copy:
        run('pbcopy', universal_newlines=True, input=datauri)
        print('Copied datauri to clipboard')
    else:
        print('\n',  '=' * 80, datauri, '=' * 80, sep='\n')


if __name__ == '__main__':
    main()
