---
name: xwd
description: Save an owned X11 window as an XWD image with an existing authorized display connection. Use when window selection, overlapping popups or image verification affects a requested capture.
---

# Capture the selected owned X11 window

Read this entire SKILL.md before acting. Require xwd, the selected owned X11 display and its already authorized connection, a window ID observed in that session, and a fresh output in a private directory. No conditional resources are required. Finish with capture status and a decoded visual check; absent display access or an image decoder remains a prerequisite gap.

Use the existing legitimate session authentication. Define `display` as that session's actual DISPLAY, `window_id` as the selected X resource ID, and `dump_file` as a fresh absolute .xwd path. Prepare the requested public/test content before capture:

~~~bash
xwd -version
test ! -e "$dump_file" && test ! -L "$dump_file" &&
  xwd -display "$display" -id "$window_id" -out "$dump_file"
status=$?
~~~

`-id` selects that window without a pointer click. Without a selection option, xwd asks the user to click a window. `-out` stores the binary dump; stdout is otherwise binary output and should not be sent to a text terminal. Record stderr/status and decode the result with the task's trusted XWD reader or supported image converter. Check dimensions and actual intended content; file existence or a completion bell alone is insufficient.

For overlapping menus or popups that belong in the requested capture, `-screen` performs GetImage against the root window for the selected region, so other windows covering that region can appear. Confirm that expanded content is within the requested capture scope. `-root` selects the whole root window and needs an explicitly selected whole-display capture. It is not equivalent to selecting one application. `-silent` only suppresses bells; it supplies no access rights or confidentiality guarantee.

An invalid/stale window ID, inaccessible display, unavailable X11 server and unsupported image format require different recovery. A Wayland desktop is not automatically an X11 capture surface; an Xwayland connection need not expose every native Wayland window. A display string or login record alone does not establish connection access. Choose a fresh destination for a retry and retain any failed partial output as such.

See the upstream [xwd selection and image options](https://manpages.debian.org/bookworm/x11-apps/xwd.1.en.html).
