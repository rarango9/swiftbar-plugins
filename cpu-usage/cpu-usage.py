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

ICON_DANGER = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA/1BMVEUAAADTAADRAADJAADoAADaAA
DSAADUAADQAABMAAA/AABLAAD8AAD/AADMAADkAADKAABNAABWAABfAADVAADTAADUAADUAADTAADRA
ADSAADUAADUAADSAADRAADTAADUAADTAADUAADUAADQAADTAADQAADTAADUAADTAADMAADUAADUAADU
AADPAADSAADUAADUAADUAADUAADQAADUAADUAADUAADOAADQAADTAADUAADUAADUAADUAADUAADUAAD
UAADUAADUAADUAADUAADTAADQAADQAADTAADUAADUAADSAADSAADUAADPAADTAADTAADSAADUAAAAAA
CfmH7vAAAAU3RSTlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAr0P6nD2rz718QqMgkc/dFxA5wfvxRE9YSA
yVBQKH9gD9S4QMQiuT2+/r426Bwx2OjskgTDsbuaRT5AsXHJGFPvhcAAAABYktHRACIBR1IAAAACXBI
WXMAABYlAAAWJQFJUiTwAAAAB3RJTUUH5QkcBAkL3Jtg2gAAActJREFUOMuNlGlTwjAQhneDJHjgDbE
iUAgql1Bu5KqggPe1//+/WAjMUIdp+35L8swmu9l9AVbCWFxeGCy0c5m4SoZDPJWWZkbAf4kskcohM0
yi65sI5hTRrQvbRcaFyBMViihKZaLyncBigSgvBGd8b0VxXqlatTpRo9my2h2iTttqNRtE9ZpV7XK+v
8Q4v+/1B2pIRCOlbEkkbaVGznKoBv3ePeNLjHV75KFel+lo1b4X1q/qaMIaED2Mt+qBaGAt8kUhak7u
Y7FVY6dKNSEQYtl8fagxdCOosWE9P8lAXL/AwQ6ibix6sMQWegS5xjD6NN181vQpimtMQloVGjqamLp
TnOpLqVGwZ5DKFZsjjY3d2Gpr1CzOn4EjtpQXplqIEQgxYXljlsBD2DFKbdsLs9ullzBcmuWO9MJkp/
yahIRrbwu20Bu8BcESkHz1v9R8h/CLfwrGERyif0HYcbDycviY+39WLgWzT/+vV+mgjfQYpC3jkJn4N
3k2FnRkAg5g4HFmFW9zqLBAVsN1tBPOvzyN61Qb3NmmDd4tbLC0aYOnm5Z5fuv0zBwjN99EpsGWpjrZ
4r0Zk2bPkVA4eZV4PzpmxoX8+cX16R/svg0U7DsmzgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0
yOFQwNDowOToxMSswMDowMDSp2hEAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjhUMDQ6MDk6MT
ErMDA6MDBF9GKtAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJgg
g==
""".replace('\n', '')

ICON_NORMAL = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRwECB0xVOTKAAADh0lEQVRIx62WPWwcRRTHf7M7exDO+JMOQ4HPE
lIk3CBRWMJ3RQQSkVBSgISMA6IIpCJQICERpULCRagpjOyCC6JBQRQIChyJKJbShCYNYCniWnzh/LFm
d2b+FHv23eH4HF/4T7Erze5v3rx5782D/yjgT+q2Qriaj+S0EP6CNkPTnxMtHG40fK2gtVAJHCkRPpQ
kpfkpT04+EtYkKfySDWd4slNKJSm8rwP/RsVjHo/DI8CUAZRkQwaLtWYYwIwnNsGQDykBMMMgPDmeV9
owW6CWES62zzCJmALAJDNmg4gxygCUqdI0IZnBADBFFaOGXzf+GgvU98zzOLLRsKiGdpQqV6FMqVLtK
kiSgnaVKlXWns2VakeNsJiNOnxnr47dOCxqQIXF3TjvwDxuWo1BYWr4ad/xWQSTjAPwOzeOPvF9zVIB
xqNJfgOwofCn2m69wVvHgC1TAQwCIaxO8rIpM1XY2Ik20zcWe2Ytb/MiLb630VfMHPzc9MEdmLEsAJj
XLc/d9+N3TLX7vHsWilll6T6LvWD1jXlVCcZEPVZVme/nLC11oxSQcfrRhnfDUj6UzCQfk3Rwh1nVlu
+xKnef5r+WUt2y3It/spgNPurAjimf/GyvgyfaIWD2E35ARQaRYR/HjWAZ6xsL/WUYY4L8sZYNF+IFh
ilTGhhW4nO2o3v+Cxt9xtBDbREMTwNEz0bKHxLVUWLDxfg8o5R5amCviT/ZVksrNl4J30YJc9R5ZEBY
xkWuBxf/bVMebQFNNCAKRJO/YIuoBAge4N7qoyAMJ7A84Z/PTiQzSTwwKs5r+XiyFd2y0ZfmpTjGdOe
AMP3RcU/NSOwnVibXNWtOY3qPURhY5fBkj1ntrXcmAmLzGrrZczksi2IEdMjomlnu+fe21ZvmNMNM8U
Z34e5Xtg9UYUedP7TND3vrVIsOomPZA43CslTVwmIbFaFh2nE2y/IxznG2sw1D+94M0Ig2eBKoUDl2a
GyERvESFeh8XfVjQ/b8W8/Xu9LH48j/r8ZlHofjn8hPq6aqViQp+Oyy5lTTWd2VJN3VWdU0l10OXpK0
oqpqfno3djjOd5v6wX6zJ3RJkoLbPhMQGtcdSdIdTYjA9pngJEmXtN/s7aHasXWFK/sRppYBjCulwoG
zTQOoFRwYSlsmJwZaHF0AA6GiNSl8l020G+RzoRk2/Xtis+hxryqEm75yMNv+BTXz0V+TWBQ6AAAAJX
RFWHRkYXRlOmNyZWF0ZQAyMDIxLTA5LTI4VDA0OjA4OjI4KzAwOjAwwHzzHwAAACV0RVh0ZGF0ZTptb
2RpZnkAMjAyMS0wOS0yOFQwNDowODoyOCswMDowMLEhS6MAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtz
Y2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_WARNING = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABL1BMVEUAAAD+ywD7yQDywQD/4AD/0g
DywgD8ygD+zAD/zAD9ywD6yABcSQD8yQD9ygBLPABaSAD/8gD//wD1xAD/2wD2xQDzwgBcSgBnUwByW
wD7yAD/0QD9ywD/zAD/zAD+ywD7yQD9ygD/zAD+zAD9ygD8yQD+ywD/zAD+ywD+zAD/zAD7yQD+zAD+
ywD6yAD6yAD+zAD/zAD+ywD1xAD/zAD/zAD/zAD4xwD8ygD/zAD/zAD/zAD+zAD6yAD/zAD/zAD/zAD
4xgD6yAD+ywD/zAD/zAD/zAD/zAD/zAD9ygD/zAD/zAD/zAD/zAD/zAD/zAD+ywD7yQD6yAD9ywD/zA
D8ygD+zAD+zAD9ygD8yQD8ygD/zAD+ywD7yAD5xwD+ywD+ywD+ywD9ygD/zAAAAABonIEvAAAAY3RST
lMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK9D+pw9q8+9fEKjIJHP3RcjEDkVwfvxRE9YSAyVB
QKH9gD9S4QMQiuT2+/r4JdugcMdjo7JIEw7GX+7zaQ8U+SsQAnDFxyTBE6oJAAAAAWJLR0QAiAUdSAA
AAAlwSFlzAAAWJQAAFiUBSVIk8AAAAAd0SU1FB+UJHAQINQThTDAAAAHvSURBVDjLjZR5W9pAEMZno7
jZtUkrHrWtRDxAWFHKJYRbuYKggPfVc77/d2hg4SnpQ5O8/2X390xmZmdegKnITsjYDStLy3v7B4eBF
RqJGkcxFf4ViyOKY66EE4gnp6s8KRC/snniHdd0xlKI6Qxh2Rxi7oyRTBoxxZiu6O+nFKX5glksIZYr
VbNWR6zXzGqljFgqmoVzSj9MMJ1eNJot0UbEjhCWgWhYQnTsz7ZoNRsXVJ9gWr6BLmqcKzJaoemGNbs
yGjNbiJe9hbpEbJnjegljRbv2Hluont2lImMEduKpUltixIkQibVLqX4MQjIDG1sLqvOUGlybYGNdgT
HDSPB6MJ/W4DpIZpgBUZEuy2jqwFniQJXRymlrCJFkptKRufWc2PSoU8mMboByUhVumKgSosCSwkx3z
GR8HZbD2Zrlhlm17G0A9hK5uuGGGfXc3T3sO84WYGM9wIMf7BHu77x/mniCwK13Cc8bsEm8G6JtASXe
7eUUXkbej5WMwPDV++lF1O8gXfkZyxDE+t5DHn/zuzI+F9Be566vdfYyh7w2tZpvfqzmI6Xfu/8zrq5
tXNvS4D5x+tcGz8Y2mJ23wW2Hqf6wZ2bEV09/IiaeNX5sd6nvMNWJ1NgRDm8+r3w5PHh82thSwrvGr9
98dvsHoYlC94oXXjwAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDktMjhUMDQ6MDg6NTMrMDA6MDDIv
q78AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTA5LTI4VDA0OjA4OjUzKzAwOjAwueMWQAAAABl0RVh0
U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=
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
        add_line(real_usage, image=ICON_DANGER, font='Menlo', color='#d40000')
    elif real_usage >= 50:
        add_line(real_usage, image=ICON_WARNING, font='Menlo', color='#ffcc00')
    else:
        # Always pad single digit numbers.
        if real_usage < 10:
            real_usage = str(real_usage).rjust(2).replace(' ', '0')
        add_line(real_usage, image=ICON_NORMAL, font='Menlo')
    add_line('---')

    # Add button for opening the Activity Monitor.
    add_line('Open Activity Monitor',
             bash=argv[0],
             param1='activitymonitor',
             terminal='false')
    add_line('---')

    # Print out the gathered metrics.
    add_line('CPU Stats')
    add_line(cpu_stats, color='#ffffff', font='Menlo')
    add_line('Load Average')
    add_line(load_stats, color='#ffffff', font='Menlo')
    add_line('Process Stats')
    add_line(proc_stats, color='#ffffff', font='Menlo')
    add_line('---')

    # Get the top 10 cpu consuming processes.
    top_procs = check_output(
        ['ps', 'c', '-Ao', 'pcpu,pid,command', '-r']
    ).decode().splitlines()[1:11]

    # Show the top 10 cpu consuming processes formatted nicely.
    add_line('Top Processes')
    for proc in top_procs:
        parts = [p for p in proc.split(' ') if p != '']
        cpu_usage = F"{parts[0]}%".ljust(8)
        pid = parts[1].ljust(8)
        name = ' '.join(parts[2:])
        add_line(F"{cpu_usage}{pid}{name}", color='#ffffff', font='Menlo')


if __name__ == '__main__':
    main()
