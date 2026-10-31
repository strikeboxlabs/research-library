---
name: "deepce"
description: "Enumerate container escape paths from inside a compromised container with deepce: privileged capabilities, socket mounts, capabilities and kernel features, with optional escape execution. Use only inside containers the engagement authorizes."
---

# deepce container escape enumeration

Installed invocation: `/usr/local/bin/deepce` (upstream single-file script from stealthcopter/deepce).

Read this entire SKILL.md before acting. Require shell access inside a container that is in scope, and explicit authorization before any escape execution — leaving the container boundary changes the target of the engagement. Finish with the enumerated escape candidates and which, if any, were executed.

~~~bash
/usr/local/bin/deepce
~~~

The default run is enumeration only: it inspects capabilities, mounts, host paths, socket exposure (docker.sock), kernel features and runtime hints, then lists viable escape techniques for the observed state. `--no-enum` skips enumeration for straight exploit attempts and should follow an enumerated run, not replace it.

Escape execution (`--exploit ...`) breaks the container boundary: it is a state-changing action on the host, and the authorization for testing the container does not automatically cover the host. An enumeration that finds no path is a completed observation, not a failed run.

References: [project documentation](https://github.com/stealthcopter/deepce).
