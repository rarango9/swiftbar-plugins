#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Jokes and Quotes</bitbar.title>
# <bitbar.version>v1.1</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Grabs a random joke or quote on each execution.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-jokes-and-quotes/image.png</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-jokes-and-quotes/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# =============================================================================

from json import loads
from random import randrange
from time import sleep
from urllib.request import Request, urlopen


# Hex color codes.
WHITE = '#ffffff'

ICON_JOKES = """
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
""".replace('\n', '')

ICON_QUOTES = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgYMNTRvGaiLAAADAElEQVRIx+2Wz2ucRRjHPzP7JhtjTEosFpvaQ
AWFVvwBVTFgLmpzUAuiN/EqxEPvQg+5W/8E9eRRiAi9eFPbUNSiFSLmkKDSSkpKs5s0777zzjxfD5vE
7O67S7wp9JnLwPvhM9953nmHF/5XdZmCHVoYBaLZl/uWkh12SJRAg6wbKDEyPFCMMGS5xbFKUYstJvF
k5MPUVSiA6wTqGB6bZtbN8Lib0A1dZL3WJcoZwfCkR9yMm+VJ97Bu6aJf7lC1EPGELWhFSbtlb1mXKv
AHRjxiH+i6wj73oQ4iAZFe0/d7jxW0ZT+k09alaiHSM3Z5f8Goba2mc/onVUDYu1qXJJV2zRbsfHwxT
ol7B1RNthFpVr/u5lm2j+2dOBNPBVe2kXs0EeltbUiSrab51qQwIpGc8oBMGPEF/SZJ2rCFcEKIRKQk
tpFEIj6nVUmya/GsKFih1fMGA5HyuH0nSVqNb4pAk6ITKSnG7EtJsp/jU8ZGx9b26nNybnu7JEn6K82
JvHdBIdJ7CpLuxDnxGVuVJyuSiDPakBTSvGgRupGckjBh30iSfXTd5ZWp2mSjZp9Kki2G0ZK8FwkY6X
XlktbSE6mzAx2qSDyjW5Ka6VUjVTA+8T7uDUZAX/mVHep9ZCPU8K/wKOhqebXkz+pOxKP6SVJuc9Y3F
xTkmX0hSXZBqJLJHJpmGvjdfoEf+8o8/iingU0tqePsHWA87hQPgVa21z0voY5Rot20Hn/cHQPdTGtQ
7+IiW7TIwE1RAxrjU871LHZXzWEAHDrGg0Ajm3SjdJPbY3caZOCOALjzvNybu7Zs826tLWOCDNyzfN3
TMudv24WJpQzwAIwz3tsF95h/vi0D53DAKCcruJPuHEuewSWXcbiq7aUaqDukjMPI/kXdl92XDZC5gY
SrmPXhPCgfxKil/dlALocMtMhZN1X52TjdsCvtQIau+E/c0324m1p0OAHl8FDl1S+KfDg6fFtGyOoPV
O+1LIYCcBcIXffm3mj/7G0CsIkosD5kgF3uv1l/AxlR+4q/ZzQIAAAAJXRFWHRkYXRlOmNyZWF0ZQAy
MDIxLTEwLTA2VDEyOjUzOjUyKzAwOjAwlQ4MoQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0xMC0wNlQ
xMjo1Mzo1MiswMDowMORTtB0AAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAE
lFTkSuQmCC
""".replace('\n', '')

HEADERS = {"Content-Type": "application/json"}


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def get_joke():
    data = request('https://v2.jokeapi.dev/joke/Programming,Miscellaneous,'
                   'Pun,Spooky,Christmas?blacklistFlags=nsfw,racist,sexist,'
                   'explicit&type=single')
    if data['type'] == 'single':
        return F"\n{data['joke']}\n"
    else:
        return F"{data['setup']}\n\n{data['delivery']}"


def get_quote():
    data = request('https://zenquotes.io/api/random/')
    return F"\n{data[0]['q']}\n\n-- {data[0]['a']}\n"


def request(url):
    count = 0
    while count < 8:
        count += 1
        try:
            return loads(urlopen(Request(url, headers=HEADERS)).read())
        except:
            sleep(15)
    # If we failed to get a response after 2 minutes, then we're likely
    # off network and just exit with an error.
    exit(1)


def main():
    if randrange(0, 100) % 2 == 0:
        icon = ICON_JOKES
        text = get_joke()
    else:
        icon = ICON_QUOTES
        text = get_quote()

    add_line('', image=icon)
    add_line('---')
    add_line(':forward.fill: Next Item', refresh='true', sfcolor='#0fb10f')
    add_line('---')
    add_line(text.replace('\n', '\\n'), color=WHITE, font='Menlo', size='13')


if __name__ == '__main__':
    main()
