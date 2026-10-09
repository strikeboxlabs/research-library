# Maintaining this repository

This repository contains independently installable Linux tool skills and existing assessment methodologies. The rules below apply to the skills, their authoring tools and documentation. Preserve unrelated methodology content when working on the CLI collection.

- Start with `GETTING_STARTED.md` for checkout, Linux adaptation, source ingestion and the Git workflow. Keep setup instructions in the repository rather than only in chat.

- Read `authoring/schema.md` before creating or substantially changing a skill. Use `authoring/create-skill.prompt.md` and the appropriate skill template.
- Put each tool's accepted guidance in its own `skills/<name>/SKILL.md`, with its own precise discovery description. Each folder is independently installable. Do not introduce an umbrella skill or make one tool's guidance a reference owned by another skill.
- Assign coverage tier A (full procedure), B (short correction), or C (defer; no installed skill). Match authoring effort to a useful knowledge gap. Assume the agent already uses the CLI competently.
- Keep executable command semantics supported by the installed tool, an authoritative source, or a recorded test. Record evidence gaps instead of inventing results.
- Distinguish source review, command execution, and agent evaluation. A formatting check does not establish any of the latter two.
- Keep runtime resources inside the individual skill folder. No sibling-skill, repository-level or shared-runtime file dependency may be required to use a copied skill. Put the useful procedure directly in `SKILL.md`; add internal references only for substantial conditional detail.
- Update the repository README's skill catalogue when accepted coverage changes. It is a maintainer/installer overview, not a runtime router. Do not advertise unimplemented procedures.
- Keep durable sources and claim mappings in the skill's own `references/provenance.md`. Load sources on demand; keep verification and material limits in `SKILL.md`. `work/` is ignored and is not a permanent provenance store.
- Keep drafts and raw source intake in `work/`. Keep local test output in `runs/`; record durable test summaries without sensitive machine data.
- Keep machine-specific binary paths and launch facts in ignored `work/machine.md`. Use `authoring/adapt-to-host.prompt.md` when adapting a skill to a Linux host; commit evidence-backed portable conditions and outcomes.
- Before delivery, check each skill's frontmatter, relative links, source-ID references, command inputs, catalogue coverage and portability when copied alone. For changed executable procedures, run a relevant Linux fixture when available and report exactly what was exercised.
- Run `python3 scripts/check_repository.py` and relevant helper tests when changing this packaging. These are structural/helper checks, not Linux tool or agent evaluation.
- Preserve the task's authorization and environment limits. Creating a reference does not authorize running its examples against a live system.
- No mandatory external services, model-specific tool names, automatic package installation, or permission changes belong in the portable skill.
- Files in `profile/` are optional user-side examples. Editing or installing the skill does not apply them to a user's shell or harness configuration.
