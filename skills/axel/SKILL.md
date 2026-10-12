---
name: axel
description: Download one selected ordinary artifact with Axel, controlling connection count and output placement while distinguishing partial state from a verified transfer.
---

# Download one selected artifact

Read this entire SKILL.md before acting. Require the intended existing Axel binary, one approved public or owned HTTP(S) URL, a fresh output path in an owned directory and independently known expected bytes or digest. Review this binary's help and effective configuration before transfer. No conditional resources are required. Finish with command status, actual destination and integrity evidence; missing prerequisites or interrupted bytes remain incomplete.

Define `axel_bin` as the installed executable and inspect `"$axel_bin" --version` and `"$axel_bin" --help`. Inspect the installed system configuration location and the invoking process's actual home configuration, plus proxy and authentication settings. The packaged manual describes `/etc/axelrc` and `~/.axelrc`, but system locations can vary. Do not infer a privileged wrapper's HOME or configuration from the login account alone.

Define `url` as the selected URL and `output` as a new absolute ordinary-file path; ensure neither it nor its `.st` state file exists. With the following options supported by the installed version:

~~~bash
"$axel_bin" --num-connections=1 --timeout=20 --max-redirect=0 \
  --output="$output" "$url"
status=$?
~~~

One connection limits this transfer's fan-out. The timeout concerns connection waiting, not a guaranteed total task deadline; keep the agreed overall stop time separately. Zero redirects confines this invocation to the selected URL: if it redirects, inspect that destination and select it explicitly only within the task's authority. Keep HTTPS peer verification enabled. An ordinary download needs no elevated wrapper.

Axel writes directly to its destination and may retain state for automatic resume. File presence or a progress percentage therefore does not establish completion. Its documented statuses are 0 for success, 1 for an error and 2 for user interruption; inspect diagnostics and verify the expected bytes or independently supplied checksum before accepting the result. On failure preserve the partial/state distinction, resolve the cause and choose deliberate resume or a fresh destination. Do not merge bytes from different artifact versions.

For an owned server without supported ranges, a one-connection restart can be ordinary fallback rather than proof of acceleration. Several mirror URLs require the same artifact bytes; a shared filename does not establish that condition. Avoid mirror search when the task selects one source.

`default_filename` supplies the fallback name for an HTTP directory/index URL. It is not a general output-directory setting; use explicit `--output` for the selected artifact. Treat a configurable User-Agent header as a request observation, not independently verified binary provenance. Do not use download output or writable configuration to replace account-authorisation files.

See the [packaged Axel options and status contract](https://manpages.debian.org/bookworm/axel/axel.1.en.html), [upstream configuration example](https://github.com/axel-download-accelerator/axel/blob/master/doc/axelrc.example) and [configuration loading](https://github.com/axel-download-accelerator/axel/blob/master/src/conf.c). Match them to the installed version when behavior differs.
