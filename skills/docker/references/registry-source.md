# Inspect the selected image behind a registry

Distinguish the registry endpoint reachable from the current network context from the image reference consumed by the selected Docker daemon. A reverse TCP forward can expose a remote registry on an operator's loopback; the daemon must also be able to reach that endpoint. Do not assume the client machine's loopback is a remote daemon's loopback. Keep the tunnel listener explicit and preserve TLS/registry authentication rather than altering global daemon settings to fit an HTTP example.

When these read endpoints are authorized, use a verified `registry_url`, selected `repository` and private response paths:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 20 --dump-header "$headers" --output "$body" "$registry_url/v2/_catalog?n=20"
curl --silent --show-error --connect-timeout 5 --max-time 20 --dump-header "$tag_headers" --output "$tag_body" "$registry_url/v2/$repository/tags/list?n=20"
~~~

Inspect status/body and follow scoped pagination links when required. Authentication can restrict listing, and returned names/tags are not an exhaustive inventory or proof that pull is permitted. A `latest` tag is mutable. Record the selected digest, architecture and image ID when acquiring the approved image.

Define `image_ref` as the selected approved repository/tag or digest reference and `image_metadata` as a fresh private output.

~~~bash
docker pull "$image_ref"
docker image inspect "$image_ref" > "$image_metadata"
~~~

Check each status and read metadata before choosing execution. For selected source inspection without starting the image, define a unique `inspection_name`, an existing private `destination` directory and known absolute `container_path`:

~~~bash
container_id=$(docker create --name "$inspection_name" --entrypoint /bin/true "$image_ref") || exit
docker cp "$container_id:$container_path" "$destination/"
docker rm "$container_id"
~~~

`create` creates container state without running its entrypoint; it can still create volume state. Match the image's declared volumes and record which filesystem was copied. `cp` extracts files through the daemon: keep acquisition isolated and inspect artifacts rather than executing recovered PHP/bootstrap code. Compare `composer.lock`, actual vendored package metadata and application call paths. A composer constraint such as `^9.1.8` is not the deployed patch version. Route code, hardcoded API credentials and environment-driven credentials are distinct evidence.

When the task specifically requires an approved interactive inspection inside a trusted image, use `docker run --rm -it --network none --entrypoint /bin/sh "$image_ref"` after confirming that shell exists and that execution/network restrictions fit the task. Appending `bash` to an image does not override its configured entrypoint. Inspect the real runtime/configuration separately from extracted source: source alone does not prove which deployment version or secret is active. See [registry listings](https://distribution.github.io/distribution/spec/api/#listing-repositories), [container create](https://docs.docker.com/reference/cli/docker/container/create/) and [file copying](https://docs.docker.com/reference/cli/docker/container/cp/).
