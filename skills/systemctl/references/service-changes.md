# Apply a selected service change

Use the exact manager/unit already identified and the task's authorized change scope. Preserve the original unit/drop-in and relevant failure output. Confirm dependencies and a recovery path before interrupting the service providing your own access.

| Change | Appropriate operation |
|---|---|
| Application configuration, service supports reload | Validate with that application's checker, then `systemctl reload "$unit"`. |
| Unit file or drop-in changed directly | Validate the unit, then `systemctl daemon-reload`; restart/reload the service separately as needed. |
| Process must be replaced | `systemctl restart "$unit"`; this starts an inactive unit too. |
| Restart only if already running | `systemctl try-restart "$unit"`. |
| Boot activation only | `enable`/`disable` change installation links; starting/stopping is a separate choice unless `--now` is supplied. |

For a reviewed unit-file edit, define `unit_file` as its actual path:

~~~bash
systemd-analyze verify "$unit_file"
systemctl daemon-reload
systemctl restart "$unit"
systemctl --no-pager --full status "$unit"
journalctl -b -u "$unit" -n 50 --no-pager
~~~

Proceed past validation only after resolving relevant errors. `daemon-reload` updates the manager's unit definitions and dependency graph; it does not tell the application to reread its configuration or replace its process. A successful restart job also does not prove the HTTP/database/listener operation works: perform the application's expected check and correlate it with the new process/start time.

When the cause of a start-rate-limit failure is corrected, `systemctl reset-failed "$unit"` clears failed/rate-limit state; then explicitly start the selected unit. Resetting the flag without correcting the failing command only hides useful evidence temporarily. Do not run a global reset/restart to fix one unit.

For an ExecStart override, systemd's list-reset semantics can require an empty `ExecStart=` before the replacement. Use a reviewed drop-in rather than copying the whole vendor unit. Validate the resulting effective configuration. If a change fails, restore the specific owned edit, reload the manager when unit definitions changed and apply the required service operation; retain both the failed and restored outcome. `systemctl revert` can remove all local overrides for that unit, including edits you did not create, so it is not an automatic rollback command.

See [unit directives](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) and [systemctl operations](https://github.com/systemd/systemd/blob/main/man/systemctl.xml).
