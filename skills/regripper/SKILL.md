---
name: regripper
description: Parse an acquired Windows registry hive with RegRipper on Linux and interpret RecentDocs evidence. Use for plugin selection, MRU order, key timestamps and missing-key or transaction-log limitations.
---

# Read a selected hive and plugin

Read this entire SKILL.md before acting. Establish the hive's source user/system, acquisition time and hash, then select a trusted installed plugin matching that hive. Finish with the parsed key/value evidence, diagnostics and coverage limits; a filename or last-write timestamp alone does not prove a document's complete path or opening time.

Define `rr_bin` as the verified Linux RegRipper launcher. Packages may expose `regripper` or `rip`; upstream also supplies `rip.pl`, which requires Perl and its registry modules. Check the actual launcher and plugin directory rather than assuming a Windows executable or an arbitrary script is interchangeable. Listing plugins loads their Perl code, so use trusted installed plugins.

~~~bash
"$rr_bin" -h
"$rr_bin" -l
~~~

For RecentDocs, define `hive` as an acquired NTUSER.DAT working copy and `report`/`diagnostics` as fresh private paths outside the evidence tree:

~~~bash
umask 077
"$rr_bin" -r "$hive" -p recentdocs > "$report" 2> "$diagnostics"
status=$?
printf 'parser status: %s\n' "$status"
~~~

Retain the full report before filtering. Confirm the plugin banner/version and intended key, including extension subkeys. Values are presented in MRUList/MRUListEx order; their numeric names are indices, not timestamps. The displayed LastWrite belongs to the key, not each document. A basename does not establish a full path, current existence or file contents. Correlate an independently acquired matching Shell Link through a format-aware parser; printable strings are leads and do not identify every link field.

RegRipper 3's `-a` runs applicable hive plugins; it does not mean every plugin covers every artifact. Missing keys, an incompatible hive/plugin, truncated acquisition and parser errors have different meanings. Read output diagnostics even when the launcher exits successfully. A missing RecentDocs key does not establish no user activity.

RegRipper does not automatically replay hive transaction logs. Preserve available logs and state whether replay was needed/performed by a suitable separate parser on a copy. Do not modify the original hive to make a plugin succeed. Missing Perl modules or plugins are installation prerequisites, not empty forensic results.

Use the [upstream documentation](https://github.com/keydet89/RegRipper3.0), [CLI implementation](https://github.com/keydet89/RegRipper3.0/blob/master/rip.pl) and [RecentDocs plugin](https://github.com/keydet89/RegRipper3.0/blob/master/plugins/recentdocs.pl) to resolve generation and output differences.
