#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>GPU Toggle</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the active GPU and allows selecting integrated, dedicated or automatic switching.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-gpu-toggle/screenshot.png</bitbar.image>
# <bitbar.dependencies>python3,pmset,system_profiler</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-gpu-toggle/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
#
# ❱❱ PREPARATIONS ❰❰
# Add the following line to your sudoers file with `sudo visudo`.
#
# %admin  ALL = (ALL) NOPASSWD: /usr/bin/pmset
# =============================================================================

from json import loads
from os import environ
from subprocess import check_output
from sys import argv
from time import sleep


# Hex color code.
YELLOW = '#ffd735'

ICON_DEDICATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgsEBChBPHoTAAACAUlEQVRIx63WzW3jMBAF4IcFBBdAwCnDdyMqZ
lWCAR8Myw0FgZtwBT6mgmS115CWxJl5Odhe/+lvE1EnXT6Q4MzwAf+WQFBPLNOFdyUEB9SoEv1tewrF
9paVSYUAQwnvdGFZNRFENCyB4JBYzkDTJXFAQJHoip88r09ZfSQBAYQuaQyWhyQ+cidqw5IkbU0EFIm
sj/8sWJAkS1n/SQIIy0mSlW0eOIGgvFAvMq3x90JtdaYzbs/cR1JDpnw5/t9x95RO4zX1yieDgU98vX
AReuaud/dIyR1FnL5+rp+KUChiLydAPbG8e1fRxTSm0bH7sHk1gWUMbZSB0Lnt6Oltp/NOLlgGXdDaK
Xm2t3OZ2Zs8d3CmC3inS1tLww3eUl2cTG2tS+9QgiDqAVQ7V4MgSkBwQBhItXMeAYL/pLo5VNc9OIBq
496TCqgSXd3WVR/Vwq3KBJadhsyJ0nk/deR0btdd8WkZbE+S3B4bJzrbDaFI0nbRnZpsS5K2B4VkoTM
DoYgp/VCMXlIFYdAZC5LyC2OuUY95fwHykwu4LY0hVdZRGvWYRTtqOxnCKI3uYRh3BHmnS8t/Nhx1yo
0uvRt3bI/6oPQ9dYboJJU0Out/6kZ9hEeNB98LLtJMfS9SWVukagh7eV/Y46ZxV20xNDTG0PchMfQxI
BsOqFF3BuT6LiB/ARINDBaffNqDAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTEwLTExVDA0OjA0OjQw
KzAwOjAwGgWnsAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0xMC0xMVQwNDowNDo0MCswMDowMGtYHww
AAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_INTEGRATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgsEAQQOk+K1AAABvElEQVRIx63WQY6jMBAF0K+RrBwAiT5GzjQcI
RKLKORCrVbuklN0D7MNBpyq+rNI6DABAsy4WHnhJyzb5Q98l0AQNpbprkoaCGoEtE5/2plCsbNljWvh
YWhQJbqzrN0IrhgpgaB2VtDTNCdqeJRO97ywq4vsv5yHB6E5jd4K765D7k4d2ZCkHQiP0snhNmbJkiT
ZyOGX8yCsIEm2dhxwAkHzoN4lDfj9oE661S1PHfflAiTl+238xD1Tml771AffDAa+8ePBXaEd1/+7IS
VPFHH/5rkllEAWcAKEjRVz1G0FM1zRbmAZ/Ty1gPOWQXe0JdQsZ7pDlWhuBxns4JCa5iS1g+ZVggYEE
RZRU1wAQTSAoIZfTE1xFTwEq6lXHNr+HVxEjXOfrgVap/u11Ci3bxwsuzeZVdQId7EMdr51hrXUX9yJ
JO0MCslSt7aa6jiDblmSlB+r57+qqMuMugFRj0aIeWijXieDj3LRKxjitqAq0dyK/2uOmvKoeZXEbdt
RH5SoT13URzhqPPi34CLj1Bg3H6lsKlJ1XC/sFXNhj8fJsNfjvmOoH42hn0tiaMc9ArKhRkB4GZDDU0
D+AzEE0RZtnHgiAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTEwLTExVDA0OjAxOjA0KzAwOjAwjClGH
QAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0xMC0xMVQwNDowMTowNCswMDowMP10/qEAAAAZdEVYdFNv
ZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def main():
    # Handle changing the GPU mode when selecting an option from the menubar.
    if len(argv) == 2:
        check_output(['sudo', 'pmset', '-a', 'gpuswitch', argv[1]])
        sleep(1)

    # Get GPU mode of integrated, dedicated or automatic switching.
    gpu_switch = [s for s in check_output(
        ['pmset', '-g', 'live']
    ).decode().splitlines() if 'gpuswitch' in s][0][-1]

    # Get data for the active gpu.
    displays = loads(check_output(
        ['system_profiler', 'SPDisplaysDataType', '-json']
    ))['SPDisplaysDataType']
    gpu = [d for d in displays if 'spdisplays_ndrvs' in d][0]

    # Create the menubar icon and indicator.
    if gpu['sppci_bus'] == 'spdisplays_builtin':
        add_line('', image=ICON_INTEGRATED)
    elif gpu['sppci_bus'] == 'spdisplays_pcie_device':
        add_line('', image=ICON_DEDICATED)
    add_line('---')

    # Get the GPU model and memory.
    model = gpu['sppci_model']
    memory = gpu.get('_spdisplays_vram', gpu.get('spdisplays_vram', ''))

    # Build the submenu.
    add_line(F"{model} ({memory})", color=YELLOW)
    add_line('---')

    # Build the GPU toggle buttons.
    gpu_switch_opts = {'0': 'Integrated GPU',
                       '1': 'Discrete GPU',
                       '2': 'Automatic Switching'}
    for key, name in gpu_switch_opts.items():
        if gpu_switch == key:
            add_line(name)
        else:
            add_line(name,
                     bash=F"\'{environ['SWIFTBAR_PLUGIN_PATH']}\'",
                     param1=key,
                     terminal='false',
                     refresh='true')


if __name__ == '__main__':
    main()
