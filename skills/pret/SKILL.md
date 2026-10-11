---
name: pret
description: Query selected PJL printer metadata with PRET during an authorized maintenance session. Use when a connected raw-print endpoint's model, configuration or status needs corroboration and a timeout is being mistaken for unsupported language.
---

# Query the selected printer's PJL metadata

Read this entire SKILL.md before acting. Require a selected managed printer and permission for the diagnostic session's startup and information requests. Use an existing verified PRET checkout and compatible interpreter; no conditional resources are required. Finish with endpoint, tool revision, returned fields and communication gaps. A connection banner alone does not complete device identification.

Define `python_bin` and `pret_script` as the installed interpreter/script paths, and `printer` as the selected printer hostname or address. Inspect local help first:

~~~bash
"$python_bin" "$pret_script" --help
"$python_bin" "$pret_script" "$printer" pjl
~~~

The upstream README describes an older Python 2 setup, while current source uses Python 3; select from the installed revision rather than guessing from the writeup. Missing imports are a runtime gap, not printer rejection. Invoking PRET without a target can discover printers by SNMP broadcast; always supply the selected endpoint. `--safe` performs additional protocol capability queries and is not a guarantee that every command is harmless.

In the established PJL session, use only the required information categories:

~~~text
help info
info id
info status
info config
exit
~~~

These query reported identity, status and configuration. PRET's PJL startup can send `USTATUSOFF` to disable unsolicited status messages, so the session is not literally free of device-side effects. Keep that startup within the maintenance authorization. Retain errors and exact returned fields privately; configuration may contain deployment details. A model/firmware string is reported metadata, not authenticated provenance or proof of a vulnerability.

An accepted TCP connection followed by no feedback can reflect a busy device, silent implementation, filtering or unsupported language. It does not uniquely prove the printer lacks PostScript or PJL. Record the timeout and stop or use separately established device capability evidence before changing language. Vendors implement different subsets; a missing category does not establish empty configuration. PRET translates commands into printer-language requests, so its prompt is not an OS shell.

Use the [upstream usage and PJL categories](https://github.com/RUB-NDS/PRET#commands-in-pjl-mode) and [PJL implementation](https://github.com/RUB-NDS/PRET/blob/master/pjl.py) to resolve revision, startup and response behavior.
