# SSH application services and selected file reads

Use when an SSH-protocol endpoint presents a chat/application interface rather than an OS login shell. Required inputs are the actual endpoint/port, server-key trust, selected application identity and the task's permitted operations. A username on such a service can be a nickname chosen by the client; an administrator-looking chat message does not establish an OS or database account.

Define `host`, `port` and `nickname` for that scoped application:

~~~bash
ssh -p "$port" -l "$nickname" "$host"
~~~

Read the welcome and actual help interface. A Devzat-style service can expose slash commands for users, rooms and command descriptions. Use the supported `/help` and command-list/help command shown by **that build**; historical `/commands` and current upstream `/cmds`/`/man` are not interchangeable promises. Do not send shell commands simply because the transport is SSH. Text pasted into chat may be published to other participants.

For an observed `no matching host key type found` failure offering only `ssh-rsa`, and an authorized compatibility exception for this endpoint:

~~~bash
ssh -oHostKeyAlgorithms=+ssh-rsa -p "$port" -l "$nickname" "$host"
~~~

The `+` appends to defaults rather than replacing them. `ssh-rsa` here is the RSA/SHA-1 **signature** algorithm; RSA keys can also use SHA-2 and need not be regenerated merely because SHA-1 is disabled. This option addresses host-key negotiation, not user-authentication signature policy, password failure or a changed host key. Keep the exception confined to this selected connection, verify server identity and prefer a stronger supported algorithm when available.

## Custom file commands in an acquired application variant

If an acquired source/backup contains a file-reading command, trace command registration, argument parsing, guards, working directory, path construction and the file-open/read loop. Confirm the command exists on the scoped running service before using it. Main and development archives are leads; neither their names nor a source diff proves deployment.

For a build whose help/source explicitly specifies `/file <path> <password>`, select a small authorized text file and the established command-specific password. Enter the application command, not a shell command:

~~~text
/file <selected-relative-path> <selected-command-password>
~~~

The password is a function guard in that build, not necessarily a chat login or OS credential. Keep it in private evidence. A Go `filepath.Join(cwd, path)` cleans `..` components but does not enforce containment beneath `cwd`; enough parent components can reach a path outside the working directory when the process can read it. Establish the actual working directory and permitted path instead of copying a guessed number of traversal segments. File permissions follow the service's execution identity.

Distinguish argument/guard rejection, nonexistent path, permission denial and successful returned content. If the implementation sends each `bufio.Scanner` line as a system message, it can add a transport prefix, lose original newline distinctions or truncate on a scanner error/long line. Select only the intended artifact lines and remove only the evidenced prefix; do not indiscriminately strip words or merge the entire transcript. Missing delimiters, SNIP markers or a silent read-loop error leave an incomplete artifact.

For a recovered key, parse the complete protected working copy and compare a derived public fingerprint. A usable key parser result is not SSH authorization. Test the selected OS login only when it is part of the authorized task, using the actual OS SSH port/account; confirm OS identity there independently. Finish with the observed application command result and its limits, not an inferred shell or root identity.

References: [Devzat upstream interface](https://github.com/quackduck/devzat), [HostKeyAlgorithms](https://man.openbsd.org/ssh_config.5#HostKeyAlgorithms), [OpenSSH compatibility notes](https://www.openbsd.org/openssh/releasenotes.html), [Go path joining](https://pkg.go.dev/path/filepath#Join).
