# Optional shared shell guidance

Merge the bullets below into the instruction file already loaded by your harness only if you want them active outside this skill. This file is not an installer. Keep existing task permissions and intentional interactive workflows.

- Prefer a documented batch form when it preserves the task. For interaction, establish that the harness can retain a session, send input, collect output and cancel it. Avoid unattended password, pager and editor prompts.
- Give potentially long commands an appropriate timeout or a managed session with a stop condition. Distinguish completed results from a timed-out sample.
- Save diagnostic stdout/stderr to task artifacts when output is large, preserve the relevant exit status, and inspect excerpts. Bound collection where appropriate; do not discard needed evidence merely to shorten tool output.
- Define variables and working directories in the invocation that needs them unless persistence has been established. Preserve a live debugger session when its state is needed.
- For an already-authorised operation requiring sudo in unattended execution, use `sudo -n` and treat failure as a missing capability. Do not infer permission to elevate from this instruction.
- Use explicit noninteractive editing/message options for the intended operation. Do not turn editor requests into successful no-ops with a blanket `EDITOR=true`.
