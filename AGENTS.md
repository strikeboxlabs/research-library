# Maintaining this repository

This repository contains portable Linux CLI guidance for agents and existing assessment methodologies. The rules below apply to the CLI skill, its authoring tools and documentation. Preserve unrelated methodology content when working on the CLI collection.

- Start with `GETTING_STARTED.md` for checkout, Linux adaptation, source ingestion and the Git workflow. Keep setup instructions in the repository rather than only in chat.

- Read `authoring/schema.md` before creating or substantially changing a tool reference. Use the authoring prompt and template when useful.
- Assign coverage tier A (full procedure), B (short delta), or C (index only). Match authoring effort to the demonstrated knowledge gap; do not create full cards for every executable.
- Keep executable command semantics supported by the installed tool, an authoritative source, or a recorded test. Record evidence gaps instead of inventing results.
- Distinguish source review, command execution, and agent evaluation. A formatting check does not establish any of the latter two.
- Keep runtime resources inside `skills/linux-cli/`. Update the index when supported coverage changes. Do not advertise unimplemented procedures.
- Keep durable sources and claim mappings in tracked companion references under `skills/linux-cli/references/provenance/`. Load these on demand; keep verification and material limits in the tool card. `work/` is ignored and is not a permanent provenance store.
- Keep drafts and raw source intake in `work/`. Keep local test output in `runs/`; record durable test summaries without sensitive machine data.
- Keep machine-specific binary paths and launch facts in ignored `work/machine.md`. Use `authoring/adapt-to-host.prompt.md` when adapting a card to a Linux host; commit evidence-backed portable conditions and outcomes.
- Before delivery, check skill frontmatter, relative links, source-ID references, command inputs, and index coverage. For changed executable procedures, run a relevant Linux fixture when available and report exactly what was exercised.
- Run `python3 scripts/check_repository.py` and relevant helper tests when changing this packaging. These are structural/helper checks, not Linux tool or agent evaluation.
- Preserve the task's authorization and environment limits. Creating a reference does not authorize running its examples against a live system.
- No mandatory external services, model-specific tool names, automatic package installation, or permission changes belong in the portable skill.
- Files in `profile/` are optional user-side examples. Editing or installing the skill does not apply them to a user's shell or harness configuration.
