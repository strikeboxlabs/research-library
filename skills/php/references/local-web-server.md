# Serve a reviewed local web test

Use PHP's built-in server for a selected disposable web test, including PHP responses or a static marker page. Define `php_bin` as the selected executable, `document_root` as a dedicated reviewed directory, and `bind_ip`/`port` as the intended interface and available port:

~~~bash
"$php_bin" -S "$bind_ip:$port" -t "$document_root"
~~~

Keep the process in the foreground so requests/errors remain observable. Choose loopback for a same-machine client; a separately scoped remote browser needs an address it can reach. Binding `0.0.0.0` exposes every IPv4 interface. A low port may require existing bind privileges; choose the intended accessible port rather than changing system settings. This server is for a controlled test, not a production deployment.

Review every executable PHP file under the root: requests can run it with the server process's permissions. A `.php` filename can contain static HTML, but actual PHP executes. Keep source secrets/backups outside the root. An optional positional router script changes request handling and must be reviewed before use.

Request a known marker URL from the actual caller's vantage and compare the response bytes/status with its expected file. A startup line establishes a listener attempt; a logged request establishes receipt, not that the browser ran the page's JavaScript or that a second request succeeded. Record Host/path and selected root when a 404 or unexpected index appears.

The normal server has one worker; a blocking request can stall another request to it. Selected PHP versions support multiple workers via configuration, but that is a separate test condition, not a default fix. Requests use the built-in server's cli-server SAPI, rather than an ordinary cli invocation. Match the chosen binary/startup configuration and extensions; a separate php -v/--ini result does not prove the running server's loaded state. This test does not reproduce an FPM/Apache/OpenBSD stack.

Without -t, the server uses its startup working directory as its document root. A service's WorkingDirectory therefore matters, but an acquired unit file alone does not establish its loaded manager state, drop-ins or the running process identity. Correlate those when reviewing an existing deployment. Keep the explicit -t root in the disposable procedure above rather than relying on the caller's directory.

For browser callbacks, preserve origin (scheme/host/port), content type and the expected callback endpoint. Request receipt, response completion, script execution and application state are separate evidence. Stop the owned foreground server and inspect/remove only its owned test artifacts when finished.

See [PHP built-in server behavior](https://www.php.net/manual/en/features.commandline.webserver.php).
