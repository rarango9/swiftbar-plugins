#!/usr/bin/env bash
# shellcheck disable=SC2207,SC2038

# == METADATA =================================================================
#
# <bitbar.title>Wireguard Manager</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Manages one or more connections to a WireGuard VPN.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugins/images/wireguard-manager.png</bitbar.image>
# <bitbar.dependencies>python3,wireguard-go,wireguard-tools</bitbar.dependencies>
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
# == PREPARATIONS =============================================================
#
# Add the following line to your sudoers file with `sudo visudo`.
#
# %admin  ALL = (ALL) NOPASSWD: /usr/local/bin/wg, /usr/local/bin/wg-quick
#
# =============================================================================

# Images.
ICON_CONNECTED=$(
    cat <<EOF | tr -d "\n"
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
EOF
)
ICON_DISCONNECTED=$(
    cat <<EOF | tr -d "\n"
iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFi
UAABYlAUlSJPAAAAAHdElNRQflCRQOBQu4DYLvAAAErUlEQVRIx92WXWgUVxTH/+feO7uzu+6a3W1II
qy7qKlVUUljNCZEH4o0GrVF8aNiaRVaGig+toU+lEryoA9S7IsIDf1AqD4FWhqboPhVFmJpjUI0xs0H
lUaJcbNds5ud2bm3D7vG7KeBvvXMw9y55/5/9xzumTNDyLPNsNwVJ8V7SJinp07YUn8ilfXYUQfD7v9
UOwZn+rvpT3g8nKfl+bB1EDvsnUxnTr5Ju+O5V4nxrKcZXmi79VNsMdP4WvGH695wnpblwxwQtWQHAH
KKfWH+dM7zFGEu9pETAMjOax350kIYzZvjTWuCfrgAAC74sSbIm14o6eWwHHDA1uxBPQCgHh7YmilQb
n15GBPbL/M46lGPOC4z0Upl1wuUNd5UtyoxRgwg+XqIN5df/RIYC3jOe+IgAApuFvhPMDC+Ggs2tvCl
/yOYAwpQC1IqBUd52EYQ1Ly5XO78J8UIG/Ngog06ZjGDCSzCMGJ4pIcanzvTfeYF7ajYnH0Km13afrE
t62y8oztmPQgijhBc0DELHtwv3zYDVvzN6b9QAx8c2/TPyJaJw+x0dEVv2OpZAEiHY0c8fYbG38q8kx
Sw/14x7IXAAURCtMPabdYIexdzcWkbufl14qxrtgm/bWeu+Wn5h1JnRCNgnfEPAWouU+bSWzf/8iuS+
rUPF33MlhNjM/y1ToCIfHybA+M3DGk6RVsmMgLpprLW8v1sJQjCJGudOMRXZDdKGF89vjsqln5u72CV
RADZaNfcXio+e4D3jGjLTts+mndkICocA8aZkWPLTGu7fp7cRU6T3OLwAF9iJk9Yt+fm6IV8/ti6nTy
5xBzg4vALVF5p8PWv+iz4x4wONVO2xBJGh380jVofX1+6zjzCZcNDjHWbP5SDmd+PdT+EDpuLPCVh5G
MhgUVYmpNqvlm3kycDphsCFIKvNMyltU+5BRLwlUxVzRgdvtEkBKJurZ1cJWEA31t51mph1d1IX1KRo
rBI+lI3WHW6xXdW7M315TVH4tpBsUu7WveOJskqBiNLk3Ue9zfa1tyoikSWSZYH7ZppqXTRyNKmpWs8
VIgq0c+oQvdeicv7xXzy/pW43UuLi/nmYCqV7rHCmS5DVaJhJ1LnZLwAFU+d2wnRQFUZkRVO96hUIez
W5KFEu5wEABJiz6AY7DWOy39yUDHj+GDvoBB7SACAnEy0Tx6StwoPIOZ8ZkZVMpvo1IjVoq6cahmwHW
S10ACYctj48fqlRnmdVk5lA0iaUeczihXCKHsBUIbV06ZiyzZEHX1v9F1wKAaQ3Je8jA1e5W0bMXv4E
bLlaoqURnbHB6n+h2JpJ6syvv3pphZlEpDs55Bo8L4vH4++W9mvRWhVoa4oTF5bOzG4km9hS9hW2yRi
sABwLKZXiNPf1ctXD0WusoXBlGFdHIe2hdUAxKgKVTnHX6NtGR+yLvKjmRZatDRo7qYiqf67grWi8Ac
MAIi13hWpfhV5LqJcmErIR3KGoKCi8onVu24iuII3ooTxxuCK9RNWr3yiogoEOSMfqQQACHOAVRhfmD
eZQ8nEFP+AzaanH0BtsqpJFfsaE1S12jR8L35KdEk9MeWRyQ6Z1Bq0L9X0v1n3vimug0aPAAAAJXRFW
HRkYXRlOmNyZWF0ZQAyMDIxLTA5LTIwVDE0OjA1OjExKzAwOjAwwIlEpgAAACV0RVh0ZGF0ZTptb2Rp
ZnkAMjAyMS0wOS0yMFQxNDowNToxMSswMDowMLHU/BoAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2F
wZS5vcmeb7jwaAAAAAElFTkSuQmCC
EOF
)
ICON_ERROR=$(
    cat <<EOF | tr -d "\n"
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
QmCC
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

# Builds out the menubar.
build_menu() {
    if [[ ${#CONFIGS} == 0 ]]; then
        add_line "" "image=${ICON_ERROR}"
        add_line "---"
        add_line "No confs found at /usr/local/etc/wireguard" "color=#d40000"
        exit 0
    elif [[ ${#PIDFILES} == 0 ]]; then
        add_line "" "image=${ICON_DISCONNECTED}"
        add_line "---"
    else
        add_line "" "image=${ICON_CONNECTED}"
        add_line "---"
    fi

    for config in "${CONFIGS[@]}"; do
        if [ -f "/var/run/wireguard/${config}.name" ]; then
            add_line ":stop.fill: ${config} (active)" \
                "bash=${SWIFTBAR_PLUGIN_PATH}" \
                "param1=disconnect" \
                "param2=${config}" \
                "refresh=true" \
                "sfcolor=#d40000" \
                "terminal=false"
        else
            add_line ":arrowtriangle.forward.fill: ${config}" \
                "bash=${SWIFTBAR_PLUGIN_PATH}" \
                "param1=connect" \
                "param2=${config}" \
                "refresh=true" \
                "sfcolor=#009800" \
                "terminal=false"
        fi
    done

    if [[ ${#PIDFILES} != 0 ]]; then
        show_connection_details
    fi
}

# Parses and turns `wg show` output into a colored table in the menubar.
show_connection_details() {
    local first_line key val

    add_line "---"
    add_line "Active Tunnels" "size=14"

    first_line=0
    while read -r line; do
        if [[ "${line}" == interface* ]] || [[ "${line}" == "latest handshake"* ]] || [[ "${line}" == transfer* ]]; then
            key="$(echo -n "${line}" | sed -E 's/(.*):[[:space:]].*/\1/g')"
            val="$(echo -n "${line}" | sed -E 's/.*:[[:space:]](.*)/\1/g')"

            if [[ "${line}" == interface* ]] && [[ ${first_line} != 0 ]]; then
                add_line "" "trim=false"
            else
                first_line=1
            fi

            while [[ ${#key} -lt 18 ]]; do key+=" "; done
            add_line \
                "\033[33;1m${key^}\033[0m \033[36m${val}\033[0m" \
                "ansi=true" \
                "font=Menlo"
        fi
    done < <(sudo wg show)
}

# Toggles a tunnel if selected in the menubar.
toggle_tunnel() {
    case "$1" in
    connect)
        sudo /usr/local/bin/wg-quick up "${2}"
        # Wait for connection so menu item refreshes instantly
        until [ -f "/var/run/wireguard/${2}.name" ]; do sleep 1; done
        ;;
    disconnect)
        sudo /usr/local/bin/wg-quick down "${2}"
        # Wait for disconnection so menu item refreshes instantly
        until [ ! -f "/var/run/wireguard/${2}.name" ]; do sleep 1; done
        ;;
    esac
}

# Main
toggle_tunnel "$@"
CONFIGS=($(find /usr/local/etc/wireguard -name "*.conf" | xargs basename -s .conf))
PIDFILES=($(find /var/run/wireguard -name "*.name"))
build_menu
