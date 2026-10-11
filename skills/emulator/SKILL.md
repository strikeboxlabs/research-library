---
name: emulator
description: Start a selected owned Android AVD with explicit DNS server settings. Use when app hostname resolution, host mappings and proxy/TLS failures are being conflated.
---

# Select the owned AVD and resolver

Read this entire SKILL.md before acting. Require the installed Android emulator, existing owned AVD and reachable permitted DNS server. No conditional resources are required. Finish with the actual AVD/build, startup result and observed DNS request/reply; launch alone does not establish app connectivity.

Check `emulator -version`, `emulator -help-dns-server` and `emulator -list-avds`. Define `avd` as one listed device and `dns_servers` as the intended comma-separated server IP list:

~~~bash
emulator -avd "$avd" -dns-server "$dns_servers"
~~~

This is a startup option: stop the selected existing instance before relaunching with it. The documented option accepts up to four servers. An AVD runs guest code and writes its state; preserve existing settings/data rather than using -wipe-data as a networking retry.

Changing the Linux host's hosts file does not configure the Android guest's resolver. Selected DNS observations need matching responses and returned addresses; a question alone establishes only that name lookup was requested. Proxy configuration, route, TLS trust and app-specific certificate checks are separate. A proxy handshake failure does not by itself establish certificate pinning. Keep the original resolver/proxy settings and restore changes made for the owned test.

Use the installed binary's supported options; a different SDK frontend does not inherit these flags automatically. Reference: [Android emulator startup and DNS options](https://developer.android.com/studio/run/emulator-commandline).
