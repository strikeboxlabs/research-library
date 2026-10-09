# Maintaining this repository

These instructions apply to authors of the Linux tool skills. Preserve unrelated assessment methodologies.

- Start with `GETTING_STARTED.md` for Linux setup and source ingestion. Use `authoring/schema.md` and `authoring/create-skill.prompt.md` when adding skills.
- Each tool is independently installable as `skills/<name>/SKILL.md`. Keep every required resource inside its folder; no umbrella or shared runtime dependency.
- Assume workers already use the CLI competently. Keep instructions that improve selection, execution, interpretation or recovery. Adapt headings to the task; omit generic advice and repetition.
- Supporting files are optional. Use a short `references/sources.md` when source notes help maintenance; detailed claim maps are reserved for genuinely disputed or complicated guidance.
- Verify command semantics and important interpretations. Report documentation review, actual execution and agent outcomes accurately; do not invent test results.
- Keep machine-specific facts and raw input in ignored `work/`, and raw test artifacts in `runs/`. Commit useful portable conditions and concise, non-sensitive evidence.
- Update the README catalogue for accepted skills. Run the repository checker and relevant tests after packaging changes; test changed command behaviour in an appropriate Linux fixture when available.
- Keep source intake and example commands within the user's authorisation. Skill installation does not install tools or apply the optional settings in `profile/`.
