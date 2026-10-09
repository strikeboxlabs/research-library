# Capture help as authoring evidence

[capture_help.py](../scripts/capture_help.py) uses Python 3.10+ and the standard library. Run it in the target Linux environment, or inside a prepared distro container containing Python and the tool. It does not install packages, pull images or alter agent configuration.

Start with your intended environment. Add a second implementation when a task depends on it, then extend to Debian, Ubuntu, Fedora, a RHEL rebuild, Alpine or Arch as observed differences justify the work. Multiple distro containers on one host still share that host's kernel; they do not establish kernel tracing or live-debugging compatibility. See [Docker's container explanation](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).

## Local capture

From the repository root, with the tool already installed:

~~~bash
python3 scripts/capture_help.py gdb --output work/sources/gdb/local-01
~~~

The output directory must be new. The helper records:

- exact argument arrays, resolved executable, working directory, date and caller-supplied environment ID;
- `/etc/os-release` on Linux, kernel release and architecture;
- full version/help stdout and stderr in separate files, exit codes, timeout state and byte counts;
- the explicit display-only environment overrides, without dumping the process environment.

`capture.json` says whether both commands completed with exit code zero. The helper exits nonzero for an incomplete capture, missing executable or invalid invocation. Inspect each command record; a nonzero help status can have tool-specific meaning. It never marks a procedure or agent evaluation passed.

Defaults are `--version` and `--help`, with 30 seconds per command and closed stdin. Confirm that those are informational invocations for the selected tool. Override unsupported forms explicitly; there is no guessed fallback:

~~~bash
python3 scripts/capture_help.py example-tool --output work/sources/example-tool/local-01 \
  --version-arg=-V --help-arg=-h --timeout 15
~~~

`example-tool` is a placeholder for an installed tool whose documented flags match. Repeated `--version-arg=VALUE` or `--help-arg=VALUE` replaces the corresponding default with an argument list. Commands are executed directly without shell expansion. The helper is intended for short informational invocations, not service startup or arbitrary investigation procedures. A timeout retains partial files and marks the capture incomplete; on POSIX it stops the command's process group, and on Windows it stops the direct child.

## Repeat inside prepared distro images

These commands are a Linux-side authoring example. Supply locally prepared images named `cli-authoring-gdb-debian` and `cli-authoring-gdb-alpine`, each containing GDB and Python 3.10+. Image preparation is a separate explicit authoring step. Record its package versions/build recipe if those facts matter to a claim.

~~~bash
(
  set -eu
  repo=$(pwd -P)
  capture_id=$(date -u '+%Y%m%dT%H%M%SZ')
  mkdir -p "$repo/work/sources/gdb"
  for image in cli-authoring-gdb-debian cli-authoring-gdb-alpine; do
    image_id=$(docker image inspect --format '{{.Id}}' "$image")
    docker run --rm --network none --read-only \
      --user "$(id -u):$(id -g)" \
      --mount "type=bind,src=$repo/scripts,dst=/capture,readonly" \
      --mount "type=bind,src=$repo/work/sources/gdb,dst=/captures" \
      --entrypoint python3 "$image_id" \
      /capture/capture_help.py gdb \
      --output "/captures/$image-$capture_id" --environment-id "$image_id"
  done
)
~~~

The example uses the resolved local image ID so a moving tag is not the recorded environment identity. It mounts only the helper directory and capture destination. Container commands and mounts follow [Docker's run documentation](https://docs.docker.com/engine/containers/run/). The image ID is supplied by the caller; the Python helper does not independently attest it.

Read the captures and compare relevant options, defaults and failure messages. Use version-matched manual sections for missing detail. Help differences belong in the skill only when they change the supported task; do not paste an entire distro diff into runtime guidance.

## Accept evidence without overstating it

Keep raw captures in ignored `work/sources/`. Retain useful findings, exact versions and source locators in concise tracked notes, such as an optional skill-local `references/sources.md`. Preserve required attribution; accepted guidance should remain reviewable without a contributor's private scratch files.

Help capture establishes available documentation and observed output, not that a recipe works or its diagnosis is correct. Run a separate fixture for procedure execution and use the [evaluation design](../evaluation/README.md) for agent behaviour.

## Helper checks

Run from the repository root:

~~~bash
python3 -B -m unittest discover -s tests -v
~~~

The tests use real Python child processes to check successful capture, separate stdout/stderr, nonzero exits, timeouts, missing tools, invalid timeout values and refusal to overwrite evidence. They do not test GDB, container launch or harness discovery.
