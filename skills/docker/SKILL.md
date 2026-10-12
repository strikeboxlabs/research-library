---
name: docker
description: Run a pinned Linux tool environment, configure an owned service container, execute in a selected running container or distinguish image layers from filesystem exports. Use for dependency, daemon, mount, network and restricted-exec context.
---

# Reproduce the tool environment

Read this entire SKILL.md before acting; reuse complete current context. Select the intended daemon and image or existing container for the task before execution. For a selected registry image, source acquisition or its approved inspection shell, read [registry and source inspection](references/registry-source.md) fully. For commands in an existing container, a restricted sudo `exec` grant or exposed-device access, read [exec and filesystem access](references/exec-and-device-access.md) fully before that procedure. Read [inspection](references/inspection.md) fully for a provisioned TLS daemon connection, network metadata, local image inventory, mounts or configured environment values, [service configuration](references/service-configuration.md) for copying owned configuration and selecting start versus restart, or [image archives](references/image-archives.md) for layer history, exports and offline image transfer. Finish with the requested artifact or daemon observation and its status; an image, container UID or mount path alone does not prove host access.

Separate the tool's runtime from the system being investigated. A legacy Python/Java image may reproduce artifact generation without reproducing the target application's runtime, dependencies or mitigations. Record the image ID/digest, architecture, tool version and invocation; a mutable tag alone is weak reproduction evidence.

A Linux container supplies userspace and shares its daemon host's kernel; choosing an old image does not select that distribution's historical kernel. For an acquired statically linked ELF, a failure is not explained simply by the host's newer glibc. Establish the actual error and dependency/syscall requirements before choosing a compatibility environment. See [container/kernel model](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).

Check the active Docker context and `docker version` where direct daemon access is available before using local paths. `docker --version` reports the **CLI** version only; `docker version` separates Client from Server/Engine and runtime components. Preserve command status and the selected context: a daemon error or missing Server section leaves its version unknown, even if Client output was printed. Do not match an Engine advisory against a client version, or infer missing security backports from an upstream version alone. See [Docker's component/version contract](https://docs.docker.com/reference/cli/docker/version/).

A restricted exec-only sudo grant does not grant those extra subcommands; use available context/configuration evidence and retain unresolved attribution instead of requiring an unpermitted query. Bind mounts refer to the **daemon host**, not necessarily the CLI machine. Inspect a supplied Dockerfile and its build context first: `RUN`, package builds and downloaded setup scripts execute code during building. A container is not a guarantee that an unknown workload is harmless.

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

On Linux, `--network host` shares the daemon host's network namespace and discards published-port mappings. It makes that host's loopback reachable in the container and removes network isolation; it is not a universal prerequisite for outbound HTTP. Select it only for an established owned task needing that context, rather than copying it as a compatibility fix. See [host-network semantics](https://docs.docker.com/engine/network/drivers/host/).

`-i` keeps standard input open; `-t` allocates a pseudo-terminal. Combined `-it` does not select a shell or daemon mode. The image's ENTRYPOINT/CMD and any explicit command determine what runs; `-d` selects detached operation separately. Inspect those inputs before an approved interactive session, and choose the actual supported executable as in the registry/source reference. Terminal allocation can change output bytes and fails without an appropriate TTY; omit it for byte-sensitive pipelines or unattended artifact jobs. Neither a container root prompt nor `-it` establishes the daemon host's identity or authority. See [run input and terminal options](https://docs.docker.com/reference/cli/docker/container/run/).
