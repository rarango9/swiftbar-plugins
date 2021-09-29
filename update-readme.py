#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import isdir, isfile
from pprint import PrettyPrinter
from re import findall
from sys import argv, exit

from tabulate import tabulate

show = PrettyPrinter(indent=4).pprint
contents = ''


def add_content(text):
    global contents
    contents += F"{text}\n\n"


def main():
    if len(argv) != 2:
        print('A plugin name must be passed to update the README.md')
        exit(1)

    plugin = argv[1]
    plugin_dir = F"./{plugin}"
    plugin_script = F"{plugin_dir}/{plugin}.py"

    # Simple validations for existence.
    if not isdir(plugin_dir):
        print('Plugin directory does not exist')
        exit(1)
    if not isfile(plugin_script):
        print('Plugin script does not exist')
        exit(1)

    # Parse the metadata from the script into dicts.
    metadata = {}
    metadata_optional = {}
    with open(plugin_script, 'r') as file:
        for line in file.read().splitlines():
            if line.startswith('# <bitbar.'):
                match = findall(r'# <bitbar.(\w+|\w+.*\w+)>(.*)</.*', line)[0]
                metadata[match[0]] = match[1]
            elif line.startswith('# <swiftbar.'):
                match = findall(
                    r'# <swiftbar.(\w+|\w+.*\w+)>(.*)</.*', line)[0]
                metadata_optional[match[0]] = match[1]

    # Begin formatting the content for markdown output.
    icon_insert = '<img src="./icon.svg" width="36" style="vertical-align: middle">'
    add_content(F"# {icon_insert} {plugin}")

    add_content(F'## Metadata')
    table_content = []
    for k, v in metadata.items():
        table_content.append([k, v])
    add_content(tabulate(table_content, ['key', 'value'], tablefmt="github"))

    add_content(F'## Optional Metadata')
    table_content = []
    for k, v in metadata_optional.items():
        table_content.append([k, v])
    add_content(tabulate(table_content, ['key', 'value'], tablefmt="github"))

    add_content('## Screenshot')
    add_content('![screenshot](./image.png)')

    # Create or overwrite the specific plugin README.
    with open(F"{plugin_dir}/README.md", 'w+') as readme:
        readme.write(contents)


if __name__ == '__main__':
    main()
