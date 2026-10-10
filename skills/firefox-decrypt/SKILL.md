---
name: firefox-decrypt
description: Recover saved logins from an authorized offline Mozilla profile with firefox_decrypt. Use when profile selection, matching key databases, NSS compatibility or incomplete records affect recovery.
---

# Recover one selected profile

Use an already acquired, consistent working copy of the authorized profile. Modern Firefox stores saved logins in `logins.json` with key material in the matching `key4.db`; older profiles may use `signons.sqlite` and `key3.db`. Preserve the captured directory and any database sidecars. A successful ZIP transfer does not prove all files were readable or captured consistently. Do not start Firefox on the evidence copy to repair it.

Define `tool` as an existing reviewed `firefox_decrypt.py` and `profiles_root` as the copied directory containing `profiles.ini`:

~~~bash
python3 "$tool" --help
python3 "$tool" --list "$profiles_root"
~~~

Even listing can fail if the tool cannot load NSS first; separate that dependency failure from a missing profiles index. The listed numbers are tool choices, not Firefox profile names. Inspect the selected path, including absolute paths, `..` and symlinks, to ensure it resolves inside the authorized copy. If the capture contains only a single profile directory, pass that directory directly for recovery; `--list` requires the profiles index and cannot list a lone profile. Always supply a path so the tool does not default to the worker's own browser data.

## Export without printing secrets into the transcript

Define `profile` as the exact selected profile directory, and `output`/`diagnostics` as fresh private files. With an interactive terminal, the tool requests the known Primary Password (historically Master Password) when required:

~~~bash
umask 077
if python3 "$tool" --format json "$profile" > "$output" 2> "$diagnostics"; then
    printf 'Export finished; inspect diagnostics and record completeness locally.\n'
else
    printf 'Recovery failed; retain the status and diagnostic before retrying.\n' >&2
    false
fi
~~~

The prompt is on stderr, now redirected: supply the known password only through the private terminal input. For automation, `--no-interactive` reads a required password as one line from stdin; provide it through the approved secret-input mechanism. EOF is not evidence of an unprotected profile. `--choice N` selects from a profiles root; using the exact profile directory avoids that ambiguity. This tool does not discover an unknown Primary Password.

JSON output contains `url`, `user` and `password`. Keep it private; report only approved redacted evidence. Inspect diagnostics even after status zero: malformed records can be skipped and some decoding failures produce placeholders. `--non-fatal-decryption` also permits incomplete recovery. Empty output or an empty array needs a profile/path/completeness check before concluding there were no saved logins. A saved website credential establishes a historical record, not current validity or an OS account password.

Missing login files, NSS initialization failure and a rejected Primary Password are different branches. Check the matching key database and library/build compatibility before treating every failure as a wrong password. Upstream notes Firefox 144+ Linux profiles need NSS 3.113 or newer. Where supported, `NSS_LIB_PATH` prioritizes a trusted existing library directory but may fall back to other locations; verify the actual loaded library. High verbosity can expose the Primary Password and recovered secrets. `--format pass` writes to a password store and can overwrite entries; it is not a passive display format.

Use [upstream usage and compatibility notes](https://github.com/unode/firefox_decrypt), [CLI/profile/error handling](https://github.com/unode/firefox_decrypt/blob/main/firefox_decrypt.py) and [Mozilla's profile-file descriptions](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data) for version or capture differences.
