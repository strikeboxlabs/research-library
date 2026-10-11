# List one approved local service directory

Use this for an administrator's requested inventory of a known directory on the selected SQL Server host. Require its exact absolute local drive path and the intended SQL session; do not derive a whole-filesystem search from a successful login. Confirm the SQL identity and whether the shell has entered a linked-server context before proceeding. An unknown instance/context or missing filesystem-inventory permission is a prerequisite gap.

Check the installed shell's help/implementation. In Impacket 0.11.0 the `xp_dirtree` helper submits `master.sys.xp_dirtree` with depth 1 and file inclusion enabled. The following is an **illustrative** invocation inside the SQL prompt; replace the path with the approved directory:

~~~text
xp_dirtree C:\ApprovedData
~~~

This is not a Linux shell command. The helper takes the line as a path, so shell quotation conventions do not apply. The reviewed implementation interpolates that path into a quoted SQL string without escaping apostrophes; use only the reviewed simple literal path, and choose a properly parameterized SQL client for an unusual path instead of submitting untrusted text. Other versions can differ.

Interpret `subdirectory` as the returned child name, `depth` as traversal depth and `file` as the file/directory indicator: 1 is a file, 0 is a directory in the source's observed result. A depth-one listing covers direct children, not recursive contents. It returns names, not file bytes, hashes or a coherent backup snapshot. Permission failures or an empty result do not independently prove the directory is empty.

The operation executes on the SQL Server side, subject to that instance's procedure availability, SQL permission and effective filesystem context. The connecting SQL user is not automatically the Windows identity reading the directory. A root-relative path does not explicitly select a drive. Use the verified absolute local path; a UNC path can initiate network access from the server and is a separate operation.

Do not infer an HTTP URL from a returned web-like directory name. Confirm the application's document-root/alias configuration and chosen hostname separately before a requested file retrieval. A file named backup is not proof of its format or current validity.

Finish with the instance/session identity, exact directory, returned direct-child names and any permission/coverage limit. This listing does not require enabling xp_cmdshell or changing server configuration. Stop at the requested inventory; credential discovery, remote path probing and authentication replay are different tasks.

Reference: [Impacket 0.11.0 shell implementation](https://github.com/fortra/impacket/blob/impacket_0_11_0/impacket/examples/mssqlshell.py).
