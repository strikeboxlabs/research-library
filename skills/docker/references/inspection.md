# Establish the source of a container mount

## Check a provisioned TLS daemon endpoint

Require the intended daemon address, trusted CA certificate and an already provisioned client certificate with its matching private key. A CA private key is not a client prerequisite. Define `daemon` as its verified `tcp://hostname:port`, and `ca_file`, `client_cert`, `client_key` as the private task's actual credential paths:

~~~bash
docker --host "$daemon" --tlsverify --tlscacert "$ca_file" \
  --tlscert "$client_cert" --tlskey "$client_key" version
~~~

Retain status and the separate Client/Server results. Resolve hostname, trust-chain, validity and client-purpose errors against the provisioned endpoint; do not disable verification as a repair. Loopback refers to the CLI's execution environment. If using an existing environment-based configuration instead, inspect `DOCKER_HOST`, `DOCKER_CONTEXT`, `DOCKER_TLS_VERIFY` and `DOCKER_CERT_PATH` together before attributing the connection; a conflicting context can redirect selection.

Successful TLS authentication and a successful metadata request establish different stages. An authorization plugin may allow one API operation and reject another. A certificate's common name is not an OS UID, and an observed container listing does not prove permission to create containers or mount host files. Review the deployed plugin policy and exact requested operation before assigning authority. A readable service unit is configuration evidence until correlated with the running daemon and its effective overrides.

See [Docker TLS client options](https://docs.docker.com/engine/security/protect-access/), [CLI context selection](https://docs.docker.com/reference/cli/docker/) and [authorization plugins](https://docs.docker.com/engine/extend/plugins_authorization/).

## Inspect the selected daemon's networks

Use only the actual permitted Docker invocation. A restricted grant to network ls/inspect does not permit container inspection, run or daemon reconfiguration. With the daemon context established as far as that grant permits, list networks and select an observed network name/ID as `network`:

~~~bash
docker network ls
docker network inspect "$network"
~~~

Preserve both statuses and the complete JSON inspection. Distinguish network name/ID, driver/scope, IPAM subnet/gateway and attached container endpoint addresses. An endpoint address with a prefix is not a host-published port. A container name suggesting a product/version is a label, not a measured binary version. Listing one bridge does not inventory all networks or demonstrate service reachability from the client. Empty endpoint metadata can reflect network type/state, while failed inspection remains unknown. Confirm a requested service separately without assuming metadata grants access.

These commands read metadata. Do not attach/disconnect endpoints to investigate a listing. See [network list](https://docs.docker.com/reference/cli/docker/network/ls/) and [network inspection](https://docs.docker.com/reference/cli/docker/network/inspect/).

## Inventory images on the selected daemon

With the intended context/daemon established by the entrypoint, list its local image records without starting a container:

~~~bash
docker image ls --all --digests --no-trunc
~~~

`--all` includes intermediate/untagged images that the ordinary list can omit; it does not enumerate a remote registry or every Docker context. Retain repository/tag, image ID, available digest and command status. A tag is mutable, a missing digest can reflect a locally built image, and reported image size is not a unique disk-usage total because layers can be shared. Images are not running containers. A displayed image name alone establishes neither host privileges nor suitable architecture/entrypoint for execution. A failed daemon query remains unknown, not an empty image inventory. See [image-list semantics](https://docs.docker.com/reference/cli/docker/image/ls/).

## Inspect a selected container's mounts

With `jq` available and access to the intended daemon already established, define `container` as the observed container ID or name in that context:

~~~bash
(set -o pipefail; docker container inspect "$container" | jq -e '.[0].Mounts')
~~~

The filter displays only mount metadata; `pipefail` preserves an inspection failure. Inspect `Type`, `Source`, `Destination` and `RW`. For a bind mount, `Source` is a path on the daemon host; for a named volume, preserve the volume identity instead of assuming an equivalent user-selected host directory. A container destination `/root` does not establish a host source `/root`. A mount listing showing the same block device for several destinations is insufficient to recover their individual sources. Read-write metadata alone does not establish effective file permissions.

If the selected daemon serves Linux containers through Docker Desktop, distinguish its Linux VM filesystem from the native desktop OS and any shared host directories. A Linux root prompt or a bind source `/` does not identify a Windows account or imply access to every native-host path. Use the actual inspected mappings and deployment configuration; historical internal addresses and shared-drive paths are not portable defaults. Desktop product version, Engine version and CLI version are separate observations.

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

For an acquired Compose file, distinguish raw interpolation expressions from a container's effective values. `${VAR-default}` uses the default only when VAR is unset; `${VAR:-default}` also uses it when VAR is empty. A port expression with an unset-only default therefore does not guarantee that port when the deployment environment sets an empty or different value. Inspect the actual launch environment/resolved configuration before attributing a listener, and correlate it with the selected daemon's current metadata. A downloadable Compose file or mutable image tag is not proof that it describes the running deployment. See [Compose interpolation](https://docs.docker.com/reference/compose-file/interpolation/).
