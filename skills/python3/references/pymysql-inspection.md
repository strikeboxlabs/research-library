# Inspect MySQL through an already installed PyMySQL driver

Prefer the installed mysql client for ordinary SQL work. Use this fallback when the application environment already has a trusted PyMySQL installation and the client is unavailable. Select `python_bin` as that environment's interpreter; `ModuleNotFoundError` is an environment/dependency gap, not a database rejection. Do not install a driver or launch an acquired application just to inspect its settings.

Read configuration as source/data first. Importing `package.settings` executes package/module initialization. Being in the same directory is neither universally required nor sufficient: the selected interpreter and module search path determine imports. `-I` excludes the current/script directory, user site and Python environment overrides; it still allows the interpreter's installed site packages. Unlike the entrypoint's standard-library locator, this procedure does not use `-S`.

For a known TCP/TLS database endpoint, define `connection_file` as an existing private UTF-8 JSON object containing the reviewed `host`, numeric `port`, `user`, `password`, `database` and trusted `ca_file` path. Map these explicitly from authorized configuration; do not copy executable settings. The host must match the server certificate. For an established Unix-socket or client-certificate deployment, adapt the connection to that verified policy before use; do not remove verification to make this example connect.

For this TLS procedure, first establish that the installed driver's handshake fails before authentication when TLS is unavailable. Older code such as [PyMySQL 1.1.1](https://github.com/PyMySQL/PyMySQL/blob/v1.1.1/pymysql/connections.py) can continue when the server does not advertise TLS; a validating SSL context alone does not prevent that fallback. If this prerequisite is unresolved, use the deployment's established required-TLS client or report the gap rather than treating these options as a universal guarantee.

~~~bash
"$python_bin" -I - "$connection_file" <<'PY'
import json, ssl, sys
import pymysql

with open(sys.argv[1], encoding='utf-8') as source:
    settings = json.load(source)
connection = pymysql.connect(
    host=settings['host'], port=int(settings['port']),
    user=settings['user'], password=settings['password'],
    database=settings['database'],
    ssl=ssl.create_default_context(cafile=settings['ca_file']),
    connect_timeout=5, read_timeout=10, write_timeout=10,
    local_infile=False, cursorclass=pymysql.cursors.DictCursor,
)
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT USER() AS client_identity, '
                       'CURRENT_USER() AS matched_account, '
                       'DATABASE() AS selected_database, VERSION() AS version')
        print(cursor.fetchone())
        cursor.execute(
            'SELECT TABLE_NAME, TABLE_TYPE FROM information_schema.TABLES '
            'WHERE TABLE_SCHEMA=%s ORDER BY TABLE_NAME LIMIT 11',
            (settings['database'],),
        )
        rows = cursor.fetchall()
        print(rows[:10])
        print('more_visible_tables:', len(rows) > 10)
finally:
    connection.close()
PY
~~~

Check the process status and any exception before using the output. A printed identity followed by an error is partial progress. The identity query describes this database session; its matched account can differ from the supplied user. Metadata visibility is privilege-dependent. **Illustrative** `more_visible_tables: True` means at least one additional visible table was omitted; `[]` is not proof that the database has no tables.

`DictCursor` returns named fields. `fetchone()` retrieves the next row, not a count or the entire result; ordinary cursors buffer query results, so fetching one does not bound an unbounded query. Here SQL limits the metadata result and the eleventh row detects truncation. For a selected data task, inspect its schema first, choose needed columns and a server-side limit, and bind values through `execute(sql, parameters)`. Placeholders represent values, not table/column identifiers. Do not replace this with a credentials-wide `SELECT *`.

Connection/read/write timeouts bound particular I/O waits, not total server execution. Closing a cursor alone does not close the connection. No commit is needed for these inspections, but that does not make arbitrary SQL read-only: stored functions and file-output clauses can have effects. Retain only the relevant result and failure details, keeping credentials private. Reachability from a container proves that vantage, not workstation access or host-root authority.

References: [connection and TLS options](https://pymysql.readthedocs.io/en/latest/modules/connections.html), [cursor and binding semantics](https://pymysql.readthedocs.io/en/latest/modules/cursors.html), [driver examples](https://pymysql.readthedocs.io/en/latest/user/examples.html), [Python imports](https://docs.python.org/3.12/tutorial/modules.html#the-module-search-path), [verified TLS contexts](https://docs.python.org/3.12/library/ssl.html#ssl.create_default_context).
