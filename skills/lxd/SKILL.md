---
name: lxd
description: Initialize a new owned LXD installation interactively with deliberate storage and network choices. Use when copied prompt answers or defaults leave daemon configuration and profile readiness uncertain.
---

# Configure the new owned daemon

Read this entire SKILL.md before acting. Require an installed LXD service, administrative authority and a concrete storage/network plan for a new installation. Review each prompt before accepting changes, then verify the resulting server, storage, network and default profile. Report any missing prerequisite rather than treating initialization as completed deployment.

LXD manages system containers and virtual machines; `lxd init` configures the daemon. It differs from client-side `lxc init`, which creates an instance. Check `lxd --version` and `lxd init --help`; confirm the local service and intended installation before running:

~~~bash
lxd init
~~~

Answer from the deployment plan: clustering, storage backend and location, instance networking, remote API exposure and image updates. Prompts depend on earlier answers and the installed release. A blanket answer of no is not a reusable configuration: declining storage creation requires an already suitable pool, while declining a bridge requires the intended alternate network. Creating storage can use a disk or partition; require an explicitly empty intended device before selecting one. A managed bridge can enable host forwarding, so account for its effect on the host's other interfaces. Leave network API exposure disabled unless remote administration and its authentication are part of the requested setup.

Use the installed LXD client to inspect the result on the local server:

~~~bash
lxc info local:
lxc storage list local:
lxc network list local:
lxc profile show local:default
~~~

Match the observed pool/network and profile devices to the chosen plan. Existence of an image or a successful command exit does not prove a default profile has a usable root disk or network. A missing service, access denial or conflicting existing configuration needs diagnosis before retrying. Reinitializing an existing deployment is a separate state-changing task; preserve its configuration rather than using new-installation defaults as a repair.

See Canonical's [interactive initialization](https://canonical.com/lxd/docs/latest/howto/initialize/) for the installed version's questions and effects.
