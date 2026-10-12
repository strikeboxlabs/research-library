# Publish the selected private release

Require an approved package name/version, exact reviewed build artifacts, a provisioned repository account and the existing private upload endpoint. Use the trusted interpreter with Twine already available. Upload changes repository state; a build task alone does not authorize publication.

Define `python` as the prepared interpreter, `artifact` as one exact release artifact, `config` as the private .pypirc file and `repository` as its selected section label. Read the configuration privately: the index-servers list and selected section must refer to the intended label. Its repository URL must match the approved upload endpoint, including hostname, port and path. The upload endpoint can differ from the consumer's /simple/ index URL. .pypirc configures upload tooling; it is not pip's index configuration.

Account for TWINE_REPOSITORY_URL and other existing overrides before invoking Twine: an explicit repository URL takes precedence over the label. Do not accept public default fallback or a guessed endpoint. Check TLS using the approved trust configuration; preserve certificate verification. Keep credentials out of command arguments and logs, using the provisioned keyring or interactive credential prompt. If the configuration contains credentials, restrict access to its owner.

~~~bash
"$python" -m twine --version
"$python" -m twine check --strict "$artifact"
~~~

Stop if checking fails. This checks distribution metadata/description rendering, not package safety, installability or repository availability. Recheck the artifact identity and selected destination before the authorized upload:

~~~bash
"$python" -m twine upload --config-file "$config" --repository "$repository" "$artifact"
~~~

Retain the actual upload status and repository receipt without credentials. If several artifacts are approved, list those exact paths; do not publish an old dist/* directory accidentally. A duplicate/version rejection is unresolved publication, not a reason to replace or delete an existing release. A timeout after sending may leave an accepted release: inspect the approved repository before retrying. Avoid skip-existing as a general substitute for checking the existing artifact identity.

Verify the intended name/version and artifact at the repository through its normal authenticated read interface. An HTTP success or upload message establishes that request's outcome; it does not prove a downstream service fetched, installed or executed this release. Keep consumer identity, interpreter, dependency and application evidence separate.

See [.pypirc labels and defaults](https://packaging.python.org/en/latest/specifications/pypirc/) and [Twine upload/check options](https://twine.readthedocs.io/en/stable/).
