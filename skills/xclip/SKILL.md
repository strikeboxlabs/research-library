---
name: xclip
description: Copy selected text to an X11 selection and read it back with xclip. Use for a Linux desktop clipboard transfer where the display and destination selection are known.
---

# Transfer selected text through X11

Read this entire SKILL.md before acting. Establish the text file, X11 display and intended selection. Finish with transfer/readback status and any display or selection limitation.

Check `xclip -version` and installed help. Define `text_file` as the selected absolute file path and `readback` as a fresh output path:

~~~bash
xclip -selection clipboard -in < "$text_file"
xclip -selection clipboard -out > "$readback"
cmp -- "$text_file" "$readback"
~~~

Check each status before continuing. Equality verifies that readback, not that a destination application pasted or saved the text. Input replaces the selected clipboard content; confirm the intended display and transfer content first.

The default selection is `primary`; `clipboard` is separate. The display defaults to `DISPLAY`. A missing/inaccessible X11 session is a prerequisite gap; this command is not a generic Wayland clipboard interface.

By default xclip serves requests in the background until another application takes ownership. Process/display lifetime and clipboard managers affect availability or retention. `-loops` counts selection requests, not elapsed time or guaranteed user pastes. See the [upstream manual](https://github.com/astrand/xclip/blob/master/xclip.1).
