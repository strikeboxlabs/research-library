---
name: docker
description: Run a pinned Linux tool environment or distinguish saved image layers from a container filesystem export. Use when old Python or Java dependencies, bind-mount ownership, configured environment values, remote daemons or published ports complicate reproduction.
---

# Reproduce the tool environment

Separate the tool's runtime from the system being investigated. A legacy Python/Java image may reproduce artifact generation without reproducing the target application's runtime, dependencies or mitigations. Record the image ID/digest, architecture, tool version and invocation; a mutable tag alone is weak reproduction evidence.

Check the active Docker context and `docker version` before using local paths. Bind mounts refer to the **daemon host**, not necessarily the CLI machine. Inspect a supplied Dockerfile and its build context first: `RUN`, package builds and downloaded setup scripts execute code during building. A container is not a guarantee that an unknown workload is harmless.

Access to a rootful Docker daemon can confer root-level control over the **daemon host**, including through host bind mounts. This authority comes from the daemon and access to its socket/API, not from the Docker client being a SUID executable. A `docker` group entry is a lead: establish the effective groups, selected context and actual daemon access. Rootless Docker runs its daemon and containers in a user namespace without host root privileges; container UID 0 therefore does not establish host UID 0. Check the applicable [daemon access model](https://docs.docker.com/engine/install/linux-postinstall/) and [rootless mode](https://docs.docker.com/engine/security/rootless/) before attributing privilege. A filesystem root changed with chroot alone does not explain the daemon's authority.

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

## Establish the source of a container mount

With `jq` available and access to the intended daemon already established, define `container` as the observed container ID or name in that context:

~~~bash
(set -o pipefail; docker container inspect "$container" | jq -e '.[0].Mounts')
~~~

The filter displays only mount metadata; `pipefail` preserves an inspection failure. Inspect `Type`, `Source`, `Destination` and `RW`. For a bind mount, `Source` is a path on the daemon host; for a named volume, preserve the volume identity instead of assuming an equivalent user-selected host directory. A container destination `/root` does not establish a host source `/root`. A mount listing showing the same block device for several destinations is insufficient to recover their individual sources. Read-write metadata alone does not establish effective file permissions.

An empty result, missing container or wrong daemon context leaves the mapping unresolved. Do not install a client, expose a daemon socket or recreate a container merely to obtain this evidence. See [container inspection](https://docs.docker.com/reference/cli/docker/container/inspect/) and the bind-mount reference below.

## Interpret configured environment values

For the selected container, define `env_report` as a fresh private output path. Inspect only its configured environment instead of dumping all metadata into a transcript:

~~~bash
umask 077
(set -o pipefail; docker container inspect "$container" | jq -e '.[0].Config.Env') >"$env_report"
~~~

Expect an array of `NAME=value` strings. Check both the command status and JSON: an empty array means no entries in this field, while null, missing output or a failed inspection needs separate diagnosis. This is container configuration, not a complete snapshot of every process's current environment or application settings. Files, entrypoint logic and external secret providers can supply other values.

Interpret the variable's application-specific meaning before assigning an account. For example, `GITEA__database__PASSWD` configures Gitea's **database** password; it does not establish a Gitea administrator or Linux login password. Any observed password reuse is a separate finding. Preserve the field name and service context, and redact the value in reports. See [Gitea's configuration mapping](https://docs.gitea.com/administration/config-cheat-sheet/#use-environment-variables-to-setup-gitea).

Default Docker CLI inspection returns an array. A custom wrapper's format may emit one object or extra text; verify that shape before reusing `.[0]`. A sudo grant to such a wrapper also does not establish direct permission to run the Docker CLI.

## Choose the right archive operation

`docker image save --output "$archive" "$image"` preserves image layers and tags for an already selected image; define a fresh archive path first. `docker image load --input "$archive"` imports images and restores tags in the selected daemon. Loading is a daemon mutation, but it does not itself start the image's workload. Inspecting a downloaded archive does not require either loading it or starting a container.

`docker container export` captures a container filesystem, not the original image-layer history, and excludes mounted-volume contents. A file removed by a later image layer may survive in an earlier layer even though it is absent from a running container. Use the image archive when investigating that history; a flattened export cannot recreate missing layers. Keep archive provenance and the distinction between historical files and current runtime state.

Consult Docker's [save](https://docs.docker.com/reference/cli/docker/image/save/), [load](https://docs.docker.com/reference/cli/docker/image/load/) and [export](https://docs.docker.com/reference/cli/docker/container/export/) references for archive semantics, and [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/) for daemon-side path resolution.
