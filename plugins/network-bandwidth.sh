#!/usr/bin/env bash

# == METADATA =================================================================
#
# <bitbar.title>Network Bandwidth</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays the current download/upload bandwidth.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/images/network-bandwidth.png</bitbar.image>
# <bitbar.dependencies>ifstat</bitbar.dependencies>
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
# =============================================================================

ICON_GAUGE=$(
    cat <<EOF | tr -d "\n"
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
K5CYII=
EOF
)

# Add a line to the menubar output.
add_line() {
    local params text
    text="${1}"
    params=""
    shift

    [ $# -ne 0 ] && params=" | $*"
    echo -e "${text}${params}"
}

# Captures data from the network interface and outputs the current bandwidth.
output_bandwidth() {
    local data dl_kbits dl_speed ul_kbits ul_speed

    # 1 sample over 0.25 seconds, data in kilobits per second
    data=$(/usr/local/bin/ifstat -n -w -i en0 -b 0.5 1 |
        tail -n 1 | sed "s/\.[0-9]\{2\}//g")

    dl_kbits=$(echo "${data}" | awk '{ print $1 }')
    ul_kbits=$(echo "${data}" | awk '{ print $2 }')

    dl_speed=$(scale_bandwidth "${dl_kbits}")
    ul_speed=$(scale_bandwidth "${ul_kbits}")

    add_line "${ul_speed// /0} :arrow.up.arrow.down: ${dl_speed// /0}" \
        "image=${ICON_GAUGE}" \
        "font=Menlo"
}

# Takes the bandwidth in Kbps and keeps or changes it to Mbps.
scale_bandwidth() {
    if [ "$(echo "${1} < 1000" | bc)" -eq 1 ]; then
        printf "%3sK" "${1}"
    else
        printf "%3sM" "$(bc -q <<<scale=0\;"${1}"/1000)"
    fi
}

# Main
if [ ! -e /usr/local/bin/ifstat ]; then
    echo "Missing ifstat"
    exit 1
fi
output_bandwidth
add_line "---"
