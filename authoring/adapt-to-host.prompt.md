# Adapt a skill to this Linux host

Run from the repository root. Supply the skill name and the scope of permitted tests.

---

Adapt `skills/<name>/SKILL.md` to the agent's actual Linux environment.

1. Inspect the selected executable, version/implementation and relevant OS, permissions and session capabilities from the agent's own shell. Save machine-specific facts in ignored `work/machine.md`; reuse facts already established.
2. Check included commands against installed help and applicable manuals. Use `scripts/capture_help.py` for known informational invocations when useful; debugger/subcommand help may need separate inspection. Verify meanings and combinations, not just flag spelling. Record missing binaries or capabilities rather than guessing.
3. Keep personal binary paths in local notes or the agent's launch environment. Put supported portable version/feature conditions in the skill. Keep its folder independent and its instructions concise.
4. Run only the authorised fixtures, choosing cases that test the affected behaviour. Retain commands, output, exit status and relevant versions under `runs/`; summarise useful findings in source or evaluation notes. Help capture, procedure execution and agent performance are different results. Preserve actual historical test coverage.
5. Check links and packaging, update the README scope if needed, and report what changed, what ran and what remains uncertain.

Use supporting sources when needed; do not add companion files or sections without a purpose. Leave edits for Git review unless committing was requested. Describe proposed global configuration changes rather than applying them without authorisation.
