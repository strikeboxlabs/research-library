# Read the intended Tomcat management interface

Use a provisioned identity on a known owned Tomcat instance. Select the interface before requesting its read-only list operation:

| Route | Role | Result |
|---|---|---|
| `/manager/text/list` | `manager-script` | Deployed application contexts, state and session counts for that virtual host |
| `/host-manager/text/list` | `admin-script` | Configured virtual hosts |

The HTML interfaces use `manager-gui` and `admin-gui`, respectively. A Host Manager GUI role does not grant the application Manager GUI or either text interface. A 401 challenge alone establishes none of those privileges; IP restrictions and realm configuration also affect access.

Define `url` as the selected exact list URL, `username` as its provisioned account and `headers`/`body` as fresh private response files. Use trusted HTTPS, or the established protected local transport. Supplying only the username makes curl prompt for the password:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --user "$username" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

Check transport status, HTTP status and the plain-text body's `OK`/`FAIL` result together. Retain the virtual-host context. A running application entry does not establish its HTTP health or complete deployment provenance. Distinguish an incomplete transfer or a login/error body from a complete list.

This read-only task does not deploy, replace or stop applications. Keep query URLs quoted: Bash treats an unquoted ampersand as a command separator/background operator, so a pasted second parameter may never reach the server.

See Apache's [application Manager roles and list](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html) and [Host Manager roles and list](https://tomcat.apache.org/tomcat-9.0-doc/host-manager-howto.html).
