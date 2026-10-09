---
name: docker
description: Run a pinned Linux tool environment with explicit input/output mounts and runtime selection. Use when old Python or Java dependencies, bind-mount ownership, remote daemons or published ports complicate reproduction.
---

# Reproduce the tool environment

Separate the tool's runtime from the system being investigated. A legacy Python/Java image may reproduce artifact generation without reproducing the target application's runtime, dependencies or mitigations. Record the image ID/digest, architecture, tool version and invocation; a mutable tag alone is weak reproduction evidence.

Check the active Docker context and `docker version` before using local paths. Bind mounts refer to the **daemon host**, not necessarily the CLI machine. Inspect a supplied Dockerfile and its build context first: `RUN`, package builds and downloaded setup scripts execute code during building. A container is not a guarantee that an unknown workload is harmless.

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

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Artificial pp. 4–5; Atlas pp. 11–13. Sources: [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/), [docker run](https://docs.docker.com/reference/cli/docker/container/run/).
