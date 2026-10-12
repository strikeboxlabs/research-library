---
name: runc
description: Inspect the selected OCI runtime's version and build metadata on Linux. Use when Docker, image tags, distribution backports or a binary in another namespace obscure which runtime was identified.
---

# Identify the selected runtime

Read this entire SKILL.md before acting. Require the controlled Linux environment and a selected existing runc executable. Identify its path and execution context, preserve the full version output/status, then correlate it with the runtime actually used by the relevant service. No conditional resources are required. Finish with verified identity and any unresolved service or vendor-patch association.

Define `runc_bin` as the verified absolute executable path in the intended host or container context:

~~~bash
"$runc_bin" --version
status=$?
"$runc_bin" --help
~~~

Check the version command's status before interpreting its output. Preserve the full release/distribution suffix, commit/build identity and any reported OCI-spec, Go or libseccomp versions; fields vary by release/build. The Go line is the runtime's compiler metadata, not proof that a Go compiler is installed. OCI-spec and libseccomp versions are separate from the runc release.

A binary found inside one container need not be the runtime used by the host's Docker/containerd service. Confirm that service's configured runtime and actual executable through its approved inventory/configuration evidence before attaching this output to it. Docker Engine's version and a base-image tag do not identify runc. A missing binary or permission failure is an inventory gap, not a runtime security result.

For a patch assessment, match the complete package revision and distribution release to the vendor advisory or tracked build provenance. A comparison using only the upstream numeric prefix can misclassify a backported fix. Version evidence alone does not establish the active configuration, a reachable exploitation condition or a successful containment test. Record the matched vendor status and remaining uncertainty; upgrading or changing a service is a separate authorized action.

References: [upstream runc manual](https://github.com/opencontainers/runc/blob/main/man/runc.8.md), [runtime project](https://github.com/opencontainers/runc).
