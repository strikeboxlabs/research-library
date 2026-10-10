---
name: impacket-mssqlclient
description: Connect to SQL Server using known Windows credentials or an existing Kerberos cache and inspect SQL identity and configuration. Use for SPN/cache failures, SQL versus OS identity and misleading command-shell results.
---

# Impacket SQL Server client

Check `impacket-mssqlclient -h`; upstream installations may expose `mssqlclient.py`. Define `domain`, `user`, `server` (the service FQDN), `server_ip` and `port` for the intended SQL instance. Windows authentication with a known password entered at the prompt:

~~~bash
impacket-mssqlclient -windows-auth -target-ip "$server_ip" -port "$port" "$domain/$user@$server"
~~~

Omitting `-windows-auth` in this password flow selects SQL authentication. A domain password is not automatically a SQL login password. For an existing authorized file cache, define `cache` as its absolute path and inspect its principal, service and lifetime before connecting:

~~~bash
KRB5CCNAME="$cache" impacket-mssqlclient -k -no-pass -target-ip "$server_ip" -port "$port" "$domain/$user@$server"
~~~

Keep the service hostname in the target while `-target-ip` selects the connection address. The TCP service principal normally includes the port, such as the **illustrative** `MSSQLSvc/sql.lab.example:1433`. Check the exact requested SPN and cache contents. A cache filename is not its principal. `-no-pass` suppresses prompting; it does not guarantee offline cache-only behavior. A missing matching ticket may trigger instance discovery or a KDC request. Check identity, expiry, DNS, time and SPN before repeating authentication.

The TLS-upgrade message is transport negotiation, not login success or proof of independently verified server identity. Check server errors and an actual SQL result. The client can print login errors without a useful failure exit code.

## Establish the SQL context before selecting an operation

At the SQL prompt, submit each statement as one command; this shell is not sqlcmd and does not require a `GO` batch terminator:

~~~sql
SELECT ORIGINAL_LOGIN() AS original_login, SUSER_SNAME() AS effective_login, USER_NAME() AS database_user, DB_NAME() AS database_name, IS_SRVROLEMEMBER('sysadmin') AS is_sysadmin;
SELECT name, value, value_in_use FROM sys.configurations WHERE name IN ('show advanced options', 'xp_cmdshell');
~~~

`ORIGINAL_LOGIN()` records the connecting identity; effective login and database user can differ after context changes. `dbo` is a database identity, not proof of Windows Administrator or SYSTEM. Role membership `1`/`0` and `NULL` are different results; `NULL` can mean invalid input or insufficient visibility. Configured `value` and active `value_in_use` can differ. Empty/denied metadata is an evidence gap, not an off setting.

Use `help` to distinguish shell helpers from SQL. `! command` runs on the local client. `xp_cmdshell` runs on the SQL Server host; UNC-path helpers can cause that server to contact another host. File, job, impersonation and linked-server helpers have additional effects.

For diagnosing an already authorized command-execution test, SQL login and child-process identities remain separate: a sysadmin's xp_cmdshell process normally uses the SQL Server service account; a permitted non-sysadmin uses its configured proxy. A successful SQL login does not establish command execution. Enabling xp_cmdshell changes server configuration, and `RECONFIGURE` applies changes. The convenience enable/disable helpers also change `show advanced options`; do not use them during metadata inspection or assume disabling restores the original state. Record exact initial values for any separately approved configuration change.

Consult the [CLI](https://github.com/fortra/impacket/blob/master/examples/mssqlclient.py), [shell implementation](https://github.com/fortra/impacket/blob/master/impacket/examples/mssqlshell.py), [SQL SPN rules](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/register-a-service-principal-name-for-kerberos-connections), [SQL identity](https://learn.microsoft.com/en-us/sql/t-sql/functions/original-login-transact-sql) and [xp_cmdshell execution context](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql) when resolving differences.
