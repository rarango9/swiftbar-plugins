#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Memory Monitor</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Shows the current system memmory usage and top 10 processes.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-memory-monitor/image.png</bitbar.image>
# <bitbar.dependencies>python3,procps,sysctl,vm_stat</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-memory-monitor/README.md</bitbar.abouturl>
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
RED = '#ff3434'
WHITE = '#ffffff'
YELLOW = '#ffd735'


ICON = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgsEHxWwYv2YAAACp0lEQVRIx61WTWsTURQ99+YlkSi2mGBLF+7cu
rGiuCh040rrRkQptNE/UFf+A0UUQUVwZ60bRYogduUm0IW0BLoogrbuXJRWG0xrTJvJzDsuMs0kNVN8
g3c2d97HmXvueXPfBTqsDg++CcZtmR4PMs+Wg/Gm8VBHrNXwWewUt/kvtm2nvkita79EbhVHwXP6HgU
AFVTjP4p+5AFs2kuysI3+9rCJVvgQYAwFgCV7W9dEeiORdkjvyygKMiYLfu9Fu6il7CxJskhYMOaxIG
yRJO3s79RuB4JGbhaHRdIALOrAEiTmWQIgdVhA0jnJ9gbrzuRwbMKG9+U6MmPb44TA3SzY3m94CmfEQ
PjdfkjtOGORR3hBjoP0WTYyKycBQHyd8p5lHLE8m56QxzCAAF9V8nuE0UdHKIBA397xkryxkzoKA+E6
p7PqCpZVOw2RQRC+LRmdwxwQymNcwSCyLndbrkLdqcVTNjyL82Ig3LDvUr/cEWy/XpYBkD4/GnkjJ1o
09Zb3JIGak/IoTNM3RfQ/pBOpmW6/ZA2vy0hLTfs6iZrBC91tqcl5oyWUQpqJ1NRNedpyFc6xHGTGjs
qIhDRTP92TZgt6TQZB+pw38koGQpqHGg+zjlgNmynKg9Z+bCga7ZmmewkSoBkhG16NDm3GOYMZDWa0G
h3aRVkMaSZTsyozYYzQJNU1jrKxF/dKkH2e+uGMQDuoN9slSGZwLKTJxr0Eat6QOy1fi4pKOO5jK5Ga
WwjvYVYMr0QXSiI1X+p6dKEsy3JIM5maNXkbxggTBZOs5krHbdubGIFy7PZy7Jc7iDXgM9cUQJkTnI6
NlACYEwXY3GGqN1gN+YCrAICJ4JOuxXYLDIZ0AgCwmgsqHRP/tdnrshpWnNrQlX1taJftODXI/l8N8h
+va7lN+ngM6gAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0xMC0xMVQwNDozMToyMSswMDowMAXWCMYAA
AAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMTAtMTFUMDQ6MzE6MjErMDA6MDB0i7B6AAAAGXRFWHRTb2Z0
d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text}|{params}" if kwargs.items() else text)


def add_memory_details(key, val, total):
    v = F"{str(round(val))} MB".ljust(10)
    p = F"{str(round((val/total)*100))}%".ljust(10)
    k = key
    add_line(F"{v}{p}{k}", color=WHITE, font='Menlo')


def main():
    # Get processes info and remove the first and last elements from list
    ps_list = check_output(
        ['ps', '-caxm', '-orss,pid,comm']
    ).decode().splitlines()[1:-1]

    # Convert the ps output line to an list of dicts with parts.
    ps_data = []
    for line in ps_list:
        parts = [p for p in line.split(' ') if p]
        ps_data.append({
            "rss": parts[0],
            "pid": parts[1],
            "comm": ' '.join(parts[2:])
        })

    # Get the total amount of memory in Megabytes as an int.
    mem_total = int(check_output(
        ['sysctl', 'hw.memsize']
    ).decode().split(' ')[1])

    # Reserved memory total.
    rss_total = 0
    for rss in [ps['rss'] for ps in ps_data]:
        try:
            rss_total += float(rss) * 1024
        except:
            pass

    # Get memory information from vm_stat.
    vm_stats = {}
    for line in check_output(['vm_stat']).decode().splitlines()[1:]:
        parts = line.split(':')
        vm_stats[parts[0].replace('"', '')] = parts[1].strip()[:-1]

    # Calculate each desired metric from bytes to Megabytes and totals.
    wired = round(float(vm_stats['Pages wired down'])*4096/1024/1024)
    active = round(float(vm_stats['Pages active'])*4096/1024/1024)
    inactive = round(float(vm_stats['Pages inactive'])*4096/1024/1024)
    free = round(float(vm_stats['Pages free'])*4096/1024/1024)
    real = rss_total/1024/1024
    total = round(mem_total/1024/1024)
    percent = int(round((real/total) * 100))

    # Determine if there is a color for the percent.
    color = WHITE
    if percent >= 80:
        color = RED
    elif percent >= 60:
        color = YELLOW

    # Show the menubar icon and text if applicable.
    add_line(str(percent).rjust(2, '0'), color=color, font='Menlo', image=ICON)
    add_line('---')

    # Output the system memory statistics.
    add_line(F"{'Memory'.ljust(10)}{'Usage'.ljust(10)}Name", font='Menlo')
    add_memory_details('Real', real, total)
    add_memory_details('Wired', wired, total)
    add_memory_details('Active', active, total)
    add_memory_details('Inactive', inactive, total)
    add_memory_details('Free', free, total)
    add_line('---')

    # Get top 10 processes
    add_line(F"{'Memory'.ljust(10)}{'PID'.ljust(10)}Process", font='Menlo')
    i = 0
    while i < 10:
        mem = F"{str(round(int(ps_data[i]['rss'])/1024))} MB"
        pid = ps_data[i]['pid']
        proc = ps_data[i]['comm']
        i += 1
        add_line(F"{mem.ljust(10)}{pid.ljust(10)}{proc.ljust(10)}",
                 color=WHITE,
                 font='Menlo')


if __name__ == '__main__':
    main()
