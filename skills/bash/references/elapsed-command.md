# Measure one selected finite command

Use Bash's `time` reserved word for an already selected, finite ordinary command. Require the actual Bash interpreter, approved program/arguments and fresh output files in an owned directory. Define `program` as the trusted executable, `args` as its Bash argument array, and `stdout_file`, `stderr_file` and `timing_file` as those separate destinations. Ensure the command's own duration or a separately agreed stop mechanism bounds the operation; `time` does not impose a deadline.

~~~bash
if (
  export LC_ALL=C
  TIMEFORMAT='elapsed_seconds=%R'
  { time "$program" "${args[@]}" >"$stdout_file" 2>"$stderr_file"; } \
    2>"$timing_file"
); then
  status=0
else
  status=$?
fi
~~~

The inner redirects retain the command's streams; the outer group captures Bash's timing message. The conditional retains the command status even when it fails. A redirection failure also fails the operation and needs its own diagnosis. Keep the selected arguments, status and all three results together. A duration can be recorded for a failed command; it is not evidence of task success. Inspect the actual result before reusing a numeric field.

`%R` reports elapsed seconds, whereas user/system CPU time are different measures. A command including network access also includes local work, transport and waiting; this does not isolate server processing. For a pipeline, Bash times the pipeline as a whole and ordinarily returns its last command's status; enable `pipefail` deliberately when upstream failure must remain visible. Suppressing the producer's stderr and grepping its output can conceal failures.

Keep comparisons on the same units and selected command context. 0.131 seconds is 131 milliseconds. Repeated finite measurements can characterize an ordinary local workload; authentication enumeration is outside this procedure. Sleeping between background launches controls launch spacing, not maximum active concurrency, and does not wait for or collect each child's result.

The Bash variable is `TIMEFORMAT`; an empty value suppresses its timing message. Zsh also supports `time`, with `TIMEFMT` controlling its display. Do not infer a missing facility merely because a Bash-specific formatting variable does not work in another shell. An external executable named time has its own option/output contract.

See [Bash time and TIMEFORMAT](https://manpages.debian.org/bookworm/bash/bash.1.en.html) and [Zsh time grammar](https://zsh.sourceforge.io/Doc/Release/Shell-Grammar.html).
