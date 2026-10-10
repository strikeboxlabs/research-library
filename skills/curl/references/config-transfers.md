# Curl configuration and job-controlled transfers

Use this branch when a scheduled job loads `-K/--config`, a writable config changes URL/output behavior, or inherited curlrc affects a request. Establish the actual invocation, working directory, effective identity, supported protocols and all selected input/output files before running it. Read the config as text first; `-K` is not a harmless URL file or a sandbox.

## Interpret the actual configuration boundary

Config options are processed like CLI arguments: one option per physical line, with its parameter on that line. Long names without dashes permit `=`/`:` separators; arguments containing whitespace require double quotes and curl's escaping rules. A bare URL line is not a URL option. A minimal **illustrative owned transfer** looks like:

~~~text
url = "http://127.0.0.1:8080/marker.txt"
output = "/absolute/owned/marker-copy.txt"
~~~

Replace both values with the actual reachable URI and fresh authorized destination. This is curl syntax, not shell variable expansion: `$name` is not automatically substituted. A default curlrc can still load even when `-K` is used. For an isolated reviewed invocation, `-q` must be the first argument after curl to skip the default config; it does not disable the explicitly supplied file.

Define `config_file` as the complete reviewed config with only the intended transfer, and `headers` as a fresh private header capture:

~~~bash
umask 077
curl -q --config "$config_file" --connect-timeout 5 --max-time 30 \
  --dump-header "$headers" --write-out 'status=%{http_code}\n'
~~~

Retain stdout/stderr/status and inspect the configured output bytes. Without an applicable HTTP-failure option, a 404 may save an error body while curl exits zero. Existing outputs can be overwritten and failures can leave partial replacements. Acquisition, file replacement and any subsequent consumer execution are separate results.

Repeated `--output` options pair with URLs in their respective order; an `-o report` after `-K input` does not constrain all config destinations or necessarily override its first output. Other options have their own repeat rules. A config can add transfers, local-file sources, uploads or additional output options. Establish its full effective behavior rather than checking only one url/output line. Relative config/output paths use the running job's context; merely being beside the config does not make that its base directory.

## Demonstrate the selected effect with an owned marker

For an authorized writable-config test, preserve the original config and its permissions, identify who can change its content or replace its path, and use a public marker served from an owned reachable endpoint. Change only the reviewed URL/output to a fresh owned destination; observe the exact selected invocation, resulting bytes and actual effective identity. Use one agreed run/window and restore the original config before concluding. A concurrent job that rewrites the config or log can race both the change and restoration; retain timing and verify the final state.

This confirms the transfer/destination boundary under that observed identity. It does not prove arbitrary command execution or that a different protected file is writable. If the authorized task specifically replaces a scheduler/application file, preserve its complete original content/metadata and recovery path first, match its consumer's format and retain write-versus-consumer evidence separately. Do not replay a copied system-job payload to diagnose curl parsing. An output file's contents can be active for its next consumer even though curl does not execute them.

For a task requiring a local-file transfer, establish FILE protocol support and define `source_uri` as the fully encoded absolute `file:///...` URI of the selected authorized file, and `destination` as a fresh owned output:

~~~bash
curl -q --proto '=file' --output "$destination" "$source_uri"
~~~

The read and write use curl's running identity and filesystem access; a valid URI does not grant privileges. This is local acquisition, not an HTTP exchange. FILE URIs, HTTP 200 output, source permissions and a privileged scheduler are different facts. For an HTTP-only job, inspect the actual allowed protocol policy; merely adding an allowlist before untrusted config options is not a sandbox.

References: [curl config syntax](https://curl.se/docs/manpage.html#-K), [output association](https://curl.se/docs/manpage.html#-o), [default config](https://curl.se/docs/manpage.html#-q), [protocol selection](https://curl.se/docs/manpage.html#--proto).
