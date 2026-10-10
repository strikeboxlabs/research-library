# Select token time without changing the machine clock

Use this branch after import succeeds and the selected backend's clock is a plausible cause of rejection. Establish the token interval and required PIN separately; a time adjustment does not repair the wrong token/account. `--next` chooses the next token interval, not an arbitrary timezone correction.

For a trusted test epoch, define `epoch` as Unix seconds, `rcfile` as this token's configuration file and `code_file` as a fresh private output:

~~~bash
umask 077
stoken tokencode --rcfile="$rcfile" --use-time="$epoch" >"$code_file"
~~~

Check status before using the result. `--use-time=+30` instead adds 30 seconds to the current time at generation; a bare integer fixes an absolute instant. Do not combine `--use-time` with `--next`. This is a scoped diagnostic override, not a system clock/NTP change. A code generated for an old fixed timestamp does not remain current while an investigation continues.

If the scoped application exposes HTTP `Date`, preserve that header, the response's cache/proxy context and local request/receipt times. It describes message origination; a cache, relay or different web host can make it a poor estimate of the authentication backend's clock. Repeated fresh responses and independently known backend time are stronger than one header.

To convert an observed date, define `python_bin` as a trusted Python 3 interpreter and `http_date` as that exact header value, without the `Date:` name:

~~~bash
epoch=$("$python_bin" -I -S - "$http_date" <<'PY'
import sys
from email.utils import parsedate_to_datetime

dt = parsedate_to_datetime(sys.argv[1])
if dt.tzinfo is None or dt.utcoffset() is None:
    raise SystemExit("Missing timezone: do not substitute the workstation timezone")
print(int(dt.timestamp()))
PY
) && stoken tokencode --rcfile="$rcfile" --use-time="$epoch"
~~~

For an **illustrative** `Sat, 10 Oct 2026 10:00:00 GMT`, the timestamp is `1791626400`, independently of the workstation timezone. Python's timezone-aware timestamp avoids naive local-time conversion with nonportable `strftime('%s')`. Invalid dates or missing timezone leave the comparison unresolved.

For continuing generation, estimate the offset between the fresh server date and the midpoint of local send/receipt epochs, with uncertainty from response latency, one-second header resolution and backend identity. Use a freshly justified signed relative offset; do not repeatedly generate at the original absolute header time. Preserve generated-time and authentication-result evidence separately. A failure after correct generation may be PIN, expiry, replay, account or authorization policy; uncontrolled retries do not establish clock drift.

References: [stoken time options](https://github.com/stoken-dev/stoken/blob/main/stoken.1), [HTTP Date](https://www.rfc-editor.org/rfc/rfc9110.html#name-date), [Python date parsing](https://docs.python.org/3/library/email.utils.html#email.utils.parsedate_to_datetime).
