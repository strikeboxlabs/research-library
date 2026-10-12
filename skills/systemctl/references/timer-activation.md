# Trace the selected scheduled service

Use the same system or user manager for every query. Define `timer` as the exact selected .timer name:

~~~bash
systemctl --no-pager --full list-timers --all "$timer"
systemctl --no-pager cat "$timer"
systemctl show "$timer" -p LoadState -p ActiveState -p Unit -p LastTriggerUSec
~~~

Retain statuses/diagnostics. list-timers describes timers currently in memory; all includes inactive ones, not every installed timer file. NEXT/LAST are trigger times rather than proof the job completed. One displayed interval does not establish the configured recurrence. Inspect the timer's actual monotonic/calendar settings and accuracy/randomization when timing matters.

Use its Unit property/ACTIVATES value to define `service`; a matching .service basename is only the default. Inspect configuration, actual execution identity and result:

~~~bash
systemctl --no-pager cat "$service"
systemctl show "$service" -p User -p Group -p ExecStart -p WorkingDirectory \
  -p ActiveState -p SubState -p Result -p ExecMainStatus
journalctl -b -u "$service" -n 100 --no-pager
~~~

Disk unit files can differ from manager-loaded settings. Trace the selected script/dependencies as data before attributing their effects. An already active service is left running when its timer elapses; no new instance is necessarily launched. Missing journal access or retained timestamps leave completion unresolved. Verify the requested output separately; do not start or alter a timer merely to inspect it.

Sources: [systemctl](https://raw.githubusercontent.com/systemd/systemd/main/man/systemctl.xml), [timer contract](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.timer.xml).
