# Selected Grafana plugin-path file read

Use for an authorized file-read check of **CVE-2021-43798**, not an arbitrary Grafana installation. The vendor advisory covers 8.0.0-beta1 through 8.3.0, excluding fixed branch releases 8.0.7, 8.1.8 and 8.2.7; 8.3.1 fixes its branch. A footer is a version lead, not proof of unpatched code or a reachable vulnerable route. Check the deployed build/backports and route. The separate markdown-file traversal CVE is not interchangeable with this one.

The vulnerable route is `/public/plugins/<plugin-id>/<file>`. It first resolves a registered plugin, then opens a path based on the plugin directory. Select a plugin known on that instance (the historical examples use `mysql` and `zipkin`); a missing plugin and a missing selected file can both produce 404. This reads with Grafana's service identity inside its filesystem namespace, which can be a container. It does not inherently read the physical host's files or execute commands.

Define `origin` as the exact scoped scheme/host/port plus any verified application subpath, without a trailing slash; `plugin` as that plugin ID; `relative_file` as the authorized absolute file path with its initial slash removed; and `traversal` as enough `../` segments to leave the observed plugin path. Define `headers` and `body` as fresh private paths. Start with a small approved control file, such as `etc/hostname`, whose result can be discriminated from a login or fallback page:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --path-as-is --globoff \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' \
  "$origin/public/plugins/$plugin/$traversal$relative_file"
~~~

Record curl's immediate exit status, HTTP status and body from this **same GET**. `--path-as-is` prevents curl removing literal dot segments; it does not prevent server/proxy normalization. Percent-encoded slashes are another representation, not guaranteed equivalents through every intermediary. Keep the exact requested representation with the result. Transport success or HTTP 200 alone is insufficient; compare a normal plugin asset/control response and expected file content. A nonzero transport status with a partial body leaves acquisition incomplete.

For an independently authorized database acquisition, repeat the capture with fresh output files and the **verified** SQLite path. Historical packaged installations often place it at `/var/lib/grafana/grafana.db`, but `[paths] data`, `[database] path`, environment/command overrides or an external MySQL/PostgreSQL backend can change this. A hostname result does not establish the database path. The container hostname can suggest an ID; it is not authoritative Docker identity.

Before database queries, check the acquired bytes, not its extension:

~~~bash
python3 - "$body" <<'PY'
import sys
with open(sys.argv[1], 'rb') as source:
    if source.read(16) != b'SQLite format 3\x00':
        raise SystemExit('Response is not a SQLite database header')
print('SQLite header present; coherent acquisition still requires verification')
PY
~~~

The header is only a format check. A live `.db` file may omit committed WAL data; a successfully parsed copy is not proof of a complete snapshot. Preserve any coherently acquired sidecars or obtain an application-coordinated backup where that is available. Query failure/truncation calls for acquisition diagnosis; do not substitute an HTML error file or discard WAL to make it open. Finish with the selected file/result, service-namespace scope and acquisition limitations. Credential recovery and use are separate tasks.

Resolve applicability with the [vendor advisory](https://github.com/grafana/grafana/security/advisories/GHSA-8pjx-jj86-j47p), [8.0.0 plugin handler](https://github.com/grafana/grafana/blob/v8.0.0/pkg/api/plugins.go), [versioned database settings](https://github.com/grafana/grafana/blob/v8.0.0/conf/defaults.ini) and [curl path option](https://curl.se/docs/manpage.html#--path-as-is).
