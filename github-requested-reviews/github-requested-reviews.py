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


COLOR = {
    "gray": "#737373",
    "green": "#58f158",
    "red": "#ff3434",
    "white": "#ffffff",
    "yellow": "#ffd735"
}

ICON_DISCONNECTED = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0SDwXNblL8AAAEe0lEQVRIx+3W32+eZR3H8df3vp+nXdutg9S0j
A1isrF1ywpzRkmEanXBkrUgaHQRkGg0HshIAGUceEA82JS5ME0AD4wZiSQzhqOtkx8JukI0BJu4ZWOr
MpxmJPtFxXV52q5Pn/vyoI+1W1vHH8Dn7P5e+b7v6/vruq64W1K0xgPxLV0ajRhMz4webE0M+J/6NBv
XZPwz8U3b/XO/+RR3SStil3s1zNjO2pGeM1X4HfiiRklIy+M7vqvwWSfnh5WK1myXLZfZOvwkRrPnJ7
DWSglpcXwlHrEBp6SkB6GsJHlpxjGLb7gXTPmLV5wCTbbVblykz8eRstST7fVLG6ZdUn44irzIa3mRl
eXu0TcT5pBPYio9ZXcxmnXGs7qRfNueJFdbE1vd79qZ34+nQRUBUXMkvRAncxf8ASXrwRG7jRBH0tNx
qwbhlkytvXZ/PGTlZUloijtnfX017koP1oZbpsPUCM4Vo4VC4j0T007VlvhRPH0Faq4+FY9Us1SHjYB
1WWeupCw+b8l0TRsqaacdzriabi0tDZCv+bR1WBrr0wcWF/fF4xZjPO0s3vXvNb9/fzBarJzVOBP+aN
gJJ2T1TI7Er2Psb4j+nviNDjBpwpLp1NpXuy8qIckUDdEbj+mWg/ds8neZmh97HLytx/v7kVUG7TAOG
rTWUW+nJ/MKA0ISk7G/+HJ62PHpzjBpyqSa2pXxZi0pPed7jkv/Lb196QGHqmoYMGBSiA/yX6Q+O52X
C+afgAxT8Xz6mn/ULXtrX49DU0perhtetU/Nvzh5/ol0t72qC1WiNGCzEKeN1S1n87HC5WPOS+jXJt6
s/TlbsKyZ6XGOGUtwYGZXszVgVBLz5GpmZ1ftoll64yrr2YeifEh9BPsItjBsM2bGnES/3v/rdKc+6Q
qfzcj6ZUJaprm+0FE0h9C/IKofodZUPwVpTteHTL98NSUPxs+sqs/n2tiYjmdnpqxyYh5Ur6TEhvxZX
1IG18QXUsVRRb48GrfabdnMqJesiW5/ys+Ed+aBdSqxIV7QXUcRPha9caHyVr6+J37uGjCpokGgPa6v
7Y9qxcUrUCtcp2jJntFdz9VFIUfZxvJQFlvrsb+RtqRNaZtz4I7s9swn5uzrFpnsdneAc2lb2pS21A+
Tjni4pAecSg/FkaQ8VBU7haa4LV5Jc2BJcJsmpPTT8q6qGErvxgE34HOZNnCsGK6pqnKwHtt16tfRbO
X1FVx0sKqqphh2DLRlLoH2rDWbvitWWATGZjfSrIZSP+AXWRFymaxVO7iUOQq6PKpNOd0c39eAlA6l+
sththolDktoiMfSzcraPKoLHCmlPdGlQSmesDk/Z50bwPH0WnJ6DuyMa3kthq1Fdwzkx7TrUsJk2pPf
9Ne4yXpkllllKRj3w/z1CYNzYKfcqPFCquhVxlKrLKvP94tpe955Kb0Zy62ele2znky/SkW2QNPiaFy
w0eIZ46QX0w+y83kno+lVp6NDm5IRL6dtld82FBwwn96xmmLsrfJQLNGh2SWH01Npe3Y+/Adjb44fHC
4lHAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yOVQxODoxNTowNSswMDowMH4jCM4AAAAldEVYd
GRhdGU6bW9kaWZ5ADIwMjEtMDktMjlUMTg6MTU6MDUrMDA6MDAPfrByAAAAGXRFWHRTb2Z0d2FyZQB3
d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_MISSING_CREDENTIALS = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACVVBMVEX/Skr/SUn8SEj9SEgAAAD5R0
f/UFD/UVH+SUn1RkbnQkL7SEj/S0vhQUGHJyf6SEjVPT3WPT3pQ0P2RkbzRUX4R0fxRUX/TEz3R0fvR
ET9SUn/bW36R0fuRETzRkbJOTm7NjbKOjr0RkbrQ0PtRERVGBhcGhr/TU3sQ0P/T0+/NzfDODjlQkLi
QUH6SEj8SEj+SUn/SUn/SUn+SUn8SEjOOzv9SEj+SUn/SUn9SEj+SUn/SUn/SUn+SUn7SEj7SEj+SUn
/SUn/SUn/SUn6R0f/SUn9SUn5R0f9SUn+SUn/SUn/SUn8SEj/SUn+SUn+SUn+SUn6SEj0Rkb9SEj+SU
n/SUn7SEhgHBzNOzvgQED+SUn9SEj6SEj3R0f7SEj+SUn/SUn9SUn8SEj+SUn/SUn9SEj8SEj8SEj+S
Un9SUn8SEj9SEj+SUn8SEj9SUn+SUn+SUn8SEj8SEj/SUn/SUn2Rkb9SUn+SUnwRUX9SUn+SUn+SUn/
SUn/SUn9SEj+SUn9SEj+SUn8SEj9SEj+SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUn7SEj+SUn5R0f9SEj
+SUn/SUn/SUn/SUn/SUn/SUn/SUn/SUnZPj79SEj6SEj9SEj/SUn+SUn+SUn/SUn8SEj/SUn/SUn0Rk
b9SEj+SUn+SUn/SUn/SUn0Rkb6SEj7SEj3R0fzRkb+SUn9SEj6SEj+SUn+SUnXPj7XPT39SEj+SUn/S
Un2Rkb7SEj7SEj+SUn9SEj+SUn+SUn5R0f9SUn8SEjYPj7aPj79SUn/SUkAAABKNdUiAAAAxXRSTlMA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADmrL+OytQQE6mh8cqPn
obgQbf+XjIQ72YAxfz+Iga/vOuNYeAkCz+iMBAwLMhBMFLcL+YSeT7resrap9IVCQFnHcyig08ZkLl5
gCdYKF588RrHTpRjSk9PfAt93UFUCxBk2//CYEBgOKFAEwEWmHYInqLN6dCjiMHBOGAwMsCgmdLQSy1
wEBR+yaBRMuw2Bh1R0cQAEBrBtUlWIAAAABYktHRASPaNlRAAAACXBIWXMAABYlAAAWJQFJUiTwAAAA
B3RJTUUH5QkdEg8TObrnrQAAAr5JREFUOMvtlNdXE0EUxmdmg07c6IIxJlnBBopYAgEbSUBBiYqQBCv
SrSjBRsReglHESOyKUSzYwI6FIlbU+b+8u2TDBl88x1fv08zO73wze8uHELakZ1hZZtb8BYTTyBE3io
xeuGgx1gwHotk2O5PCkZNLtPBlDOXxkqV5+ctisOU2FokCp26sZhwR6IqVqxgrXM3HxyeM108YwopAq
9jlLgTOUyIYJnJr1q5bD5vCDRtLS0s36TijScLKgCqvqKyqZqxmMya6LVu3DWlv31FbW7tzVx01JgBm
ZcxVQfTYC6r1ut179rLY2LefCoDByl2pN5MGH2MHGg+yP+LQYQNgmfCMKkyMR2oYO2qsO3Z8JHbiJOQ
JnYJVtbfB3wTPOS2SSYEzZ+XT5nMtLS3nYRG8AJlBrQ5Y2n2gxUKNJsFEL166fAU2+VevXb9xU8LaJO
xWTkFEPRgWEzU84fHtOx4pbxjj9ihGcu96JKmCUFg0J0lVQDyqu3c/D6qgwjiCHnTA7uEj0Ryp6eQpZ
OrjJ0+pGtPoaWcQdl1iYlK0hLyBPnsuxGAa3CZh7epKa6bxBuEvsKH4j/07Nj1SLEqSY6GUOLFLwjqp
SS79C7n0L2kKp6ZEs/jqNRx0vEGEQ6TbKTdS89swl5Si0jKL4ZDUijXvnN0EvVe3ZdwwJojhoDLnOR9
GNPkMhZppagxJUj7JORytkZEJyCPTQ6NyBtoDtzT5A16Yc5alDGCqXxpApFcwLToKWv5UgqvAN3oj4z
xLHuc+RBWMoj7GfAGSrO13AxJrDoiPtjmqhyd7sZZ8dDFmjVhN/8AnuOMzTlOwNPwFXlE90F9RXsxYh
tq4vn4TZivYHKHEI9mX2wWUPR1Z1DY4dzhv83ROJaHMZkH4+whTVX6V5OY45AO7LRujqEUP/iAxNeXI
z8FfvcxaVmTB6De1ss0l3cTC8AAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yOVQxODoxNToxOSs
wMDowMHUpYiQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDktMjlUMTg6MTU6MTkrMDA6MDAEdNqYAA
AAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_NO_REVIEWS = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCR0SDQsY4B15AAADyklEQVRIx+2WTWxUVRTHf+/NTGkHW6NV8KOih
ESJEdIFfsTEpGxkZcLGnYllKSSNJt0aIyESiTEm7kzcuWgMXVQXJXEBgY0K1MTAgEaNFgktFipQ3nTe
u+f8XbzHdDqdaeOes3z33t8759xzz/kjRDoQDvpZLUta8MmwdyYKGK3WQASEvepf6GnRxRwb8gk1tGJ
zPpaVA3eLHddwMkT2pH+gq7qi7V1h6YBPqN0SGxV/AUcJpDiNB+xt/0mSNKtnMi5ykRrzJNxphYVDhV
eZz/gJzeY0r6XbUpa5hbEU24h/q7T40Wy2YzQ6XzpfOl/6MxaGqDfDPJej7Eg6WK9ku/x0TrMDeZbCc
/65bq7yejocD5NhMkz61/Z+2O6IWg7TsiT5TDoYSBC2P/fUPxNhi73nv2ld8x/DTicFIGYTANftdkoD
Q3+zDBD11TdHH8afRjtY16IX43dvx17AbgBEz5d39tFPiWgv/QCa77urY/qIOTaw6OX+BytFzo4X7p6
2/WGPjft8npnwuuWVtce/0lJLXHWd0rSmNa3fiy8X9GhRLNmI5oqPDd2SF+ipZHOdlDpOo8fe8JMKxa
4relZl9aikY03YIwXsl8jHlLRl9YINGymQEcgQ6UP2jtfu1ZkQQkfXwAJZ2Ue9ds8nJT5lw8YiN5svQ
GSIsN0/1nVdzV9AR1iemfCC/iiWvlyqGottb/MOPxD4DnvFP/Eh7wIrl0jopXSNpDg335cYorQK1g9k
vEb0fXK2p+u9xlAlgmjlpmN6eLjD1go/Y5StzekWK29URa320gbr8f+BbWT3Yfdh3WFLCFaml0Tgn3U
P3aCBt52pA7HRS0R4nGqxsLVRjYm7vxmMmDJJn7YWH6r+REQFg0BattYWVPdvbNi4mffzDl4tYtiwTz
W7oPslG03LAS51bY6NjrAUw4Z1oX1s+9ilaN22/eYa1FvUSTb71D2fdKspLOaykVUDxVoGiu3zDr4t4
9i+PBKft3HbY/uLsS2fRAvF0N9V6Jzx3Ds/rGa/XLG7CD9czPzx/ES2KxcVvhAzCKBauFznXwydyrVI
9Bj0roH1FSvAHU4ZiyRkl1UDiAbjIpYtpYEeqpSIhnKGEjqUhxUrQC9DJapsojLAFgAaq4RLUsl2+5k
iiFGxVocJ4QeKRJzOdieVdNCOKJMkP9tNUl1sPJVycg3sDCnptmKCSrN+wmdylBrh4Dpi72rHOptF2O
iaypRPpANoQxnafp+BrOxjzeqUpIZP2JDyLLQJ5JHLawTy6ksI/BqFETvuC5KW/Vw4lA4I8R8KtS9L7
8HM4AAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wOS0yOVQxODoxMzoxMSswMDowMEvYXAQAAAAldEVY
dGRhdGU6bW9kaWZ5ADIwMjEtMDktMjlUMTg6MTM6MTErMDA6MDA6heS4AAAAGXRFWHRTb2Z0d2FyZQB
3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==
""".replace('\n', '')

ICON_PENDING_REVIEWS = """
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAMAAACf4xmcAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACqVBMVEX/4E//3E782U392k0AAAD510
z/8lb/9Fb+3E7100vnyEf+20772E3/3U7/4lDhwkWHdCn82k362Ez72U3VuEHWuEHpyUf21Evz0Ur62
E341kzx0Er/4VD/5FH31Uz/5lHWuULvzkn/5lL9203//3T9207610zuzUnnx0f/30//4FDz0krJrT27
oTnKrj7000vrykjtzUn31UvuzkntzEhVSRpcTxz51kz/6FL11Ev/3k/sy0jry0j/7VS/pTrDqDzlxkb
iw0X62Ez82U3+207/3E7/3E7+20782k3Osj/92k3+207/3E792k3+207/3E7/3E7+20772E372U3+20
7/3E7/3E7/3E7610z/3E79203510z9207+3E7/3E7/3E782k3/3E7+3E7+207+20762E300kv92k3+2
07/3E772U1gUx3NsT/gwUX+20792k362E331Uv72E3+207/3E7920782U3+207/3E792k382U382U3+
207920782k392k3+20782k39203+3E7+3E782k382k3/3E7/3E721Ev9207+207wz0n9207+20782U3
+207/3E7/3E792k3+20792k3+3E782k392k3+207/3E7/3E7/3E7/3E7/3E7/3E7/3E772U3+207510
z92k3+207/3E7/3E7/3E7/3E7/3E7/3E7/3E7Zu0L92k362Ez92k3/3E7+207+207/3E782U3/3E7/3
E7000v92k3+207+207/3E7/3E700kv62E372U331Uzz0kr+20792k362E3+207+207XukLXuUL+2079
2k3+3E7/3E721Ev+3E772E362Ez72U3+20792k3+20772E3+207510z82k39207920362E382U3YukL
avEP9207/3E4AAAANgXqfAAAA4XRSTlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOasv47K1BATqaHxyo+ehuBBt/5eMhDvZgDF/P4
iBr+8641h4CQLP6IwEDAsyEEwUtwv5hJ5Put6ytqn0hUJAWcdzKKDTxmQuXmAJ1giGF588RrHTpRjSk
9PfAt93UFUCxBk2//CYEBgOKFAEwEWmHYInqLN6dCjiMHBOGAwMsCgmdLQSy1wEB6UfsmgWQExMuw2B
hLtUdamAcDkABAaxV1pt4AAAAAWJLR0QEj2jZUQAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAAd0SU1FB+
UJHRIODkOnujUAAALhSURBVDjL7ZTnX1JhFMfvcy+WdtG6aBGkFBEabZtqm0RbMiwtrUwBm+ZuWtGUb
GiLosxI2mWUDVvatuFsl5bV8590LnAF7E2fT287r85zn+89z/mc8SMIpJwRq8Jx8TNnkRTPaX7dyO6z
58xFPI8R/glqDWZNq0skA+BLD5ofOG9+UvICH2yhGrstJTWoJ68XI6AXLV6CcdrS4JCQ3n2EfV1YOsT
K0BvSgDNmisT9qGXLV6yEQ9qq1VlZWWtCqTAJi2UDlZObl1+AceHaQCZo3foNrtgbNxUVFW3espXuPw
AwFcb6XFKITBB1W+j2HTuxr+3aTYsAA8+QJ5QyxWaM95TsxX/Yvv1iwOIgjXzEDDxQiHFpWNnBQ12xw
0egTsRR8ApMxZZjkM5xGTnIeuKk87b8VEVFxWlwbGegMkSlFlyNGWJhe4lEJKHPnjt/AQ7JFy9dvnKV
xapY7JouxR3d5pCH84IZPrp+w8jWDSFU3YkxiTeNbKgUu0MmjYASDVbwh5Tdup0EXfDCKFJxpwZOd+/
Jpe6eDh3GDL//4CHtjfGEdK0NTnXy8IjOFvLF9KPHIh+Mh6pYrNq707wRwWLBX2Au+4/9OzbS3SyaHO
ULRfpRdSxW6z+abT3xxNn6p3Qk5U3JpLJnz+Gi5oWCpAiyPtU5SOUvHdSYSA81Vipz2NlRLHyVWk8Sr
73H0s+DCeQOG7fnujddhnwcR42XlNjZUGZWObSV7pWxWhrgr0Z6AoeJ6UZ4pcFiNcGe43huAaMs7AIq
hBwWHVMKsSxRDMoH3Whyr/NE5zo3x9AcRsc0Y2y2MpOiWwyA+IhDq4LfOeaKVkjZhKLJt3qMVS6pedf
y/gO88RFN5rDJ6BNkUfC5JTcnA+NYb+H68lUwhcOmijKNrHwZ9EBp2gilRwbbQ6d56jY9qJ0rKFYrCf
Sti6i6LYBM1GmdFxp1AiII9L3NKdEdPxifnlLMz45fTViVna5ExG9rHh8qX+kyvAAAACV0RVh0ZGF0Z
TpjcmVhdGUAMjAyMS0wOS0yOVQxODoxNDoxNCswMDowMPs8aNoAAAAldEVYdGRhdGU6bW9kaWZ5ADIw
MjEtMDktMjlUMTg6MTQ6MTQrMDA6MDCKYdBmAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3J
nm+48GgAAAABJRU5ErkJggg==
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
                 color=COLOR['red'],
                 font='Menlo')
        add_line('---')
        add_line('Access Token and Github Login must be set',
                 color=COLOR['red'])
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
                 color=COLOR['gray'],
                 font='Menlo')
        add_line('---')
        add_line('Cannot connect to github.disney.com', color=COLOR['white'])

    # Show normal when no items are requesting a review.
    elif response['issueCount'] == 0:
        add_line('00',
                 image=ICON_NO_REVIEWS,
                 color=COLOR['white'],
                 font='Menlo')
        add_line('---')
        add_line('No Pull Requests to Review', color=COLOR['white'])

    # Show a colored icon to notify the user that there are requested reviews.
    else:
        add_line(F"{str(response['issueCount']).rjust(2).replace(' ', '0')}",
                 image=ICON_PENDING_REVIEWS,
                 color=COLOR['yellow'],
                 font='Menlo')
        add_line('---')

        # Loop through each PR and format them for the menu
        for pr in [r['node'] for r in response['edges']]:
            title = F"❱❱ PR #{pr['number']} • {pr['title'].replace('|', '-')}"
            subtitle = (F"{pr['repository']['nameWithOwner']} • "
                        F"Created {parse_date(pr['createdAt'])} • "
                        F"by {pr['author']['login']}")

            add_line(title, href=pr['url'], color=COLOR['white'], size='14')
            add_line(subtitle, color=COLOR['gray'])
            add_line('---')


if __name__ == '__main__':
    main()
