# Recover a supplied offline bundle

Define `bundle` as the existing absolute artifact path and `destination` as a fresh repository directory. Record its fingerprint; inspect advertised refs first:

~~~bash
git bundle list-heads "$bundle"
git -c core.hooksPath=/dev/null clone --bare --template= "$bundle" "$destination"
git -C "$destination" bundle verify "$bundle"
~~~

Check each status before continuing. The bare clone imports objects without materializing a working tree or recursively fetching submodules. `--template=` avoids populating hooks from an initialization template. Verify requires a repository context and checks prerequisites against that repository; do not treat invocation outside a repository as proof of corruption.

Incremental bundles can require earlier commits. If the clone reports missing prerequisites, retain that diagnostic and obtain the corresponding base repository/bundle. A directory name, bundle suffix or advertised branch is not proof of a complete backup. Git can read/fetch from bundles; pushing into a bundle is unsupported.

Inspect selected refs/blobs with the entrypoint's history and stored-mode guidance, using this bare repository as `repo`. Defer checkout or builds until their task requires them. Finish with imported refs, prerequisite/integrity status and omitted history, not merely a clone success message.

See [Git bundle documentation](https://git-scm.com/docs/git-bundle).
