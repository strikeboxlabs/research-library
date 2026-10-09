---
name: snap
description: Inspect snap installations, confinement and task results on Linux. Use when local package installation, sudo policy or dangerous/devmode/classic options are being mistaken for equivalent operations.
---

# Establish installed state and execution scope

Define `package` as the observed snap name. Inspect the installed revisions and connected interfaces:

~~~bash
snap version
snap list --all "$package"
snap connections "$package"
snap changes
~~~

Distinguish the CLI/snapd version, application version, revision and tracking channel. `--all` includes retained disabled revisions; their presence does not mean they are active. `snap info "$package"` adds publisher/store information, which is not itself proof of the locally active revision or permissions.

The installation options change different things:

| Option | Consequence |
|---|---|
| `--dangerous` | Allows a local snap without assertion/signature verification; it does not by itself disable confinement. |
| `--devmode` | Allows system-resource access while logging confinement violations; intended for development. |
| `--classic` | Applies to a package built for classic confinement, with broad traditional-package access; adding it to a strict package does not convert that package to classic. |

Review local package metadata and `meta/hooks/` contents before an installation decision. Hooks are executable parts of the package and can run during installation/configuration; installation is not a passive way to list its contents. Store identity checks and confinement are separate from trust in the hook's behavior. A sudo rule allowing package installation must therefore be interpreted together with its argument restrictions and permitted installation modes.

For an observed change, define `change_id` from `snap changes`:

~~~bash
snap tasks "$change_id"
~~~

Read individual task states and errors. A submitted change, an in-progress task and a completed installation are different outcomes. A failing hook does not justify blindly reinstalling or assuming every external side effect was undone. Diagnose missing interfaces versus application failures from the relevant task/log evidence; enabling devmode changes the test's behavior.

Do not turn the walkthrough's historical package-building script into a general installation recipe. Preserve the package identity, local mode/connections and observed change result before deciding whether any package modification is actually needed.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Armageddon pp. 10–12. Sources: [install modes](https://snapcraft.io/docs/explanation/snap-development/install-modes/), [hooks](https://snapcraft.io/docs/reference/development/supported-snap-hooks/), [change monitoring](https://snapcraft.io/docs/how-to-guides/manage-snaps/manage-updates/), [installed revisions/interfaces](https://snapcraft.io/docs/tutorials/get-started/).
