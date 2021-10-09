#!/usr/bin/env bash
# =============================================================================
# <xbar.title>Menubar Positions</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Rob Arango</xbar.author>
# <xbar.author.github>aranr018</xbar.author.github>
# <xbar.desc>Reorders the menubar icons</xbar.desc>
#
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# =============================================================================

# ----------------------------------------------------------------------
# NOTES
# ----------------------------------------------------------------------
# defaults find "NSStatusItem Preferred Position"

killall "Hidden Bar"
killall SwiftBar

# Position Tracker
INDEX=500

function position() {
    local domain item
    domain="${1}"
    item="${2}"

    defaults write "${domain}" "NSStatusItem Preferred Position ${item}" "${INDEX}"

    INDEX=$(( INDEX + 50 ))
}


position "com.dwarvesv.minimalbar" "hiddenbar_expandcollapse"

position "com.ameba.SwiftBar" "gpu-toggle.30s.py" 
position "com.ameba.SwiftBar" "memory-usage.3s.py" 
position "com.f5networks.EdgeClient" "Item-0" 
position "com.ameba.SwiftBar" "wireguard-manager.10s.sh" 
position "com.ameba.SwiftBar" "network-bandwidth.3s.sh" 

position "com.dwarvesv.minimalbar" "hiddenbar_separate"

position "com.scaleft.ScaleFT" "Item-0"
position "org.pqrs.Karabiner-Menu" "Item-0"
position "sh.chef.chef-workstation" "Item-0"
position "org.pqrs.Karabiner-Menu" "Item-0"
position "com.microsoft.OneDrive" "Item-0"
position "com.google.drivefs" "Item-0"

# Restart All The Things
open -a SwiftBar
sleep 5
open -a "Hidden Bar"
#killall -KILL SystemUIServer
