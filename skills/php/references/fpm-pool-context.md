# Attribute a selected FPM endpoint to its worker pool

Require the acquired or approved live listener/process evidence, actual master configuration and included pool files. Keep these captures tied to the same instance/time; a conventional port or filename alone cannot identify the pool serving a request. This procedure inspects configuration and existing process evidence without submitting PHP code or restarting FPM.

Follow master includes to each relevant named pool, then compare its `listen`, `user` and `group` with the selected endpoint and workers. Listen can be TCP or a Unix socket; there is no mandatory universal port9000. A root-owned master and a worker under another account are distinct execution contexts. Several pools can have different identities and settings.

For known `pid` and `port`, inspect current evidence through approved procps/iproute2 tools:

~~~bash
ps -ww -p "$pid" -o pid=,ppid=,euid=,ruid=,lstart=,args=
ss -lntp "sport = :$port"
~~~

Missing process ownership in ss is a visibility gap, not an ownerless service. Correlate the actual pool/socket; a similarly named www.conf file is not sufficient. For a Unix socket, inspect its actual ownership/mode/ACL rather than applying TCP allowed-client settings. For TCP, compare bind scope and `listen.allowed_clients` with the intended consumer; unset/blank allowed_clients accepts any address that can reach it.

Source configuration describes intended settings, not proof they were loaded. A saved backup or CLI PHP --ini result does not identify the running FPM instance. Finish with pool, endpoint, observed worker identity and any unresolved include/time/ownership discrepancy. Use the existing approved application observation if one is needed; a raw FastCGI code request is not a diagnostic prerequisite.

See [PHP FPM pool configuration](https://www.php.net/manual/en/install.fpm.configuration.php).
