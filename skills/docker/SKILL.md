---
name: docker
description: Run a pinned Linux tool environment, execute in a selected running container, evaluate restricted exec/device access or distinguish saved image layers from a container filesystem export. Use when old Python or Java dependencies, bind-mount ownership, configured environment values, remote daemons, registry source acquisition or published ports complicate reproduction.
---

# Reproduce the tool environment

Read this entire SKILL.md before acting; reuse complete current context. Select the intended daemon and image or existing container for the task before execution. For a selected registry image, source acquisition or its approved inspection shell, read [registry and source inspection](references/registry-source.md) fully. For commands in an existing container, a restricted sudo `exec` grant or exposed-device access, read [exec and filesystem access](references/exec-and-device-access.md) fully before that procedure. Read [inspection](references/inspection.md) for mounts or configured environment values, or [image archives](references/image-archives.md) for layer history, exports and offline image transfer. Finish with the requested artifact or daemon observation and its status; an image, container UID or mount path alone does not prove host access.

Separate the tool's runtime from the system being investigated. A legacy Python/Java image may reproduce artifact generation without reproducing the target application's runtime, dependencies or mitigations. Record the image ID/digest, architecture, tool version and invocation; a mutable tag alone is weak reproduction evidence.

Check the active Docker context and `docker version` where direct daemon access is available before using local paths. A restricted exec-only sudo grant does not grant those extra subcommands; use available context/configuration evidence and retain unresolved attribution instead of requiring an unpermitted query. Bind mounts refer to the **daemon host**, not necessarily the CLI machine. Inspect a supplied Dockerfile and its build context first: `RUN`, package builds and downloaded setup scripts execute code during building. A container is not a guarantee that an unknown workload is harmless.

Access to a rootful Docker daemon can confer root-level control over the **daemon host**, including through host bind mounts. This authority comes from the daemon and access to its socket/API, not from the Docker client being a SUID executable. A socket can belong to a custom group such as `engineer`; do not assume the group must be named `docker`. A group entry is a lead: establish the effective groups, selected context and actual daemon access. Rootless Docker runs its daemon and containers in a user namespace without host root privileges; container UID 0 therefore does not establish host UID 0. Check the applicable [daemon access model](https://docs.docker.com/engine/install/linux-postinstall/) and [rootless mode](https://docs.docker.com/engine/security/rootless/) before attributing privilege. A filesystem root changed with chroot alone does not explain the daemon's authority.

For an already prepared image with Python 3, define `image` as its pinned reference, `inputs` as a dedicated existing absolute directory containing reviewed `job.py` and required data, and `outputs` as a dedicated existing writable absolute directory:

~~~bash
docker run --rm --network none --user "$(id -u):$(id -g)" \
    --mount "type=bind,src=$inputs,dst=/input,readonly" \
    --mount "type=bind,src=$outputs,dst=/output" \
    --workdir /output --entrypoint python3 "$image" /input/job.py
~~~

Inputs are read-only; generated artifacts must go under `/output`. Running with the invoking UID/GID avoids routine root-owned output, but the image may require a writable cache/home or a named account. Diagnose that requirement instead of mounting the whole home directory or switching to privileged mode. The example deliberately has no network and assumes dependencies are already present; a callback-generating job can fail under that condition.

`--mount` normally fails on a missing bind source, whereas `-v` can silently create a directory. `--rm` removes the container's writable layer, so verify retained artifacts in the output bind and the exit status. A generated file does not prove the same file can be consumed remotely.

If a service is required, publish only the intended address/port. `-p 127.0.0.1:host_port:container_port` binds locally; omitting the address normally publishes on all interfaces. `EXPOSE` alone does not publish a host port. Remove temporary containers after the test, preserving needed output first.
