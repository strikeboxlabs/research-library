# Explain a vsftpd account's view

Use this branch when you already have authorized read access to the server's active configuration, or acquired copies. Do not change the configuration to test a theory. Client-visible `/` can be a chroot; it need not mean the operating system's `/`.

Locate the actual service invocation/configuration first. In the main configuration, inspect these keys and follow the observed per-user file where applicable:

| Setting | Consequence to verify |
|---|---|
| `local_enable` | Needed for non-anonymous logins, including virtual users; its name does not prove authentication uses `/etc/passwd`. |
| `pam_service_name` | Selects the PAM service stack. Read that actual service and included files; do not assume the upstream default or a distro default. |
| `guest_enable`, `guest_username` | Guest mapping can give an authenticated virtual identity a different OS file-access identity. |
| `user_config_dir` | The file named for the login can override session settings, such as root/mapping. Not every daemon setting supports a session override. |
| `local_root`, `chroot_local_user`, `user_sub_token` | Explain the session root and substitutions, subject to actual filesystem access. |
| `write_enable`, `virtual_use_local_privs`, relevant anonymous-write settings | Gate operations separately from successful authentication and OS permissions. |

For an acquired `config` file, a bounded read-only selection is:

~~~bash
grep -nE '^(local_enable|pam_service_name|guest_enable|guest_username|user_config_dir|local_root|chroot_local_user|user_sub_token|write_enable|virtual_use_local_privs|anon_.*)=' "$config"
~~~

Read surrounding configuration and the actual referenced files before concluding; this selection alone omits other relevant settings. A global root can be superseded for one user. An OS account or database login sharing a name with the FTP login does not establish shared credentials.

For PAM, trace `auth` and `account` stacks independently, including `include`/`substack` and their order. A successful `sufficient` module normally returns success immediately for that stack when no earlier `required` module failed; later lines may not execute. Its failure alone normally allows evaluation to continue. A database-backed module's configured query, password representation and options determine credential comparison; the table name does not establish MD5, plaintext or OS-password reuse.

If `pam_shells` is reached, it checks the account's shell against the configured shell list, conventionally `/etc/shells`. A listed `nologin` path can satisfy that membership check; this does not make `nologin` an interactive shell or prove SSH access. Inspect the deployed module's behavior rather than inferring it from the shell filename.

Finish with the supported mapping from login to PAM result, OS identity, session root and the requested operation. Missing included files or database-module parameters leave that part unresolved. A file listing proves only the observed listing; confirm a needed download or separately authorized write on the chosen object rather than assuming permissions from its appearance.

Resolve details with [vsftpd configuration](https://security.appspot.com/vsftpd/vsftpd_conf.html), [PAM control semantics](https://github.com/linux-pam/linux-pam/blob/master/doc/man/pam.conf-syntax.xml) and [pam_shells](https://github.com/linux-pam/linux-pam/blob/master/modules/pam_shells/pam_shells.8.xml).
