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
UAABYlAUlSJPAAAAAHdElNRQflCgsEGgiuE2UEAAADKklEQVRIx+2WwWscZRiHn5nZTZvURE0TrVTTp
pKTSnpQckgFRRFBPQmKghcP3krPot4KCnpL/RPUVsFDb2qhoYIaL4FSo6EtSRtB2iRuzWazuzPf+/56
2G0sO7uz6Lm/uQx8Dw/v9877fQzclSoisJlkx+xzX1ZT7qea5ZR8Ak6GSKfsA1/QluQ/2eRdwAYbCDv
ip/yG7mQpjIecagFhZMN+wn+XtcmGvboLGFsIe94X24tBN3XFP2qUmh2qGkJkE35mV1TRNT8TDraBLR
oEspd8VZJU92/9LXsie6RRSumUOSnNw/Z9y+O/+gl/JkykQ9Za3ocQNqOrkqQVe2dnrzAy8qpAINvvZ
yVJNf84e1g4gRRvAQ0C4YBfkCQt+7OiiXOpS+NvklJP/DNJUtWPb8YZovIvcJ0drkb+iST5X+FFo84O
3SOEvaYtSZm9X4lylRuGzWpdUmbHxc6dgnNptLb4oyT56fpQRseX/o2URtm/kCQ/m92XUaNXhPD3ZJJ
W7SkjNzQpjh1TRfJK9pyhnqolMtJR/0WS7ENRoZov/TQ+J0n+1d/lKms9ZQFhr6sp6XI6GdjOI0aY0G
VJdXvFC7YITWpJux2fKjcy7T7YmwqSFsKDoUC2TCA8rmuSbtms0+3ExqtR9AIJ6Iekss2+nrIjJMQzH
ARd9IvOQDfZY+PR00Bd82KwYJMpwCwJcKFUvdSViaMpDgFrWnL2FMgGCMMcBVJ+FhNdmVI0zf2gP2yd
wsRwIDoMrGsZRnswT5IASwNZKJRFMMEo6Lrf6HVCYqYAuAJJgWqdiOgQe4GVW7VmD6rEo0BTf8Ke3PS
LdUYpA2MArctvbczVhTQgjsaABpUGJJ3PNg+RUgM2AcbbRRLlSMUloKThCAbjk4P/5Ns0XLWv0+/Kvk
iZxejoAwDR28wQdZJx8Hn/EhVnI7wswPFE3xSSwebi4oFgf/zGCoEoV0wuSfxuPxnRyGSS9INaGeorK
7jgcukv+w+5J7sn+9+yqMtbT5n3IUKQEC5CH9JjnS8EzOdLvo0Ru89jRajOE6b93O7vZGdqNpeOZFTJ
yEhHbE61HqT5uTB9G+iee+uIEMNHAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTEwLTExVDA0OjI2OjA
4KzAwOjAw8TmO0QAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0xMC0xMVQwNDoyNjowOCswMDowMIBkNm
0AAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
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
