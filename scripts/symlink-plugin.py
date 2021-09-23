#!/usr/bin/env python3

from argparse import ArgumentParser
from os import remove, symlink
from os.path import isdir, isfile, islink, join
from pathlib import Path
from posixpath import splitext
from subprocess import PIPE, Popen
from sys import exit


def get_app_plugin_path():
    cmd = Popen([
        'defaults', 'read', 'com.ameba.SwiftBar', 'PluginDirectory'
    ], stdout=PIPE)

    result = cmd.communicate()[0].decode().strip()

    if 'does not exist' in result:
        print(result, end='\n\n')
        print('ERROR: Is SwiftBar installed?')
        exit(1)

    return result


def get_repo_plugin_path():
    scripts_path = Path(__file__).parent.resolve()
    repo_path = str(scripts_path)[:-8]

    return F"{repo_path}/plugins"


def parse_args():
    p = ArgumentParser()
    p.add_argument('plugin')
    p.add_argument('interval')

    return p.parse_args()


def main():
    args = parse_args()
    app_plugin_path = get_app_plugin_path()
    repo_plugin_path = get_repo_plugin_path()

    file_parts = splitext(args.plugin)
    plugin_link = F"{file_parts[0]}.{args.interval}{file_parts[1]}"

    src = join(repo_plugin_path, args.plugin)
    dest = join(app_plugin_path, plugin_link)

    if not isfile(src):
        print(F"Plugin {src} does not exist")
        exit(1)

    if not isdir(app_plugin_path):
        print(F"SwiftBar plugin path {app_plugin_path} does not exist")
        exit(1)

    if islink(dest):
        print(F"Removing existing symlink {dest}")
        remove(dest)

    print('Creating symlink to plugin script')
    print(F"SRC  : {src}",
          F"DEST : {dest}",
          sep='\n')
    symlink(src, dest)

    print('Done')


if __name__ == '__main__':
    main()



