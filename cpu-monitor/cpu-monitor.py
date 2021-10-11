#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>CPU Monitor</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the current CPU usage and top 10 consuming processes.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-cpu-monitor/image.png</bitbar.image>
# <bitbar.dependencies>python3,procps,top</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-cpu-monitor/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# =============================================================================

from subprocess import check_output, run
from sys import argv, exit

# Hex color codes.
RED = '#ff3434'
WHITE = '#ffffff'
YELLOW = '#ffd735'

# Icon in Data URI PNG format with prefix stripped.
ICON = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgsDIw5Mu1sOAAADFElEQVRIx62WQWtbRxDHf7PaxuDaKQRXMfbBz
ScImJSYRgSffOmpIaSkpTQ5NLeYQr5EKbSGHHtJgiml4B5y8CUnQ9ViWtfkEzjtwYqjuKaJVcmK9Obf
g6Rnq9FTJCfzYN+y7Pxn/juzMws9xElmfcufJgtCJAXf9u2kIESy4E99K5n1XmqEXouGzdkZmwjzAFa
wKZuyAkCYtwk7Y3M2OBhYBCAezl9eGRgMG2AcFExlHLQDoCdHxh3AVe6t1cPhEo5Ww5eM+nIAfCWMga
8EQMtEqr5qlMnzCvkX0UT8bDU7MOUUFZWrWz2dH1jNfjPRQFR6nk0K1eAdmjPhI3vfxrJNqsIfyU/xr
384wduZmxAvLvpDDSD+8MVFoSyoEg0aMylU0udrwzVmGjw+GgBPmToBXbKzwJ+6bdtZCYA0bYu8Z2dz
l2wpn3onomaZs4iprNXi/oVzALptS/3CZAj7Fjj3q50f14eWR2pqHd/q0PKbNdN9SYmuiGYmVBOhK0o
k3a+Z30xpbwUbb+8JjNqhaWImWDySBQajaeKPR/80zBMx7fjySGBIGQl+h6ZNIppai+EBD1o2Qj93Mo
/PyvZNh9rQvvST6AUrWMT0xFdyz4bWl58Kl+00UlPFaD/aVJvmWH1pZEisup+41qJpUHqzNPUxKc3jR
DO5GyopzVCk2KZ5rGiGPfuupW9vOpoLh0mb+3tofXk+fNZKWl+L9j0TbZqx/vUxonndvmoz/iKw3153
qmmpE30vemtH+1el05H3oy53SpCvbnChYhA0beSyqyjg0yGAKpucvxd2OyUo2qZtdqJRQBt8ArbohD7
F0afDIgAbH8if2w8t/S4p0XzNst1t8jUbSpd3VRqcHKLVPeOt7FYH1XYT/qWrCR90zWv2u7V2Vf+n3e
OQH5NHJ8PnjPqdUAY/Fa6B3w174Plwnarfs+d7vMtAIvyqEslvCeE3JMlvCOG3JCV+tXfaZL3P8gSwS
QA7fWScBIJlvFmyLroGGAcFU+s2NQ/nL68MCCa0rkfs+hqAiiqppCKAr7GrR1rv7dp/k75CEZPY6/sA
AAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMTFUMDM6MzU6MTQrMDA6MDCt+YagAAAAJXRFWHRkYXR
lOm1vZGlmeQAyMDIxLTEwLTExVDAzOjM1OjE0KzAwOjAw3KQ+HAAAABl0RVh0U29mdHdhcmUAd3d3Lm
lua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def main():
    # Open the Activity Monitor if option was passed.
    if len(argv) == 2 and argv[1] == 'activitymonitor':
        run(['open', '-a', 'Activity Monitor'])
        exit(0)

    # Create dicts to store the desired cpu stats.
    cpu_stats = ''
    load_stats = ''
    proc_stats = ''

    # Query top and iterate through the output to grab what we want.
    for line in check_output(['top', '-F', '-R', '-l1']).decode().splitlines():
        if 'Processes: ' in line:
            proc_stats = line.replace('Processes: ', '')

        elif 'Load Avg: ' in line:
            load_stats = line.replace('Load Avg: ', '')

        elif 'CPU usage: ' in line:
            cpu_stats = line.replace('CPU usage: ', '')

    # Calculate the real cpu usage.
    idle_usage = float(cpu_stats.split(', ')[2].replace('% idle', ''))
    real_usage = round(100.00 - idle_usage)

    # Determinie the color for the percentage.
    color = WHITE
    if real_usage >= 80:
        color = RED
    elif real_usage >= 50:
        color = YELLOW

    # Show the menubar icon and potential usage.
    add_line(str(real_usage).rjust(2, '0'),
             color=color,
             font='Menlo',
             image=ICON)
    add_line('---')

    # Add button for opening the Activity Monitor.
    add_line('Open Activity Monitor',
             bash=argv[0],
             param1='activitymonitor',
             terminal='false',
             color=WHITE)
    add_line('---')

    # Print out the gathered metrics.
    add_line('CPU Stats', size='14')
    add_line(cpu_stats, color=WHITE, font='Menlo')
    add_line('---')
    add_line('Load Average', size='14')
    add_line(load_stats, color=WHITE, font='Menlo')
    add_line('---')
    add_line('Process Stats', size='14')
    add_line(proc_stats, color=WHITE, font='Menlo')
    add_line('---')

    # Get the top 10 cpu consuming processes.
    top_procs = check_output(
        ['ps', 'c', '-Ao', 'pcpu,pid,command', '-r']
    ).decode().splitlines()[1:11]

    # Show the top 10 cpu consuming processes formatted nicely.
    add_line('Top 10 Processes', size='14')
    for proc in top_procs:
        parts = [p for p in proc.split(' ') if p != '']
        add_line((F"{parts[0].ljust(8)}"
                  F"{parts[1].ljust(8)}"
                  F"{' '.join(parts[2:])}"),
                 color=WHITE,
                 font='Menlo')


if __name__ == '__main__':
    main()
