# InfluxDB v1 HMAC candidates and query acceptance

Use when the authorized task has established an InfluxDB v1 endpoint and a relevant HMAC configuration/implementation. Required inputs are the reviewed `jwt_script` absolute path, the exact selected secret bytes, a selected InfluxDB username with its evidence or explicit hypothesis, and private output paths. An application record or chat nickname does not establish that username. Keep unrelated token scan/delivery modes out of this local signing task.

## Establish the blank-secret case before interpreting it

The upstream 1.7.5 handler passed the configured shared secret to HMAC verification even when blank. Its 1.7.6 successor rejects Bearer authentication with a blank secret. A version header is a lead, not proof of the installed backport/configuration. If query authentication is disabled, a token-bearing success cannot establish a JWT bypass. Compare the same permitted query without authorization and with the single selected candidate.

The v1 handler requires `username` as a nonempty string and `exp` as a numeric positive expiration, with normal token validation rejecting an expired token. It looks the user up in its metastore; valid signing alone does not create that user or give it administrative privileges. A selected username can be tested as a stated hypothesis; acceptance must establish the metastore/user context rather than assuming it from chat. Use a short future expiration tied to the test clock, not a copied historical timestamp or a year-long default.

## Sign with exact key-file contents

Define `influx_user` as the selected metastore username. This builds a local **unsigned seed**, not an authenticated token, for the signing tool:

~~~bash
seed=$(python3 - "$influx_user" <<'PY'
import base64, json, sys, time
def part(value):
    raw=json.dumps(value,separators=(',',':')).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode()
print(part({'alg':'HS256','typ':'JWT'})+'.'+
      part({'username':sys.argv[1],'exp':int(time.time())+300})+'.AA')
PY
)
~~~

For the explicitly established blank-secret test, define `key_file` as a fresh private path and create a **zero-byte** file; a newline is a different HMAC key. For a nonempty candidate, use its exact private text file instead:

~~~bash
umask 077
(set -C; : > "$key_file") &&
python3 "$jwt_script" "$seed" -S hs256 -kf "$key_file"
~~~

Run signing only after the file-creation step succeeds, and do not overwrite an existing key file. The reviewed `-S ... -kf` signing path reads the complete text file, including an empty file; no interactive `-T` edit is required for the seed above. This is different from cracking/checking an original signature with `-C`. Check installed behavior and inspect the resulting compact token's header/claim types; a printed candidate is not application acceptance. Initial tool setup/logging behavior still applies as described in SKILL.md.

## Test one candidate under the selected application context

Place the resulting token in a private `auth_headers` file as one `Authorization: Bearer ...` line. Define `base` as the endpoint reachable from this host and `headers`/`body` as fresh private response paths:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --get --header "@$auth_headers" --data-urlencode 'q=SHOW DATABASES' --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$base/query"
~~~

Keep curl completion, HTTP/error body, unauthenticated control and returned database inventory together. Authentication failure, unknown user, expired/wrongly typed claims and database authorization failure call for different corrections; revise only the relevant username/key/clock hypothesis in response to the observed diagnostic, keeping each request and result distinct. A successful query establishes only this request's access. For a selected measurement, use `db` plus separately URL-encoded InfluxQL, inspect each series' column/value mapping and account for errors/partial results. Application records or stored credentials are separate from an OS login and its observed identity.

References: [v1 authentication](https://docs.influxdata.com/influxdb/v1/administration/authentication_and_authorization/), [1.7.5 handler](https://github.com/influxdata/influxdb/blob/v1.7.5/services/httpd/handler.go), [1.7.6 handler](https://github.com/influxdata/influxdb/blob/v1.7.6/services/httpd/handler.go), [jwt_tool signing/runActions](https://github.com/ticarpi/jwt_tool/blob/master/jwt_tool.py), [v1 query API](https://docs.influxdata.com/influxdb/v1/api/query/).
