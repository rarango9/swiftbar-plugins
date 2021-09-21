#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir, walk
from os.path import isfile, join
from pprint import PrettyPrinter

images_path = '../images/'
plugins_path = '../plugins/'
show = PrettyPrinter(indent=4).pprint

contents = ''
header = """
# SwiftBar Plugins

## Usage

## Plugins
"""
footer = """
## Color Reference

- GRAY: `#3c3c3c`
- RED: `#d40000`
- YELLOW: `#ffcc00`
- GREEN: `#009800`

## Attributions

Icons from [www.flaticon.com](www.flaticon.com) made by:

- Freepik
"""


def add_content(text):
    global contents
    contents += F"{text}\n\n"


def main():
    add_content(header.strip())

    for plugin in sorted([p for p in listdir(plugins_path) if len(p.split('.')) == 2]):
        dependencies = ''
        description = ''
        image = ''

        print(F"Processing : {plugin}")
        with open(join(plugins_path, plugin), 'r') as file:
            for line in file.read().splitlines():
                if line.startswith('# <bitbar.desc>'):
                    description = (line
                                   .replace('# <bitbar.desc>', '')
                                   .replace('</bitbar.desc>', ''))
                elif line.startswith('# <bitbar.dependencies>'):
                    dependencies = (line
                                    .replace('# <bitbar.dependencies>', '')
                                    .replace('</bitbar.dependencies>', ''))

        image_filename = F"{plugin.split('.')[0]}.png"
        if isfile(join(images_path, image_filename)):
            image = join(images_path, image_filename)

        if any([dependencies, description, image]):
            add_content(F"#### `{plugin}`")

            if description:
                add_content(description)
            if dependencies:
                add_content(F"**Requires** : {dependencies}")
            if image:
                add_content(F"![{plugin}]({image})")

    add_content(footer.strip())

    with open('../README.md', 'w+') as readme:
        readme.write(contents)


if __name__ == '__main__':
    main()
