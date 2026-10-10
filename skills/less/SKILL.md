---
name: less
description: Inspect an existing Linux text artifact interactively with less while preserving literal content and search context. Use when wrapped lines, terminal controls, inherited secure mode or a privileged parent obscure content or child identity.
---


# Inspect literal text before interpreting it

Read this entire SKILL.md before acting. Use an existing working copy; identify what configuration/history is in scope. For a selected pager shell/privilege assessment, read [pager process context](references/process-context.md) fully before that action. Finish with the needed source lines or actual child identity and its context, not a conclusion drawn from a wrapped display or parent prompt.

Define `file` as the selected path. For plain configuration text with possible long lines:

~~~bash
LESSSECURE=1 LESSSECURE_ALLOW= LESSOPEN= LESSCLOSE= less -N -S -- "$file"
~~~

`-N` displays line numbers; `-S` chops long lines instead of wrapping, and horizontal arrows reveal the rest. `/pattern` searches forward, `n` repeats, `g`/`G` go to the beginning/end and `q` exits. Check local help for this build. The invocation disables the external input preprocessor and requests secure mode rather than allowing shell/editor commands while inspecting untrusted text.

Do not add `-r` to make arbitrary control bytes render as raw terminal instructions. Default less displays controls visibly; `-R` permits a restricted set of escape sequences for color, which is rarely needed for a configuration file. Display wrapping is not a newline in the original file. Preserve an exact selected line before copying a URL, SQL string or credential candidate into another tool.

A password-like value in a configuration file is a candidate for its labelled service/account at the acquisition time, not proof of OS or AD authentication. A database URI identifies driver, host and database context; a Python file containing SQLAlchemy code does not by itself identify the web framework. See the [upstream less manual](https://github.com/gwsw/less/blob/master/less.nro.VER).
