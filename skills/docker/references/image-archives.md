# Choose the right archive operation

`docker image save --output "$archive" "$image"` preserves image layers and tags for an already selected image; define a fresh archive path first. `docker image load --input "$archive"` imports images and restores tags in the selected daemon. Loading is a daemon mutation, but it does not itself start the image's workload. Inspecting a downloaded archive does not require either loading it or starting a container.

`docker container export` captures a container filesystem, not the original image-layer history, and excludes mounted-volume contents. A file removed by a later image layer may survive in an earlier layer even though it is absent from a running container. Use the image archive when investigating that history; a flattened export cannot recreate missing layers. Keep archive provenance and the distinction between historical files and current runtime state.

Consult Docker's [save](https://docs.docker.com/reference/cli/docker/image/save/), [load](https://docs.docker.com/reference/cli/docker/image/load/) and [export](https://docs.docker.com/reference/cli/docker/container/export/) references for archive semantics, and [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/) for daemon-side path resolution.


## Transfer an already selected image to an offline daemon

On the source daemon, define `image` as the approved image already present, and `archive` as a fresh absolute output path. With jq available, save its identity and platform alongside the transfer:

~~~bash
(set -o pipefail; docker image inspect "$image" | jq -er '.[0] | [.Id, .Os, .Architecture] | @tsv')
docker image save --output "$archive" "$image"
sha256sum "$archive"
~~~

After an approved transfer, verify the same archive checksum on the destination. With permission to import into the intended destination daemon, load the archive, then define `loaded_ref` as the restored tag or image ID reported by that operation:

~~~bash
docker image load --input "$archive"
(set -o pipefail; docker image inspect "$loaded_ref" | jq -er '.[0] | [.Id, .Os, .Architecture] | @tsv')
~~~

Check load status and the restored names/IDs/platform, not just the presence of a tar file. Loading may retag existing names; preserve conflicting image identities before an intentional import. Matching transfer bytes alone does not establish source trust. A loaded image may still have an incompatible architecture or unavailable runtime dependencies; loading never proves its workload started.

An empty `docker images` list describes the chosen daemon/context, not every daemon on the machine. Do not turn an image import into an unrequested pull, privileged run or host-root bind. Those are separate operations with different effects.
