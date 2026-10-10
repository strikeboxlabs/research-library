# A permitted authenticator with its own password and key-enrollment effect

Start with the exact effective sudo listing, RunAs identity, command path and arguments. A successful sudo authentication only satisfies that layer. The permitted program can require a second application password; the user's sudo/Linux password need not pass it. Conversely, a program's "authenticated" message alone does not prove what privileged effect occurred.

Follow the acquired matching binary or deployed source's input/comparison and successful branch. If it uses embedded key/counter/ciphertext, recovered bytes are a candidate for its predicate. Preserve byte length/encoding and any trimming. A debugger-modified success path is not proof the ordinary privileged launch accepts that input. Running a copied binary under an unprivileged debugger can differ in identity/filesystem/environment from the actual sudo launch.

For an explicitly authorized execution, define `run_as` and `permitted_command` from the reviewed policy, then invoke the real permitted operation:

~~~bash
sudo -u "$run_as" -- "$permitted_command"
~~~

Supply its selected secret through the intended prompt, not command arguments/logged shell history. If its successful branch asks for an SSH public key, that input authorizes a persistent key-enrollment action by the program; it is not merely a harmless password check. Select the task's own public key and establish the destination account/path and append/replacement/option behavior from actual code or observed state. Do not assume the usual `authorized_keys` path just from the prompt. Use only public material, never a private key, and record the authorized change for cleanup.

Retain the policy, actual application acceptance and enrollment result separately. Confirm the selected SSH server/account/key and remote identity through the authorized login; a claimed enrollment line or root-looking prompt alone is weaker evidence. Failure of that login may reflect key type/options, account policy, destination path or incomplete write, rather than incorrect decrypted bytes. If only source review is available, report the supported capability and the precise missing runtime evidence.

The mechanism may be a privileged configuration/file effect rather than a root shell inside the authenticator. Identify the actual authority and resulting state. A path-only policy permits additional arguments unless constrained separately, but it does not make an application's own password optional. Preserve existing task inputs and avoid repeated enrollment to diagnose an unrelated login failure.

See [sudoers RunAs/argument policy](https://github.com/sudo-project/sudo/blob/main/docs/sudoers.man.in) and [OpenSSH authorized-key semantics](https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT).
