---
name: ipython
description: Inspect an owned IPython launcher's version and acquired profile/startup configuration. Use when working directory, profile selection or installed package identity can explain unexpected startup behavior without launching a session to test untrusted code.
---

# Inspect the selected IPython startup context

Read this entire SKILL.md before acting. Identify the selected trusted launcher/environment and its version, then inspect the acquired launch/profile inputs as text. No conditional resources are required. Finish with the supported version/profile association and unresolved startup-code effects; a version string alone does not establish the code loaded by a different process.

Define `ipython_bin` as the actual trusted installed launcher, not an acquired executable. From an owned trusted working directory:

~~~bash
"$ipython_bin" --version
~~~

Retain status and output alongside the launcher/environment. This is a version query, not an interactive session or a request to execute a profile. If the selected launcher is untrusted or its interpreter mapping is unknown, inspect it and its distribution metadata without executing it. A trusted Python3.8+ environment can read that metadata without importing IPython:

~~~bash
"$python_bin" -I - <<'PY'
from importlib.metadata import PackageNotFoundError, version
try:
    print(version("ipython"))
except PackageNotFoundError:
    raise SystemExit("IPython metadata unavailable in this environment")
PY
~~~

Define `python_bin` as that environment's trusted interpreter before using the second command. Isolated mode excludes the current directory/user site, so missing metadata does not prove every possible launch environment lacks IPython. Site initialization can still run that trusted environment's startup hooks; this is not a sandbox. Metadata may differ from a wrapper-selected environment or be stale.

For the acquired job/launch configuration, establish the actual working directory, explicit profile and IPython directory, relevant environment and account. A shell `cd directory && ipython` invokes IPython only after successful cd; a process command line showing that expression does not prove which profile files loaded. Default IPython files normally live under the account's .ipython directory, while explicit settings and version-specific system locations can change the search. Inspect the selected acquired configuration/startup files as text; Python configuration, extensions and startup scripts can execute code. A debug launch with `-c 'exit()'` still starts the application and is not static inspection.

Historical CVE-2022-21699 concerns untrusted current-directory profile startup code; the maintained fixes include8.0.1,7.31.1,7.16.3 and5.11 in their corresponding branches. Match the installed distribution's patch/build evidence as well as its numeric version. Do not plant a profile or launch someone else's scheduled session to test applicability. A file's owner alone does not prove which process created it, and a process UID is separate from directory ownership or modification rights.

See [IPython configuration and directory inputs](https://ipython.readthedocs.io/en/stable/config/intro.html), [maintainer advisory](https://github.com/ipython/ipython/security/advisories/GHSA-pq7m-3gw7-gq5x) and [Python distribution metadata](https://docs.python.org/3.12/library/importlib.metadata.html) for version-specific interpretation. No installation, profile creation or application execution is required to finish the configuration review.
