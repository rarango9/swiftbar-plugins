#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# == METADATA =================================================================
#
# <bitbar.title>GPU Manager</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the active GPU and allows selecting integrated, dedicated or automatic switching.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/images/gpu-toggle.png</bitbar.image>
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
# # == PREPARATIONS =============================================================
#
# Add the following line to your sudoers file with `sudo visudo`.
#
# %admin  ALL = (ALL) NOPASSWD: /usr/bin/pmset
#
# =============================================================================

from json import loads
from os import environ
from subprocess import check_output
from sys import argv
from time import sleep


ICON_DEDICATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRcECyMMGS2jAAABW0lEQVRIx+2WwUoCURSGv3tTdGjEECxbRLSIo
KCN+yioXQ8RBeED9BTRI5T0CIHLFkVtBAlp0yYioiBTCEPFiZw5bWbGMAeMcRPMuZsD5/Dd//z3LK46
ZJNFTMJFmweuUVCZX5pOhYS1uK/nn9TLfuYgMaNDwhw+3+pHql2fzIYkudFpKFvCquqrUyJjYgHjkhX
BIlgEi2AR7B/CLGtcKMvSzWJvLLie1SyqM3N1Y3YhqUKqktfH24uY2c6UkqF1JclgEqBIIM4WWZyBgq
bBOV9/GkSQtFRkWFQkHfQJ8FdjD6FMB0EQADvwJhu3q0MZYdcvxLzkGHAy5NzBhRTGUJTBCi2vy6nxf
kLRLfnDl7BTa6dT68pzSZNmYqiuD89J0c3Lq51Ya3tQmUJrZZD4YXknYMx43yRlaN1/DD8T4Ca3PGcw
enS5e87X+L0SBYQqXdfa0U6XKkLBZ3wDHoGTxuTPT6oAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDk
tMjNUMDQ6MTE6MzUrMDA6MDAKQU32AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTA5LTIzVDA0OjExOj
M1KzAwOjAwexz1SgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CY
II=
""".replace('\n', '')

ICON_INTEGRATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRcECSpH8/eFAAACa0lEQVRIx+1WPWhTURT+bt7La34a05DiUKSK0
NRKOxiH4lqbQTCLg4tULIjgWKLSwbGDIigo/oCTTiqIQ2g7KFQXS5e0lEqkaTRRm6YxaRNekiZ5L+84
JDFpepc845bvDA8O53znO/fed+4F2o9BhPEaEVCLFsErfMdAlUUEAAFfkUBcYg4YWhPBtPiutbQOK/I
AGADcx0Ukjh+b6T5tZK2RKSQHored4Te4WXPdArD9UCM90CjxCPABQKWtAq5I4mCLomqNwuCa6CrUyV
SoTNO9eRorQ62T/TtYO8nQIeuQdcj+F5m+CbQvU6x+CSn8rk6S1iAgCWogk7GjwAerTmX5pPJX3HOE8
Y6RQAadJoTYBl5UlPlxFbZr5NU9bAWH3/lsBgC7h3GU+kfem126NwB760GP8cdcZe03p8q6bqYayrQ1
RQDYIpTD7nmrm1exLBuSjSeGoPUKNl5kLhA4Z0yA8HNSVXn1lGz0crGPjtSt1BedULJcbermJAHzDnm
BLz676LcRMhJ1VawgbeGtLfuZHy0vzDnEIa9plCecUPh4Xt4YOXoXZhAAJuzlpy+sJj9ZzvB+FtPoSS
/SS/xKSj7iIcR99UeDRts3CN88Sp6fkVkySNylB5RQbOWBZDlbV8FgHnsqxVZKIX6G0Y3MMr/OzhPCl
+FiotFXTASHCanH/Iz0shi7TtOWoeanVFnLzXajZ0DcRbruFemQS13LzdrHBKGpD8oFf91hCl6axnv6
m8hKtJY6pezYnLbaRKh0mpR75VXjCafUFB+lD+lLBVGEvaDFD66ABAaSSd5/aAmAqLAD8QQ7TGgr/gC
KzFGrJfvWMgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yM1QwNDowOTo0MiswMDowMBd65VUAAA
AldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjNUMDQ6MDk6NDIrMDA6MDBmJ13pAAAAGXRFWHRTb2Z0d
2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def main():
    # Handle changing the GPU mode when selecting an option from the menubar.
    if len(argv) == 2:
        check_output(['sudo', 'pmset', '-a', 'gpuswitch', sys.argv[1]])
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
        add_line('🄸' if gpu_switch == '0' else '🄰',
                 image=ICON_INTEGRATED,
                 font='Menlo')
    elif gpu['sppci_bus'] == 'spdisplays_pcie_device':
        add_line('🄳' if gpu_switch == '1' else '🄰',
                 image=ICON_DEDICATED,
                 font='Menlo')

    # Get the GPU model and memory.
    model = gpu['sppci_model']
    memory = gpu.get('_spdisplays_vram', gpu.get('spdisplays_vram', ''))

    # Build the submenu.
    add_line('---')
    add_line(F"{model} ({memory})", color='#ffcc00')
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
