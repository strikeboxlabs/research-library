# Local Linux authoring environment

Copy to ignored `work/machine.md`. Fill from the actual agent execution environment. This is local authoring context, not an automatically loaded runtime reference. During the later Linux pass, put stable shared-image facts the worker needs into its relevant skill reference or references/environment.md, following adapt-to-host.prompt.md. Keep node-specific/private details here; workers must not depend on this authoring note.

- Recorded date:
- Distribution and release:
- Kernel and architecture:
- Agent/harness and version:
- Shell and effective user/privileges relevant to the task:
- Python version:
- Batch/persistent-session capability actually observed:

| Tool | Selected executable path | Version / implementation | Capture location | Relevant differences or missing capability |
|---|---|---|---|---|
| {{tool}} | {{observed, not assumed}} | {{observed}} | {{work/sources/...}} | {{specific limitation or none observed}} |

## Local launch settings

{{Any deliberate PATH or display settings needed for this account. Do not dump credentials or the full environment.}}

## Executed checks

{{Named cases, outcome, command/output artifact locations, and what was not tested. Help capture is distinct from procedure execution.}}

## Portable changes to propose

{{Version/feature conditions, invocation corrections or interpretation changes justified by evidence. Keep personal paths and machine identity in this ignored note.}}
