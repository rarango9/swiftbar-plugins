#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ UPDATE READMES
# Updates the readmes for each plugin and the root of the project.
# =============================================================================

from os import chdir, listdir
from os.path import isdir, exists
from pathlib import Path
from pprint import PrettyPrinter
from re import findall

from tabulate import tabulate

show = PrettyPrinter(indent=4).pprint


class Readme():

    def __init__(self):
        self.contents = ''

    def add(self, text):
        self.contents = F"{self.contents}{text}\n\n"

    def clear(self):
        self.contents = ''


def color_link(hex_color):
    return (F"![{hex_color}](https://via.placeholder.com/15/{hex_color[1:]}"
            F"/000000?text=+) `{hex_color}`")


def update_plugin_readmes(plugins):
    readme = Readme()

    for plugin in plugins:
        script = ''
        for f in listdir(F"./{plugin}/"):
            if plugin in f:
                script = f

        # Make sure a script was found.
        if not script:
            print(F"Missing script in ./{plugin}/")
            continue

        # Parse the metadata from the script into dicts.
        metadata = {}
        optional_metadata = {}
        with open(F"./{plugin}/{script}", 'r') as file:
            data = file.read()

            matches = findall(r'# <bitbar.(\w+|\w+.*\w+)>(.*)</.*', data)
            for match in matches:
                metadata[match[0]] = match[1]

            matches = findall(r'# <swiftbar.(\w+|\w+.*\w+)>(.*)</.*', data)
            for match in matches:
                optional_metadata[match[0]] = match[1]

        # Make sure metadata was found.
        if not metadata and not optional_metadata:
            print(F"Missing metadata in ./{plugin}/{script}")
            continue

        # Add header.
        if exists(F"./{plugin}/icon.svg"):
            readme.add(F"# <img src='./icon.svg' width='36' "
                       F"style='vertical-align: text-bottom'> "
                       F"{metadata['title']}")
        else:
            readme.add(F"# {metadata['title']}")

        # Add metadata.
        readme.add('## Metadata')
        readme.add(tabulate(
            [[k, v] for k, v in metadata.items()],
            ['key', 'value'],
            tablefmt="github")
        )

        # Add optional metadata.
        readme.add('## Optional Metadata')
        readme.add(tabulate(
            [[k, v] for k, v in optional_metadata.items()],
            ['key', 'value'],
            tablefmt="github")
        )

        # Add screenshot.
        readme.add('## Screenshot')
        if exists(F"./{plugin}/image.png"):
            readme.add(F"![screenshot](./image.png)")
        else:
            readme.add('None')

        # Update the README file.
        with open(F"./{plugin}/README.md", 'w+') as file:
            file.write(readme.contents)
            readme.clear()
            print(F"Updated ./{plugin}/README.md")


def update_root_readme(plugins):
    readme = Readme()

    # Header section.
    readme.add('# SwiftBar Plugins')

    # Usage section.
    readme.add('## Usage')
    readme.add('Copy or create a symlink of the plugin script to your '
               'swiftbar plugins directory, usually `~/.swiftbar`.')
    readme.add('Any environment variables available in the scripts should '
               'be added to your `~/.bash_profile`.')

    # Plugins section.
    readme.add('## Plugins')
    readme.add('\n'.join([F"-   [{p}](./{p}/)" for p in plugins]))

    # Color Reference section.
    colors = [["Gray",   "#737373", "#4d4d4d"],
              ["Green",  "#58f158", "#0fb10f"],
              ["Red",    "#ff3434", "#ff4949"],
              ["White",  "#ffffff", "#ffffff"],
              ["Yellow", "#ffd735", "#ffdc4e"]]
    readme.add('## Color Reference')
    readme.add(tabulate(
        [[c[0], color_link(c[1]), color_link(c[2])] for c in colors],
        headers=['Name', 'Text', 'Icon'],
        tablefmt='github'
    ))

    # Attributions section.
    readme.add('## Attributes')

    # Write the contents to the readme.
    with open('./README.md', 'w+') as file:
        file.write(readme.contents)
        print('Updated ./README.md')


def main():
    # Make sure we are running from the projects root.
    chdir(str(Path(__file__).parent.resolve()))

    # Get the names of all plugins from the diriectories in the project.
    plugins = sorted([d for d in listdir('./') if isdir(d) and d != '.git'])

    # Update all the READMEs.
    update_root_readme(plugins)
    update_plugin_readmes(plugins)


if __name__ == '__main__':
    main()
