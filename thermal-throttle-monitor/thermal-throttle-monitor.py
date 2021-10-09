#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Thermal Throttle Monitor</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
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
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAC31BMVEUAAADy8vLt7e3///+mpKTQz8
/+/v6Jhob9/f37+/v5+fn8/Pzc3Nz09PTm5ub6+vrZ2dn19fX39/fKysrV1dXz8/NlZWXs7Oz4+Pjw8
PD29vbNzc3Mysri4uLn5+fv7++rq6vh4eHf39/q6urS0tLT09P9/f3+/v7////////+/v78/Pz9/f3+
/v7////8/Pz+/v7+/v76+vr////////7+/v+/v7////////+/v739/f+/v79/f3////////8/Pz9/f3
////////8/Pz8/Pz+/v7////////////9/f3+/v7////8/Pz////////+/v7////8/Pz///////////
/////////+/v7////////////9/f3+/v7////9/f3////+/v7////////+/v75+fn+/v7////////+/
v77+/v7+/v+/v7////////7+/v7+/v+/v7////////+/v7////////9/f3////////9/f3/////////
///9/f3////////////7+/v+/v7////+/v77+/v+/v7////9/f34+Pj+/v7+/v739/f7+/v////////
////9/f38/Pz+/v7//v79/f3+/v79/f3+/v7+/v7////6+vr+/v7+/v79/f36+vr4+Pj9/f3+/v7+/v
7x8fH////9/f3////////9/f39/f3////9/f38/Pz////////////+/v7+/v75+fn+/v7+/v77+/v//
//+/v7+/v7////9/f3+/v7+/v7s7Oz////8/Pz8/Pz////9/f3////////+/v76+vr////////////+
/v78/Pz9/f3+/v709PT+/v7+/v79/f3y8vL+/v7+/v79/f39/f3+/v7+/v78/Pz+/v7////d3d3+/v7
+/v77+/v7+/v+/v7////9/f3+/v79/f37+/v8/Pz+/v7+/v77+/v6+vr////5+fn8/Pz+/v7+/v77+/
v///8AAAAszJdSAAAA83RSTlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFHM/
Pi6OTbh/VHp1jNp/hfO7PGrB2FK+dk8VO3nKBmOr66rbGajC8j2PwMDoAzF90KGkpGOUpnwAq1u6++7
Bys0MzETEjU4NxULpvPyvx3hFdDuQ4qMiU5BZ0AntMaXGAUFBD3UvSYQtLOwcC7XpD4DU7VG+gys2k0
DCmrsiAFNV/XqRWnmLB3e3dygsQq2cg0cGuj0P2inAuAfP8AJ38EKC1dWU+03Xq4EZ75/Bal+NDhv4B
bBygFNnwUPV2ZEgjofIpXTKFnjPUNp7gxrQeYjAAAAAWJLR0QAiAUdSAAAAAlwSFlzAAAWJQAAFiUBS
VIk8AAAAAd0SU1FB+UKCQMULKPVclUAAALDSURBVDjLjZT3X01xGMefPHx9zz1y3Ru6MpNVuKSQkSTZ
MpOQkcyyIntG9iykZFNERmYZ2XtlRGXvvZ5/wDl3u04v3r+c13le79f3PM/n+z1fAACHYlCrdh13j7p
YvASwevXJHr2HZEFJbNBQfvNsxBHQi/7GW9aExk2ImvoQNWuuAmyhoLnLGmvpS638WvtTmwAReNvAdu
3t6NBR1rATUWfs0pWCujFAht3t6YEGTWqnJ+vVm4L7IJRCFdrDHS0amjSJ0tKKdihpiAEhfUNt6NdfS
VOXGWA3aZiSxgYOsk9ESdPg4CFhtoQPVdK0QsSw4SNsGDlKSQNB/eeoTFTU5OPARPYfGrLRkVFjjERF
ji1KE8aNnxBtxmdiURqbFPOvQGT45Ck21tSiNI3TtOkzzMycJVXKWrXZWM6kaTV2W68uj3PM2lyGGpP
n7MxR1BlD4Rqo4CzOizVo80m/IE5EF7D0x3HhIpnFCBVxyVIyaUTLlguW74K4ImTlKpnVawDjE6SDsn
Ydrk/c4C55cZxZQklKNk3qCxtTiDZt3iI1gFu3bSfasVO07MQuvSW31DTavQcFVqmyqMN0X9q7j1cx9
5YRu/+AzMFDkEkUiCpDP1V1h48QHcVq5tXw2HEDJyIgi7JPMsFcP0V0+oyjSauKoumEqEFPOWdFJ2Pd
lZ9Lo/MXOFgRBTk6DkQXM8xNV+d+2XTpMrOxxCtJV69dD4AbFHaTq41FFd7yptt3rAFLv8XdYL1e7wm
5RPdQZ/w/VfcfED1EV6vGMNQYSHoy5eRxrRpUOjVPjKbwR8zNqmnxsZxdPhQUEj3JQyaI7OmzHKLnL2
wnQP7ylZfX6zzAN9IVGPP23fsP0z76E336zNBGA27IhIMLfpGvyuj8r0HSI+EbYg1QQK3F74WmLU5Li
Uc3B1BE64gFP3J/euuzMlN/YU1l6zeCMc1k8qEzwwAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0xMC0w
OVQwMzoyMDo0NCswMDowMDYLyEwAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMTAtMDlUMDM6MjA6NDQ
rMDA6MDBHVnDwAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg
==
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
