# Select metadata and verify an acquired signature

Use the entrypoint's verified endpoint/region/local credential context and `local_aws` function. Select the requested service and retain status before interpreting output. Define each output as a fresh private JSON file; metadata itself can contain sensitive names/descriptions. These tasks do not retrieve secret values, alter key states or decrypt credential archives.

## Secrets Manager metadata

For permitted local secret inventory, define `secrets` as the output:

~~~bash
umask 077
local_aws secretsmanager list-secrets --page-size 25 --max-items 25 > "$secrets"
~~~

Read exact names/ARNs and metadata separately from values. By default, secrets scheduled for deletion are omitted; this is not an inventory of every historical secret/version. Listing is eventually consistent on AWS, and emulator consistency must be observed separately. Preserve `NextToken` and resume with `--starting-token` only when the requested coverage requires it. An inventory response does not prove permission to retrieve a value or validate an application credential. A bare RotateSecret/RestoreSecret message in a log is not proof that rotation completed.

See [ListSecrets semantics](https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/list-secrets.html).

## KMS state and purpose

If the key is unknown and inventory is needed, define `keys` as the output:

~~~bash
local_aws kms list-keys --page-size 25 --max-items 25 > "$keys"
~~~

This lists identities in the selected namespace/region, not material or state. Preserve CLI `NextToken`/`--starting-token` continuation with the same limits. Choose the exact observed `key_id` or ARN and define `metadata` as a fresh output:

~~~bash
local_aws kms describe-key --key-id "$key_id" > "$metadata"
~~~

Use an existing key ID/ARN for this task. A predefined AWS-managed alias without an existing key ID can cause key creation under AWS semantics. Read `KeyState`, `Enabled`, `KeyUsage`, `KeySpec` (older output may use `CustomerMasterKeySpec`) and supported algorithms together. `SIGN_VERIFY` and `ENCRYPT_DECRYPT` support different operations; enabled alone does not establish the caller's permission. DescribeKey does not return all policy/grant, alias, tag or rotation information. Use a JSON parser rather than cutting colon-delimited text, which can damage ARNs or conceal API errors.

See [ListKeys](https://docs.aws.amazon.com/cli/latest/reference/kms/list-keys.html) and [DescribeKey](https://docs.aws.amazon.com/cli/latest/reference/kms/describe-key.html).

## Verify one nonsecret acquired artifact

Establish the trusted signing key identity, exact nonsecret `message_file` bytes and binary `signature_file`, all already acquired. Define `algorithm` from the signing contract and selected key's supported algorithms, not a guess from the signature filename. This command supports a raw message of 1–4096 bytes. Define `verification` as a fresh private output:

~~~bash
local_aws kms verify --key-id "$key_id" --message-type RAW --message "fileb://$message_file" --signature "fileb://$signature_file" --signing-algorithm "$algorithm" > "$verification"
~~~

`fileb://` sends exact bytes independently of CLI binary-format defaults. Do not normalize line endings, reserialize YAML or submit base64 text as if it were the original file. Larger messages need the established digest contract and corresponding `DIGEST` mode; an already hashed input sent as RAW can be hashed again. Stop with that prerequisite gap rather than silently changing the producer's contract.

Check command status and the returned key identity, algorithm and `SignatureValid`. A signature failure is different from denied permission, unsupported algorithms or an incompatible key state. Verification ties those bytes to that key/algorithm; it does not independently identify a human signer, authorize deploying the content or prove production AWS behavior when performed by an emulator. Report the result against that explicit trust context and preserve unresolved byte/key mismatches.

See [Verify CLI binary/message options](https://docs.aws.amazon.com/cli/latest/reference/kms/verify.html) and [Verify API outcomes](https://docs.aws.amazon.com/kms/latest/APIReference/API_Verify.html).
