---
name: adb
description: Inspect a selected Android device, install an owned APK and diagnose emulator-to-host traffic with adb. Use for package-ID mistakes, device identity, transport privileges and proxy or CA-trust confusion.
---

# ADB device and network context

Read this entire SKILL.md before acting. Identify the intended device/serial, authorization and requested observation or mapping. Finish with actual device/build identity and the requested result or missing transport prerequisite; report mapping cleanup separately.

For an owned APK install/update or explicitly requested uninstall, read [package operations](references/package-operations.md) fully before changing the selected device.

Inspect `adb version`, `adb help` and `adb devices -l`. Choose `serial` from the intended authorized device/emulator and keep `-s "$serial"` on subsequent commands. `offline` or `unauthorized` needs transport/device authorization resolution; it is not an application result. The `device` state alone does not prove boot completion.

~~~bash
adb -s "$serial" get-state
adb -s "$serial" shell getprop ro.build.version.sdk
adb -s "$serial" shell id
adb -s "$serial" shell settings get global http_proxy
~~~

Distinguish the Linux adb client/server, Android's adbd, a device shell and the app's UID. Obtaining `su` inside one shell does not give a later `adb push` that shell's identity. `adb root` restarts adbd and depends on a build that permits it; it is not a general repair for permission denied. A writable shell directory does not imply a writable system trust store.

For one selected existing device file, define `remote_file` as its observed absolute path and `local_file` as a fresh private destination:

~~~bash
adb -s "$serial" pull "$remote_file" "$local_file"
~~~

Check transfer status and completeness. Do not substitute a broader private-data dump for an unreadable file. `push` changes device files and uses adbd's access, not privileges obtained in another shell.

For a controlled app/proxy test, Android's `127.0.0.1` refers to the device. `forward` carries host connections toward a device endpoint; `reverse` provides a device endpoint leading to the adb server host. With an existing host service on port 8080 and a verified unused device port 18080:

~~~bash
adb -s "$serial" reverse --list
adb -s "$serial" reverse --no-rebind tcp:18080 tcp:8080
~~~

The device can then use `127.0.0.1:18080`. This does not configure the app or its HTTP proxy automatically. If changing a device-wide proxy for the task, save its previous value and restore that state afterward; some apps ignore it. On completion remove only the mapping created here:

~~~bash
adb -s "$serial" reverse --remove tcp:18080
~~~

Route, hostname resolution, cleartext policy and TLS trust are separate checks. Apps targeting API 24+ generally do not trust user-added CAs by default; their network-security configuration matters. Installing a CA does not alone defeat certificate pinning. Prefer an owned debug build's intended test-CA configuration when available. System trust-store locations/write mechanisms vary by Android build; a historical emulator's remount-and-copy recipe is not portable. Record device/build, app context, actual route and remaining failure layer.

Sources: [ADB guide](https://developer.android.com/tools/adb), [command semantics](https://android.googlesource.com/platform/packages/modules/adb/+/refs/heads/main/docs/user/adb.1.md), [Android network security](https://developer.android.com/privacy-and-security/security-config).
