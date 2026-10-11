# Inspect names on the selected system bus

Require the owned Linux namespace's accessible system bus and a trusted interpreter whose installed dbus-python binding is compatible with it. Define `python_bin` as that interpreter's verified absolute path. Missing bindings or bus access are prerequisites to report; this task does not install a library, start services or change bus policy.

~~~bash
"$python_bin" -I - <<'PY'
import dbus

bus = dbus.SystemBus(private=True)
try:
    for name in sorted(str(name) for name in bus.list_names()):
        print(name)
finally:
    bus.close()
PY
~~~

Record status, caller/namespace, time and the returned names. `private=True` supplies this helper's separate connection, closed on completion. `-I` excludes the working directory/user site but still imports the installed binding and trusted environment's startup code. An import failure in this search path does not prove a running service lacks its own binding.

ListNames reports currently owned unique and well-known bus names. An **illustrative** `:1.24` is a connection name; `org.example.Service` is a well-known name. This is not a list of every activatable service or exported interface/method, nor proof of method authority or OS identity. SessionBus would select a different bus. Connection/name changes can occur immediately after this snapshot; an absent name does not establish that its application is uninstalled.

When comparing an acquired policy, `own` grants permission to own a bus name; it does not prove who owns it now. `send_destination`/`receive_sender` are message rules for the connection owning that name, not application-level argument validation. Keep name, object path, interface, member and OS identity distinct. Report the policy fragment as configuration evidence with effective-policy/runtime gaps; do not invoke a mutating method to infer its authorization.

References: [dbus-python connection types](https://dbus.freedesktop.org/doc/dbus-python/dbus.html#dbus.SystemBus), [bus API](https://dbus.freedesktop.org/doc/dbus-python/dbus.bus.html#dbus.bus.BusConnection.list_names), [D-Bus names](https://dbus.freedesktop.org/doc/dbus-specification.html#bus-messages-list-names), [daemon policy](https://dbus.freedesktop.org/doc/dbus-daemon.1.html).
