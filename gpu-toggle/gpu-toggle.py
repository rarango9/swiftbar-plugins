#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>GPU Toggle</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the active GPU and allows selecting integrated, dedicated or automatic switching.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/gpu-toggle/screenshot.png</bitbar.image>
# <bitbar.dependencies>python3,pmset,system_profiler</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugins/gpu-toggle/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# <swiftbar.environment>[SB_GRR_ACCESS_TOKEN:, SB_GRR_GITHUB_LOGIN:, SB_GRR_GITHUB_HOSTNAME:github.com]</swiftbar.environment>
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


COLOR = {
    "gray": "#737373",
    "green": "#58f158",
    "red": "#ff3434",
    "white": "#ffffff",
    "yellow": "#ffd735"
}

ICON_DEDICATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0ROSua4nAfAAAClklEQVRIx62WQW7iQBBFv4KF7UijiVggseQWn
IHDsMkaKQucINiw4g6Edc7CCSJlkkAyYwlMu7v+LNo0JqSJo1C7RtRTubq6/gcOgiBYY19PlvEaGxgY
qFimMt3GGhoZNniL9YR91gjiRFyCYMAeUyo9eA3XMFCRJFRUkmwjjQ3eQj2gYsoeA+LSD2uCYJcpSVL
p5E9dhXLLnCSZy902fK3rhIokmbJLNP2wBgTS4pwscEMZFakWN9JDd56blqDhh12BEJgm74sEQ8Ny7M
/3pikgrk51bbXDzSgliHw4zSzq6RgQoYHf+OVwAoFpc7H/PI45LjpHkgvdNhCHukIDTXsVBEEIiEcAs
MMQScLMoYYMGXLocJm9WQ0AeCmyCQIEA+malsUVqFuXmHPIiCAYlXC53FmcRZkWuwwIsMYeU5nbLmgf
yoMT2+E5U/ZYA/t2ruTeNH1VuXYc4cz+7lP2oSe7yZGZbkvyOcqDS3SbMzeVE7zHelDghIuDtkcE0XG
wzjEu46IYGqUHqxgZ3kP3ROirylvdrqpkGa6BLTZY1vWwNOsO9XAEe/gMZ/Twub5GVsxVKCMH81blrc
7IaBtqaHiHoeOFdbyDAhWfusHK1eWSbGPI1DVfOGZYBeVwIcduBSiZXlTKrBpn/cziCamzXMA5R+Mih
8I/irj/BrjGDSJ4hxZAhBtcI9j9KvKXCjmseJ3rOb2d7aEv49IK4sx8ewWZwxW0W45WvH64HO3aZrG2
zQ/XNhiwEJSnbwuK1VlxguKkzurgd6VuVZY64BJNNJzQv1QW4ccioyTCh/FSyR5IYQ8ecSKqGxf52rg
0rDpXslTylaX6aPaej8zesmT25LTZO7Shy5/Z0LJBXsVrZJ8a5HevQf4PDyANh2dMXQ8AAAAldEVYdG
RhdGU6Y3JlYXRlADIwMjEtMDktMjlUMTc6NTc6NDMrMDA6MDAK5UWEAAAAJXRFWHRkYXRlOm1vZGlme
QAyMDIxLTA5LTI5VDE3OjU3OjQzKzAwOjAwe7j9OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBl
Lm9yZ5vuPBoAAAAASUVORK5CYII=
""".replace('\n', '')

ICON_DEDICATED_AUTO = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0ROQ7R5qRYAAACfElEQVRIx62WQW7iQBBFvwaE7UijsZBiiSXX4
TDcgB1OLNiw4gwBDsQJImWSQCJZArvprj+LNh2T2A5M6F0v+smu+lX/AyeHINjiSM82wQ57GBioQOYy
zwMNjQx7vAV6xhFbBNFwbkCwzSFTKj1+9XYwUL7EVFQS577GHm+eHlMx5ZBt4qYeFoHggClJUun4b0d
5cscDSfIg97n32tExFUky5YCI6mFdCKTHFVngEpkUTy1uohN3X5meoFsPC0EITMRl8cDQsHw+7ksTCY
iwqWrbI25BKUHk021hUU9fAT66+IPfDicQmD7XH7/HKadF5UhyrfsG4lAhuohsKwiCEBCPAGDF4EvMz
KESevSYOFxmO6sBAC/Fa4IAwbYMTM/iCtSde3hgQp8g6JdwB7m3OIsyPQ7YJsAWh0xlZaugq1Ehw2qc
2AqvmHLIFjiyupKliWq+6pYPfOBtFc589D7lCHp2VI4sdF/iShTJSlys+1w4Vc7wHuhxgROuT8peRlX
jMq4L0Sg93gbI8O65EWEDqhp3/Kp44+2AHHtsOjopab0OVYczOnnu7JAVuvJk4mBNqGqckUnuaWjUia
EOVdeK+9zXgAoaOngJLs4DyNwVXzilRzD8BmVxIUGPU7cClMx/4Zrnqr9ZjJC6AFffgKtKI8Mer1cR7
R7WvK41Tm9XG/RNUFpBXJiLV5A5XUHH5WjN64fL0a5tFmvb/HBtg20WhvJ0saFYnxVnKM7qnv7L6rZl
qwNuEKHrjP7lbBN+/GrCp+flrHggRTx4bBr684OLfB9cutadz4pU8l2k+hz2nr+EvU0p7Elz2DuNoZu
fxdByQN4GO2SVAfm9NiD/A210XSnXEWTHAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTA5LTI5VDE3Oj
U3OjE0KzAwOjAwh6J1bgAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wOS0yOVQxNzo1NzoxNCswMDowM
Pb/zdIAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_INTEGRATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0ROgQaHh6FAAABAklEQVRIx63WQQ6DIBAF0J9uxBt5QVsT996kh
xNlfnfUVsAZhJ2JvnwQhgGKIyDA97LIsvY7dtwYAQHeyUhPL+PqdoSb1JMbSXKT1+oq0/1Rd7gEdeBM
kz1RQqlMd6I2zpy/TwYuQU3s2HEyc0nKEQSdkQvYc5SVy1MAbFyZMnF5aojvDDruOpU6XZ56n7B3mdO
nUqS7Xqv/kV87+F5GfapCunHtIQt9PM4zOw0VuY5zLAFelofqS+1oOs3Q8gfk60TF1ihx5k1b5kyprj
nzQdelM1a00Ko4lrnKW6DZhZLl6q66DFd7CSe5+vYgyf1Q5i6tYUuV4O5QB65FGxo5dYP8AZ+3cx/RH
XzpAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTA5LTI5VDE3OjU4OjA0KzAwOjAwugMufQAAACV0RVh0
ZGF0ZTptb2RpZnkAMjAyMS0wOS0yOVQxNzo1ODowNCswMDowMMtelsEAAAAZdEVYdFNvZnR3YXJlAHd
3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_INTEGRATED_AUTO = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0ROhAAxMr4AAABAUlEQVRIx63Wva7DIAwFYKtLyJalj5x7K2XPM
/QVQ2KfDpXSPwI+BG8sn0Dgg0WypaISe5ttXvpNNjlRKiox2IiIaOMSNtGT1B9WAMBq/0uo3N0XdYZL
UG8cddgfymCVu/uhVkyYXiuCS1A3dOhwo7kkFSAQBJJT2dLUgIHkDqkr7rjjSnBZCgDBFSk/56J8nJs
qcxRV4kgqy0nsbaSoI25cerEZcW/nCR0EQ4F6cgMEHaY9AqLNFyZNitX0mNryApTlSi+N4Dw94OS83e
ngmNzQVhFU5Dgqy/GxneV46pCr++oOuNpPOMnVjwdJ7oOip7SGI1WCO0O9cS3G0J1zD8gPrAaoyNIKN
GUAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDktMjlUMTc6NTg6MTYrMDA6MDDhNj/KAAAAJXRFWHRk
YXRlOm1vZGlmeQAyMDIxLTA5LTI5VDE3OjU4OjE2KzAwOjAwkGuHdgAAABl0RVh0U29mdHdhcmUAd3d
3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def main():
    # Handle changing the GPU mode when selecting an option from the menubar.
    if len(argv) == 2:
        check_output(['sudo', 'pmset', '-a', 'gpuswitch', argv[1]])
        sleep(2)

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
        if gpu_switch == '0':
            add_line('', image=ICON_INTEGRATED)
        else:
            add_line('', image=ICON_INTEGRATED_AUTO)
    elif gpu['sppci_bus'] == 'spdisplays_pcie_device':
        if gpu_switch == '1':
            add_line('', image=ICON_DEDICATED)
        else:
            add_line('', image=ICON_DEDICATED_AUTO)

    # Get the GPU model and memory.
    model = gpu['sppci_model']
    memory = gpu.get('_spdisplays_vram', gpu.get('spdisplays_vram', ''))

    # Build the submenu.
    add_line('---')
    add_line(F"{model} ({memory})", color=COLOR['yellow'])
    add_line('---')

    # Build the GPU toggle buttons.
    gpu_switch_opts = {
        '0': 'Integrated GPU',
        '1': 'Discrete GPU',
        '2': 'Automatic Switching'
    }
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
