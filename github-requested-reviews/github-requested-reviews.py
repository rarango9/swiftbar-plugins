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
UAABYlAUlSJPAAAAAHdElNRQflCgsDKjvLyiRkAAAEoElEQVRIx+3WX2zXZxXH8df5fn+/FmiL5Y/t2
B9Wy9om/mH+y7KM6IgJlNHixiKLy7hSgxdumXNmGv/FRNmNi0ScN2QkLCGCWcaFDLbB3KZOZSExGpcZ
AZGVjAW0pYb+o7/f9/t4QelaLGrmnfFz9zw5zzvnOec8zzmxymKpI77gU5YrnbQ77YizuUkHXVafQlX
qip1OpM8pnzG3ssV8NPb4sg6Zim7fjidTVyGfgaJBuiV2+ZhrohKupix1+KFbUTjjrCTTG9tSa9KLm/
ULB5R3x163+TfK4n634q30YLo9rU7fMIx1cVd4t07LkRr7H4onvAckdfpttG4OWN6zQ6sifa3yo3LI3
5b8crzFx2XKct9Eea0kLcm2xlc1T9mPOydcUA89uhyf7ZkbcNbzdTWFQemAESyPplCXyx72gIZp+5X2
ejGeTvdZyMQV/mVK5CpkAqoCpUQomLziLhXt1tsVP04fbhbumAU7iTZ3L5XLXKzEJk34czmahCR933e
MTtu/5SVnUdEXPyl7qwprZsRskdtl8ZHxFuM6q1/yWVWT6dHstdxPdXOx9ovszbhFC3glbbI/RvRYYL
FV6Ujlzao/TcGivz2e1AtGhCawu/x8jE06NFVlVfXVsc0H8aw7U225gXXxA914MW0yVPfclGejXtXpJ
qFBAybtSY9k53kWHNetkJ1KL0eHbiftjWJI9UT5x1irWUeczo7+wd8vwd4rDaWDcUyndrySHknbsvNh
xKkp54/r0qQ2mA5Fg2O1lzMXJfP+Us73CaE17WufOHYJtkIwEb/TaRUei11qjHhpRpaOa9PIePGCX1W
L8JxuJadjg0UWORwDy7yB7ID9U4G6FEMmPTMLhal1VqglZ3BQYfINr6I5PuBSUanA2KyDh+Z8d/uvWF
dVy3QpjTeYeiCZd6gxieHLDsV/B3sB0uy9dwybS/+H/c/BFszaWvMfHZxtNR9U1suNmu6FiUb9Lvj5v
wCtvtxfpot2zAaF/H0SrT4d97kGLelCOpXV5rl2+gv6Z9RCpAXujM+4ES1pwqmYqMq7pK7YEQ9bBpbH
XdGZjhipOnYV2PuRlmXb41s6QXt8Mlamo2ko726PHe4QGFHTILcy2svno3ajk3PGqiItyLbbLMeoSQ1
Cd3Snw1lssQbDtqa1ab3HjeOe6Isr0vJ2qEP0uQfjHk/r01pbDWNNbKnYLJPS95Y8OoiJX8/jfg2xsd
hXFnPBSinPNmrAzomHGuss/s3gWHxXZnOmE+fsG1QoNdbTU0axImu62rQTTVZgND3VWC8VBtnnHDozG
Qr1qSZOTTLd3uemyZDUSEqoK5BlTqNdb0VVbqno04yBNJquwkqjBtAcfUvlqir0asfpvOd6t8niQ+WE
89rGtsQXzVN4LH7b4rU5UDcrSgtskFk5lvur1vLe+LqFeCL6O2LP1LB3Vq5N4EDabPhyn56tdSq0xm5
9SM4ptMtxJN2b9wz7vZWul2nRLJQOpQfjTMyYaWfqhB4xkY5Gt06ZZi0yHPFAvJ63mX8m/SzqrrNQ4Y
Tt6ZsxkKtfMci9rZtUpaF0OC64zrswYGf6Srx+3j8AtfqowuiP7+wAAAAldEVYdGRhdGU6Y3JlYXRlA
DIwMjEtMTAtMTFUMDM6NDI6NTkrMDA6MDCDg+dgAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTEx
VDAzOjQyOjU5KzAwOjAw8t5f3AAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAA
ASUVORK5CYII=
""".replace('\n', '')

ICON_ENABLED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCgsDKwxqbLAqAAADuUlEQVRIx+2WT2hcZRTFf/NmGjUd0tRChy7EC
AmNBV1IUQISBBcRu9N25WbAZRB0G8xGShdtQTBbESHQXVemJRtdtIQQXGi7sASxra2TRmOSxkz+zHzf
vcfFe8lMJjNtyVI8q/fgfufdd+/5zr3cRMQ+v+T3ZAqat/FQEmKTBrZYQcQBv+HfhMToCGGnfVYNmE/
bgPDdiBrbiPimz0i6ri51Jot9GVVURYtySfKp0Bv5G/iaSADsA78rPZXML0uSL9ho7I+DNuarkqKVhf
gUJ7D1nH2mlSzva0qciFhu+5v3JUUbFYGIsPOS5Fe3C3WEUz/mX6m2W4Rb/qGfis+LgNjaR2aSKrE/8
BdrGDakdUk/2hEjIvyC9iJo0a/5R6FH3GNlD1eCA3kKObrIAxwiBziCBKDe8vUCpdz7uW/zV+yNPgqs
78lsXpLbmIgYfxRsQpL8yma+joiEHv9C1d28FvwHLaaP/quPiD952CCzcZnkq3behmzYJrQpqWbnhIB
IYDlvZVUysuvhiL3uF7UkSbob30rjMoSST2eB6zsZ+GS9O/IIgO1UZe/4T5k0DhkivufzkuTfhxcDj5
tEO+BTst0fqfmknXAaOt9mExFP+neSptUlHiPCu/5Ikvuo+LhBJkKvl3VLknTTzta7HXGnqa5VhFE/Z
l/6+HIucI9lhH0uST4Te2Pj3qUi1EVJ0idpI35paeEdROSf/PahtEYbROwV/SZp3d52bqfSeIEklUSK
HCyR51QL2asAdFkS4CpwmC2WftccUOS1XCoiCvvvxIm21y7X8l6k6JoHSF6Ck5loD4gHQNbGwk5OByZ
7Gci1GMiBydrhf7L/OFnlmQ4utCPboNluEBzHsovbCbcxjmfRKQynumNBVtbPOxZU63a0zzeaqYRT77
azfiOdWFau9wo9izm2wnDshE82DUDzKRtQZ9sOHWq3QKDe7ZPZmarWszPTodQyULxloOyHEHZONUmbP
mHDNuTnfVWS2XjTqDOMSsGbRl071NnK+xVJ8olKwTCEjcklzaMgaTEORtbYwLBhVSXNWU/7qhnWozlJ
VRs2qqwRiYNalBQSEsCIokZEEBCQ7LPWBlKXFgEiNQQRA5KEh0ApN1LgKIfJwxmKoAdho1NmcYMHQJE
zCUWOUiA3Qgl42GGl8vITG1BWlHzVxuJg7LdRX5Akv/SEZW+lLdkqkdDrU6ketKiKoiT5bOxD+FPW0F
Z4KvTpJqHLZ/20YDZbkHW/84K8F5sIEUs+rnkFme775dgnZvgXsWPNXIPV8CcAAAAldEVYdGRhdGU6Y
3JlYXRlADIwMjEtMTAtMTFUMDM6NDM6MTIrMDA6MDDqDNZeAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIx
LTEwLTExVDAzOjQzOjEyKzAwOjAwm1Fu4gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5v
uPBoAAAAASUVORK5CYII=
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
