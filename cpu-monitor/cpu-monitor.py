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
UAABYlAUlSJPAAAAAHdElNRQflCgQSJh3w9TeEAAADHUlEQVRIx62WwWtdVRDGf3POeb0vmIp5D4QIr
roQpa6Cm0q1uLC6CC6y6J8QcNVFFZSAdaNFC62LLPonBJpVVoWij7SUbrIpou5rsRReEiJp3n33nvlc
vJQk5MW8FzIHDsPAfPebM3NnBg7JDiIvqJJ8cSd1zW8oK/uNru0kX5RU5QWxw0ji5KbuS5KeeMsn9Vi
S9NgnvaUnkqT7uelDPNNhk2FGACBYYE83wis92DAa4Qh6NsI9CrOM16lrgDa8pArrBmjdKwgbBqhb18
NYHPiGcJxAIJ8PVyz5SngEeSbOgS+HNfALYVa1L8XfRcaIBwBsPxSIfmy8E95G+57Bh+imv8u/imxHx
Vzj5Lbf0nNVI5znfiu3nTycWUWOZ27aVcQ/lPy/FExjut2/FnNjD+wlTQzIGLwXfuVN3fQ78RiwXIR5
u8YL/4Q/nASIEkRuakIT/YbQZVV6Vp/L6JiTqc/pmSpdFv2GJjSRmyL5QrhEwFI3X48CylgeWUj7k1V
SAsrn03XaKLh3UvhuUGtG+JMHjC3his3tah+HvbK1ND7UAa+UtGgfETBtaCVMjg/mK3bRphCu1VReLV
63AF7Gf/ls/CjDo/x5LEBebqXtXPQxoDpJkAAaeOplTq0f7RIBC+v52+hjI3meiT/QQuZTnWRfDdqQE
dfojM8rzvHpQLMPwvjuR0vSz4Mwte7LsT0+gC/bjLUQrk7a/OaN18zAq9g7UTbX8hexAdLmdmpGzuw2
794Jo2tQAD7RS81f7CIBCxv+dThBNv1C+IkpZF48SPblwGrYLL+NTyvM8uEuwvuB+pVZ9fhQB7zqpO9
tkM2uL8W3xgfzpfCutQfZPLXm6E2RehQ9gIDD09Bl2uZ157gZoMLmmeaFP4VQDf7r3ukOlH1yqqNuMI
SrmE48hA+tB8KGrgd5OR67HgyRin7D70qSP6zPVk2/J0l+r27WZ/2hJPndfmNYUaahpkQbwKZiAbQAr
BUbFEwBWLuRhnXmo/qZRrhHAROu3Yd2ufZ0yffpo4GVhJ461KDVcmtjWx0cV2dzu9zSKlCrY71hhfgf
wrM8F4BfzTcAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMDRUMTg6Mzg6MjkrMDA6MDAwZiOzAAA
AJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTA0VDE4OjM4OjI5KzAwOjAwQTubDwAAABl0RVh0U29mdH
dhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=
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
