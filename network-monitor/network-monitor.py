#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Network Monitor</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the current bandwidth and other network information.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-network-monitor/image.png</bitbar.image>
# <bitbar.dependencies>python3,ifstat</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-network-monitor/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# =============================================================================

from os.path import exists
from subprocess import check_output
from sys import exit

# Hex color codes.
RED = '#ff3434'

ICON = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgsEJA9xsuvaAAAEXklEQVRIx62WwW9UVRTGf/fNtOC0IBSmidEFh
AFCSDTRNBAaC2xcQNgYFhoT6oK4AbvARDP+A6xYiSv+AVaS4IKo2ACywBLdkhBbo7aNMARoZzqdee+d
87l405l2OlVM+O7uvHPPu+fcc8/3BbpgODkCKmokHGeEUijSD8SqMM0UtzQVVYQRkeNfUEMYwkpe1pS
q6oWqpvxL25t51jYKVaeKkwx7WTNdARa00GWZ8XIy7FRZ6hWqQQNhY36n5W4ySVLsV+ywHfYritfY5X
fSMRGTdIdapsGjyMY139pw175WVZL7JdvsOLbZL8klVe2y/9QKOG8f16KYxtoEGzyKfEKLkqQ5uxAP2
2VJ8snmUIoQKc0h/1GS7HKzaBc016rgxN9Rg3qn7FWEjWeh/J6NCjuoeUm19KRjAAgnPamapHk7KNIj
fk+StGjj6tROODaWJWg3k5IQ9oUk+Y16YZllAH5nmXrBb0iSfS6ceI/90Ep2zFHWV0YynJXd7yUl0aA
54JOS3D9R5tT6qfBP5JJPNgcaiLSUnc7vJMOGQYLwcqtWo0I4/pYqkmZ9v/NXO9gfOL5fs5Iq9qZliR
/xWUnyskjAsb2akZTYhMiWn5FLfn0+crRqObORX5fkfmbFZhNKJc3YXicf4DS7gcUwxHkiwMMpArDlt
XOE1bceeF3aAoTwEVsz32gHCwyxO5wOF7GipvQyMGXFiBEO8DJwgJF8OM4g8DO3WymJnXxAgadcpbY2
TUAM8iHbqXOVJ+0dRznEYDiO35YkO9spcvqOnkv+S7x1bflbX7fqV0nP07c7X+2sJPntiD1AnYedfgr
b2AQsKInX5WIoYQHYFLZ3DhseUgf2RKEI1KiIsLIGyAMNLNC9HDMtA/kwsGITqlCDUMzTD6rbqrEUAo
DqFetbd7KnxPZGPbS9stOyFOoB+qONr0cvaOsgT0x/KOQGVm1QAEJhONcaGKuwA+VCoeMFkIOBUADiS
BVgkGLo3NkSKbCZnNbdZkQuF14BUi2t2AKhyCCoEvEbUGBfp6H0jCaEbbm+/nWJ5Ah9vAo0edauMdpH
AZjOc5+jEJ1lb9aCQbmd9AG7chfXN21QbpBdQF90rtO04SgAU9iJDSjt/6JqJyLu84CXgQfhfj6q6Fo
YAZ7qq/AkGyuc4j3QrfBNj7f5PseA7/m25VvkPEOga6GCY6UXH45zGw3HaSv5f4/tP9uHaqwb28JGM8
qzsqiDkdAsriaUJnFPQknXEUrSJpS4mGTM3qK6uV5Ut1RYbhFsnZi44N91qC4p2c0uqoMlaoj0TG8St
tabsi4SttHVJFzrCJg6DZ5E/umKPPDP0t7yYDKTB8lwWx4s+sTjqNEi6nZx6zwMGwkXw9YKl7tt4TL+
OGqsFS4ANeoIezcb42slVbqBpLIx0SMUwDI1nLhoZU13PZX1Ym/ays2iU+von24sIZIXkaFlK4kE79K
N3c+FBKO/JZA5Fg6FEjt7CeQGfXSP9X8AVgMqdUnVgXUAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMT
AtMTFUMDQ6MzY6MTUrMDA6MDCdyjBPAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTExVDA0OjM2O
jE1KzAwOjAw7JeI8wAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5C
YII=
""".replace('\n', '')


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def scale(bandwidth):
    bandwidith = float(bandwidth)

    if bandwidth < 1000:
        return F"{str(round(bandwidth))}K"
    else:
        return F"{str(round(bandwidth/1000))}M"


def main():
    # Check if ifstats is installed.
    if not exists('/usr/local/bin/ifstat'):
        add_line("Missing ifstat", color=RED, image=ICON)
        exit(0)

    # Parse the bandwidth output into just the upload and download values.
    bandwidth = [b for b in check_output(
        ['/usr/local/bin/ifstat', '-n', '-w', '-i', 'en0', '-b', '0.5', '1']
    ).decode().splitlines()[-1].split(' ') if b]

    # Split the parts into upload and download vars and scale based on speed.
    dl = scale(float(bandwidth[0])).rjust(4, '·')
    ul = scale(float(bandwidth[1])).rjust(4, '·')

    # Show the speed in the menubar.
    add_line(F"{dl} :arrowtriangle.down.fill: {ul} :arrowtriangle.up.fill:",
             font='Menlo',
             image=ICON)
    add_line('---')


if __name__ == '__main__':
    main()
