---
name: firejail
description: Inspect the selected Firejail executable's version and compile-time features on Linux. Use when sandbox configuration, runtime isolation and vendor patch evidence must be kept separate.
---

# Identify the selected sandbox build

Read this entire SKILL.md before acting. Require the selected host/context and verified executable, then retain version/status and complete feature output. Finish with build identity and supported configuration findings; missing binary, package provenance or live policy remains unresolved. This narrow task has no additional required resources.

Define `firejail_bin` as the actual verified absolute executable path for this installation:

~~~bash
"$firejail_bin" --version
"$firejail_bin" --help
~~~

These information options do not launch a sandboxed application. Preserve the complete release, compile-time support fields and invocation context. A compiled-in feature is available capability, not proof the selected process uses it. Disabled AppArmor support, for example, describes this build; it does not determine every host confinement mechanism.

An observed command line naming Firejail and a profile is evidence about that process's invocation, not the effective contents of the profile or all namespaces and restrictions. A procfs PID is relative to its visible namespace, and process arguments can change; correlate the process, executable and host context before making an isolation claim.

For a patch question, establish the exact executable's package/source provenance and full vendor revision, then consult that vendor's advisory. An upstream version alone can miss backports or a locally built replacement. Group ownership or a filename returned by a search is not evidence of setuid mode, effective access or a successful privilege transition.

Retain the requested metadata and unresolved runtime-policy or provenance gaps. A process join or application launch is a different operation; neither is needed to identify this build.

See the [upstream manual](https://github.com/netblue30/firejail/blob/master/src/man/firejail.1.in) for information options and configuration semantics.
