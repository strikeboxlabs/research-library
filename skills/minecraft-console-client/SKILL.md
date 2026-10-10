---
name: minecraft-console-client
description: Use Minecraft Console Client for a headless Java Edition server session, inspect connection results and send a selected chat message or command. Distinguish protocol mismatch, offline identity and server-side permission failures.
---

# Inspect a Minecraft session through the existing console client

Read this entire SKILL.md before acting; reuse complete current context. Select the intended Java Edition server and account mode, review the active client configuration/bots, and check the connection result before sending anything. Finish with the requested response and connection/identity limits, then disconnect when the task ends. If the client, compatible protocol or required account is unavailable, report that prerequisite.

Define `mcc` as the existing Linux Minecraft Console Client executable. Its filename can contain a release date and architecture; do not infer compatibility from that name alone. Check its help, build information and supported server versions. The skill does not implement the Minecraft protocol or install a client:

~~~bash
"$mcc" --help
~~~

For an authorized server deliberately accepting offline players, define `player` as the chosen test identity and `server` as the exact `host:port`:

~~~bash
"$mcc" "$player" - "$server"
~~~

The password-position `-` selects offline mode. Empty `""` is not a dependable substitute: releases can prompt or use an account-authentication flow. Joining offline confirms that this session was accepted, not Microsoft identity verification or administrator permission. Servers requiring online accounts need the installed client's supported sign-in flow; do not retry arbitrary password strings. Review any loaded configuration and automatic chat bots before connecting, since they can send actions without manual input.

At the **MCC console**, a slash normally selects an internal client command. Use the explicit send command when the intended text must reach the server; these are console input, not shell commands. The message below is illustrative:

~~~text
/send Connection check from the approved test session
/quit
~~~

`/send` forwards text or a server command; `/quit` closes the session. A local command's acknowledgement is not the server's reply. Sending a server command still depends on that player's permissions; retain the rejection or result instead of treating a connected session as elevated access.

If a status scan succeeds but joining fails, compare the client build, advertised server version, negotiated protocol and actual disconnect reason. A ping response is weaker evidence than a completed session. A protocol mismatch, online-account requirement, whitelist or server-plugin rejection calls for a different correction; none alone proves the service is down. An old advertised version alone does not prove a specific vulnerability or missing mitigation.

Use the [MCC usage guide](https://mccteam.github.io/guide/usage.html) for current argument and console-command behavior and the [project](https://github.com/MCCTeam/Minecraft-Console-Client) for build/protocol support.
