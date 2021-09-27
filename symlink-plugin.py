#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ INFO
# Easy script to create a symlink from the repository plugin scripts to
# the SwiftBar plugins directory with a time interval.
# =============================================================================

from argparse import ArgumentParser
from os import remove, symlink
from os.path import isdir, isfile, islink, join
from pathlib import Path
from subprocess import check_output
from sys import exit


def main():
    # Parse the 2 required arguments.
    p = ArgumentParser()
    p.add_argument('plugin')
    p.add_argument('interval')
    args = p.parse_args()

    # Determine SwiftBar plugin path.
    plugins_path = check_output([
        'defaults', 'read', 'com.ameba.SwiftBar', 'PluginDirectory'
    ]).decode().strip()

    # Validate that we did not get an error message.
    if 'does not exist' in plugins_path:
        print(plugins_path, end='\n\n')
        print('ERROR: Is SwiftBar installed?')
        exit(1)

    # Get the absolute path to this repository's root.
    repo_path = str(Path(__file__).parent.resolve())

    # Validate the SwiftBar plugins directory exists.
    if not isdir(plugins_path):
        print('Swiftbar plugins directory does not exist')
        print(plugins_path)
        exit(1)

    # Validate the plugin name passed has a matching plugin directory.
    if not isdir(args.plugin):
        print(F"Plugin {args.plugin} directory does not exist")
        exit(1)

    # Validate that we have a matching script to symlink to.
    plugin_relative_path = join(args.plugin, args.plugin + '.py')
    if not isfile(plugin_relative_path):
        print(F"Plugin {plugin_relative_path} does not exist")
        exit(1)

    # Generate absolute paths for the source and destination.
    src = join(repo_path, plugin_relative_path)
    dest = join(plugins_path, F"{args.plugin}.{args.interval}.py")

    # Remove a symlink if it already exists.
    if islink(dest):
        print(F"Removing existing symlink {dest}")
        remove(dest)

    # Create the symlink.
    print('Creating symlink to plugin')
    print(F" SRC : {src}",
          F"DEST : {dest}",
          sep='\n')
    symlink(src, dest)


if __name__ == '__main__':
    main()
