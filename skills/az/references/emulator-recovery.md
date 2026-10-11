# Select the endpoint before reading a blob

Use the task's protected connection setup to supply `AZURE_STORAGE_CONNECTION_STRING` to this process. Verify its account, protocol and explicit `BlobEndpoint` without printing the key. For a path-style Azurite endpoint, the account follows the service address; an illustrative shape is `http://127.0.0.1:10000/ACCOUNT`. Match the emulator's configured URL style and any tunnel/network namespace. `localhost` inside a container need not refer to the workstation's listener.

An account name alone can select a public Azure endpoint or trigger account-key lookup. Check conflicting inherited storage/auth settings before proceeding. Retain the deployment's TLS requirements; HTTP is appropriate only for an intended HTTP development listener. See [Azurite connection strings](https://github.com/Azure/Azurite#connection-strings).

Define `container` and `blob` as the exact selected object identifiers, `metadata` as a fresh private file and `output` as a fresh absolute file path. With the established environment:

~~~bash
umask 077
az storage blob show --container-name "$container" --name "$blob" --output json > "$metadata"
~~~

Check status and expected size/type before downloading:

~~~bash
az storage blob download --container-name "$container" --name "$blob" --file "$output"
~~~

Check status, resulting size and the intended format parser. Failure can leave partial bytes. Metadata and download are separate requests; retain version/ETag differences rather than assuming a stable object. `--file` writes locally; without it download can emit data to stdout. Do not use batch recovery for a single-object task. A table listing is not a complete metadata record. Unexpected public-host routing, missing authentication or API-version errors require resolving that specific configuration/compatibility issue. Debug logs can contain credentials. See [Azure CLI blob commands](https://learn.microsoft.com/en-us/cli/azure/storage/blob).
