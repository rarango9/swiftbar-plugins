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
UAABYlAUlSJPAAAAAHdElNRQflCRcOJSZ641XWAAABEklEQVRIx+2WPU7DQBBG3zhrYeIgQ0UVqiiiS
5U0iFNABefgEtwDqvgUiAYugAxSJHoEBEUJspOhII2ztnGk7fDXrOZnn2ZHu9qRIe5kiNzB5PnRIUzV
Hcxzh2pgDayBNbAG9p9hZukSdnftDiZV36YU+KryjZQElORyfiYbXdBWEvdvhK00ADOJtUCTGDMoqyx
vjtfrO0nU7hVtaPeuov7bwdo6r4KlEHKE11mOjoNuESzojk6zp7TFildmlT3+Qk/klgDE3933Cpqz0v
mHpsBCL+R+r6qyDvgcslPeTU/C3zN+41sxK1tqvgrPvjkblb2gU3kg4K+pTVjoVCxnTkMwhLUqgxlZf
uw0VkrGZ02YpR++5E9aHqEmmgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yM1QxNDozNzozOCsw
MDowMKPrBMYAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjNUMTQ6Mzc6MzgrMDA6MDDStrx6AAA
AGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_INTEGRATED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRcOJTCON+CHAAAAvElEQVRIx+3VLQ7CQBBA4TfLiib8BFELkgOA5
DYosJwChSPcAc8h0HUIDBLThAbTdhdRQgDXThPMvgN8mTEzEKqbgGfLBFEgnjNrBAsgQ+lrMJA7KRU2
Xc5WpmhOOdvbs3lhUdwd69aMYgAD4L1XLempAKNSfgpYwAIWsL9jugfwFixAmRWpKZtLrlNmADYHkt3
gYBSX20lym5MjpwWIUz4BRLwByZXMF6md6TP7uLQ42XHU4mT+2h4Wqt8Tm/0vkIJSjFEAAAAldEVYdG
RhdGU6Y3JlYXRlADIwMjEtMDktMjNUMTQ6Mzc6NDgrMDA6MDCpLg3fAAAAJXRFWHRkYXRlOm1vZGlme
QAyMDIxLTA5LTIzVDE0OjM3OjQ4KzAwOjAw2HO1YwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBl
Lm9yZ5vuPBoAAAAASUVORK5CYII=
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
