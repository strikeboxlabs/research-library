# Configure before building an existing CLI

Use when a reviewed project provides an Autotools `configure` script or when the produced CLI lacks a required feature. Confirm the selected source revision and its build instructions. Configure, Makefile generation and compilation execute source-controlled programs; `--help` is also execution. Do not use them as a trust check on unknown code.

Read the project's dependency/feature options and inspect the actual reviewed `configure` helper. Define `source_dir` as that selected source directory. For a project whose instructions support an in-tree build:

~~~bash
(
  cd -- "$source_dir" || exit
  ./configure > "$configure_log" 2>&1
)
status=$?
~~~

Here `configure_log` is a fresh private file. Require success before make. If the project supports a separate build directory, follow its documented invocation from that directory rather than assuming every project supports out-of-tree builds. Do not run `autoreconf` merely because a downloaded source archive lacks configure; that introduces additional dependencies and execution whose need should be established first.

Configure checks can select a compiler, headers, libraries and optional features. The command completing does not mean every optional feature was enabled. Review its summary and generated configuration against the requested task. A compiler test failure may be a bad compiler/linker flag, unavailable development file or incompatible architecture; preserve the underlying diagnostic from the log rather than only the final rejection.

For the legacy Sucrack project, `--enable-statistics` is the documented configure option for its statistics display. An ordinary successful configure/make can produce a binary that warns that `-a`/`-s` are unavailable. If statistics are unnecessary, omit those switches; if the task requires them, use that supported configure option and the project's rebuild rules, then inspect the actual resulting binary's help. Do not assume the warning means authentication attempts did not run.

After the selected build, check the exact project-defined output. Sucrack's in-tree build places the CLI in `src/sucrack`; this is a build-tree-relative artifact, not a deployed image path. Review its help/feature banner where running the trusted artifact is permitted. Deployment or authentication is a subsequent task.

Do not make `make install`, privileged compilation, or deleting the source's Git metadata a default build step. Keep the source revision and the configured feature choice so that an apparent success can be distinguished from a stale artifact.

See [GNU make's manual](https://www.gnu.org/software/make/manual/make.html) and Sucrack's [build options](https://github.com/hemp3l/sucrack/blob/master/README.md) / [configure definition](https://github.com/hemp3l/sucrack/blob/master/configure.ac).
