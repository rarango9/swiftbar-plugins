#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Github Requested Reviews</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Retrieves any Pull Requests that require peer review from GitHub/GitHub Enterprise using a Personal Access Token.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/github-requested-reviews/screenshot.png</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugins/github-requested-reviews/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# <swiftbar.environment>[SB_GRR_ACCESS_TOKEN:, SB_GRR_GITHUB_LOGIN:, SB_GRR_GITHUB_HOSTNAME:github.com]</swiftbar.environment>
# =============================================================================


from os import environ
from sys import exit
from urllib.error import URLError
from urllib.request import Request, urlopen
import datetime
import json


CLR_GRY = '#4d4d4d'
CLR_RED = '#d40000'
CLR_WHT = '#ffffff'
CLR_YLW = '#ffcc00'


ICON_DISCONNECTED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRwFECt9N4M9AAAEUUlEQVRIx9WWS2xVVRRA1z73vk/7bOkPCFig1
VBq8YPKAEKiiLZQS2N00GhETQwJwcjAOGDgTIwxfkdqIokTjRpjBG2tKRANSSHEhNR2YBootqVVgbbA
64O+z/1sB+++21eaIMlzoGdwc/fZ+6yzz977fOC/2gSgEwBFUQzKD7cwcCtVZDEIgmK4xCkE2rEhQb2
mSXkp2wVF6L4JqAOXCELGxCqolHKdMpd9erDBx+DvYb+kuWyfo1/7rg8neBIXP3Bd8bEABTwiKGW4q2
mNb2UddVTIN+4+cUFgJ9TJEe4PJ57gC/1QJiAt8RhllKvlia04OqdzMcdFq3lRdrMuHyTgkrYyNIINg
rbQVLSKVeyXRzlIVVkL9dRSIZaIKI4kueiOcE4eZ3sIAljGJhmawgaQlZTdEJaNbFyUp5vlsUHYhAls
/8n6lqoiD0vilAibVv7Kw/Q8yZJQDmfBx7Sj8AeTJcGu6IiyEtOLQbZxR0mwWnlqShTrNNoon7CqJJj
h3vIT1oS5DdnN+pJQAHWy14uaa010lYwCaDMPGnbQ+K/Alkq7LW1YixQuihXU4OKmuEh+7yxoD9ncs6
DD4xTdDONqQlawhjWsYAnlQJpZLjLJuE5KEkMDO9hGvGhsk3RmiYZihnf0A7kCggIWOcuUE5c4ohkyf
jrmuBS0XpnZJW9SN78euwgFH+vruDGyD2sXU/qpex6PFCkNtq7gQJW8oHfrEQ5LOnowF5P3iQSjbenU
EHVW2xgTdLN8TT3Qo89x1aEvNOjAt+23eQW4zl75zIdKOcwjBb1hLrQ9lhgD35K91APQLu3FcX4Mg72
B5wFI8LJfDTLLd6GBY7gUCgNzgCxnUyBbbF3CvOMAbKY2+GsODtQh0kFP0nCmED6dAkFqqA6H1l+JzB
90cSDwOe/bSgG4SjbomTScCCY3xEHRdKiElOfNe6YAqfncyTUAjYT1OGj0GDN5mDQIwIXQVzgd9XOhY
AE6QKHjTz2rALdTDkCOn4wO0F+IhxtV5Dpf4gHwu3b7RdvgexROcjIQD+XGPaLIliBHZ/Rnq9nVlDxB
FFgup2RU0WGM1DOqr0X7Mxwpiv5dkNHf5E4sDusBK2Xw1soBagB41/woHahtvcWrAJzwd5kxxbesFZq
OzGQQeotgrRylE62kyr9osoJWyUc8A0Cf/6zMWE0Yn1+kjvswrJYHdMSdtH2dJZ3DIstoEWw1LUyTyJ
IUL4bbIu/RhQD9+pKZEKQTBTQhe2QfDcAM3+ohBnU6kvNvrDIEQ8421TTLTrpoAK7xlb4h4xGuIpDHR
XCa5Wl20kwCl/OMMMoFkkEyCqxKlrKGtTQSx2eC43yuxyUHHr2Fy7cDxWDh1dAiG1hPI8uoIIYdbuN8
qTk4zDHDJGcY1F913HiKoPSw4N5vxyeCADa5qMSJEyMqxTA0g0NG024m5iv5x1cuPAoWPQu2UItXpFh
ooMFXSRHnKP+X9jeoVJkbNcFJgQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yOFQwNToxNjo0My
swMDowMAbFmJQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjhUMDU6MTY6NDMrMDA6MDB3mCAoA
AAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_MISSING_CREDENTIALS = """
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
oAAAAASUVORK5CYII=
""".replace('\n', '')

