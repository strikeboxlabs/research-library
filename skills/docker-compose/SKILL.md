---
name: docker-compose
description: Resolve and run a selected Docker Compose project with explicit file, directory and service scope. Use for legacy docker-compose differences, interpolation, hidden startup failures and capability or privileged-wrapper boundaries.
---

# Resolve the project that will actually run

Read this entire SKILL.md before acting. Establish the daemon, Compose implementation and project inputs, inspect the resolved model, then run only the selected reviewed services. Read [capabilities and wrappers](references/capabilities-and-wrappers.md) fully when a privilege wrapper or unusual capability grant affects execution. Finish with actual service/exit evidence and the intended cleanup; configuration validity alone is not successful startup.

Use an invocation array `compose=(docker compose)` for the plugin, or `compose=("$compose_bin")` for a verified standalone `docker-compose` executable. Check `"${compose[@]}" version` and relevant command help; current plugin flags need not exist in the older Python implementation. Define absolute `compose_file`, `project_dir`, a unique owned `project`, the selected `service`, and a fresh private `resolved` file. Inspect build sources, images, mounts, credentials and any `.env`/env-file inputs first.

~~~bash
umask 077
"${compose[@]}" -f "$compose_file" --project-directory "$project_dir" -p "$project" config > "$resolved"
~~~

Check status and read the resolved file before execution. `config` merges selected files, substitutes variables and expands shorthand; the saved result can contain secrets. A wrapper that copies YAML into a temporary directory can change relative bind/build paths and environment discovery. Match the effective directory and environment instead of assuming the original filename controls them. `command` changes the image command; it does not implicitly supply a shell for pipes or variable expansion. A reviewed shell command requires an explicit shell, such as list-form `command: ["/bin/sh", "-c", "..."]`, and the image entrypoint still matters.

For an approved project with already prepared images and intentional dependencies:

~~~bash
"${compose[@]}" -f "$compose_file" --project-directory "$project_dir" -p "$project" up -d "$service"
"${compose[@]}" -f "$compose_file" --project-directory "$project_dir" -p "$project" ps -a
"${compose[@]}" -f "$compose_file" --project-directory "$project_dir" -p "$project" logs --tail 100 "$service"
~~~

`up` can recreate existing containers and start dependencies; use the unique project deliberately. Add `--no-deps` only when dependencies are intentionally excluded, and `--build` only for a reviewed build context that the task requires. For a one-shot attached job on supporting versions, `up --exit-code-from "$service" "$service"` returns that service's exit status and stops the group when a container exits. An attached interruption can return zero despite incomplete work. Detached command success establishes startup initiation, not health or job completion; inspect actual state, logs and the requested application/artifact result.

After preserving needed output, remove only this owned project's containers/networks:

~~~bash
"${compose[@]}" -f "$compose_file" --project-directory "$project_dir" -p "$project" down
~~~

`down --volumes` additionally removes declared named and attached anonymous volumes; select it only when deleting that data is intended. Default `down` retains volumes but a subsequent run need not reuse unnamed ones. See [project selection](https://docs.docker.com/reference/cli/docker/compose/), [resolved configuration](https://docs.docker.com/reference/cli/docker/compose/config/), [startup status](https://docs.docker.com/reference/cli/docker/compose/up/) and [cleanup](https://docs.docker.com/reference/cli/docker/compose/down/).
