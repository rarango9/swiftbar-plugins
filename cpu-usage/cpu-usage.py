#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>CPU Usage</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the </bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/cpu-usage/screenshot.png</bitbar.image>
# <bitbar.dependencies>python3,procps,top</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugins/cpu-usage/README.md</bitbar.abouturl>
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

COLOR = {
    "gray": "#737373",
    "green": "#58f158",
    "red": "#ff3434",
    "white": "#ffffff",
    "yellow": "#ffd735"
}

ICON_DANGER = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAz1BMVEUAAAD/SUnjQUH6SEj+SUn8SE
jHOTn9SEj7SEjMOzv5R0f4R0feQED/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn5R0f9SEj+SUn/S
Un/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn8SEj5R0f9SEj+SUn/SUn7SEj+SUn/SUn/SUn9SEj/SUn/
SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn3R0f
8SEj6R0f/SUkAAAAqJvsjAAAAQ3RSTlMAAAAAAAAAAAAAAAAAE9LoKHwP0SR6CkNlaHTl8oBnaWayRA
sNmvYNVfv8VXnPnqB/EIMvb27zjnh3upGPxWWvCkMKpM29MwAAAAFiS0dEAIgFHUgAAAAJcEhZcwAAF
iUAABYlAUlSJPAAAAAHdElNRQflCR0RBShwGFhaAAABTklEQVQ4y7XU2VrCMBAF4IxtBZeSFlrZCyj7
JkvZVdR5/3cyaQKC0jQXem56838wPU2GEBmwM0gdIOAiuuzhUMzYQH7mz9iVYZgA2RxSDwB8RJ89PIq
5LIBpWNeSmdZDvlAslbFSDWr1BmKjXguqFSyXioXHJyslWarZamNM2q2OdRir28PY9AeHAWGIOBo/X8
h4hDiMGJuWswlczIQzFmLb9nSmYrMpIyTDQjkjvxHhjHJB5KSczcPFScK5YFEIZVkKFp6/YyjYkgviO
I63EmxxzhaCrTxGoonWKraOppS9xbPv3jYqtol+zXVdf6tiW5+R00IuM1GIJtP8U81X0CwkkYl6j+dN
+2OpPv1ut3t5TT5IJ71pHUv1IQ+C4G2ffGVkvUkXkPc26Mdf5173wKyOajk0jzsk/f4Rt2ryn5Yp2c3
tnWJxpe//ZVtqsC861rcmmKs0VQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yOVQxNzowNTo0MC
swMDowME6vI2YAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjlUMTc6MDU6NDArMDA6MDA/8pvaA
AAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_NORMAL = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0RAwL9+TYKAAACcUlEQVRIx82Wv2sUQRTHP7u3NmeOiAkJaiHIF
WnECCKmO5A0opgmjdhGxEISyxAR0cbCX41g8k8I2omYLo2gl8oixELQSyrB5NDcznwtduZu9zzPvSWC
3+J239uZ771f8+ZBF4RGtC6poQkl8pIkaclJE2pIWteIurcSso/4F2Sf2WMPiwDi5EFM8mJxv+5rEo0
YhGWPmDVHFiWPY1hMWVOcCEoMMQqUucpXQgznADjHNUpYjlAGRpljR8Z+0hq7Z7MGGkzFLqupQdG0y6
1K3J1DO6vWwFSSFJtZZd2EoEoEfOB97qRYTjNJKax6RdRVLS+4O0D67jDpPUssG3FBKxeuiDKHKCVkb
51qrO0wysGQWjXHZR+zkz3XnqL2R86AVeopeZxxT7blVAcZSi2o8aSPWfMZsh12PVkNgJgbLKQW9Pc0
+3WFZ0lVRHx0qu180e6BbTacZYH/q6AwWeA3d+rMFiaznTpbcopaYbLzlJJTE3GvMInHNNPJy742x4j
bbTenC3K8ZtW7ed+pTGGyNzxwlrVLo7jDYbs09iFUapdGng7xF4xR9ccpxZ9C//OQ/TrHFRczngJgyV
4xq8z3bUFpDPl+E3Gz54Z6psn0x5ZvEj0SkC+KqVUrPPRt+7pz8wIzuW3Josk3b9lzpzrMDDDD8YGuu
nYYIVW0djM0lJj0l1duxNroSn1Mq/B4YComYx8GS1w+MBUmg8sCR/nOIze4XOQS8JJXbnC5RYUvPGZH
RptmLWyG2ci84yc/sAihYdUlNVRVIi9KkhadVFVDUl3DciNVi018AgA4k0551Dm3QacFhE6KnEfR78f
k/x1DfwH4F33RJGueRgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yOVQxNzowMzowMiswMDowMF
BkTPIAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjlUMTc6MDM6MDIrMDA6MDAhOfROAAAAGXRFW
HRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_WARNING = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA21BMVEUAAAD/3E7jw0X62E362Ez+20
782U3HrD382k392k372U3MsD/510z41kz72E3ev0T/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E751
0z92k3+207/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E782k3510z92k3+207/3E772E3+207/3E7/
3E792k3/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7
/3E7/3E772U331Uz82k3610z/3E4AAADRhyGIAAAAR3RSTlMAAAAAAAAAAAAAAAAAAAAAE9LoKHwP0S
R6CkNlaHTl8oBnaWayRAsNmvYNVfv8VXnPnqB/EIMvb27zjnh3upGPxWWvDQpDCiTmyYYAAAABYktHR
ACIBR1IAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAB3RJTUUH5QkdEQYelI+eAAAAAVFJREFUOMu11Nla
wjAQBeCM0AquJS20shdQQJBFlrK7O+//RiZNQFCa5kLPTW/+D6anyRAiA1YGqQ0EHESHPWyKGQvIz/w
ZO0kkDYBsDqkLAB6ixx4uxVwWwEiap5IZ5k2+UCyVsVL1a/UGYqNe86sVLJeKhdu7VFqydLPVxoi0W/
fmdqxOFyPz0NsOCH3EwfDxSIYDxH7I2LScjeBoRpyxEMuyxhMVm4wZIRkWyhn5jQhnlAsiJ+VsGsz2E
kwFC0Moy1yw4PAdA8HmXBDbtt2FYLNDNhNs4TISTrRUsWU4pewtmn33tlKxVfhrjuN4axVbe4zsF3Kc
iUI0meafar6CZiGxTNS7O2/aH0v16TebzdNz/EHa603rWKoPue/7L6/xV0bWG3cBeW+9h+jr3O1smfm
mWg7N3Q45e/+IWjX5z5Qh2fnFZfTiSlxd/8u21GBfNh3Ds2YXgE8AAAAldEVYdGRhdGU6Y3JlYXRlAD
IwMjEtMDktMjlUMTc6MDY6MzArMDA6MDCvXZF8AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTA5LTI5V
DE3OjA2OjMwKzAwOjAw3gApwAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAA
SUVORK5CYII=
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

    # Show the correct icon and rounded CPU usage percent.
    if real_usage >= 80:
        add_line(real_usage,
                 image=ICON_DANGER,
                 font='Menlo',
                 color=COLOR['red'],
                 size='13')
    elif real_usage >= 50:
        add_line(real_usage,
                 image=ICON_WARNING,
                 font='Menlo',
                 color=COLOR['yellow'],
                 size='13')
    else:
        # Always pad single digit numbers.
        if real_usage < 10:
            real_usage = str(real_usage).rjust(2).replace(' ', '0')
        add_line(real_usage,
                 image=ICON_NORMAL,
                 font='Menlo',
                 color=COLOR['white'],
                 size='13')
    add_line('---')

    # Add button for opening the Activity Monitor.
    add_line('Open Activity Monitor',
             bash=argv[0],
             param1='activitymonitor',
             terminal='false',
             color=COLOR['white'])
    add_line('---')

    # Print out the gathered metrics.
    add_line('CPU Stats', color=COLOR['gray'], size='14')
    add_line(cpu_stats, color=COLOR['white'], font='Menlo')
    add_line('---')
    add_line('Load Average', color=COLOR['gray'], size='14')
    add_line(load_stats, color=COLOR['white'], font='Menlo')
    add_line('---')
    add_line('Process Stats', color=COLOR['gray'], size='14')
    add_line(proc_stats, color=COLOR['white'], font='Menlo')
    add_line('---')

    # Get the top 10 cpu consuming processes.
    top_procs = check_output(
        ['ps', 'c', '-Ao', 'pcpu,pid,command', '-r']
    ).decode().splitlines()[1:11]

    # Show the top 10 cpu consuming processes formatted nicely.
    add_line('Top 10 Processes', color=COLOR['gray'], size='14')
    for proc in top_procs:
        parts = [p for p in proc.split(' ') if p != '']
        cpu_usage = F"{parts[0]}%".ljust(8)
        pid = parts[1].ljust(8)
        name = ' '.join(parts[2:])
        add_line(F"{cpu_usage}{pid}{name}", color=COLOR['white'], font='Menlo')


if __name__ == '__main__':
    main()