ICON_NO_REVIEWS = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRwFEiYxsJ0CAAAEQUlEQVRIx82VX4jVRRTHPzP3z6573XXXdZXVd
f8E2qIUPRi0WCY+lEoPEUT10FNFBIFg9B5BURC+VeC+REVBET0IklGGpNI/NaMw1k1dXcN1d9Xr/T9/
zulhf969NzOiC9F3ns7M+X5n5syZc+B/DUUQAo4ykeo/4vyCUsDhEQLK54CB6yyFHANSkUKtsDQIiiH
1N0IVynSRZtqu6rRdtkNmU1dkgTGHIrt1Rs/JcflYdsXRUwQUpYrDEXFcwxOpUeEKikfxg/KUvCff6R
mdlbdL6drCPg63Qo7rIs7La36topwzrt31xDVu8NqQH4z9tWWVjKK4nviCnFKpM2b8nYFXMSDoFrufX
FMUf2CcbjYwQK/p1JQao8Zrnhkm+Y2d5kFMo788a/duJQ0Gs5olzVExm9jUYCVMw61ghuEAtsn738OA
YkHRPL5FsTn4JBE7T74lKc9pxWMLROQi0y2JXdVJ5THsUjLYbdzWklgvjxwwASJhRH7WFiGzfrNgLfZ
ps7HF8GNW2OeqWcJ6Pd3quVRV9XIcs2Y7I62eC4A+syNtHviLAhFQUklC3wwlYEjfNL8lzR1NE5FvdB
+/miA5+s0QQ/SbZXSAVrjODNNM6bTJYxlmu9lGewN3PVpruHdFXvY9yuIopnxn6Itr46Bf6bvKmca1y
pLwjMw2sD1ND7zHpQOK3C9vykthMFLCEYhEPI4KgdAtu2Q8PhoyDiU+r26R3yAmE344oIQxvaCqKvtC
d2S24R5VCmnZo6qqRXlSCcQuPdgoVqqLvaU4qil5N5kI8oRSqUtNIcRNOpd4f+t7Aorsqms5q5fr3if
Akl5l7knsFFubH9FgxuhN0nTUrDco/HRjP81bJm6kg84qFrucnjp/wGUW82YNYAbqZs6sNhjMNZLyz7
TlCAqApR0UrdQXoVCKi4VOAC0s5qIpgiKZej6etPIF8wtiZtggxEs6UScc65H5upFF0RO4xPxdT+vCg
TsAcBy0/oQeTpbHytlApsSHRAA9I/uEtrqYQZCjejSJ0KczUyUMZnPyFyb0K4S4Uwuqqno1bIvUqHTE
V/SMHIsPK3N/+keKv1u+1Cl5J/RHIn6dJGVCXlSoUkzLG8nE4dqw4imm4oDrVQoUm8QuAorvioPltoA
QuuWDhPmZ6w3gCLhuGdegqiqH4r1XrBBxzFPhbJPYLxTZjycQUPwG+WihEcvX4faIghDw1HJxt5xVVd
U52Rt3xNUu2/gPG0cp7fviffJ64l+Q8TgkKJML/U4Q0oTR1OM8ZEbJETjPpJ7lEnkTG2Jm6KKPIbOOE
doRLugh3o+HUs5QJnej+ToCWVL45akN3GU2MsJKOk2bpk2m6QU8nrLOM82EnuRHP9UWIxYlRVPHL1Bl
GWkM4LK2nXbbFrOZTKOWVI3Xaqzkq30CgpBijpXcAkdQKtTweCKuKVpCIBKoUeT7Flvtf4s/APwRevY
ww1fIAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTA5LTI4VDA1OjE4OjM4KzAwOjAwEM71xAAAACV0RV
h0ZGF0ZTptb2RpZnkAMjAyMS0wOS0yOFQwNToxODozOCswMDowMGGTTXgAAAAZdEVYdFNvZnR3YXJlA
Hd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
""".replace('\n', '')

ICON_PENDING_REVIEWS = """
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
""".replace('\n', '')


QUERY = """{
  search(query: "type:pr state:open review-requested:%(github_login)s", type: ISSUE, first: 100) {
    issueCount
    edges {
      node {
        ... on PullRequest {
          repository {
            nameWithOwner
            url
          }
          author {
            login
          }
          createdAt
          number
          url
          title
        }
      }
    }
  }
}"""


def add_line(text, **kwargs):
    params = ' '.join([F"{k}={v}" for k, v in kwargs.items()])
    print(F"{text} | {params}" if kwargs.items() else text)


def parse_date(text):
    return datetime.datetime.strptime(
        text, '%Y-%m-%dT%H:%M:%SZ'
    ).strftime('%a %m/%d %H:%M')


def main():
    access_token = environ.get('SB_GRR_ACCESS_TOKEN')
    github_login = environ.get('SB_GRR_GITHUB_LOGIN')
    github_hostname = environ.get('SB_GRR_GITHUB_HOSTNAME')

    # Validate that the environment variables are no longer the defaults.
    if not all([access_token, github_login]):
        add_line('!!',
                 image=ICON_MISSING_CREDENTIALS,
                 color=CLR_RED,
                 font='Menlo')
        add_line('---')
        add_line('Access Token and Github Login must be set', color=CLR_RED)
        exit(0)

    # Query the GitHub API for any open Pull requests with pending reviews.
    try:
        url = F"https://{github_hostname}/api/graphql"
        query = QUERY % {'github_login': F"{github_login}"}
        data = json.dumps({'query': query}).encode('utf-8')
        headers = {
            'Authorization': F"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        response = json.loads(urlopen(Request(
            url, data=data, headers=headers
        )).read())['data']['search']
    except URLError:
        response = None

    # Show as disabled when not able to access the API.
    if response is None:
        add_line('··',
                 image=ICON_DISCONNECTED,
                 color=CLR_GRY,
                 font='Menlo')
        add_line('---')
        add_line('Cannot connect to github.disney.com', color=CLR_WHT)

    # Show normal when no items are requesting a review.
    elif response['issueCount'] == 0:
        add_line('00',
                 image=ICON_NO_REVIEWS,
                 color=CLR_WHT,
                 font='Menlo')
        add_line('---')
        add_line('No Pull Requests to Review', color=CLR_WHT)

    # Show a colored icon to notify the user that there are requested reviews.
    else:
        add_line(F"{str(response['issueCount']).rjust(2).replace(' ', '0')}",
                 image=ICON_PENDING_REVIEWS,
                 color=CLR_YLW,
                 font='Menlo')
        add_line('---')

        # Loop through each PR and format them for the menu
        for pr in [r['node'] for r in response['edges']]:
            title = F"❱❱ PR #{pr['number']} • {pr['title'].replace('|', '-')}"
            subtitle = (F"{pr['repository']['nameWithOwner']} • "
                        F"Created {parse_date(pr['createdAt'])} • "
                        F"by {pr['author']['login']}")

            add_line(title, href=pr['url'], size='14')
            add_line(subtitle)
            add_line('---')


if __name__ == '__main__':
    main()
