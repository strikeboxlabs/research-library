---
name: gdbus
description: Read a known D-Bus capability result with GLib gdbus on Linux. Use to distinguish logind operation authorization, authentication challenges, unsupported operations and failed bus calls.
---

# Read logind capability evidence

Read this entire SKILL.md before acting. Require an authorized session on the owned Linux host, its system bus and systemd-logind. All instructions are inline. This selected task calls only `CanReboot`; finish with the returned value, calling identity/session, host, time and command status. It does not reboot the host.

Check `gdbus call --help` and confirm timeout support. Run in the intended user's existing session without sudo changing the caller:

~~~bash
gdbus call --system --dest org.freedesktop.login1 \
  --object-path /org/freedesktop/login1 \
  --method org.freedesktop.login1.Manager.CanReboot --timeout 10
status=$?
~~~

The output is a GVariant tuple, such as the **illustrative** `('challenge',)`, not JSON or shell instructions. A normal call status means the method returned; it does not mean the capability result is affirmative.

| Result | Supported interpretation |
|---|---|
| `yes` | The operation is supported and this caller needs no further authentication for this check. |
| `challenge` | The operation is available but needs additional authorization. |
| `no` | The operation is available but this caller is not allowed. |
| `na` | The operation is unsupported by the relevant system components. |
| Inhibitor-related or unfamiliar value | Preserve it and consult the installed logind API version; newer releases can report inhibitor states separately. |

`yes` does not establish a global polkit `allow_active` status, permission for storage operations, a local-seat identity or that a reboot occurred. Policy, inhibitors and session context can produce different results for different actions or times. Inspect the relevant effective policy and session metadata when attribution matters; do not change PAM, environment or policy to force a result.

Bus unavailable, unknown service/object/method, timeout and access-denied errors leave the query incomplete. A container's bus or a different user's session may describe another context. Do not replace the system bus with the session bus and assume equivalence. Arbitrary D-Bus methods can change state; the read-only property belongs to this selected method, not to `gdbus call` generally.

References: [gdbus CLI source documentation](https://github.com/GNOME/glib/blob/main/docs/reference/gio/gdbus.rst), [logind method and return-value contract](https://github.com/systemd/systemd/blob/main/man/org.freedesktop.login1.xml).
