# Runtime guidance

Use only the parts relevant to the selected workflow. Reuse environment facts already established in the current task.

## Ordinary command execution

- Resolve the installed skill's references relative to the skill folder. Use explicit paths for the target and output artifacts.
- Check the actual executable and version when the procedure depends on its implementation or flags. GNU and BusyBox variants may expose different options.
- Define command inputs in the same shell invocation that uses them unless the runtime demonstrably preserves shell state. Do not assume a previous call preserved variables or the working directory.
- Preserve stdout, stderr, exit status, and any reported truncation. For large output, save the complete result to the task's artifact directory and inspect relevant excerpts.
- Use an appropriate command time limit. When a command times out, distinguish a partial observation from a completed sample.
- Keep pipelines and composed commands when they help; preserve the status of the stage relevant to the question.

## Sessions

Check whether a workflow needs one bounded command, a batch script, or an interactive process. Prefer a batch form when it preserves the intended investigation.

For interactive work, the harness must be able to keep the process alive, send input, read output, identify completion, and cancel it. An actual terminal may be required by a particular program, but not by every interactive interface.

If those capabilities are absent, use a documented batch equivalent or report the missing capability. Do not repeatedly launch a debugger while pretending its live process state survived between calls. Reopening the same offline core for additional batch queries is a different, valid operation.

Track any process the task starts and end or detach it according to the procedure. Debugger attach, tracing, and service-control commands can have effects beyond file reads; apply the task's existing authorization to the actual chosen operation.

## Conclusions

Tie the conclusion to observed output and the scope of the measurement. Keep an unresolved hypothesis distinct from a verified cause. Report missing permissions, unavailable symbols, truncation, or unsupported versions only when they materially limit the answer.
