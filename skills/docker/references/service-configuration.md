# Apply owned service configuration

Require the selected daemon/container and reviewed configuration change. Define `container`, absolute local `config` and exact container `destination`. Inspect its existing path/backup and the image's configuration contract first:

~~~bash
docker inspect --format '{{.State.Status}}' "$container"
docker cp "$config" "$container:$destination"
status=$?
~~~

Copying works with stopped or running containers. An existing destination file is overwritten; a directory receives the source basename. Missing parents are not created. Confirm destination permissions and the service's own configuration validation before activation. Copy success does not make a running process reload configuration.

For the selected stopped service:

~~~bash
docker start -a "$container"
status=$?
~~~

`-a` attaches output and forwards signals; a foreground service can keep this command running. Start operates on stopped containers. An authorized restart of a running service uses `docker restart "$container"`; use its documented reload instead when appropriate. Retain startup diagnostics and the requested readiness observation; a running container alone is insufficient.

Check required published protocols separately: UDP53 publication does not also publish TCP53. CLI host paths and container paths have different contexts; bind sources belong to the daemon host.

Sources: [copy](https://docs.docker.com/reference/cli/docker/container/cp/), [start](https://docs.docker.com/reference/cli/docker/container/start/), [restart](https://docs.docker.com/reference/cli/docker/container/restart/).
