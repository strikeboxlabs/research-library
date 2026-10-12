---
name: snap
description: Inspect snap state or install one selected Store package on the controlled Linux image. Use when channels, publisher identity, confinement, aliases or asynchronous task results obscure what was installed and what can run.
---

# Establish installed state and execution scope

Read this entire SKILL.md before acting. Require the controlled Linux image with an existing working snapd service. Choose installed-state review or the selected Store installation below; local package/mode review is a separate conditional decision. No additional resources are required. Finish with active revision/channel, interfaces and relevant change/task results; an installation result does not establish application compatibility. Installing this skill does not install snapd or an application.

Define `package` as the observed snap name. Inspect the installed revisions and connected interfaces:

~~~bash
snap version
snap list --all "$package"
snap connections "$package"
snap changes
~~~

Distinguish the CLI/snapd version, application version, revision and tracking channel. `--all` includes retained disabled revisions; their presence does not mean they are active. `snap info "$package"` adds publisher/store information, which is not itself proof of the locally active revision or permissions.

For one intended Store installation, define `package` as an exact approved snap name and `channel` as the selected track/risk channel. Check `snap help install` and `snap info "$package"`; review publisher, available channel/version, confinement and the intended application before the permitted privileged transaction:

~~~bash
sudo snap install --channel="$channel" "$package"
status=$?
snap list --all "$package"
snap connections "$package"
snap changes
~~~

Keep the install status separately from later inspection commands. Installation can add required base/dependency snaps and run hooks or start services. A copied request to install core/snapd is not proof that those changes are required on this image. A channel is a moving update stream, not an immutable version pin; stable does not mean the application's globally newest version. If the package is already installed, a refresh or channel switch is a separate requested change.

Inspect the actual application's entrypoint/alias and version after installation; a packaged helper can have a qualified command name different from the snap name. Store metadata or a successful installation does not prove that a converter supports the selected file format. `--no-wait` returns a change ID before completion; use the task review below rather than claiming success from that ID.

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

Sources: [install command](https://manpages.debian.org/bookworm/snapd/snap.8.en.html), [install modes](https://snapcraft.io/docs/explanation/snap-development/install-modes/), [hooks](https://snapcraft.io/docs/reference/development/supported-snap-hooks/), [change monitoring](https://snapcraft.io/docs/how-to-guides/manage-snaps/manage-updates/), [installed revisions/interfaces](https://snapcraft.io/docs/tutorials/get-started/).
