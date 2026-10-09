# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md).** It explains where to clone on Linux, how to expose the skill to Pi/Claude Code/Codex, how to adapt it to the actual binaries and versions, and how to ingest documentation to add a tool and commit the result.

This repository also contains the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md). The CLI collection lives directly in this repository root.

## Linux CLI skills: practical MVP

Design date: 2026-10-09. Schema: v0.2. Target: agents working on Linux through Pi, Claude Code, or Codex.

Build one small, portable skill that finds and reads a procedure for the current tool. Keep the tool knowledge in ordinary Markdown. Start with a few useful investigations, then expand the catalogue when those investigations work.

This starter contains a tiered schema, authoring/review prompts, source capture guidance and helper, an optional user-side shell profile, deployment instructions, an evaluation design, and a populated GDB reference with provenance loaded on demand. The GDB procedure has been checked against documentation but has not been executed here. This is a design and starter package, not a completed collection or a measured improvement in agent performance.

## Start here

1. Read the [schema and its rationale](authoring/schema.md).
2. Assign A (full procedure), B (short delta), or C (index only). For A/B, fill the [source intake](authoring/intake.template.md) with the specific knowledge gap and relevant material. Use [help capture](authoring/capture-help.md) when useful for grounding options.
3. Give an LLM the [authoring prompt](authoring/create-tool-card.prompt.md), [A template](authoring/tool-card.template.md) or [B template](authoring/delta-card.template.md), [provenance template](authoring/provenance.template.md), schema, and source packet. C needs only the index row and triage reason.
4. Use the [review prompt](authoring/review-tool-card.prompt.md) to check the result against its evidence, then the [evaluation procedure](evaluation/README.md) to test commands and agent behaviour at the appropriate depth.
5. Add accepted coverage to the [tool index](skills/linux-cli/references/index.md), then copy the complete skill folder into the desired harness location using the [deployment guide](docs/harnesses.md).

The [GDB card](skills/linux-cli/references/gdb.md) shows the intended depth: one bounded job, observable evidence, and useful next steps.

A development index may include a source-reviewed reference whose execution status is visibly `not-run`, as this starter does. Claiming tested support for an environment requires the actual execution and harness checks described below.

See the [validation record](docs/validation.md) for checks executed during this update and the Linux/harness work still untested.

## The four gaps

The previous discussion separated verification from continuation. This design groups them into four knowledge gaps:

| Gap | What a useful reference supplies |
|---|---|
| Selection | The question this tool can answer, conditions where it applies, and an alternative when it cannot answer that question. |
| Reliable execution | Relevant prerequisites, exact commands, defined inputs, effects, output handling, and session requirements. |
| Interpretation | What an observation supports, what it cannot establish, and common misleading results. |
| Follow-up and verification | A next action tied to the observation, a way to test the explanation, and a condition for finishing or reporting an unresolved blocker. |

The [source strategy](authoring/sources.md) maps each gap to useful kinds of material and concrete starting points.

## Architecture

Use one discoverable `linux-cli` skill for the MVP. Its description names the symptoms and tools actually covered; its body directs the agent to a short index and the relevant reference. A/B tools have a card and a provenance companion; C tools have an index row only. These references are not separate discovered skills.

| Tier | Content | Initial planning estimate for 200 tools |
|---|---|---|
| A | Full procedures, decision branches, recovery and verification. | About 40 complex tools. |
| B | Only the non-obvious correction, failure or variant. | About 100 short cards. |
| C | Selection terms and scope in the index; no specialised card. | About 60 entries. |

These are estimates, not quotas. Use observed agent failures to allocate effort and revisit tiers. A familiar tool can still need guidance for a difficult task. The current accepted index contains only GDB (A); no additional tool coverage is claimed by introducing the tier system.

