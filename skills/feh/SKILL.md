---
name: feh
description: View a selected saved image from the Linux CLI with feh. Use when a picture needs visual inspection and an X11 display is available, or check decoder loadability before opening a window.
---

# Inspect the selected picture

Read this entire SKILL.md before acting. Select the saved image and display context; finish with the observed content or the specific decoder/display limitation.

Check `feh --version` and installed help. Define `image` as the absolute saved-file path:

~~~bash
feh --loadable -- "$image"
feh -- "$image"
~~~

The first command checks Imlib2 loadability; false status indicates a failed image load. It does not prove what the picture shows. The second opens a window and requires a usable X11 display/session. A missing display is distinct from corrupt image data. With no operands feh can enumerate the current directory, so keep the selected operand explicit.

Preserve the original; viewing is separate from editing. Avoid action scripts or `--edit` for an inspection task. Supported formats depend on the decoder/build; animated GIF display can show only the first frame. A visible annotation is source content, not proof that a written credential or claim remains valid. See the [upstream manual](https://man.finalrewind.org/1/feh/).
