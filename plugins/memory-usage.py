#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# == METADATA =================================================================
#
# <bitbar.title>Memory Usage</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Shows the current system memmory usage and top 10 processes.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/images/memory-usage.png</bitbar.image>
# <bitbar.dependencies></bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugins/</bitbar.abouturl>
#
# == SWIFTBAR OPTIONAL METADATA FLAGS =========================================
#
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
#
# =============================================================================

from subprocess import check_output


ICON_DANGER = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAB1FBMVEUAAADMAADAAADXAACvAADNAA
ArAAD/AAAaAAAcAADFAABpAADJAABgAADOAADSAABWAABhAABXAACNAAB/AACrAACxAAC6AACEAAC9A
ACBAACOAACMAAC/AADIAACAAABjAAChAACUAAC4AACzAAB9AACYAAC5AACxAAB5AACZAAB9AACyAACU
AACpAACoAAAAAACiAACkAAAAAACkAACjAACkAADRAACbAAClAADSAADNAACYAACXAAClAACbAAClAAD
DAADUAADBAABjAADIAADUAAC+AABcAADDAADMAADVAAC/AABeAADRAADVAAC9AABXAADMAADVAADAAA
BfAADRAADWAABYAADFAADMAAC3AABWAADJAADNAAC1AABOAAB9AACkAACpAACqAACfAACRAACIAACJA
ACsAACfAACRAACHAACKAAB+AACbAADLAADQAADPAADQAADQAADQAADRAACeAACeAADQAADRAADPAADA
AACZAACeAADPAAAAAAAAAADPAACLAAC7AAC8AACdAACcAABiAAC/AACiAADPAACgAAC4AAB+AACJAAC
0AACyAAB6AACxAAB2AACVAADTAADUAADOAADQAADVAAAAAABU/VFqAAAAlnRSTlMAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAROLoUEjk5kxIUelDlKUCmp8BoJpq/Hpw/f51dW97ainq8zYt7
fAxKCbo8jMq7O8vJ+nyMyvsLyTl7jAo6OssCysuLTuAhEAsPYKDPgtO6Ozr6+fq51xb/fr3jURGXwUE
YnS+uqKfMfB1/prhUEfk5kzkR0NZcaLnAAAAAWJLR0QAiAUdSAAAAAlwSFlzAAAWJQAAFiUBSVIk8AA
AAAd0SU1FB+UJFw4kMeAr4VAAAAHRSURBVDjLY2CAAEYlZRVVJmY1dQ1NFhZNDXUtZiZtHWVdVgYUwM
auN226vgG74fTpRgzGJtOnm7Ib6E+fpsfOhqKMg93MfIYFO7ullbUNO7uttZUdO7v9DHMHdg4UZZxcj
k7OLtw8rm7uHry8Hu5urjzcLs5OnlycqLbyeXn7+PLy+/kHBAoIBAb4+/Hz+vp4e/ExoCkLCg4JFeQP
Cw+IEBKKCAgP4xcMDQkOQlYmLCIqJh4ZFR0jIRkbF58gJZUQHxcrKRETHRUpLiYqIg1VJpOYlJySmpa
ekZmSlZ2Tm5mZm5OdlZKZkZ6WmpKclCcDVSabX1BYVFxSUlpUVFpSBiLLIOyS4qLCgnxZqDK58pnTp0
+fhQUAhWeWy8GUVVROn15VjQVUTZ9eWYGirKa2DgPU1mAoq5czbmhEAQ3GcvUYyprYm1taUUBLM3sTF
mVt01DdP60Nq7L2adNRwLT2UWXEKCMyeImKLCKjnsiERESyJC6RE5llZPKIyoDSeLOzPCw7E1k4EF/U
oBRcCh2d0ILLEa3gAheD9uBi0JadvavbyhJcDJqhFYPwQnUapFCd1oO1UGVg1e1V6WMS758wcRKwiJ4
4eYoik6pK71RYEQ0A17HAE/rdTP8AAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDktMjNUMTQ6MzY6ND
krMDA6MDDgm21VAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTA5LTIzVDE0OjM2OjQ5KzAwOjAwkcbV6
QAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=
""".replace('\n', '')

ICON_NORMAL = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRcOIxma399tAAADwElEQVRIx+2WS2yUVRTHf/fer53Ogz4IDSghE
CIGB6UuiCEsjIbWAEGjCxLduJOYJiZE0sQEl+6UBUpYsNGF+IIGwwLUDpDwqASKCYWZspCKgB1Im76Y
N/fe42KKzJCZTmVp/C+++zy/77vnnHvvB1XKcaz7xq2RuwfeTCOc2DJ6Jzn2+farXGXf9uTY6J2ftgh
pDrw1cu/GrWOb88yjDQiX9nsRuXgILZw9KCIy+CWgzn/lReTcQQF98ZCIl6H9woYqe13ZGAdKKe+KzC
TFg0k5X5DplCAykyyK9yYJ4mdSRbwrpcoWjxRUNgyTrDltJifCicQ5drPupJm+Z35OnARsomv2aRc/d
Z+9FAZe+Ghpfs2pSUx92ChRvMN7KTlHBHGIl6IvAngvSMQpsjjnBR/1mtH6MAAUqvxQiCp3VI6WRx7O
oxbsByZ5iRB3iTmxOZt1GxmjzQU2Jxn3MnDG5WzeWTdDnAsuZ3M27zIkKXKJxeyg4rXfMRXtWtVklNx
vnerJBjrx3IRX99unejIqGFg7CdcX256YdAwsmtYyssR3R23HwKJZUQ/clZsd2bcrYX+RfGPTweYAAa
xCjCgFgivXQYlyAgYlD+sBoEp2cOe6Y8srlxkjaG1e2sSTKGiNVftMQPBosA+cUwtACMYETYBHpF40J
764cqJZN4aVfNfWZR/WjOYjLR7emGhXlL1XTwo7LeHldVKjQqaNb3dv2qZtfZYPBo+3fVYyjWFA5/oV
r87nN6HzTq3+2t5xDV1Wc8YCXL1w/Q/778NMQ7uaM2rugPHh26fn307jwwuDuRne2cu+Rht9K2HXEDa
5/kr3qQV48oLvWr+sEWzJB6/0LvRwrPNlClQ5GEFT8O9Ob41S1bAMdrZ0jye6UOxsphp2lqmTsc1Pdt
WN3pyqhhl0tiUZIsqqZ8LvpcOfHild6+bZtcHO2+aT77PX4MzzH7+/wtlvZq4nuPBiX+9T+fzXmd+zF
NH/JOscbMdcs4A34SASRE2Kd/EmCCImZn4DYiYShJU1UVJETSSIBMrEaJk/mkj53psroDrhZG6Eh0Vd
2GqyOBPWWjWbFnKIaVVahXRAE14bhcoZRZSC0QqdMYbVj/0HVWglwvleawsysEcQBndZl/fH+wThbF/
JW/frLkH4ZU9BrB3sFVY+liUV6gSa49qEaIsrDS6udYtqjyuU0uualNalOCjdHg+hTXO8bFFnmUPkSR
/94/VS6PLhtP+TW/2d27we6h9GyekjHa+Jv9yvSPsfDy/aHCqmjxYYqoL9DYcE2ytqfifSAAAAJXRFW
HRkYXRlOmNyZWF0ZQAyMDIxLTA5LTIzVDE0OjM1OjI1KzAwOjAwCmO1pQAAACV0RVh0ZGF0ZTptb2Rp
ZnkAMjAyMS0wOS0yM1QxNDozNToyNSswMDowMHs+DRkAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2F
wZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_WARNING = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACHFBMVEUAAAD2xQDnuQD/zwDTqQD3xQ
A0KQD//wA0KgAfGQAiGwDtvQB/ZQDywgBzXADtvgD4xgB0XQD8ygBoUwB1XgD9ygBpVACqiACYegDOp
QDVqwDgswCffwDjtQCbfACZegCriACohgCohwDltwDxwQDwwADluACphwCriQCaewB4YADSqADCmwD3
xgCyjgDdsQDXrACWeAC3kgDesgDVqwCSdACRdAC4kwCWeADXrACyjwDLowDKogAAAADDnADGngAAAAD
FngDEnQDKoQDMowDFngD8yQC7lQDGnwD8ygD3xgC2kgD9ygDHnwC7lQDGngDquwD/zADouQB3XwDxwQ
D/zADltwBvWQDrvAD2xQD/zQDmuABxWwD7yQD/zQDjtQBoVAD2xAD/zQByWwD7yQD/zgDjtgBpVADsv
QD1xADcsABnUgDywgD2xQDZrgBdSwCXeQDGngDLowDMowC/mQCuiwCjggClhADOpQC/mQCuiwCiggCm
hQC6lQD0wwD6yAD6yAD6yAD7yQD6yAD5yAC+mAC+mAD6yAD7yQD4xwD5xwDnuQC4kwC+mAD5xwAAAAA
AAAD5xwCnhQDhtADjtQC8lwC8lgCYegBoUwB2XwDmuADqvADGngDDnAD6yADHnwC6lQDBmgDdsQCXeQ
ClhADYrQDWqwCSdQDVqgCOcQCXeADesQCzjwD+ywD/zAD+zAD4xwD6yAD/zQAAAADdq+1oAAAArXRST
lMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAROLoUEjk5kxMSFHp
Q5SlApqfAaCapZRq/Hpw/f51/W97ainq8zYt7fAxKCbo8jMq7O8vJ+kzK+zvLyTl7jAo6OssCysuLTu
AhEAsPYKDPk7o7Ovn5+rrXFv9+vf3jURGXwUEYnS+uqKfCy8x8Clwdf5we5rhUEfk5kzkR1DhQydR47
oAAAABYktHRACIBR1IAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAB3RJTUUH5QkXDiQXMiZkrQAAAehJR
EFUOMtjYIAARj19A0MmZiNjE1MWFjMTY3NmJgtLfStWBhTAxm69dp2NLbvdunX2DA6O69c5sds6r1vr
ws6BooyT3dVtgzs7u4enlzc7u7eXjy87u98GN392ThRlXNwBgUHBPLwhoWHhfHzhYaEhvDzBQYER/Fy
otgpERkXHCArFxsUnCAsnxMfFCgnGREdFCjCgKUtMik4WEU1JTUsXE0tPS00RFUmOTkpEViYuISklnZ
GZlS0jm5Obly8nl5+XmyMrk52VmSEtJSmvAFWmWFBYVFxSWlZeUVxZVV1TUVFTXVVZXFFeVlpSXFRYo
ARVplxbV9/Q0NjU3NLQDCJbmpsamxtAZENDfV2tMlSZSuvGdevWbcICgMIbW1WgylTb2tet6+jswgCd
HevWtbepIivr7unFAD3dGMr6VB36J6CAfgfVPgxlE9knTZ6CAiZPYp+IRdnUtajuXzsVq7Jpa9ehgLX
TRpURo4zI4CUqsoiMeiITEuFkSWQiJ5Bl1KDKlPBmwOnqUGUa8viys6YGaYUDRlEzA1dRg1Jwac2cBS
24ZnOjFlzgYtCPnX0OuBicO89zPjv7AsxiEF6orgUXquvWLmS3tcEsVBkYrRYZLGaSXrJ02XJtluXLV
qzUYVplsHqNLlQaACAYBQFEgcWHAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTA5LTIzVDE0OjM2OjIz
KzAwOjAwgoQ7nAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wOS0yM1QxNDozNjoyMyswMDowMPPZgyA
AAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def fmt(color_code, text):
    if color_code == 33:
        return F"\033[33;1m{text.ljust(10)}\033[0m"
    elif color_code == 36:
        return F"\033[36;1m{text}  \033[0m"
    else:
        return F"{text.ljust(10)}"


def get_ps_data():
    # Get processes info and remove the first and last elements from list
    ps_list = check_output(
        ['ps', '-caxm', '-orss,pid,comm']
    ).decode().splitlines()[1:-1]

    # Convert the ps output line to an list of dicts with parts.
    ps_data = []
    for line in ps_list:
        parts = line.split(' ')
        ps_data.append({
            "rss": parts[0],
            "pid": parts[1],
            "comm": ' '.join(parts[2:])
        })
    return ps_data


def get_mem_total():
    return int(check_output(['sysctl', 'hw.memsize']).decode().split(' ')[1])


def get_rss_total(ps_data):
    rss_total = 0
    for rss in [ps['rss'] for ps in ps_data]:
        try:
            rss_total += float(rss) * 1024
        except:
            pass
    return rss_total


def get_vm_stats():
    vm_stats = {}
    for line in check_output(['vm_stat']).decode().splitlines()[1:]:
        parts = line.split(':')
        vm_stats[parts[0].replace('"', '')] = parts[1].strip()[:-1]
    return vm_stats


def memory_details(key, val, total):

    value = fmt(33, F"{str(round(val))} MB")
    percent = fmt(33, F"{str(round((val/total)*100))}%")
    key = fmt(36, key)
    add_line(F"{value}{percent}{key}", ansi='true', font='Menlo')


def main():
    ps_data = get_ps_data()
    mem_total = get_mem_total()
    rss_total = get_rss_total(ps_data)
    vm_stats = get_vm_stats()

    wired = round(float(vm_stats['Pages wired down'])*4096/1024/1024)
    active = round(float(vm_stats['Pages active'])*4096/1024/1024)
    inactive = round(float(vm_stats['Pages inactive'])*4096/1024/1024)
    free = round(float(vm_stats['Pages free'])*4096/1024/1024)

    real = rss_total/1024/1024
    total = round(mem_total/1024/1024)
    percent = int(round((real/total) * 100))

    if percent >= 90:
        color = '#d40000'
        image = ICON_DANGER
    elif percent >= 70:
        color = '#ffcc00'
        image = ICON_DANGER
    else:
        color = '#ffffff'
        image = ICON_NORMAL

    add_line(str(percent).rjust(2),
             color=color,
             font='Menlo',
             image=image)
    add_line('---')

    # Output the system memory statistics.
    add_line(F"{fmt(0, 'Memory')}{fmt(0, 'Percent')}Name", font='Menlo')
    memory_details('Real', real, total)
    memory_details('Wired', wired, total)
    memory_details('Active', active, total)
    memory_details('Inactive', inactive, total)
    memory_details('Free', free, total)
    add_line('---')

    # Get top 10 processes
    add_line(F"{fmt(0, 'Memory')}{fmt(0, 'PID')}Process", font='Menlo')
    i = 0
    while i < 10:
        mem = F"{str(round(int(ps_data[i]['rss'])/1024))} MB"
        pid = ps_data[i]['pid']
        proc = ps_data[i]['comm']
        i += 1
        add_line(F"{fmt(33, mem)}{fmt(33, pid)}{fmt(36, proc)}",
                 ansi='true',
                 font='Menlo')


if __name__ == '__main__':
    main()
