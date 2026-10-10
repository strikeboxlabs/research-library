---
name: git-dumper
description: Recover an authorized exposed Git repository over HTTP with arthaud's git-dumper and assess incomplete acquisitions. Use when directory listing is denied, objects are missing or a successful exit masks checkout failure.
---

# Check the acquisition boundary

Read this entire SKILL.md before acting. Establish the approved endpoint and disposable isolated acquisition environment before downloading; the downloader automatically checks out recovered Git content. Complete the acquisition and object checks below, retaining logs and gaps. Finish with the recovered commit/path coverage and observed checkout/object status, not downloader exit status alone.

Use arthaud's `git-dumper`, not similarly named shell scripts. Inspect installed `git-dumper --help`; newer options such as `--branch`, `--method` and `--any-status` may be absent from older packages. The source-script entrypoint is `git_dumper.py`.

This tool automatically invokes Git checkout on downloaded material. The [upstream warning](https://github.com/arthaud/git-dumper) explicitly identifies local code-execution risk from attacker-controlled repositories. Run only in a disposable isolated environment without worker credentials, host secrets or trusted workspace mounts. A config sanitizer is not a security boundary. Upstream also disables TLS certificate verification; HTTPS success alone does not authenticate the server. Establish the intended endpoint independently.

First confirm the scoped site's `.git/HEAD` response is plausible Git content, not a login/error page. Directory `.git/` returning 403 while `.git/HEAD` returns valid content can still allow object recovery. A 200 status alone is insufficient. Establish redirects/virtual-host routing separately; the downloader does not follow redirects.

# Acquire into a fresh destination

Define `url` as the approved site or `.git` URL, `destination` as a fresh absolute output directory, `log` as a separate private log path and `budget` as a positive overall duration such as `120s`. With GNU `timeout` available:

~~~bash
umask 077
timeout --signal=INT --kill-after=5s "$budget" git-dumper \
    --jobs 1 --retry 1 --timeout 10 "$url" "$destination" > "$log" 2>&1
status=$?
~~~

The downloader timeout applies to individual timed requests, not the entire operation; some discovery calls lack that timeout. The outer duration bounds the run. Timeout status 124, or 137 after forced termination, leaves partial evidence. Keep it separate from a completed acquisition. A larger job count increases concurrent requests; use a deliberate budget rather than the default ten workers.

Preserve the log and downloaded files. Existing files can be skipped, so a reused directory may mix old and new evidence. `--any-status` relaxes a status filter; it does not validate Git objects and can admit mislabeled error bodies. Add a known branch with `--branch` only when the installed version supports it and that branch is relevant; guessed refs cannot guarantee full history.

# Verify what was recovered

In the same isolated environment, inspect the captured config and object-store references before using Git. The tool can alter `.git/config`; its output is not a byte-for-byte acquisition of that original file. For the selected working copy:

~~~bash
git -C "$destination" fsck --full
git -C "$destination" --no-pager log --all --format='%H %s' -n 20
~~~

Check each status and diagnostic. `missing blob/tree/commit` or a hash mismatch leaves content incomplete or corrupt; a `dangling` object is present but unreferenced and is not the same failure. Preserve such objects instead of pruning. Upstream's non-listing recovery path suppresses checkout errors and returns zero, so an empty working tree is not proof of no source files.

A clean fsck concerns available objects and roots, not every remote ref, ignored file, uncommitted change, LFS payload or submodule repository. Record the recovered commit/path and remaining gaps; do not execute the recovered application to test completeness. See [Git object diagnostics](https://git-scm.com/docs/git-fsck) and the [downloader implementation](https://github.com/arthaud/git-dumper/blob/master/git_dumper.py) when status and files disagree.
