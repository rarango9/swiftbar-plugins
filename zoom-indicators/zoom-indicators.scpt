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
property iconDisabled : "iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAHdElNRQflCgsFFAeh7T8sAAADI0lEQVRIx6WWQWgUVxjHf9+bmbW7mxCMYNEGIa0YunopNgdPG0Vo2t0FC6kBoZBLQNEevBiFiiBSzLGg9ODFU2BVEEwsoQdljmKlnvZQqW1ppBAkxmR3aXd23+dh12Qn7GZnk+8289785n3/733v/QVGiRNAjLScIs0AHtEiYAFfZ9Q3FYf/mEe+oMBn2EG5xBg7I2Ka4w339Lq8fM5B5AQ19LD8xHDjb0uU0AgQIUl/I4tf9bR55iA59GPJ8zlQZo68FliVCCyFXkkxTpYE8FTH+VMyMXODSWCRKZ2RigIRYQgak1NMsxu4pedcSTMGlJniNijKw4hiZQAq3AZukmCMu87QZY4A9/UqNWGOF5GVf8HvDKFQkEMcJC41QxoIyEsFZrsu5SwgFfIEQNowACxpQSOVsJV2ihZYAgYMHlBilchaheMhQJES4Ll1fJT6tQsBW0/LbX79JRav7cZQLLK2/gwgNMRpfNIEy6B8QC1OrA0tiJWr5FghiYPiUk1q2aqzNqEJZtnD4gn5jr7WtZBi7Rdu8bq3/rizNiHHnHPO37SCOSzulR/4dBN5RiSlZyiqK8flAiOs0Nc8bJqFlF182EHtkzJS9cw17nAUoRrOwd0wudNmi5FyFzlLT6tBQ7fhSh87Wg91D9tk/VuDtYkwLGojtJkXhgXUIuT4lv87whT9l5cdWW71N26y2gFWxSzrjyxvviz9ywvs95zkMYobTjjUAZbaHbfIBPvaqGL1kT4AqTKvT2SCY7wNSZlT4A/SvJoli2Kwrkm0hqktFZMKdq3RbdmqBx/h88mGDpjjq3q+K61zFOIoRXwgQ4CUJFTBDe30c0f938f6uZxb28R1mGzt/G8kD0YEwBAASXob92DXkQHoIQkEhgWgX1ISeftv1FEgRT+wYPABj3Ebg1zXqBxgYzKOB/jOgbJkiTMo/8hz5QD7I9/pGYbqK/uW83i80SsuPveYJME06IypGLJdGBdbNy4J4C6+ZGFQ8gyzbqmKYjvyVA09pCRsqb6mun2z91TPyDMXGWWeHDooF/lmOzZ0llFk3SBLmi0ZZHxpGOR3XpgclRW5U9MAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMTAtMTFUMDU6MjA6MDcrMDA6MDDX+Vf6AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTEwLTExVDA1OjIwOjA3KzAwOjAwpqTvRgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII="
property iconEnabled : "iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAQAAAACNCElAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAHdElNRQflCgsFFyVfoC0LAAADDUlEQVRIx62WPY8bVRSGn3tnPAm2w5KlQGIFUgJIkSWQIkgNRFqJggKliMu4BAH/gJI/QIFQlmILKqdEKSKKoC1RiBDNNgQDUhAJIs5+2N54Zu55KWYVxruZ9azDO83M1Z1H95w558wLPEQE0iSs2roGSlVXqQa2HlbTxBAPAB5wBZGdsTUNa2PKGtpaflZcYYgTEN70X7kLAGQMGSPmy9FimQaAfrQPo9vgDDvr++4tYMJ19W2T3agGK8Ap33Fd3qcJuhW6/jfSxNYkSfetlyUiJ0c1rmJfmlhP9yXJ1tKEsKqhpLH1jEDgUY1TFZoSCBjW01jSMKxi65KkfpqEWqmaVVEH6kuSraOBpNQuiXBsVJE7ES4plTRAqaR7+bmc6UKwKYH8nO5JSj0NYMwunFgIdgJwI8ZAIy5Cr1MMVfJgRbrj8vI2KaepAmekxJzcf3qEw5MXmXbFWgm2h/Es+TMkVbTWJEf8zGs0MTx5K0yyUgmUYDlt7IPoU5aeXCPxyL7T1/rndQTotHrRxeYn+qO0RZJ0RysiJ3vRNo/uavsmbeeksb2nmzJt6Q0htKI7kuT/w0bEz7sXjk62uxy/s9OIPnfXeBdHPhtDfGD3vCZIXGfpb/8x7YrvekzFfqmqJI8PO+L8i8EqNAtzNd+q2FeCCWV1RodtV82EEsywvzSYy4p3frIv2Z0DGxFt6Qu2jkTJfl/K8s90me8R8WzApTprkjG91hy5nnu5IitmN8O3nih3N8IPvsdFtssJdBLwK2/zpyNDNJjGSdO5J7N+Gb0qxx6t/UafTjI9Byts8MqBDmgwooHP2amK8iUCm5xnfwSNZ8fVgXZqU1cnH9/pcREXMLfYz2Q/ePDeAXgyoMUp2FsItQeoTQvIPHeBZdeJKgfs0UpwuA7LwF2vDaDhulkyf/4cloA8cV0aoI1D9mByjAAP2YOsZFzSRARCLeNSgErG5WqWuICdifruAjDRdfW16Ube5s4PmVfbdVzXlSzV/2P2btlH0W1gCIUNvfp0NhQeAmwhAtlTGuQh8C9Rhcgtxl6G3gAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0xMC0xMVQwNToyMzozNyswMDowMLJB6xoAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMTAtMTFUMDU6MjM6MzcrMDA6MDDDHFOmAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg=="

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
