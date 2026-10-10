---
name: rdate
description: Compare a selected time server with the local clock using print-only rdate queries. Use when clock skew complicates TOTP or Kerberos and protocol defaults or automatic clock correction are ambiguous.
---

# Measure a time mismatch before changing clocks

Confirm the installed implementation with `man rdate`. The following uses Linux OpenRdate's `-n` SNTP and `-p` print-only options. Other programs share this executable name; do not assume identical flags. Define `time_server` as the approved server whose clock matters to the failing service:

~~~bash
date -u '+%Y-%m-%dT%H:%M:%SZ'
TZ=UTC rdate -n -p -v "$time_server"
date -u '+%Y-%m-%dT%H:%M:%SZ'
~~~

Keep `-p`: without it, rdate can attempt to set the system clock. This diagnostic needs no sudo. `-s` suppresses printing; it is not a safe substitute. SNTP uses UDP/123; OpenRdate's default RFC 868 query normally uses TCP/37. An open TCP service or an SSH TCP tunnel therefore does not establish SNTP reachability.

Compare the returned time/adjustment with the surrounding local UTC readings and elapsed request time. Timeout means no usable sample, not zero skew. A single server reply does not prove an accurate or authenticated time source. Timezone display differences are distinct from an incorrect Unix clock.

If skew is material, identify the existing time service and any VM host synchronization before proposing a correction; competing synchronization can undo a manual change. TOTP enrollment parameters and Kerberos clock-skew policy remain separate checks. Do not widen acceptance windows or change the system clock simply because one login failed.

See the [Linux OpenRdate manual](https://manpages.debian.org/bookworm/rdate/rdate.8.en.html) for the supported options; [OpenBSD rdate](https://man.openbsd.org/rdate) has different protocol defaults.
