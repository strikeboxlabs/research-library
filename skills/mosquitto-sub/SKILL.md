---
name: mosquitto-sub
description: Observe a selected ordinary MQTT topic with mosquitto_sub and distinguish retained messages, delivery count, TLS configuration and incomplete connection evidence.
---

# Observe the selected MQTT topic

Read this entire SKILL.md before acting. Require the approved broker, port, exact ordinary topic, authentication/TLS requirements and observation window. Review installed-version options and loaded client configuration first. Finish with connection status, selected topic, received-message evidence and time/count limits.

Define `broker`, `port` and `topic` from that task. Keep credentials in the approved private configuration rather than command arguments. POSIX defaults load `$XDG_CONFIG_HOME/mosquitto_sub` or `~/.config/mosquitto_sub`; review them for additional topics, wills or other broker-changing options before subscribing. This task requires an ordinary clean subscription without retained-message deletion or will publishing.

~~~bash
mosquitto_sub --help
mosquitto_sub -h "$broker" -p "$port" -t "$topic" -v -C 10 -W 30
status=$?
~~~

`-v` displays topic and payload. `-C` counts messages, not lines; payloads can contain newlines. `-W` starts after connection, so also stop an unresolved connection at the agreed overall window. Quote topics containing shell metacharacters. A retained initial value can be old; use installed-version `-R` when the question specifically requires fresh publications. No received message can reflect idle publishing, a wrong topic, denied subscription or connection failure; preserve diagnostics before choosing a cause.

For TLS, use the broker's required verified trust/identity options, such as `--cafile "$ca_file"` with its actual CA file. Changing the port alone does not establish TLS. Topic text and successful delivery do not authenticate the claimed publisher or prove application success. Keep private payloads out of general reports.

See [mosquitto_sub options and configuration](https://mosquitto.org/man/mosquitto_sub-1.html) and [MQTT retained/delivery semantics](https://mosquitto.org/man/mqtt-7.html).
