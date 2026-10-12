---
name: mqttui
description: Inspect a selected MQTT topic with MQTT TUI and preserve payload, retained-message and subscription limits. Use for an owned broker's telemetry diagnosis without changing topic contents.
---

# Observe the selected topic

Read this entire SKILL.md before acting. Establish the owned broker, permitted topic and observation interval; confirm the installed CLI before connecting. Finish with received bytes, status and freshness limits. An empty observation cannot establish an absent topic.

~~~bash
mqttui --version
mqttui --help
mqttui read-one --help
~~~

Define `broker` as the approved broker URL, `topic` as one exact permitted topic, and `payload`/`diagnostics` as fresh private files. Configure a provisioned read-only account through the installed client's supported private environment settings; do not embed credentials in URLs or command history. For TLS, retain certificate verification and the correct CA. If the installed version lacks the required transport/authentication support, report the missing prerequisite.

~~~bash
umask 077
timeout 20s mqttui --broker "$broker" read-one "$topic" > "$payload" 2> "$diagnostics"
status=$?
printf 'observation status: %s\n' "$status"
~~~

`read-one` returns the first payload, with its topic on stderr; that stream can also contain diagnostics. Preserve binary payload bytes before parsing a working copy. Default subscription can include retained data, so first receipt does not establish a new publication or current device state. When a new publication is required, use `--ignore-retained` only after confirming installed support. A timeout, connection rejection or subscription failure remains distinct from successful receipt; retain partial files without declaring success.

For repeated observation, the documented `log` subcommand records messages and retained status. Specify the same topic explicitly: omitting it can select a broad wildcard. A visible topic tree reflects received traffic and access, not a complete broker inventory. Payload hostnames, timestamps and healthy flags are publisher assertions, not independent reachability checks. Keep observation separate from `publish`, `clean-retained` and TUI deletion controls, which change broker state.

See the [upstream usage](https://github.com/EdJoPaTo/mqttui) and [CLI definitions](https://github.com/EdJoPaTo/mqttui/blob/main/src/cli.rs) for version-specific options and environment names.
