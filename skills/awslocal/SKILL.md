---
name: awslocal
description: Inspect bounded CloudWatch log pages and selected Secrets Manager/KMS metadata on an owned LocalStack endpoint, or verify an acquired nonsecret artifact signature. Use when emulator routing, resource state or pagination changes the conclusion.
---

# Inspect the selected LocalStack service

Read this entire SKILL.md before acting. Establish the owned emulator endpoint, region, local credential namespace and installed wrapper/AWS CLI combination. Use the log task below; for secret/key metadata or artifact verification, read [service metadata and signatures](references/service-metadata.md) completely first. Finish with actual service status, selected resource and bounded coverage or the specific missing prerequisite.

`awslocal` wraps AWS CLI rather than implementing all its service operations. Its maintainer now marks it deprecated in favor of `lstk aws`; retain this procedure for an already installed compatible wrapper. Check `awslocal --version`, `awslocal -h` and the installed operation help. Do not install or replace a CLI as part of inspection.

Define `endpoint` as the verified emulator URL and `region` as its configured region. Establish the intended existing local credentials before invoking the wrapper: it can reuse credentials already found by the AWS provider chain and supplies dummy defaults only when none are found. Do not assume the word local isolates production credentials. LocalStack account selection can depend on access-key configuration. Loopback refers to the CLI's current host/container, not the workstation automatically.

Use Bash with service names first in the wrapper's arguments and configure its documented endpoint variable for each call:

~~~bash
local_opts=(--region="$region" --output=json --cli-connect-timeout=5 --cli-read-timeout=30)
local_aws() {
    AWS_ENDPOINT_URL="$endpoint" AWS_PAGER="" awslocal "$@" "${local_opts[@]}"
}
~~~

Confirm that the installed wrapper/client supports `AWS_ENDPOINT_URL`; older versions have different host/port settings. The upstream implementation can inject `--no-verify-ssl` for HTTPS endpoints. Where certificate verification is required, use the trusted AWS CLI with an explicit endpoint and CA rather than assuming this wrapper verifies it. Configuration inspection and successful API responses identify the selected emulator; an ARN resembling AWS does not establish production AWS state.

## Select a group and stream, then read one event page

If the group is unknown, define `group_prefix` from the requested scope and `groups` as a fresh private JSON file:

~~~bash
umask 077
local_aws logs describe-log-groups --log-group-name-prefix "$group_prefix" --page-size 25 --max-items 25 > "$groups"
~~~

Inspect status and the JSON before selecting `group`. If known, skip discovery. Define `streams` as a fresh private output:

~~~bash
local_aws logs describe-log-streams --log-group-name "$group" --page-size 25 --max-items 25 > "$streams"
~~~

These two list operations use the CLI paginator. Retain any `NextToken`; it means the requested listing remains partial. Resume only as needed using `--starting-token` with the same scope and limits. A missing token after successful bounded retrieval differs from an authorization or unsupported-operation error. Stream metadata can lag event ingestion; a date-like stream name is not its actual event interval.

Select the exact observed `stream`, a fixed interval `start_ms`/`end_ms` in UTC epoch milliseconds, and a fresh private `events` file:

~~~bash
local_aws logs get-log-events --log-group-name "$group" --log-stream-name "$stream" --start-time "$start_ms" --end-time "$end_ms" --start-from-head --limit 25 > "$events"
~~~

This returns a bounded service page. The end time is exclusive. Read `timestamp`, `ingestionTime` and `message` separately; the message may be plain text or another serialized format. A service name in the message is a lead, not a complete authenticated CloudTrail event.

An empty or short event page does not prove the interval complete. For approved continuation, pass the returned `nextForwardToken` through `--next-token` with `--start-from-head` and the same interval. Completion in that direction occurs when the returned token equals the token supplied. GetLogEvents tokens differ from the list operations' CLI `NextToken`. Keep the fixed end time and task page budget; a growing stream without an end can otherwise outrun pagination.

Finish with endpoint/region, selected group/stream, actual interval and page coverage, observed status and relevant event findings. Retain raw messages privately and report only the requested fields. No secret-value retrieval or service mutation is required by this task.

References: [wrapper configuration](https://github.com/localstack/awscli-local), [wrapper implementation](https://raw.githubusercontent.com/localstack/awscli-local/master/bin/awslocal), [local credential namespaces](https://docs.localstack.cloud/aws/connecting/credentials/), [group inventory](https://docs.aws.amazon.com/cli/latest/reference/logs/describe-log-groups.html), [stream inventory](https://docs.aws.amazon.com/cli/latest/reference/logs/describe-log-streams.html) and [event-page semantics](https://docs.aws.amazon.com/cli/latest/reference/logs/get-log-events.html).
