---
name: forge
description: Diagnose Foundry Forge build failures using an explicit project root, local compiler availability and scoped trace logs. Use when missing dependencies, remappings, helper commands or an empty build obscure the actual failure.
---

# Diagnose a Foundry build

Check `forge --version` and `forge build --help`; this is the Ethereum Foundry tool. Define `project` as the absolute path to a reviewed project working copy, and `log` as a fresh private log path. Inspect its `foundry.toml`, selected profile, source paths, remappings and compiler requirements first. A default root may come from the Git repository or current directory rather than the directory assumed in a walkthrough.

For a build using available local dependencies and compiler versions:

~~~bash
umask 077
RUST_LOG=trace forge build --root "$project" --offline > "$log" 2>&1
~~~

This runs a build and can write cache/artifacts and invoke helper programs. `--offline` prevents normal network access and missing compiler downloads; it does not supply dependencies or isolate arbitrary external tooling. Preserve the exit status and log. Narrow `RUST_LOG` to the relevant crate/module after locating the failing stage; trace output can reveal paths and other sensitive context.

**Illustrative diagnoses:**

| Observation | Next decision |
|---|---|
| `Nothing to compile` | Check the root/source configuration and cache state before claiming a fresh successful compilation. Do not clear artifacts just to hide the ambiguity. |
| A `git submodule status` helper returns `not a git repository` | Inspect the logged working directory and dependency layout; the helper failure and overall build result are separate observations. |
| Offline mode reports a missing compiler | Match the project's required compiler to locally available versions; obtain the missing version only as a separate approved environment change. |
| Import/remapping error | Check the referenced file, installed dependency and actual remapping before changing compiler options. |

`RUST_LOG` enables events emitted by instrumented code, not a complete system-call trace. A log naming `git` does not establish the executable path ultimately resolved by the OS. For a permitted disposable reproduction that needs that evidence, a process/system-call tracer can observe actual child execution, but it also runs the build and can affect privileged behavior.

When comparing a sudo invocation, retain RunAs identity, effective PATH/configuration and the actual binary version. A locally downloaded Forge release is not proof of a restricted target binary's behavior. Diagnose helper resolution without inserting replacement executables into PATH or running an elevated build merely to see what happens.

See the [build options](https://getfoundry.sh/reference/forge/build/) and [Foundry logging guide](https://github.com/foundry-rs/foundry/blob/master/docs/dev/debugging.md) for release-specific diagnostics.
