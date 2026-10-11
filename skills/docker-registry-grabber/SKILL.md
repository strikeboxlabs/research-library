---
name: docker-registry-grabber
description: Retrieve one known repository's legacy image blobs with the installed DockerRegistryGrabber drg.py. Use for an owned loopback registry fixture when schema-1 manifests and raw layer retrieval are sufficient, without a Docker daemon.
---

# Retrieve the selected legacy repository

Read this entire SKILL.md before acting. Require a reviewed installed drg.py/Python dependency environment, one known repository on an owned loopback registry, and a fresh private working directory. Confirm the installed revision's tag/manifest behavior before downloading. Finish with status, selected tag/manifest evidence and verified blob coverage; downloaded files are not a reconstructed runtime filesystem. No conditional resources are required.

The upstream implementation disables TLS verification, clears HTTP_PROXY/HTTPS_PROXY, follows authentication challenges and has no explicit request timeout. This task is therefore scoped to an already prepared loopback fixture with no sensitive credentials. For a remote registry or required peer verification, use an approved registry client that satisfies that transport contract. Do not use a failed challenge as a reason to follow an unrelated authentication realm.

Define `python_bin` and `script` as the verified absolute interpreter and drg.py paths, `port` as the fixture's existing listening port, `repository` as one known safe repository name, and `work_dir` as a new absolute directory. Require a name without traversal, absolute path or shell expansion. The script forms its output path from that name.

~~~bash
"$python_bin" "$script" --help
umask 077
mkdir -m 700 "$work_dir" && (
    cd "$work_dir" &&
    "$python_bin" "$script" -p "$port" --dump "$repository" http://127.0.0.1 > download.log 2>&1
)
status=$?
~~~

Use the owned job's total runtime budget. The reviewed version chooses `tags[0]`, not a requested tag/digest, then parses legacy `blobSum` manifest entries. Preserve the actual tags/manifest separately through the fixture's trusted administrative interface; changing tag order can change the downloaded image. An empty tag list, modern schema-2/OCI manifest or `No blobSum found` is a compatibility gap, not an empty image. This is not a general OCI pull tool.

It writes `<digest>.tar.gz` files below the repository directory and can overwrite same-name files, hence the fresh directory. Compare each file's SHA-256 and expected coverage with the captured manifest; a download message precedes completed writing and is not integrity evidence. Inspect/list individual archives before extracting selected members into separate fresh directories. Blobs preserve historical layers; unordered extraction into one directory ignores layer order and whiteouts. No daemon import or workload launch occurs here.

The upstream -U/-P and -A options place authentication material in process arguments; they are not a private credential store. Repository listing can omit pagination. Broad --dump_all is a different scope and is unnecessary for this selected retrieval.

Resolve revision differences against the [upstream CLI documentation](https://github.com/Syzik/DockerRegistryGrabber/blob/master/README.md) and [download/tag/authentication implementation](https://github.com/Syzik/DockerRegistryGrabber/blob/master/drg.py).
