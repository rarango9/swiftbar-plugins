#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Network Monitor</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the current bandwidth and other network information.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-network-monitor/image.png</bitbar.image>
# <bitbar.dependencies>python3,ifstat</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-network-monitor/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# =============================================================================

from os.path import exists
from subprocess import check_output
from sys import exit

# Hex color codes.
RED = '#ff3434'

ICON = """
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
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def scale(bandwidth):
    bandwidith = float(bandwidth)

    if bandwidth < 1000:
        return F"{str(round(bandwidth))}K"
    else:
        return F"{str(round(bandwidth/1000))}M"


def main():
    # Check if ifstats is installed.
    if not exists('/usr/local/bin/ifstat'):
        add_line("Missing ifstat", color=RED, image=ICON)
        exit(0)

    # Parse the bandwidth output into just the upload and download values.
    bandwidth = [b for b in check_output(
        ['/usr/local/bin/ifstat', '-n', '-w', '-i', 'en0', '-b', '0.5', '1']
    ).decode().splitlines()[-1].split(' ') if b]

    # Split the parts into upload and download vars and scale based on speed.
    dl = scale(float(bandwidth[0])).rjust(4, '·')
    ul = scale(float(bandwidth[1])).rjust(4, '·')

    # Show the speed in the menubar.
    add_line(F"{dl} :arrowtriangle.down.fill: {ul} :arrowtriangle.up.fill:",
             font='Menlo',
             image=ICON)
    add_line('---')


if __name__ == '__main__':
    main()
