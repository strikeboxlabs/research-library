---
name: jwt-tool
description: Inspect and modify controlled JWT fixtures with ticarpi jwt_tool. Use when claim types, signing algorithms, key-file bytes, public-key algorithm confusion or confusing decoded claims with verified identity causes mistakes.
---

# Inspect the token before selecting a mode

Read this entire SKILL.md before acting; reuse complete current context. Keep the original token unchanged when testing a candidate key. For a JWKS/public-key algorithm-confusion candidate, read [algorithm/key testing](references/algorithm-confusion.md) fully first. For a scoped InfluxDB v1 HMAC/blank-secret assessment, read [InfluxDB HMAC tokens](references/influxdb-hmac.md) fully first. For local signing/claim changes, read [fixture signing](references/fixture-signing.md); for a valid token that still cannot perform an action, read [application sessions](references/application-sessions.md). Finish with decode, signature and application-acceptance conclusions kept separate; selected references are required only for that task.

Use ticarpi's `jwt_tool.py`, not an unrelated package with a similar name. Check its help and version banner. Define `jwt_script` as the reviewed script's absolute path and `token` as the original compact JWT without its Bearer prefix:

~~~bash
python3 "$jwt_script" "$token"
~~~

This decodes locally when no target/request options are supplied. The first invocation may initialize configuration/keys and exit with status 1; inspect that setup message and rerun rather than diagnosing a token failure. The three segments are base64url-encoded header, payload and signature bytes; decoding does not verify the signature or establish that the service accepts the claims. Preserve the original string. Tokens appear in process arguments and this tool can retain them in local logs under `~/.jwt_tool`; use private fixture material and inspect its configuration before working with sensitive captures.

Read `alg`, claim types and timestamps, then establish the service's actual allowed algorithm and key source independently. A field named `API_KEY` is not necessarily the signing secret; trace its use in the application settings. A changed account record also does not rewrite an already issued token. Obtain a fresh authorized login token when testing updated account state.

## Check one known HMAC candidate against the original

After independently establishing the expected HMAC algorithm, define `candidate_secret` as the known nonempty text candidate. With private local fixture data and no target/request options:

~~~bash
python3 "$jwt_script" "$token" -C -p "$candidate_secret"
~~~

This mode checks the original compact token's signature; it does not sign a replacement. Both token and candidate are exposed in process arguments, and a match prints the secret, so keep output private. In the reviewed implementation this branch exits with status 1 even after a match: inspect the explicit matching/mismatch diagnostic, rather than using status alone as the verdict. `-C -kf` has different key-file handling and is not interchangeable with signing's `-S ... -kf`.

A signing editor can silently recompute a token when its key is changed. Verifying that newly signed string with the same key is circular evidence. Preserve the original encoded header/payload/signature bytes and check those. A match supports this token/key pairing, not key freshness, current service configuration, issuer/audience/time validity or authorisation. A failure calls for checking bytes, algorithm and source context; do not “repair” the original by signing it.

See [jwt_tool's checkSig/testKey and runActions implementation](https://github.com/ticarpi/jwt_tool/blob/master/jwt_tool.py) when interpreting option or exit-status differences.
