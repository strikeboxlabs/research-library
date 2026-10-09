---
name: "{{skill-name}}"
description: "{{Specific supported tasks, symptoms and tool; no promises beyond the included coverage}}"
---

# {{tool}} — {{practical capability}}

Tier: A.

## Identity and selection

- Executable and aliases: {{executable; common alternative names/search terms}}
- Use for: {{question or symptom}}
- Choose another approach when: {{important boundary and alternative; omit only if immaterial}}

## Preconditions

{{Required inputs and environment; check only facts relevant to this procedure. State whether it works as a bounded command, batch job, or persistent session. Mention effects or privileges only when they matter.}}

## Procedure

### {{workflow name}}

**Question:** {{what this workflow establishes}}

**Inputs and effects:** {{defined input values, paths and operational effects}}

**Actions:** {{commands or concrete steps; keep detailed source mappings in the provenance companion}}

~~~bash
# Replace with a supported command using defined inputs.
~~~

**Observe and decide:**

| Observation | Meaning and limits | Next action |
|---|---|---|
| {{expected observation}} | {{what it establishes}} | {{targeted next step}} |
| {{inconclusive or failing observation}} | {{what remains unknown}} | {{recovery or needed evidence}} |

**Finish when:** {{observable completion evidence or specific unresolved blocker}}

## Failure and recovery

| Failure | Discriminating check | Recovery |
|---|---|---|
| {{likely failure relevant to the procedure}} | {{check that changes the next decision}} | {{bounded corrective action or alternative}} |

## Verification and gaps

- Source review: {{pending/checked; actual review date and scope}}
- Execution: not-run.
- Agent evaluation: not-run.
- Known gaps: {{unsupported modes, version uncertainty, missing evidence}}

Sources and claim mapping: [provenance](references/provenance.md). Read when checking evidence, compatibility or maintenance history.
