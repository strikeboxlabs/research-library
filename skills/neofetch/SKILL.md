---
name: neofetch
description: Display a local system summary with Neofetch, bypass user configuration for a baseline and interpret missing or environment-dependent fields.
---

# Local system summary

Read this entire SKILL.md before acting. Require a trusted installed Neofetch script and a local user context. Use the baseline below unless a reviewed custom configuration is part of the task. Finish with the actual summary, invocation/version and any unavailable fields; a formatted display does not establish a complete hardware or package inventory.

Neofetch is a Bash script. Its user configuration is sourced shell code; ordinary launch can also create a missing configuration file. For a baseline without that user file, define `neofetch_bin` as the installed executable and use:

~~~bash
"$neofetch_bin" --config none --version
"$neofetch_bin" --config none --stdout
~~~

`--stdout` removes colors and the image/ASCII backend. The pinned 7.1.0 implementation exits with status 1 for its version/help display, so preserve the output and status rather than treating that status alone as a broken installation. `--config none` bypasses the external user configuration; the script still evaluates its built-in defaults and runs its information helpers.

For a deliberately customized display, require a fully reviewed configuration in a trusted local directory, then pass its absolute path with `--config "$config_file"`. Configuration can redefine `print_info()` and select fields such as `info "OS" distro` or `info "Kernel" kernel`. Treat the file as executable code, including expressions in values. Record the exact file used; don't elevate the display merely to collect system information.

By default the configuration base comes from `XDG_CONFIG_HOME`, falling back to the user's `.config` directory. A displayed user/host label belongs to that invocation's environment. Missing GPU, desktop or package fields can reflect helper availability or session context; confirm a consequential fact with its underlying system source instead of interpreting a blank field as absence. Keep host/user details private when sharing a support report.

See the [upstream 7.1.0 configuration loader, argument parser and main function](https://github.com/dylanaraps/neofetch/blob/7.1.0/neofetch) when behavior differs from the installed script.
