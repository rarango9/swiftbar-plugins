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
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgoDFycNn1fwAAAEJ0lEQVRIx42WXYiVVRSGn3PmjJPNIDY62ghWS
kRRyigkSKAEhglChEQJlkhXiuhFjZSRgRcJEsyV0EXeVTeaKXmVXWQKEWRgZOHPGGoY45z5PXPmfD97
rbeL73M683/W3eHb+znvu/Zaa+8CDUdECzHNFKk1L1jBc8Uu1rCazsJjtFEEKDUGiilTAtSiZ7T5kc2
FtayglULjUvKoMUCCCI/7bj+nPtWHqaqyatmPedgDtBMoEa9sfquwq/BCZgcY1t/8yV/06j6jxeO8Mo
+iqwRiRLLEDvi1OjWX/KBtSNpHikI4Qt9kH2ZFDSMCA8Ww1S/K6535EWEkRIgxHG/St3PCKtzBSDrsm
IZzxK/eoyFJ8itpR1qXUeHHJcl7Z0l5DZF2+YVczD07nHaOLfDzkqTEd/jEWuGEZb7H99n6GVBj1BC2
3W9IkoKfDutEivBdcknmO/93dPZh3vDpqCrjfF+w3XogSd5v78VtTo2EQLrYTuiyd/uiGTZOj1GqXCz
43ixTfi1syzRdB4SolKw1UzJvVBhD2Dt50oPtF2NU86/9GDWMmGR+1DB3ELY9MyhJfitsEX2MAQ8QAS
cinh91FWGkXQ/TnuNu20Ynzk2GVl9eKaak88ECgaQjKwa/Zvv9Vo47KlLAsFV+Vtftk1pLzNBcqDIx5
aIdkyT1h20ibNFtyf8Jm5yRrJ4OSpIie0NzH4AQYauGJQV7X1QRvtGPpptEQn8GezdrK/85XRYmjmVa
1EhJlvhFSfLTUVtMlTKOMCIMACMs918y594tynw+m0lhB+SS7oV1jgFjxCSM0F+n3d5UlHVheNZmPtV
AQrQyGzJ2WIxzc8YaTEkWej5s/ES5OM749GVVhHVnkyHtTGctScMJL6ksSRq0l50wdUmEYZ36XZK8p9
YiAqJvBthtYgYL3pNr+y5qjRmbfo6+WyZJGvLzvitdrDzpUyPFCE8rK+vY3p5WIilpi5+rH6R2olKqz
WJ1KKs3y4fkipRJK42wZsqNc9labRZYRCBt95/y//1YjPJhvU3fn18TR/yKEpl3a45mFsJeU1WS/G5Y
a/UHFjf7KUnyAyLt8B2+0xf5HLAaCVGLf51rO1kpRdyfsPmUbkgasg1GijP/6AsY4UX9K0katVedlAo
RgG1TRfLf0vYGRl4OqyH801zbBXsifTSbx/gHcsm/HC1GDcLI7oMn/Q9JUqrr/qMfSpYK/CtJ8o/UyF
yfiEsI25tXZ6bwTNJZYjXg9DJTp80azwOU6l9Bhdeb7qI7kqq2yXFqiFMNGk0W+g+TqlPeh0Ykla1Le
FODlxjg+JKsn+ujRBvQWjxOpVDUTf+s+KARmEGtaXDye0yDTJG6pzFlFYQfmrzXvpgK29cYLCKQLPUz
dTsvpKsmwbzX1jf0iiDr0aTTerxP8gE/ma4S/wGUWShxSLXIyQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjA
yMS0xMC0xMFQwMzoyMzozOCswMDowMEqE1b8AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMTAtMTBUMD
M6MjM6MzgrMDA6MDA72W0DAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJR
U5ErkJggg==
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
