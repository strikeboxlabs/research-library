---
name: steghide
description: Inspect a local JPEG, BMP, WAV or AU artifact and recover Steghide data with a known passphrase, choosing the output filename and distinguishing extraction failure from absence.
---

# Recover known-passphrase embedded data

Read this entire SKILL.md before acting; reuse complete current context. Require the installed Steghide, an acquired local artifact and its known passphrase. Inspect the format, then extract to a fresh private output below. Finish with status, recovered bytes and format/integrity gaps; do not execute the recovered content.

Define `artifact` as an absolute preserved-input path:

~~~bash
steghide version
steghide info "$artifact"
~~~

The supported cover formats are JPEG, BMP, WAV and AU, identified from their headers rather than extensions. Info asks whether to inspect embedded data, then prompts for its passphrase. A capacity value alone does not establish a message exists.

Define `output` as a fresh absolute file under a private working directory. Enter the known passphrase at the prompt:

~~~bash
umask 077
steghide extract -sf "$artifact" -xf "$output"
status=$?
~~~

`-xf` selects your output instead of trusting the embedded filename. Avoid `-f`, which forces overwrite, and keep secrets out of `-p` command arguments. Status zero reports completion; warnings still require review. Failure may mean a wrong passphrase, unsupported format, altered data or another embedding method, rather than universal absence. Preserve diagnostics and the acquired original; retries need a supported reason.

Inspect recovered bytes as data. An optional embedded CRC32 is consistency evidence, not authenticity. Recovery does not establish account ownership or current credential validity. See the [Steghide manual](https://manpages.debian.org/testing/steghide/steghide.1.en.html) for format and option differences.
