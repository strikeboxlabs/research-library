---
name: winetricks
description: Install a selected .NET Framework 4.8 runtime into an explicit Wine prefix with Winetricks. Use when prefix selection, architecture warnings or recorded installation is confused with application compatibility.
---

# Supply the selected Wine runtime

Read this entire SKILL.md before acting. Require the trusted installed Winetricks/Wine versions, an existing initialized prefix owned by the current user, and an approved application requirement for .NET Framework4.8. Read that installed version's dotnet48 verb before changing the prefix; finish with installation evidence and a separate application compatibility result. No package-local references are required.

Define `prefix` as the selected absolute prefix directory. Record versions, confirm that this build offers dotnet48 and inspect the selected prefix's installed-verb record:

~~~bash
winetricks --version
wine --version
winetricks dlls list
WINEPREFIX="$prefix" winetricks list-installed
~~~

The installed verb can download and run Microsoft installers, remove Wine Mono, install supporting components and change DLL/runtime settings. Its implementation includes version and architecture checks; review those for this prefix rather than assuming every Wine release works. Preserve recoverable prefix state before an approved change. A Linux mono-complete package is not equivalent evidence of Microsoft's runtime inside this prefix.

Run the selected installation as the prefix's owning user:

~~~bash
WINEPREFIX="$prefix" winetricks dotnet48
status=$?
WINEPREFIX="$prefix" winetricks list-installed
~~~

Retain status/installer diagnostics and the resulting prefix record. In the reviewed implementation, list-installed displays winetricks.log rather than testing each installed runtime; a missing log does not prove that no runtime was installed by other means. This record does not prove the dependent application works: run its separately approved compatibility check in this same prefix. A download failure, installer error or version/architecture warning requires its specific cause; a partial installation can leave changed state. Do not use --force or unattended mode merely to hide a failure. Selecting a different prefix changes the test subject.

Consult [upstream usage](https://github.com/Winetricks/winetricks) and the installed equivalent of the [dotnet48 verb implementation](https://github.com/Winetricks/winetricks/blob/master/src/winetricks) for consequential version differences. Skill installation does not download or apply this runtime.
