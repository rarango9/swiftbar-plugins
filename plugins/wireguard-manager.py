#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Wireguard Manager</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Manages one or more connections to a WireGuard VPN.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/images/wireguard-manager.png</bitbar.image>
# <bitbar.dependencies>python3,wireguard-go,wireguard-tools</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugins/</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
#
# ❱❱ PREPARATIONS ❰❰
# Add the following line to your sudoers file with `sudo visudo`.
#
# %admin  ALL = (ALL) NOPASSWD: /usr/local/bin/wg, /usr/local/bin/wg-quick
# =============================================================================

from glob import glob
from os import environ
from os.path import exists, join
from subprocess import check_output
from sys import argv
from time import sleep

ICON_CONNECTED = """
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
bmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_DISCONNECTED = """
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
3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=
""".replace('\n', '')

ICON_ERROR = """
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
""".replace('\n', '')

# Full paths to executables and other assets.
BIN_WG = '/usr/local/bin/wg'
BIN_WG_QUICK = '/usr/local/bin/wg-quick'
PATH_CONF = '/usr/local/etc/wireguard/'
PATH_RUN = '/var/run/wireguard/'


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def get_file_list(path, ext):
    file_list = []
    for file in glob(join(path, F"*{ext}")):
        file_list.append(file.replace(path, '').replace(ext, ''))
    return file_list


def toggle_tunnel():
    if len(argv) == 3:
        action = argv[1]
        conf = argv[2]
        pid = F"{join(PATH_RUN, conf)}.name"

        # Wait for pid file to change state so menu item refreshes instantly.
        if action == 'connect':
            check_output(['sudo', BIN_WG_QUICK, 'up', conf])
            while not exists(pid):
                sleep(1)
        elif action == 'disconnect':
            check_output(['sudo', BIN_WG_QUICK, 'down', conf])
            while exists(pid):
                sleep(1)


def main():
    toggle_tunnel()

    confs = get_file_list(PATH_CONF, '.conf')
    pids = get_file_list(PATH_RUN, '.name')

    # Show the appropriate colored icon.
    if len(confs) == 0:
        add_line('', image=ICON_ERROR)
    elif len(pids) == 0:
        add_line('', image=ICON_DISCONNECTED)
    else:
        add_line('', image=ICON_CONNECTED)
    add_line('---')

    # Show the message if no confs exist.
    if len(confs) == 0:
        add_line(F"No confs in {PATH_CONF}", color='#d40000')

    # Build the menu section to toggle tunnels.
    else:
        for conf in confs:
            if exists(F"{join(PATH_RUN, conf)}.name"):
                add_line(F":stop.fill: {conf}",
                         bash=F"'{environ.get('SWIFTBAR_PLUGIN_PATH')}'",
                         param1='disconnect',
                         param2=conf,
                         refresh='true',
                         sfcolor='#d40000',
                         terminal='false')
            else:
                add_line(F":arrowtriangle.forward.fill: {conf}",
                         bash=F"'{environ.get('SWIFTBAR_PLUGIN_PATH')}'",
                         param1='connect',
                         param2=conf,
                         refresh='true',
                         sfcolor='#009800',
                         terminal='false')

    # Show the connection details of each tunnel.
    if len(pids) != 0:
        add_line('---')
        for line in check_output(['sudo', 'wg', 'show']).decode().splitlines():
            if line == '':
                add_line('', trim='false')
            elif 'interface:' in line:
                add_line(F"{line}", color='#ffcc00', trim='false')
            elif 'peer:' in line:
                add_line(line, color='#009800', trim='false')
            else:
                add_line('⤷ ' + line, color='#ffffff', trim='false')


if __name__ == '__main__':
    main()
