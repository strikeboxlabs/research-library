---
name: aws
description: Inspect authorized S3 bucket inventory and selected objects, DynamoDB tables and Lambda metadata with the AWS CLI against explicit AWS-compatible endpoints. Use to diagnose endpoint or credential mismatches, preserve bounded pagination evidence and interpret service responses.
---

# Select the service endpoint and credential context

Read this entire SKILL.md before acting. Establish the intended endpoint, region and trusted existing credential context, then follow the selected S3 or DynamoDB task below. For Lambda inventory or selected function metadata, read [Lambda inspection](references/lambda-inspection.md) fully first. Finish with request status, selected resource/version and coverage limits; missing credentials or endpoint support are prerequisites, not successful empty results.

These commands use AWS CLI v2 and Bash arrays. Check `aws --version` and the installed operation help. Define `endpoint` as the verified service URL, `region` as its configured region, and `profile` as the existing profile intended for that environment. A hostname or `x-amz-*` header is a lead, not proof that an endpoint is Amazon AWS or accepts particular credentials.

~~~bash
aws_opts=(--endpoint-url "$endpoint" --region "$region" --profile "$profile" --no-cli-pager --no-cli-auto-prompt --output json)
~~~

Keep the explicit endpoint on every service call, including after switching from S3 to DynamoDB; they need not share an endpoint. `localhost` belongs to the CLI process's host/container. A forwarded service may also require its expected DNS name. Diagnose TLS with the intended CA and hostname rather than disabling verification.

Use a known credential source: profiles can refer to external credential processes, role assumptions or other providers. If isolating configuration, point `AWS_CONFIG_FILE` and `AWS_SHARED_CREDENTIALS_FILE` at existing private task files; changing `HOME` relocates unrelated tools too. Check inherited credential/session settings before drawing conclusions about the selected account. Do not send production credentials to an emulator. Some LocalStack configurations accept dummy keys, but their account namespace and signature behavior are configuration-dependent; this is not an AWS authentication bypass. See [LocalStack credentials](https://docs.localstack.cloud/aws/connecting/credentials/).

For a specifically permitted public S3 read, replace the profile option with `--no-sign-request` to avoid loading credentials. Rejection means that unsigned operation failed; it is not a reason to invent credentials or switch environments.

# Select an S3 bucket, then retrieve one object

When the bucket is unknown and account bucket inventory is permitted, define `bucket_listing` as a fresh private file and request bounded CLI output:

~~~bash
aws "${aws_opts[@]}" s3api list-buckets --page-size 25 --max-items 25 > "$bucket_listing"
~~~

The [ListBuckets operation](https://docs.aws.amazon.com/cli/latest/reference/s3api/list-buckets.html) requires `s3:ListAllMyBuckets` on AWS and lists buckets owned by the requester; it does not prove object read/write rights or inventory other accounts' accessible buckets. Preserve status, names and coverage. A CLI `NextToken` means output is incomplete; resume only when needed using `--starting-token` with the same limits. This is a CLI output bound, distinct from the API's `ContinuationToken`; do not mix tokens. Older emulators/clients may lack this pagination support: record the incompatibility rather than silently removing the limits.

When the bucket is known, skip account inventory. Define `bucket` from configuration or an observed response, `prefix` as the selected key prefix (empty only when the bucket root is intended), and `listing` as a fresh private file.

~~~bash
aws "${aws_opts[@]}" s3api list-objects-v2 --bucket "$bucket" --prefix "$prefix" --no-paginate --cli-input-json '{"MaxKeys":100}' > "$listing"
~~~

Check status and stderr before parsing. This requests one service page, at most 100 keys. `Contents` carries exact keys, sizes and metadata; slash prefixes are not necessarily filesystem directories. `IsTruncated` and `NextContinuationToken` establish whether more pages remain. For another bounded page, retain `MaxKeys` and put the token in the API input's `ContinuationToken` field. CLI paginator `NextToken`/`--starting-token` is a separate mechanism; do not mix the two. An empty page and AccessDenied are different outcomes.

Select a reviewed `key`, a fresh explicit local `object_file`, and a separate `metadata` file:

~~~bash
aws "${aws_opts[@]}" s3api get-object --bucket "$bucket" --key "$key" "$object_file" > "$metadata"
~~~

The object bytes go to `object_file`; stdout contains response metadata. Preserve exit status, length and any applicable version/checksum evidence. An ETag is not universally an MD5 digest. A failed transfer may leave a local file; existence alone does not establish completion. For a versioned investigation, request the observed `--version-id` when supported. This avoids turning arbitrary keys into local paths through a whole-bucket download.

For an approved bulk copy, inspect `s3 sync ... --dryrun`, direction and destination first. Sync can replace local files and is not an immutable snapshot; `--delete` removes destination entries. S3 storing a `.php` object does not mean it executes PHP: execution requires a separate consumer/runtime, such as an application copying objects into a web directory.

# Read a bounded DynamoDB page and its key schema

Switch `endpoint` and rebuild `aws_opts` if this service uses a different address. If the table is unknown, `dynamodb list-tables --no-paginate --cli-input-json '{"Limit":25}'` returns a bounded name page; preserve `LastEvaluatedTableName` and resume with the API field `ExclusiveStartTableName` if needed. For the selected `table`, inspect schema/status before choosing data:

~~~bash
aws "${aws_opts[@]}" dynamodb describe-table --table-name "$table"
aws "${aws_opts[@]}" dynamodb scan --table-name "$table" --no-paginate --cli-input-json '{"Limit":25}' --projection-expression '#field' --expression-attribute-names "file://$attribute_names" > "$page"
~~~

Define `page` as a fresh private file and `attribute_names` as a reviewed JSON file mapping `#field` to the needed field; for example, **illustrative** `{"#field":"status"}`. Prefer a key-based Query/GetItem when the required key is known. Projection limits returned attributes, not the cost of scanning the underlying items. The low-level API uses typed values, such as `{"S":"ready"}`; retain type tags when interpreting or constructing data.

`Limit` bounds evaluated items before filtering, and a response can stop earlier at the service's byte limit. `Count` and `ScannedCount` describe this page. Empty `Items` with `LastEvaluatedKey` does not establish an empty table; continue only as needed using that full typed key as `ExclusiveStartKey` in the next request JSON. `--query` filters CLI output locally. `--consistent-read` does not turn a multi-page scan into a transactionally consistent snapshot. These API limits deliberately avoid automatic full-table pagination.

`KeySchema` distinguishes the partition (`HASH`) and optional sort (`RANGE`) key; `AttributeDefinitions` is not a list of all permitted columns. A put replaces an existing item only when its entire primary key matches. If content itself is a sort key, changing that content creates a different item even with the same title. Do not assume a series of puts left only the newest row, or that an application's last scanned row is deterministic. Creating tables and writing items are separate operations from this inspection.

For version-specific behavior consult [endpoint selection](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-endpoints.html), [S3 listing](https://docs.aws.amazon.com/cli/latest/reference/s3api/list-objects-v2.html) and [DynamoDB scan](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/scan.html).
