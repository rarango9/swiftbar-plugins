#!/usr/bin/env osascript
#
# ❱❱ METADATA ❰❰
# <bitbar.title>Zoom Indicators</bitbar.title>
# <bitbar.version>v1.1</bitbar.version>
# <bitbar.author>Rob Arango</bitbar.author>
# <bitbar.author.github>rarango9</bitbar.author.github>
# <bitbar.desc>Displays indicators for zoom mic, video and screenshare.</bitbar.desc>
# <bitbar.image>https://github.com/rarango9/swiftbar-plugin-zoom-indicators/image.png</bitbar.image>
# <bitbar.dependencies>AppleScript</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rarango9/swiftbar-plugin-zoom-indicators/README.md</bitbar.abouturl>
#
# ❱❱ SWIFTBAR OPTIONAL METADATA FLAGS ❰❰
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# =============================================================================

--Base64 Icons.
property iconDisabled : "iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAHdElNRQflCgcEFzkAtaTLAAACpUlEQVRIx62WTUhUURTHf+feN2NZ+YErW4SWUxB+oEK4qIE2RaZBGbpq16KWWpugwDBoF66ihWTtympTpLVo0cdCChXBPkiJikASIhtirHHeOy0csnnzmnGc+W8e7957fu9/zzv3coSU2tlAAoNbIU20SB2l/F9xnWNKp+13jxKWGE0Ny8rjMGDxqqWbLhoow5BdHjFmuKe3zbwLPFyFHUJQYzvlAq3kpwm95N4XTxkD7IqrZSfUK4PU5omCrdIuy4lX1tvJLLYdARPqlQE25Y0CKJGojeu4aATbAHBEBteJAnCkTd7adyXYHWi1XFvHBtPdRfSB+9MYpDvvtGeqVXoMxq3keMEogC63wkgT9UWB1UuToZmyosDKaDFSl7Pa1yYjdY7vDHo84xUasHgze2jG/n2P8ZrdlP+zotTxhbzQHlkI+rAlWSWnOJeqx0XOeLfMRc6mmfPFTMmCQzIDpcThW+IyV1OovtB1E+dT+ionI4okY4FJ6SDk6bCcYCN9pcPxACsOa9YPyuELH3kkK6jMf7B22HMEcfnKqAIPCoMBICRJBKPyh2VVAExyRRjoXBPMCFXZUEqZtkAwzg+rdcMLHMiGC8t5osFT/tLYK/vkSYijfGarbyqBgopSwxAneQb+Y+d3VilXdD+Om4GCMALb2QZEGCIqsCW7M2iUO/JUP+AF7MNKlBoAIgzrYw76YZnFXMUxcms7p30jcaNzgR7yl6dzhkliRYHFmDQ6zUxRYDM6bewid4sCu+ssGg8dYaJg1ISOuJgwZl4HCsxbTAfMfBhbi6KzsizRfC7KNP3Sfu+mahI7yy5UEy/tkrRRsi5X/b8HrWt4iIX31GE9HZc3Egk4Rbly1efdsK4yyt/LqwNdbUPrKS+gDYW0BrmR1vU1yH8AZNzhNkN9c0EAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMDdUMDQ6MjM6NTcrMDA6MDB9j5m/AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTA3VDA0OjIzOjU3KzAwOjAwDNIhAwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII="
property iconEnabled : "iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAHdElNRQflCgcEGBolSsl2AAACZklEQVRIx62WPUwUURDHf/P27kguyEcwJtcYJNAYAgESKiWxsoSokd7OSkOu097CRDsr47UmUptYgqUEQoIdMRoxokYPuLvFPXffWNzlPnYPjj32/7rd2d/OzHuz+xfqqpAlwKE65EzLrIxLlhOlru6y5W9nigEOFfrbb1fxUPycfWDXtaiBdlOgRfvePvRzyl+qragSLiUTLNqNrpCQ7EawVDIVjppZuXxLBXk9jItSVdXDIP81XallV8ajbIK8Pe4Jpar2OMiXjUcZFCVY7DGrZnZLioKPn4vfq2jv/JyPcTB3ZY5zSubMsoPxhrlzXhQAt70hk56WySRYMpmaNswwkEhmAzJrZByTCMzIeCo0g5Z1PqDRWO1nXmZwGheO+MhVBlsKzaKFti1e8y8pnde/EftIy/XAor3nZe3TtvNRCJUoW85PmpPWkM8+8rv4RF8AcMCKvEq78iVUabgagEEktNLkgCFrC+xzyAoFRSJPx2j+Jhbd08/6vI6KKHV22DwKAT/sWwDpsEsxYLWm4psqHfOKVWZ3xYcZNYo9E6wbXBnQWenYscjDesXLVPl+Gi5jHrNwpjLlWvp6hhGU15EJ+EWAVZRRXtZxeiqMYXlmb9gULEfeexEHHeMyMFHD6YX2iMjRkCl5k1njU8ceO2aBUQAmKOg7uRmCqRs5MyNy66SGtcSOyf1Qv12juyfsc1xZ3TW62eEj0YuOdNP427qTBEt3/G3Td8BqIrDVvoNEf8JJ2YNFRWvGpZKUcUnCUu2lKk3DV8Kl0rPZK7eavVp2LTb0Tzwb6jWyasxHi0GekrneDPJ/MJTS9wDX3LYAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMDdUMDQ6MjQ6MjYrMDA6MDAz4YBrAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTA3VDA0OjI0OjI2KzAwOjAwQrw41wAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII="

--Menu Button Titles.
property muteTitle : "Mute audio"
property shareTitle : "Start Share"
property videoTitle : "Stop Video"

--Default icon to disabled.
set icon to iconDisabled

--Default states to empty.
set muteState to ""
set shareState to ""
set videoState to ""

--Default all icons to red.
set muteColor to "#ff4949"
set shareColor to "#ff4949"
set videoColor to "#ff4949"

--Main.
if application "zoom.us" is running then
    --Update the icon to enabled since Zoom is running.
    set icon to iconEnabled

	tell application "System Events"
		tell application process "zoom.us"
            --In a meeting.
			if exists (menu bar item "Meeting" of menu bar 1) then
    
                --Is mic hot?
                set muteState to ":mic:"
				if exists (menu item MuteTitle of menu 1 of menu bar item "Meeting" of menu bar 1) then
					set muteColor to "#0fb10f"
				end if
				
                --Is screen sharing active?
                set shareState to ":dock.rectangle:"
				if not exists (menu item shareTitle of menu 1 of menu bar item "Meeting" of menu bar 1) then
					set shareColor to "#0fb10f"
				end if
				
                --Is video transmitting?
				set videoState to ":video:"
				if exists (menu item videoTitle of menu 1 of menu bar item "Meeting" of menu bar 1) then
					set videoColor to "#0fb10f"
				end if
			end if
		end tell
	end tell
end if

--Output the menubar.
return muteState & " " & videoState & " " & shareState & "| image=" & icon & " sfcolor=" & muteColor & " sfcolor2=" & videoColor & " sfcolor3=" & shareColor & "
---"