This uses the standard distinction between a skill entrypoint and references loaded as needed. See the [Agent Skills specification](https://agentskills.io/specification). A tool-named request can go straight to its indexed file; a symptom-named request uses the index to choose a tool.

The initial layout is:

~~~text
research-library/
├── README.md
├── GETTING_STARTED.md
├── AGENTS.md
├── CLAUDE.md
├── .gitattributes
├── .gitignore
├── authoring/
│   ├── schema.md
│   ├── create-tool-card.prompt.md
│   ├── review-tool-card.prompt.md
│   ├── intake.template.md
│   ├── local-machine.template.md
│   ├── adapt-to-host.prompt.md
│   ├── tool-card.template.md
│   ├── delta-card.template.md
│   ├── provenance.template.md
│   ├── sources.md
│   └── capture-help.md
├── docs/
│   ├── harnesses.md
│   └── validation.md
├── evaluation/
│   ├── README.md
│   └── case.template.md
├── profile/
│   ├── display-env.sh
│   └── agent-shell.md
├── scripts/
│   ├── capture_help.py
│   └── check_repository.py
├── tests/
│   ├── test_capture_help.py
│   └── test_check_repository.py
├── methodologies/
│   └── arcanum-llm-assessment.md
└── skills/
    └── linux-cli/
        ├── SKILL.md
        └── references/
            ├── index.md
            ├── runtime.md
            ├── gdb.md
            └── provenance/
                └── gdb.md
~~~

The installed runtime unit is only `skills/linux-cli/`. Everything else supports authors and maintainers. All resources needed during tool use live inside that installed folder, so it can be copied without breaking links.

As A/B tools are accepted, add their cards, provenance companions and index rows. For C, add the row alone. Keep raw captures and drafts in ignored `work/`; retain durable evidence in tracked provenance. Do not create empty files for the planned catalogue.

Domain playbooks can connect accepted tool cards inside the same skill: symptom, discriminating check, interpretation, next tool, sufficient evidence. Add one when a supported task needs that progression. At roughly 30-40 indexed tools, review discovery and context cost; this is a checkpoint, not an automatic split. Introduce separate domain entrypoints when symptom-based evaluations show that routing needs them. Keep each resulting skill self-contained. A vector database, generated API, custom MCP server, and central knowledge service are unnecessary for this MVP.

## What is essential

The runtime needs `SKILL.md`, the index, shared execution guidance, and the actual tool references. The authoring schema and prompt make generation consistent. The evaluation template provides a repeatable way to find errors.

`AGENTS.md` instructs agents maintaining this repository. `CLAUDE.md` imports it for compatibility. These repository files are not installed as global instructions and do not carry the tool catalogue.

The optional [display profile](profile/display-env.sh) and [short shell instructions](profile/agent-shell.md) can be applied separately using the [harness guide](docs/harnesses.md). Installing the skill does not apply them. Display defaults are separate from authentication/package-operation settings; editors are never replaced by a successful no-op.

The [capture helper](scripts/capture_help.py) runs known help/version invocations in its current environment, including a prepared container. Its [tests](tests/test_capture_help.py) check evidence capture and failure handling. Captured help is not a successful workflow test.

`.gitattributes` keeps text suitable for Linux checkouts; `.gitignore` excludes local scratch work and run artifacts. Add a repository license when you choose the distribution terms. No license choice is assumed in this starter.

A small [repository checker](scripts/check_repository.py) validates local links, the runtime boundary and the current simple frontmatter. Optional later: an installer that reports conflicts, a Pi package manifest, Codex UI metadata, and CI for repeatable fixtures. Add them when repeated maintenance work justifies them. A checker can establish structure, not diagnostic competence.

## Producing a larger catalogue

Organise production around user tasks, then add the tools those tasks require. A proposed first group is:

| Investigation | Candidate tools | An observable result |
|---|---|---|
| Find relevant configuration or log evidence | `rg`, `find`, `jq` | Locate the right record despite filtering or format complications. |
| Explain an HTTP connection failure | `curl`, `ss` | Identify the failed stage and obtain evidence for the next check. |
| Explain a service failure | `systemctl`, `journalctl` | Connect the service state to the relevant event and verify the explanation. |
| Investigate a stuck process | `ps`, `lsof`, `strace` | Distinguish a plausible wait from evidence of the actual fault. |
| Examine a native crash | `gdb` | Localise the crash using matching artifacts and state the limits of the conclusion. |
| Investigate CPU usage | `perf` | Attribute sampled work within the limits of available symbols and permissions. |

These are 12 candidate tools, not 12 implemented references. The supplied GDB example is the first format specimen. Start by refining that specimen and one basic tool such as `rg`; expand to the first group after both survive realistic tests.

For each tool:

1. Identify the task and guidance gap, choose a provisional tier, and gather only the evidence needed for it. A practical walkthrough, semantics reference and failure example often suffice for A. B can be much smaller; C needs no invented card pipeline.
2. Let the authoring model produce the appropriate card and provenance companion, or C index row. Missing evidence becomes a research question or excluded scope.
3. Review semantics against captured help and applicable manual sections, then run the smallest useful Linux fixture. B needs a focused correction check; A also needs a failure/incomplete-evidence variant.
4. For a card, evaluate whether an agent using it reaches the right outcome. Keep the answer key outside its workspace.
5. Accept the supported workflows and update the index. Keep incomplete drafts under `work/`, outside the installed skill.
6. Record actual failures from use. Revise the affected guidance and reconsider its tier instead of expanding every card.

The LLM can do source extraction, drafting, reference checking, fixture preparation, and run analysis. Your recurring input can be limited to choosing useful tasks and resolving source conflicts or intended operating scope. Better prose alone does not justify marking a procedure as tested.

## MVP shortcomings and triggers for expansion

- **Retrieval is initially simple.** A broad skill can fail to activate; an index can miss the user's phrasing. Test explicit invocation and ordinary requests separately. Add aliases or split domains when observed failures justify it.
- **Coverage is narrow.** One to three procedures will not capture an entire debugger or system utility. Put excluded modes in the card and use authoritative documentation for unsupported work.
- **Compatibility is declared, not exhaustive.** GNU, BusyBox, distribution, kernel, and tool-version differences need targeted checks. Add a tested environment matrix as actual runs accumulate.
- **Source review is not execution.** A checked tutorial can still yield a bad local command. Record exact test coverage and keep unexecuted status visible.
- **Captures check documentation, not diagnosis.** Compare relevant versions and semantics, then test the procedure separately. When assessing the optional profile, compare baseline, profile only, and profile plus skill to distinguish the sources of improvement.
- **Procedures influence behaviour without guaranteeing it.** Test conclusions, recovery, and unnecessary commands. Do not grade by how closely an agent repeats the document.
- **Runtime capabilities remain external.** A reference cannot create a persistent terminal, add permissions, or extend a run budget. The shared runtime guide explains when a workflow needs those capabilities.
- **Maintenance is manual at first.** Use source locators, review dates, and Git history. Automate freshness checks after there is enough content to maintain.

For the mechanical problems discussed earlier: native shell access permits normal CLI composition; selective reference loading limits catalogue context; batch procedures reduce session requirements where appropriate; explicit evidence and next-step criteria help sustain an investigation. Each still needs an execution test in the actual harness.
