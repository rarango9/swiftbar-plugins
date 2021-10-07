#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ LINK PLUGIN
# Easy script to create a symlink from the repository plugin scripts to
# the SwiftBar plugins directory with a time interval.
# =============================================================================

from argparse import ArgumentParser
from os import remove, symlink, listdir, readlink
from os.path import isdir, isfile, islink, join, splitext
from pathlib import Path
from subprocess import check_output
from sys import exit


# Get the absolute path to this repository's root.
root_path = str(Path(__file__).parent.resolve())


def parse_args():
    p = ArgumentParser()
    p.add_argument('plugin')
    p.add_argument('interval')
    args = p.parse_args()
    return args.plugin.replace('/', ''), args.interval


def main():
    # Parse the 2 required arguments and assign to simple vars.
    plugin, interval = parse_args()

    # Validate the plugin name passed has a matching plugin directory.
    if not isdir(F"./{plugin}"):
        print(F"Plugin ./{plugin} directory does not exist")
        exit(1)

    # Determine SwiftBar plugin path.
    plugins_path = check_output(
        ['defaults', 'read', 'com.ameba.SwiftBar', 'PluginDirectory'],
        encoding='utf8'
    ).strip()

    # Validate that we did not get an error message or the plugins
    # directory does not exist.
    if 'does not exist' in plugins_path or not isdir(plugins_path):
        print(plugins_path, 'ERROR: Is SwiftBar installed?', sep='\n\n')
        exit(1)

    # Get the script name.
    try:
        name, ext = splitext(
            [l for l in listdir(F"./{plugin}/") if plugin in l][0]
        )
    except IndexError:
        print(F"Could not find a usuable script in ./{plugin}")
        exit(1)

    # Check if a prior script exists and remove it.
    for f in listdir(plugins_path):
        if name in f and ext in f:
            path = join(plugins_path, f)
            if islink(path):
                print(F"Found and removing prior symlink",
                      F"  ⤷ {path} -> {readlink(path)}", sep='\n')
                remove(path)
            else:
                print(F"Found matching non-symlink",
                      F"  ⤷ {path}", sep='\n')
                exit(1)

    # Create the symlink.
    script_path = join(root_path, plugin, F"{name}{ext}")
    symlink_path = join(plugins_path, F"{name}.{interval}{ext}")
    print('Creating symlink', F"  ⤷ {symlink_path} -> {script_path}", sep='\n')
    symlink(script_path, symlink_path)


if __name__ == '__main__':
    main()
