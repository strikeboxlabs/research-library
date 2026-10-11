---
name: nano
description: Edit a selected plaintext artifact with GNU nano or review an editor permission boundary. Use when wrapping, save destination, startup settings or external-command capabilities affect the intended task.
---

# Edit and verify a selected text artifact

Read this entire SKILL.md before acting; reuse complete current context. Select working-copy editing below, requiring its exact path and intended byte changes, or static permitted-editor review, requiring the actual grant/executable/options. Finish with the saved artifact checked by its consumer or the supported policy finding; exiting the editor successfully does not validate its contents or confinement.

Use `nano --version` and the installed help. Nano is an interactive terminal editor; without a usable terminal, report that prerequisite rather than sending blind keystrokes. Preserve acquired originals and use a private working directory for credentials. Define `file` as the selected working copy:

~~~bash
nano -I -w -- "$file"
~~~

`-I` ignores nanorc settings; `-w` prevents hard wrapping. Visual soft wrapping is different from inserted newlines. Confirm the filename shown by the editor before changing content. For a transferred key, remove only an established transport prefix from the selected key lines; preserve the complete begin/end delimiters, encoded line order and final newline. A SNIP marker or missing material requires reacquisition, not invented replacement bytes.

With the default bindings, Ctrl-O opens Write Out: check the destination, press Enter to save, then Ctrl-X to exit. Read the status message and follow any overwrite/save prompt deliberately. A marked selection can be written instead of the whole buffer, and append/prepend or DOS line-ending settings change the resulting file. Use Ctrl-G for this version's bindings if the interface differs.

Reopen or inspect the resulting file and run the intended parser. A visible save message proves that write operation, not that the private key, JSON or configuration is valid or that its permissions suit the consumer. Keep secret contents out of public terminal recordings; limit subsequent evidence to the needed fingerprint, parse result or specific edit.

For a permitted-editor policy review, distinguish the requested filename from the editor's capabilities. An ordinary unrestricted Nano can insert other files and execute external commands with its process authority; a sudo grant naming one initial file does not by itself confine those features. Review the exact executable, options, startup configuration and effective policy as data, without invoking an elevated child to demonstrate the finding. Restricted/view modes have different limits and are not interchangeable with a normal editable session.

See [GNU nano's manual](https://www.nano-editor.org/dist/latest/nano.html) for write-out behavior, options and bindings.
