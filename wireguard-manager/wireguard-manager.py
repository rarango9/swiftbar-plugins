#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Wireguard Manager</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Manages one or more connections to a WireGuard VPN.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-wireguard-manager/image.png</bitbar.image>
# <bitbar.dependencies>python3,wireguard-go,wireguard-tools</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-wireguard-manager/README.md</bitbar.abouturl>
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
# %admin  ALL = (ALL) NOPASSWD: /usr/local/bin/wg, /usr/local/bin/wg-quick
# =============================================================================

from glob import glob
from os import environ
from os.path import exists, join
from subprocess import check_output
from sys import argv
from time import sleep


# Hex color codes.
GREEN = '#58f158'
RED = '#ff3434'
WHITE = '#ffffff'
YELLOW = '#ffd735'

ICON_DISABLED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgUDGBUaswrpAAAEhUlEQVRIx42WW2xUVRSGv7VnptMy01aubQlyK
XQKiEAgohYQQQqWEQyEGI1iNEqilcRoTCTxQUNCJDH64IMxeOHB8ISpkqKtiQiIEaUhaTHcsaAFEYvD
pZfpzJyzlw9zHOgMzMx+Onvtvf69/rX+vfYR8oxHKMEgE1nMTJnFHM7oF9rqu/oXY2i/zX7fnaGi+PB
jsAkJUi8PMImINMmDerL8oo96IkQ4XSxYBDUS5Q1ZKCGZxMOUAX7KpAGHCp3IZdxpnLnFw5+P5nU7qp
swG4cZ+5nJJ8RF2dr/XplSLFgFHNctspyxtxinEde9EuMfTpX5SRUNhjBdnqMsM7/EYa7hyhCVuldaJ
Wu7Px+Sr1be4X4sStrvl9RTpQmDkixJpQLAN8UXgAG+ZyfdspARAEwwCdtpUynE9eVAFQJzJW4dM1W7
Jcx4IChLZYp2masWyYHKA7aYUgQwKX4z+7VdqrkHwTBblujvwW6HyDBZ5AFbhQ8f1kitLGIJc/DTKjH
mEQSqZYXbEzqWpD5LtHI7qCjgx71XXqGJGgLAEN3sZoBmxgPwN09ywBYuQBPC3VxfL5/RSKW3w89YFl
Oqu6SeciDMGPs1znCiJhcshOHCKvmI2pylBmnSnQx53zOyaeWANTKErZEtGdVfooOTJL3ZAirpBKBSa
guCfYAgjzMPAJdPtVGX61J9iQtekmfR42U7R/A5hs3gNyu8wrTZ16UPuOHb4bqynSCQ8gJw6cv2zYlM
kDCTAFC+NH2guDjQ5snqOFMAiOk5zfL154LhowQAh15waAdWwxCDwFFNyiwAjuq5gjQVkpImEKBOMDy
WXqhhAmfZJ09QAigtJl5aiKZlTx9d3mSjvS8AKEmjazjCPtZTA8Cv2qIMZPnmiDbCdLCsJQCMk5VarZ
dI+hpokKk8ykgAruirpstPayGa/YRhn2nhGQCqdLZskrnMoCJz9Xr1tXD7jeFN9vaR/UE94tApc5lMP
7tktKxjotdCwHJC2/kzeUKsFNM16rD4rukPUkkXc1iYyatDp34njjTJWonVdsSoy4LLuhHpyqVMYL4s
1155iA0Z9j9qC5Nlg6fBy7qOn2FP/pwBowJvygsE2c5qz7Jf39WDofhghBKaCQNV8rI9LE4emqsQtNx
8KM2M4KjEWQDAEfu0OaJOAvPv5b0hvzyMAKPYTWx4c8zSmcE8z7PE6eEQ09I23WHOB7G0YalSPucsAO
MkkrdrCG6pVvG2RnWRvs9dAMQ5pgzSBnyLQi/nASihKjs/2TlL2i3+BCiMwXrHBf4/MwqoX9LPnmqqU
D+zJFI4KNrPRQCCsjSAEmUFPgwynYgXcU/eyG4+D00EhvQnGgF40eko/SpJEMVWmbe8HtzNyewWdIen
rg4DMdZQAYRY5ozElWpdZrax0tvycWBP0qvFzZzfYUQZx5XNbM0kIo5DKDPr0HVccGkrJjKoZxA6ZTT
zvQMDBDNHn9Jmc8xk6T8P2GkikOSADDCD8lsWErTrJg5bbLG/B+nYgOTFg+WHxDKacgw3OKTb2CrnXX
w5ccF/5ZiNKjCaJgcAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMDVUMDM6MjQ6MjErMDA6MDAMl
Z3eAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTA1VDAzOjI0OjIxKzAwOjAwfcglYgAAABl0RVh0
U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAUdEVYdFRpdGxlAFdpcmVHdWFyZCBpY29uz3Z
8GAAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_ENABLED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgUDFyIllrMpAAAEVUlEQVRIx5WWa4iUVRjHf+edcWa91FqaZoi5m
SJeiIzEiErDpPxQFBGEGEEEgVAUFVFkJSRJ9CUITboiCEXshyTtixkbKWpRapZk3u/rZdeZ3Zl53/Oe
59+HedfLrO6O/08z5/D/n+c8/+d5zusYAPsYQ5FoAve5aW4Gd7BXa/y6Ylc7cxnFNaFGBSGSlnROeN9
2qSapahvDbGEYHt/AcFcXi4mjYQujRylxiOluMcMAdJJDWuX2S2Gbi319cXBU6cBPs7W6DLZXJXmVdN
5e/8f1Nh9ZL61oaq6Dmy4/xTrcOdepTdX1+OGXbOQHii1yTI2eZeiFhRPa5roJrkarbYzW5VCzBqQkk
+wbHdR5WXbF9u6i6qYUTrmEWvNupsSFdFSYEJ63M1nCSuG1ZJhRIaZG3I+Ru7rY2yhQ9emQSbbfjXC3
AEU3L2oLO4pdCY6W5uPaSoonUL+Wn2BrFbLL/pHOFxWq/ThXcbOHXkZTi1ra3DR3s1IdDkfzT7uXuR5
AJ8NL+W8rFAf2r44qVUQ601bpkBJJUtV22/Lwlo5l0Z0ID9gVYuuHcl3qSdunBtiv/l0dz36vqw2NBx
cTIixUp64A2xo+VFWSdDadFRqYUaPUcVL8OLfsQtWfYDt7SLIUz6ZVfwLQGt0WDSY2jjy5x9wsAII+s
4fC/DDPXtDRjDDDHcms65f9fgsJli8uqLusDfErhTKolPsyhNxqioBX5OoHlRu5UX/1wgh3a5a874pl
EaiQYBu0F8D+pg2Aczpgg0UWQY4CACmnHT2MBAxqrgLaSeJmAGhnODDoNT0k+bIDGMJkKOBxCMa58fy
nTdFTFADRXhi8zHoBW5kVwl/hbpGScDYKr9r3YbWOZjtb/JiUymBiVQx7RL1ZYR0KHyTT49bwYPjENq
uWrZ4OD6uZWbaDmFqLrclotbA+rLQt6u6baZJ1JotEhe7BxSAlkLbZz5LK9pX9pPSSFgi2O6xMF4W8b
6Yzocr5+tD5PHxq2y8R8vZ7+MJ+UJcqtkT00NvAdI1ROURXdMNdbj6n3f1ucbbRow61MzFaTL0GT9kT
bB5wtoLH428MK3RG5fQjdWVZ2hQWxENFmGIrVM7iXJPk/UBSPSTE19nXkmTb+0yw3+KJRkKJlHYXlmZ
WHElvDwOJ9SLsRUkVHQ4f25Ys50uE6AZ68aTj9a8kKQ4LB2ynPElLfizv6Bf24dyPdT9st6gxEhhOgk
7nDjIZKLixbiAxIImXDY1BMJr6wZEb4ihmPgvyGlYfKfKNYg1TQ0ZcokxC0qNjABSjeRFGzAlayJOb6
qZkykeafM+7EbY0863THq9/RIlkrLVntuzyY31zYiUMm9nX1uoMy8NcmxOesY4LTfWe6GpOrJ6f8Ebf
wyupotLFf7bNj/eUmhXzpPgRtvJig1+CPeHepqbGRaR4/IjwZt/D2zdHbF16ZyC+lm8gECkpawj32Go
7oFTSedsUnvMjRQm7AuN/pdR5EqDAG+EAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMDVUMDM6Mj
M6MzQrMDA6MDBw26meAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTA1VDAzOjIzOjM0KzAwOjAwA
YYRIgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAUdEVYdFRpdGxlAFdpcmVH
dWFyZCBpY29uz3Z8GAAAAABJRU5ErkJggg==
""".replace('\n', '')


# Full paths to executables and other assets.
BIN_WG = '/usr/local/bin/wg'
BIN_WG_QUICK = '/usr/local/bin/wg-quick'
PATH_CONF = '/usr/local/etc/wireguard/'
PATH_RUN = '/var/run/wireguard/'


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def get_file_list(path, ext):
    file_list = []
    for file in glob(join(path, F"*{ext}")):
        file_list.append(file.replace(path, '').replace(ext, ''))
    return file_list


def main():
    # Toggle the passed tunnel configuration.
    if len(argv) == 3:
        action = argv[1]
        conf = argv[2]
        pid = F"{join(PATH_RUN, conf)}.name"

        # Wait for pid file to change state so menu item refreshes instantly.
        if action == 'connect':
            check_output(['sudo', BIN_WG_QUICK, 'up', conf])
            while not exists(pid):
                sleep(1)
        elif action == 'disconnect':
            check_output(['sudo', BIN_WG_QUICK, 'down', conf])
            while exists(pid):
                sleep(1)

    # Get conf and pid filenames.
    confs = get_file_list(PATH_CONF, '.conf')
    pids = get_file_list(PATH_RUN, '.name')

    # Show the appropriate colored icon.
    if len(confs) == 0 or len(pids) == 0:
        add_line('', image=ICON_DISABLED)
    else:
        add_line('', image=ICON_ENABLED)
    add_line('---')

    # Show the message if no confs exist.
    if len(confs) == 0:
        add_line(F"No confs in {PATH_CONF}", color=RED)

    # Build the menu section to toggle tunnels.
    else:
        for conf in confs:
            if exists(F"{join(PATH_RUN, conf)}.name"):
                add_line(F":stop.fill: {conf}",
                         bash=F"'{environ.get('SWIFTBAR_PLUGIN_PATH')}'",
                         param1='disconnect',
                         param2=conf,
                         refresh='true',
                         sfcolor=RED,
                         terminal='false')
            else:
                add_line(F":arrowtriangle.forward.fill: {conf}",
                         bash=F"'{environ.get('SWIFTBAR_PLUGIN_PATH')}'",
                         param1='connect',
                         param2=conf,
                         refresh='true',
                         sfcolor=GREEN,
                         terminal='false')

    # Show the connection details of each tunnel.
    if len(pids) != 0:
        add_line('---')
        for line in check_output(['sudo', 'wg', 'show']).decode().splitlines():
            if line == '':
                add_line('', trim='false')
            elif 'interface:' in line:
                add_line(F"{line}", color=GREEN, trim='false')
            elif 'peer:' in line:
                add_line(line, color=YELLOW, trim='false')
            else:
                add_line('⮑ ' + line, color=WHITE, trim='false')


if __name__ == '__main__':
    main()
