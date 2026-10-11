# Inspect Lambda metadata without invocation

Use the entrypoint's explicit `endpoint`, `region`, existing `profile` and `aws_opts` array for the intended service. Confirm `aws lambda list-functions help` and `get-function help` for the installed CLI. Define `listing` and `function_metadata` as fresh private JSON outputs.

~~~bash
umask 077
aws "${aws_opts[@]}" lambda list-functions --max-items 25 > "$listing"
~~~

Check status and stderr before interpreting `Functions`. This is an intentionally bounded CLI paginator result. Retain a returned CLI `NextToken`; continue with `--starting-token` only when the task needs another page. A service `NextMarker` and CLI `NextToken` are different interfaces. Automatic pagination without the bound can read the full regional collection. Empty output and access denial differ; a listing is not proof of invocation rights or all versions.

Select `function_name` from observed metadata and request its configuration/code descriptor:

~~~bash
aws "${aws_opts[@]}" lambda get-function \
  --function-name "$function_name" > "$function_metadata"
~~~

Use `--qualifier` with an observed published version or alias when that is the requested deployment. An unqualified mutable version can change between calls. Preserve function ARN, version, package type, revision and relevant configuration rather than assuming a name identifies identical code everywhere. Lambda listing provides only a subset of configuration fields.

For a ZIP deployment, `Code.Location` can be a temporary code-download URL. Treat the saved response/URL as sensitive and do not paste it into routine reports. Metadata retrieval does not download or execute code. Image deployments have a different code descriptor, and layers are separate artifacts. A later authorized download needs its own complete-transfer and archive validation; do not derive a universal download route from an emulator.

Compatibility services can implement only some operations, signing rules or response fields. A version-specific failure needs the actual error and service/version facts; do not install or downgrade from a historical writeup's unsubstantiated pin.

See [list-functions and pagination](https://docs.aws.amazon.com/cli/latest/reference/lambda/list-functions.html), [get-function descriptors](https://docs.aws.amazon.com/cli/latest/reference/lambda/get-function.html) and [endpoint precedence](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-endpoints.html).
