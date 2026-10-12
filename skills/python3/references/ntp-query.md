# Query an owned NTP server without setting the clock

Use for one approved NTP endpoint when the trusted Python environment already supplies `ntplib`. Require its distribution metadata and a known compatible NTP version. This library request reads a time sample; it does not synchronize the local system clock or supply authentication.

Define `python_bin`, `ntp_host` and `ntp_version` (normally 2, 3 or 4 as supported by that endpoint):

~~~bash
"$python_bin" -I - "$ntp_host" "$ntp_version" <<'PY'
import sys
from datetime import datetime, timezone
from importlib.metadata import version
import ntplib

print("ntplib", version("ntplib"))
sample = ntplib.NTPClient().request(sys.argv[1], version=int(sys.argv[2]), timeout=3)
print("transmit_utc", datetime.fromtimestamp(sample.tx_time, timezone.utc).isoformat())
print("mode", sample.mode, "stratum", sample.stratum, "leap", sample.leap)
print("offset_seconds", sample.offset, "delay_seconds", sample.delay)
PY
~~~

`-I` deliberately omits current-directory/user-site packages; missing ntplib is a dependency/search-path gap, not proof the endpoint failed. `tx_time` is the server transmit timestamp converted to Unix time. Offset/delay use the exchange's timestamps and the local clock; report them as one sample. A server-mode reply with stratum 1–15 and leap other than 3 is a plausible synchronized response, not independently trusted time. Unsynchronized/invalid values, timeout, parse failure or rollover failure leave that sample unsuitable. Plain UDP NTP here is unauthenticated. The library's socket timeout does not bound DNS resolution or an entire series of unrelated received datagrams.

Retain endpoint, interpreter/library versions, sample fields and diagnostics. Human-readable local-time formatting is not evidence that the host clock changed. Do not couple this diagnosis to generating or replaying account authentication tokens. For clock adjustment, use the deployment's separately approved time-service procedure.

See [ntplib request and statistics](https://github.com/cf-natali/ntplib/blob/master/ntplib.py).
