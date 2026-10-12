# Interpret acquired login-message evidence

Read this entire reference before the selected task. Use acquired configuration, file metadata and existing logs. Follow the selected server's distribution and package version; upstream OpenBSD and a distribution's portable OpenSSH/PAM build can differ. Do not execute a copied login hook to find out what it does.

Identify the message stage and producer. OpenSSH `Banner` supplies text before authentication; `PrintMotd` concerns an interactive login's MOTD. PAM session modules and shell startup files can supply additional text. Follow relevant includes and the selected session's effective configuration before attributing duplicate or delayed output. A banner or prompt alone does not establish successful authentication or remote identity.

Distinguish a displayed text file from a generated message. Upstream `pam_motd` describes message-file selection and display. Ubuntu's `update-motd` framework additionally documents executable fragments generating dynamic MOTD content under root. This is distribution-specific behavior, not a consequence of every SSH daemon running initially as root. Establish which mechanism is configured and enabled on this server, the selected fragment's eligibility, and its observed process identity. Missing configuration remains an explicit gap.

Directory group ownership does not establish group write permission. Check the file's actual mode/ACL and every parent separately; executable eligibility, content write authority and directory-entry control are different observations. A periodic copy may replace modified content without proving a complete metadata-preserving restoration. Retain the original displayed command and its uncertain quoting rather than inventing the scheduler's exact recurrence or shell grouping.

A foreground fragment can delay the login that invokes it. That observation does not establish that all SSH connections or the entire daemon are blocked. A background marker does not establish a process's later lifetime, completion or cleanup. Finish with the supported producer/stage, selected configuration and permission evidence, plus missing facts; do not turn source assertions into an execution receipt.

References: [OpenSSH server configuration](https://man.openbsd.org/sshd_config.5), [upstream pam_motd](https://github.com/linux-pam/linux-pam/blob/master/modules/pam_motd/pam_motd.8.xml), [Ubuntu update-motd](https://manpages.ubuntu.com/manpages/jammy/man5/update-motd.5.html).
