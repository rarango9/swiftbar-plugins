#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Github Requested Reviews</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Retrieves any Pull Requests that require peer review from GitHub/GitHub Enterprise using a Personal Access Token.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-github-requested-reviews/image.png</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-github-requested-reviews/README.md</bitbar.abouturl>
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

# Hex color codes.
GRAY = '#737373'
GREEN = '#58f158'
RED = '#ff3434'
WHITE = '#ffffff'
YELLOW = '#ffd735'

ICON_DISABLED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgUEETcbXubBAAAEsklEQVRIx+3WX2zWVx3H8dc5z9NS2tk/tFPIt
oKUP0MYsaKwGMVNzEJpC93Umcw01psRYiTTsF0YL9BdaCaJUaJm3szEGM2yTDYYkAjLYIIMU0n4P8af
wRKtwtrS9Rml9PkdL54W6B8S461+bn7JOef7Pud3vt9vzidAi7xMNKYMvf5iojrcELDD1Aq0y0RZVVg
ePqXGlfRWdiQOB2y/beEa010XEH3g9Slh+RaZKDXHzVapgtCf25aeTeeDhd4Gn1crGeZeX3EoOxTucL
KYF6Xm8DtrSyjU6govaEzmg1bVSBWeCK/6aXq8zD/uAMtnVMXNFuGK15yz1Gp3WRk23Xgql7WYZsR01
z4dn7bONETmmisTnXBhPCyy3CpcSU9e3VaXbuRz68MWFR7L/9LpKGPm0Pqw3qzRiBnDC0JIvT2X77HI
4nHJiFimCq9d3VadMrmR9BuHMDMsDoTUHl61+SZK+HLY743w+j0/S0vyaJ0Aqwbn6lKwwzULCi4i5yO
ESt/1mXH/UuljZlpiY/hjWh2N3ewY7ApYeiPPKtOdqXM/bnif/kL6vl1GboP1OeYdQ5hna7YkZ+E42F
v6sTq3PlUtlerCJstwKR1LqoUD6WtpgxM3I3Z7OH0hdXob88KTgyHdnMrNl12O831SefhiWNn7cHgqf
FUeP69/pVDabTj+Le0MRQtVotvvDcaTqSeslXdX2UuhcObWyeJw+qH9qPCQb1ghjxfT1vcFO21XdJZ3
rz+dHrVDppCTZBzwHhrU3ZaAPoELqdNWf5eQOW9z2qCXP4Fd6lCWwpvpCY+lXxT9SxCGDUEIt/ohHiw
16KXTG3XpxwWPlv9ALwyPLjpghyJ84BWngoo7dQDbLdLkfi4axofeG5bZcxM1du+3q33q3oRTpTqOt8
Z2TkD9Z4r/Rcz/Yf87sEXaKL1wo981yu8YUm7NhNVtmsZg7ebhLI3KUOm+aaJHShtMUptHROXSfSpRb
vZxfEI7cp9VKdFY/6zvuVtQa3WxzjHXeLfUkeNO1QQzsmfCj3xcUOFLH53jhKtBvdAqMDe8YOW4qBfT
Br2ZnRNga0RmhF95fNzw/vRN55PcAqk8/sQ6DPmzfa6bKVocrt29b9DZCbB5ZvnwGd/CiL/aq99MebN
DTbYrFGMUm3VgMG3K2pq6spb0nBF0Xp6Tm3RjOf+coxMj6bmspakra0ubDKIjNkeRsEItdhefD4XjQl
/aohuN4YHJNiAID2hEd9oS+o4LheLzdqM2rCiVRgM4WjbCHkMW9DmNMvVTprNeGU7P7xuyB2UjjlKiR
AyApr6QtJnmTJXZKI6OT9SAIma/UzVNm6QvjBbZQAnWrYDWmo6BEGX50OVB9KSTU7HSST14MHRl+Wgg
1HRoRUF3ybgcjnut1RB+XbsuncsvtVoFXh45MzkBmeKZspd9W0X4cf6hdLS2SasG7M0OB6GdkqVaNKF
yOl2a7BHboDH8dkJVnkpfD0fINSH2pINhlntHG7LfH9J3XAwuuDypNOq5al+oMWf0kSrYnTaGI0XZ7T
Y0LrdM9Z1s6JhK71JWHput0GBAd3Y4FjLRdoGSQU5uVVWGPgdNrc+plcbZ6WjELvwbP9qmSJonob0AA
AAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMDVUMDQ6MTc6NTUrMDA6MDD9uWuOAAAAJXRFWHRkYXRl
Om1vZGlmeQAyMDIxLTEwLTA1VDA0OjE3OjU1KzAwOjAwjOTTMgAAABl0RVh0U29mdHdhcmUAd3d3Lml
ua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=
""".replace('\n', '')

ICON_ENABLED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgUEERy34h+BAAAD7ElEQVRIx+2WT2hcVRTGf29M0uoQJUkVWyRNW
0gjlEJUWkFcFCy4KVLsypULd8HiQheKJSLUgkrR4D5BRChZBcGdxiBomqBCLKW0Ke0itYG0GZJJ5s99
95zPxZs0M5mZgm71wGzuO/Pj49xzzv0AKOIEHCGEUyHwA80hAimRdpGAqLCLNN9xLHkueUL3dLn6x66
QALm6xE0ew3gEkXCDwda0dco4NuxT2lAWBR+PBw3xUS1nHicg0mf8HXtR3GwnzXFsWFfVED4T+40UgE
AZp7Lb3/DfJbsoPmsHC1TzPiVJWvEJP+eTKkqSj63myqwhUkR8wS+pIknpF8KIlEh5u4WyE9qQtJKen
k9EsSOOqCxpyYaMCiI87aP6a0tz/NoG/XB88hucTcLOG/J3Jckn5pMKMVM6LSn6604lsVM+11CBTS3r
rv70L+2ICI04oY8lyc+JCNxC+IQk6U0RM3DruOGvik0+bFB2VpJ8cr0jcIuU0OOzkoKfcn7FXvLvldY
hVrWg6ypnODviWH3N7LgKkopxpJoX1R47r1TSog0YGzix297yKw9g36ov7rUzfi27pqtJdRtWodTl45
Kksk/7hM9mOnxUbFBEREQ64J/rniRpPDuxMypLuhKfqpuIgGEHNLOjzy7F3kiZbNg+JXI3sZf9O5l/J
apE4l5dl7QcD9fBZnCM2O9juiOXZLrpo7E3Yuyp5fxMoIoTu/01e1ZMIdSnBUnLPuSNnSaMD/CTWpW0
aEdFxOoLCxQQVvvN1cE0pMZeu0CKo0EtS1pQj1N+oKp1tIblAN6nk2R7SeQSHuUe/zxy/+I//8P+O7A
LpAi25sJF6SFNu4fyjuyU97Y+ZuP0Cf6K7tePU9oSZVi2NY5qUdKqnzyLoYzdetDThkGvV2VEYq+P6q
ZMkuuOj8V+w/mxtoIOetMKSnsjpSZYKUNdanoYDxrh4cux2AQrInxUkpT6rE/4dLbAfbzUVWle26Fhb
beo2IAWJaV2PvSIaj6OqCipYMd954Nym1j3oKgJJvyUguSzoSdym8B6h09Kkp8VOUiyOi90xxwDLNFZ
4BrQmfS1us2kj07gWmdhiQFydEcWIKPkQOsAHJpPIpF9hDz7Aaud79S2jgH7Q34fkchcwqHaeaM9uJy
ItQZ70KJmQ1qSVI4jax1iNklPa0XShp/whxmXQq7SBCtzP+djkqSiT/o5n9CKJPlUNR/aWSrVWar6SD
Fi/86HUVdt2PF2Zs8OGOJiE+wCwrADPq5CLXvDp2zYKbG2bUNjvuMYzyePt7Oh25MMInR1DSfHkz1a5
7d0rnOzym6Srb5uNMhVAj/RLn4hpVqXHXCyi/8brcJDM4JuMxcAAAAldEVYdGRhdGU6Y3JlYXRlADIw
MjEtMTAtMDVUMDQ6MTc6MjgrMDA6MDCWqwNXAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTA1VDA
0OjE3OjI4KzAwOjAw5/a76wAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASU
VORK5CYII=
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
        add_line('⚠️', color=RED, image=ICON_DISABLED)
        add_line('---')
        add_line('Access Token and Github Login must be set', color=RED)
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
        add_line('', image=ICON_DISABLED)
        add_line('---')
        add_line(F"No connection to {github_hostname}", color=GRAY)

    # Show normal when no items are requesting a review.
    elif response['issueCount'] == 0:
        add_line('', image=ICON_ENABLED)
        add_line('---')
        add_line('No Pull Requests to Review', color=GRAY)

    # Show a colored icon to notify the user that there are requested reviews.
    else:
        add_line(response['issueCount'],
                 color=YELLOW,
                 font='Menlo',
                 image=ICON_ENABLED)
        add_line('---')

        # Loop through each PR and format them for the menu
        for pr in [r['node'] for r in response['edges']]:
            title = F"❱❱ PR #{pr['number']} • {pr['title'].replace('|', '-')}"
            subtitle = (F"{pr['repository']['nameWithOwner']} • "
                        F"Created {parse_date(pr['createdAt'])} • "
                        F"by {pr['author']['login']}")

            add_line(title, href=pr['url'], color=WHITE, size='13')
            add_line(subtitle, color=GRAY)
            add_line('---')


if __name__ == '__main__':
    main()
