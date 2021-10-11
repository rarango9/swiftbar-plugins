#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Thermal Throttle Monitor</bitbar.title>
# <bitbar.version>v1.1</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Monitors if the CPU is thermal throttling.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-thermal-throttle-monitor/image.png</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-thermal-throttle-monitor/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# =============================================================================

from subprocess import check_output


# Hex color codes.
GRAY = '#737373'
GREEN = '#58f158'
RED = '#ff3434'
WHITE = '#ffffff'
YELLOW = '#ffd735'

ICON = """
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
Jggg==
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def main():
    # Parse the result from `pmset -g therm` to important info.
    for line in check_output(['pmset', '-g', 'therm']).decode().splitlines():
        if 'CPU_Scheduler_Limit' in line:
            scheduler_limit = int(line.split('= ')[1])
        elif 'CPU_Available_CPUs' in line:
            available_cpus = int(line.split('= ')[1])
        elif 'CPU_Speed_Limit' in line:
            speed_limit = int(line.split('= ')[1])

    # Calculate the available performance.
    available_performance = round(scheduler_limit * speed_limit / 100)

    # Show the menubar icon and available performance.
    if available_performance >= 80:
        color = WHITE
    elif available_performance >= 50:
        color = YELLOW
    else:
        color = RED
    add_line(str(available_performance).rjust(2, '0'),
             color=color,
             font='Menlo',
             image=ICON)
    add_line('---')

    # Show details about the CPUs Thermal Throttling.
    add_line('Scheduler Limit'.ljust(18) + str(scheduler_limit),
             color=WHITE,
             font='Menlo')
    add_line('Available CPUs'.ljust(18) + str(available_cpus),
             color=WHITE,
             font='Menlo')
    add_line('Speed Limit'.ljust(18) + str(speed_limit),
             color=WHITE,
             font='Menlo')


if __name__ == '__main__':
    main()
