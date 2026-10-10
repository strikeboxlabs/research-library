# Establish the source of a container mount

With `jq` available and access to the intended daemon already established, define `container` as the observed container ID or name in that context:

~~~bash
(set -o pipefail; docker container inspect "$container" | jq -e '.[0].Mounts')
~~~

The filter displays only mount metadata; `pipefail` preserves an inspection failure. Inspect `Type`, `Source`, `Destination` and `RW`. For a bind mount, `Source` is a path on the daemon host; for a named volume, preserve the volume identity instead of assuming an equivalent user-selected host directory. A container destination `/root` does not establish a host source `/root`. A mount listing showing the same block device for several destinations is insufficient to recover their individual sources. Read-write metadata alone does not establish effective file permissions.

An empty result, missing container or wrong daemon context leaves the mapping unresolved. Do not install a client, expose a daemon socket or recreate a container merely to obtain this evidence. See [container inspection](https://docs.docker.com/reference/cli/docker/container/inspect/) and [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/).

## Interpret configured environment values

For the selected container, define `env_report` as a fresh private output path. Inspect only its configured environment instead of dumping all metadata into a transcript:

~~~bash
umask 077
(set -o pipefail; docker container inspect "$container" | jq -e '.[0].Config.Env') >"$env_report"
~~~

Expect an array of `NAME=value` strings. Check both the command status and JSON: an empty array means no entries in this field, while null, missing output or a failed inspection needs separate diagnosis. This is container configuration, not a complete snapshot of every process's current environment or application settings. Files, entrypoint logic and external secret providers can supply other values.

Interpret the variable's application-specific meaning before assigning an account. For example, `GITEA__database__PASSWD` configures Gitea's **database** password; it does not establish a Gitea administrator or Linux login password. Any observed password reuse is a separate finding. Preserve the field name and service context, and redact the value in reports. See [Gitea's configuration mapping](https://docs.gitea.com/administration/config-cheat-sheet/#use-environment-variables-to-setup-gitea).

Default Docker CLI inspection returns an array. A custom wrapper's format may emit one object or extra text; verify that shape before reusing `.[0]`. A sudo grant to such a wrapper also does not establish direct permission to run the Docker CLI.
