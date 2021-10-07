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
UAABYlAUlSJPAAAAAHdElNRQflCgQTLBacCmyxAAAC5klEQVRIx62WzUojaRiFn/wOMzDDBLII0oMLi
TZ4GdMwcwmSTece0u68JUHBTUsnYOgbkdmKTE9XyvjVl3NmUVVJqYnSmjeLokjVw1vf+3NOjQcRgCZQ
w9RZHyquEWg/+OfBGymgOrt0oEYGQMJ3AoFvfC8QNWrQYVf1/I0NcYfR0Ne+1HtjFpiIuW/MG2bBggX
G+L0vfa2hudsMi4Smzm3bX3OcyHoa+dSnGsWeStRX29Z5aMbNsBQTj3xr2x6ra9TX2GWM1Tfqemzbuo
1Hfu4zZ8z4i/hRt7ZvdKA9T22nOtOZU9tT7enAN7Zu4/ADCbOn+dwRSZkVOIgDTzTSoa9spz4O7dD2s
VPbV4tDjTyJA5iRAAkzInd5joGACU2TkBQ4E1raL1Cf3BDCDX8qcPuh5QJVPN00gQCBeV1DncejDyQk
ZBij/gplit8Sp74x8/JYjnSu4bweQGjX1/kpQFKipk9QVdw0x82gPOFr7QqEOr4s6jN4ihLa0YlOtKM
1uDhQXvvP8fcIqnbOJLSeZPXOF7btC797nF1oaVLtSpaNOPaNRtVjf4Bah7ta7GvkG3/JUXd53xujrg
6WzbAOtR53qIPYNWY5C/nEae8F1Fqc9oRZrNp2gdh4Vi/hpuoLl6iEBbHncbWCG1EFrlpZjbNeLAfrP
4xG+eDkWWnnGZRtX2inyO7Yqa2Ri21HYN7wqa2z0M5rqxO/EDrJF1Ro68z26X0je7xptxBb/cyESNbT
dgoA3l5rvLVpXW3at46TVuO0hUEfl0r2xhXkxyvobcuxEMZLdbSNte3V2g7cLwVl9gpB+bsQlPt6gIz
sVVKXrJO6lQinFRHWsyKsSRywxKUrEX69PfhznT2owirG5UvsCvW9NC76MeOyzlLFpaXKfsxSLc3e59
Ls5fYuN3tZYf82m71a9SaliertP/St8S9EWuSd9xMwp8avQKQBuMNv2T81RX7ZBCsNsmgw5+cN+YsaZ
p1B/h+QyDs5njaC0gAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0xMC0wNFQxOTo0NDoyMiswMDowMNzw
W8EAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMTAtMDRUMTk6NDQ6MjIrMDA6MDCtreN9AAAAGXRFWHR
Tb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_INTEGRATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgQTLCkqbEGMAAACyElEQVRIx62W3WrjVhSFP/+WFlpq8IVvSi6Ck
4E8RgfaRwi+qd/Bk8cKJJcTxoaYeZHQ2xA6HVl2jo7X6oVkWUmsND/euhBC0sc5++y912rwIALQBhqY
JrtDxT0C3QdvHvyRAmpyQA8aZAAkfCcQ+Mb3AtGgAT0O1Mz/qIklRmPf+EofjFljIua+tWqZNWvWGOM
PvvKNxmZZD4uEti5t219znMgGmvjc55rEgTaor7aty9CO9bAUE099Z9ueqm801NSbmGpo1PfUtnUXT/
3cNhcs+IP4l+5s3+pYh57bTnWhC6e25zrUsW9t3cXxRxIWT9ezJJKyKHAQR55pohNf2059Frqh6zOnt
q/XJ5p4FkewIAESFkSW+RoDARPaJiEpcCZ0dFSgPrklhFv+VOCOQscFqvi6bQIBAqumxrqMpx9JSMgw
RsMtyhRXidPQmNUmLae61HjVDCB04Js8C5BsUPMqCniIm+e4BWwyfKMDgVDPV8X5jOpQdbg4Un72n+O
vEVStnFno1KF24UJHs2pVUhbi1LeaVNP+GPUEd70+0sS3/pKjlnndG6O+jstiqEHtwJ3oOPaNKXsh7z
gd/j/qKU6Hwqy3r9eI53L1LG6uobbfJ6yJA09finqM0zQbxE1j/YvRJG+cl6EquDOntiYuph2BVcvnt
i5CVy9E5TgRurqwfX7fyqB2Nr819rrNhEg20H4OIN/9nkrjvUXratG+t520bac9NPp0o2TvHEF+PILe
NxwLYbxST/sY296O7cB9KSiLNwjKn4Wg3DcDZGRvkrpkl9RtRThlK8J6VoQ1iyNKXLoV4Wq8zh78vss
eVGEV4/Il9oWGLo2LXmdcdlmqWFqq7HWWqjR7nzdmL7d3udnLCvtXb/Ya1YeUNmp2f9O31j8Q6ZBX3g
/AigY/A5EW4B6/ZH83FPmpDrYxyKLFih9r1i8amF0G+T8OddpxF07nmgAAACV0RVh0ZGF0ZTpjcmVhd
GUAMjAyMS0xMC0wNFQxOTo0NDo0MSswMDowMCt3SNsAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMTAt
MDRUMTk6NDQ6NDErMDA6MDBaKvBnAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgA
AAABJRU5ErkJggg==
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
