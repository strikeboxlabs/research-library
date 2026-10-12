---
name: env
description: Run a selected trusted diagnostic with a deliberate environment using GNU env. Use when inherited variables, missing startup inputs or terminal labels obscure a reproducible local result.
---

# Control the diagnostic's environment

Read this entire SKILL.md before acting. Select the trusted executable and intended environment change; retain its actual output/status and configuration differences. No conditional resources are required. A clean environment does not establish isolation, new privileges or a working terminal.

Confirm `env --version` and local help. Define `program` as the verified absolute path of a trusted diagnostic executable and `argument` as its selected ordinary input argument. For the intended clean-environment comparison:

~~~bash
env -i LC_ALL=C "$program" "$argument"
status=$?
~~~

`-i` ignores inherited environment entries; following assignments supply deliberate replacements. It affects this child, not the parent shell's exported environment. Omit the argument if this diagnostic needs none; keep a real argument vector rather than placing a whole command string in `program`. Env invokes an executable, not a shell builtin or shell command parser. Use an absolute path to avoid relying on command-search behavior after PATH removal.

Compare against the same trusted program/input in its normal context. A changed result can reflect removed configuration, locale, proxy or runtime inputs. Missing HOME, PATH, DISPLAY or other required inputs can make a legitimate program fail; add only the established requirement for the next comparison. Clearing variables leaves working directory, descriptors and process credentials intact. The child may load configuration or change its own environment.

`TERM` names the terminal type expected by a consumer; setting it does not emulate that terminal, allocate a PTY or prove the required terminfo entry exists. Match the real terminal and installed capability database before attributing an unknown-terminal error to authentication.

An acquired CI/container environment describes that process at that moment. It does not establish the host environment, another container's values or their origin. Trace a relevant variable through the job, runner and container configuration when diagnosing inheritance; a matching name alone does not establish provenance or credential type. Keep diagnostic output limited to the needed nonsecret fields instead of publishing the whole environment into a shared job log. See [GitLab runner variable configuration](https://docs.gitlab.com/runner/configuration/advanced-configuration/).

Without a command, env prints the resulting environment, potentially including secrets; that is a separate inspection task. GNU env normally returns the child's status; its own failures use 125, a command that cannot be invoked 126, and one not found 127. These numbers can also be returned by the child, so retain diagnostics rather than identifying the failed stage from a number alone. Finish with the actual comparison and unresolved prerequisite.

Reference: [GNU env manual](https://www.gnu.org/software/coreutils/manual/html_node/env-invocation.html).
