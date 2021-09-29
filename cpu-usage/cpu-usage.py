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
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAllBMVEUAAAD/SUn8SEj+SUn9SEj/U1
P/UFD/UVH9SUn7SEj/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn+SUn/SUn/SUn/SUn/SUn/S
Un/SUn/SUn/SUn9SEj+SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn+SUn/SUn3R0f/SUn/SUn+SUn2
Rkb/SUn+SUn/SUkAAACkj4pZAAAAMHRSTlMAAAAAAAAAAAAAA67gHw7KrRsKySJNWVzrblhj3Al13vr
+dfz7wZ4UTAErTysB2UyuFH1jAAAAAWJLR0QAiAUdSAAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAAd0SU
1FB+UJHQURIEtCDJEAAAFdSURBVDjLjZTpcsIwDIStOECb+yI3TZwDCqSg93+6KoE2hTTB+8cznm/k0
Vpaxm4CTUc0TADLRrQtANNA1DVgoxSFA4BDmAvg+Yi+B+AS5tA1V/mN4nwVbMOIqsRJGmY5Yp6FaRJT
1SjcBmvOb9TuoyiFQJIQz2dZVLuBUzdVjQuqq7XaVwsKbNr9jNoGi6CvBtsS2wPM6NBi+Un9AoQC98D
/pzjsUYQATIOox0BVppCiQo9FoDHdIScIU46n85O6L6XH0HZ0NnRDGJwudfOg+tLBgJFG7DyxpT6PmG
HEd6x5xpo7FhsGM91ELGMicU0yJH2FpWTI3bclrPfN8rJXWOZZzPbzVy3kvv3HkFns0bdFTPJRyRYkD
ZG0V/KzJL9ecpB+sW46lqcRG4e8mwz5cRxyyZWRXEDJdZYNB4qaiWMPtlQbVS641CHg3lbBdS4Grz8x
SKH6LhOqMhH9De8+m/rG9bjkAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTA5LTI5VDA1OjE3OjMyKzA
wOjAw691glgAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wOS0yOVQwNToxNzozMiswMDowMJqA2CoAAA
AZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_NORMAL = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0FETvBJ8V9AAACtklEQVRIx62Wv08UQRTHP3M7ajh+NHehIRcCS
wU1DY0NpRZKRUJtSWFyBQUVBa2xNaG1MOA/QENjAtRcYsKdGLEhZyNI4t3MfC12l+UQOc7lO8lsdmb2
u2/em/fmCz0QirQjSTrRpBAa04Ek6UBjQmhSJ5KkHUXq/RibPBxQwgB4sjUu7ZX+x10bBeFBCGEo5WQ
BMGiaOUaIqAEwzBJnGMpUAKiwzCVinGEAaqzgueCo1BIhpSMQ8EOhrpY6CgrKENJ213tHLdX9UCAkZB
6hupz+F0514QEDAabNLlM4PtFkMMQsYPmiRVqlNILP1ZG0F6pisBaq2pPU0TMBJQGMYIGmaWsgs4Rp0
wQsoyBKRECUTRsC/l5EnpAcpQQREFk+IGr5uOiaaJaZPjYddxqP820YVnmB4VpUtlJPzOmznLp3NKfP
YS5dvZUT2Ft+O0Ocb/xfUTQzHN0ctHwFhqne8Gx/3/eizS+wPMWxxJvr3hwYYoNtbGLZWQGiBGd8J83
PIlaRM1jGcJQLk5UpYy27iEpB2wxrvMJY5gtbBRATZz57IFgOERXigjxNfmAsiziWeVfwnG3yHmv5CV
wW3uEll5nPBitjt9sGWCZxjBcmG2cCa9kDhgufs3VeJ5bdNtn/815UqV7d6D3bPzZN4jv9aGhy/Pew5
SOilueBp9t48tL0Ldu/G4+uV9BDvmFQJLSikJVtj7vXJeeSyzsp20ErQpHFQ34h6d75FQHKXecBXzIA
FzggVnWwoBpUJQYc52CwIDgyp0yxYLYHlQcmZgE4VePKQqG6usWFCw8lqVIVBAFRQtPMmlEiVpkH2my
kYm+NGGiymYq9darAIW/xOqdhWqKnMDq6hCzs26mmnRBCZe1LkvZVFkITqabdTnUQPhN6WQZkiSCIru
Jt096kobM9Sw0Rvjf6fwDqPoCvYTASsAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yOVQwNToxN
zo1OSswMDowMC+1PesAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjlUMDU6MTc6NTkrMDA6MDBe
6IVXAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_WARNING = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAApVBMVEUAAAD/3E782k382U3+20792k
3/+1n/8lb/81b/9Fb/9Vf9207/+ln72U3/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7+207/3
E7/3E7/3E7/3E7/3E7/3E7/3E7/3E792k3+3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7/3E7+207/3E73
1Uv/3E7/3E7+3E721Ev/3E731Uz+3E7/3E4AAADxohcvAAAANXRSTlMAAAAAAAAAAAAAAAAAAAOu4B8
Oyq0bCskiTVlc625YY9wJdd76/nX8+8GeFEwBK08rAdkBTLnV4TsAAAABYktHRACIBR1IAAAACXBIWX
MAABYlAAAWJQFJUiTwAAAAB3RJTUUH5QkdBRISqLgO0gAAAWFJREFUOMuNlOlywjAMhK3GLj1zX+Smi
XNAgZSi93+1OoGSQprg/eMZzzfyaC0tISeBqiHqBoBpIVomgKEjaiqQQQ8KBQBbYA6A6yF6LoAjMFtc
U0ZPFKWP/jIIRZUoToI0Q8zSIIkjUTUMlv6C0hO1+sgLzlGI89uzyMtVz7GnssIZVeWCddX8HOtmPaG
mxtzvqsGywGYDE9o0WHyKfgECjmug/1MU1sgDAKJC2GHAlDGkMOiwEFSi2cIJgSnb3f5G7ZfSYWjZGu
m7ERjsDlV9perQQo8JDdh+ZEu1HzBdj85YfYvVZyzSdWI4MZ/HeOwYwpDkHpYIQ86+zWGdb6ab3sNS1
ySWl91rIfOsP4ZMYte+zWKSj0q2IGmIpL2SnyX59ZKDdMHa8VjuBuwy5N/taMi3w5BLrozkAkqus2w4
sOdy5NiVLeULkwsu1gfc65t/nIrB428MilB9lwlVmYj+AWi7rdLhDSF7AAAAJXRFWHRkYXRlOmNyZWF
0ZQAyMDIxLTA5LTI5VDA1OjE4OjE3KzAwOjAwCssTwQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wOS
0yOVQwNToxODoxNyswMDowMHuWq30AAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaA
AAAAElFTkSuQmCC
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
