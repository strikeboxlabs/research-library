# A wrapper's checks are not the container's full authority

Trace the exact permitted program, accepted YAML, working directory, environment, selected daemon and executed Compose command. A validator that rejects only `privileged: true` can still accept `cap_add: [ALL]`. A read-only bind controls writes to that mount; it does not remove capabilities, constrain all accessible filesystems or make an arbitrary container command harmless. Check the complete resolved service model, including namespaces, devices, socket mounts, security options, build contexts and entrypoint.

For an authorized reproduction on an owned fixture, use a reviewed pinned image and a fresh project. Preserve the actual grant being evaluated rather than substituting `privileged`; those are different configurations. This **illustrative configuration** reports current identity and capability masks, without requesting host files:

~~~yaml
services:
  inspect:
    image: ${REVIEWED_IMAGE:?set an approved pinned image}
    cap_add: [ALL]
    entrypoint: ["/bin/sh", "-c"]
    command: ["id; grep '^Cap' /proc/self/status"]
~~~

Run it with the explicit project procedure in SKILL.md after confirming that this grant is within the test scope. Compare the observed effective capabilities with the control configuration. Container UID 0, a declared grant and a capability mask are separate observations; they do not by themselves prove host-file access. Decode masks using the controlled image's known capability definitions/tooling. `CAP_DAC_READ_SEARCH` is relevant to `open_by_handle_at`, but filesystem handle support, a mount anchor, user namespaces and syscall/security policy also govern that operation.

A wrapper checking `abspath(path).startswith('/allowed')` confuses `/allowed-other` with a descendant and may leave symlink components unresolved. A check on only the final path's `islink` misses symlinked parents. Short-form volume strings and structured long-form mounts need consistent handling; rejecting one representation is not policy coverage. During review, compare canonical resolved path components against the intended root, handle symlink/race conditions and inspect the value the daemon finally receives. Record a demonstrated bypass separately from a code-review lead.

Copying the source YAML into a temporary directory does not freeze images, external files or environment values. `yaml.safe_load` prevents arbitrary YAML object construction; it does not sandbox the Compose program described by the data. If a wrapper ignores subprocess status and hides stdout/stderr, its own exit status is weak evidence. Capture permitted diagnostic output and actual service state. A cleanup call to `down --volumes` can also destroy evidence/data before inspection; identify that behavior before starting a reproduction. See [Compose service settings](https://docs.docker.com/reference/compose-file/services/) and [file-handle capability requirements](https://manpages.debian.org/bookworm/manpages-dev/open_by_handle_at.2.en.html).
