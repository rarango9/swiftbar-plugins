#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Wireguard Manager</bitbar.title>
# <bitbar.version>v1.1</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Manages one or more connections to a WireGuard VPN.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-wireguard-manager/image.png</bitbar.image>
# <bitbar.dependencies>python3,wireguard-go,wireguard-tools</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-wireguard-manager/README.md</bitbar.abouturl>
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


# Hex color codes.
GREEN = '#58f158'
RED = '#ff3434'
WHITE = '#ffffff'
YELLOW = '#ffd735'

ICON_DISABLED = """
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
yZCBpY29uz3Z8GAAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_ENABLED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgoDKituwVNlAAAFnUlEQVRIx32Wb2iddxXHP7+nN41NsklJbmeNm
ZKk0/rCIXVqWxrWjb6wqG+kiIPRiqagQtRlSFPF+Q9fFF8MxmAoOhBhDqXgO5kV25QtaatTkNplXRp0
Sbs0G+mSe2/u8zy/c76+eJLbm9xk57773ef35fy+33O+5wQ2RMRoIxB7kk/zcPgMA6GHdiDV27yhy5z
nSrIg6rTRxntEDWEIH/Qxn9SyNotlXfIxGxQRUd0KqsoSIpZ9TNNNl6ua9xmf0byqTafTfjruEivkTQ
jh7vOcNmwo+Vk4BIDrDV7WRJjSQqxCqZMyHw37ORgGSQB0UT9IxjPE+9ZnlZNTTeyEbkqSTBM+nH3oe
hCOkZJiOOJKiH32dX9FJkm6acfnkzr19Q9MWUo0UrDkszaa9xg5FVb4d+OrW9S4Q0Rk3faEZiVJSz5y
O6lTW/uowhLCTqxCTeYHRE4F35TZOQrq4wGfLODsuFhek0KIOOQ3JcleygaMd4lkqPFzIgtUGoArLGN
kA/ZS8dg45Khgy8h3+bgk+UQ+IEQNI/9wPGajPmbf8mO2L+4URopxpFFEIh8osvPxfJeRQx1hYwVX+f
4C6s69+b74CTtoX/VnfNxva9Ev+4/twYXEqZEBcA7h2EHNSZKNiRo4NqhpSeaj4g7/o06lPT1sT/tZf
85/5D/1K6u1dcufs4cmQrqqXoUVhI3KJE37HgfhY5KkidgTyTEyMpys047677Swof7fyr/xakjJuMY1
DCP2aEKS/LQg7/FJSebDhsi3W2/aH3uzzptBxH4/29JOS/YV4ThCZAgflkm6ZOVgR5MX6dJ1ezS8yUe
Sn4RDKoW6bjFLKTzIarWv1bZeDh9ju36vceaTe9SZ/am0Ql9yLjxAxb+MnZEkf34mZGSddswvyrVVVO
L3/ZXVHqmprtSfjfcI/40k2Rn8vCTZsMjIEOlO+7W2Dms5eEL4SUnyC6WwB6gxJe7g3Efbol7gsY292
4gENKPLVBIDAiUMeI0aHfSX6AYqLIgyRkobzLDI7vewvW3BCb6SyP+evrDDhRZChY5QLtEOqlkVEgLz
offjyZfo2ASizruqhhSFhE9BuI96+NsOz3Gobq8FaC+t2ZoQ2t337fA4H2xF0qyPhKteS7JExYn3Q3I
pYs1yqy5p3vZGst1+VvnmvPt/snJR0mvNbzg5ETBsr+YlpYneBrooB0JVv9AX9Zi+o19pCmvOLDyw7W
tXg4B/EQgEtpHQRom3CFCmC7TQVBp5o65F/EJhSc2DxH+YdVnLEKkhbFiS/HyiywDhwHSok5BgxJ36b
vLzcC9x3a2u8FTpl94vknU2nfGPEPYDcAX7nJYkfz3vi1QAJ+/WkA7rkJ3w6y3cvWpHRMT45qqxRvI+
n5K0bEebGl2oAGuQHPf5hRYtbttI2m44U1BQs9rosYywU2sWZHcHA0vcwsl6/bctLZT5s3l3iqhgWI8
mJclOCRwf1A1JZqNiqYneCiJS77SnWme7/2H5AznTCH+yMEcbdIgNe/TZeMAQf23AvUMk453Ejmujtr
I/5j1G/KS/uWbbK+DNA2UyGxBieZ1aKcKO+Gst2T0d8Mclycezcl4sCkLYkFZHXT7gVNeJX6OKsIf8n
xvdzT4fe/1FnbPPam3KVosJdVxLRXZ2UBh50xBe5HVEvs+vbsjtzysd+fbYIa7flS4n43biIwWc5vxJ
63EylqkxB8A1xjHiIxu4q8TDhrHI0np/SVm4S7Rp0k9mfTfWLS45wkbWWcGcPbLpElEvHjtUSCHJfMq
f95M+ZHvT+9P7bW8cmA7p+xv/y8dt6C9NS8OGlq3gxF1bLXv+33hM+PckSTdsLC07laYyb4FrrKGnNl
tD/RlhD/tFP217CpfZcg0tIlLHEbHHjtoZv6BZ1SVJqV/zR518R+wWRoW05e7/AXdL+5tbxy2VAAAAJ
XRFWHRkYXRlOmNyZWF0ZQAyMDIxLTEwLTEwVDAzOjQyOjQzKzAwOjAwRTEpIQAAACV0RVh0ZGF0ZTpt
b2RpZnkAMjAyMS0xMC0xMFQwMzo0Mjo0MyswMDowMDRskZ0AAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmt
zY2FwZS5vcmeb7jwaAAAAFHRFWHRUaXRsZQBXaXJlR3VhcmQgaWNvbs92fBgAAAAASUVORK5CYII=
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


def main():
    # Toggle the passed tunnel configuration.
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

    # Get conf and pid filenames.
    confs = get_file_list(PATH_CONF, '.conf')
    pids = get_file_list(PATH_RUN, '.name')

    # Show the appropriate colored icon.
    if len(confs) == 0 or len(pids) == 0:
        add_line('', image=ICON_DISABLED)
    else:
        add_line('', image=ICON_ENABLED)
    add_line('---')

    # Show the message if no confs exist.
    if len(confs) == 0:
        add_line(F"No confs in {PATH_CONF}", color=RED)

    # Build the menu section to toggle tunnels.
    else:
        for conf in confs:
            if exists(F"{join(PATH_RUN, conf)}.name"):
                add_line(F":stop.fill: {conf}",
                         bash=F"'{environ.get('SWIFTBAR_PLUGIN_PATH')}'",
                         param1='disconnect',
                         param2=conf,
                         refresh='true',
                         sfcolor=RED,
                         terminal='false')
            else:
                add_line(F":arrowtriangle.forward.fill: {conf}",
                         bash=F"'{environ.get('SWIFTBAR_PLUGIN_PATH')}'",
                         param1='connect',
                         param2=conf,
                         refresh='true',
                         sfcolor=GREEN,
                         terminal='false')

    # Show the connection details of each tunnel.
    if len(pids) != 0:
        add_line('---')
        for line in check_output(['sudo', 'wg', 'show']).decode().splitlines():
            if line == '':
                add_line('', trim='false')
            elif 'interface:' in line:
                add_line(F"{line}", color=GREEN, trim='false')
            elif 'peer:' in line:
                add_line(line, color=YELLOW, trim='false')
            else:
                add_line('⮑ ' + line, color=WHITE, trim='false')


if __name__ == '__main__':
    main()
