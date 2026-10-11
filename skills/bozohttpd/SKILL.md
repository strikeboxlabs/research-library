---
name: bozohttpd
description: Interpret an existing bozohttpd process configuration or serve an owned static directory on loopback with its portable daemon. Use to distinguish URL handlers, user-directory translation, indexes, process identity and build-dependent authentication.
---

# Understand or run the selected HTTP daemon

Read this entire SKILL.md before acting. For inspection, require the actual process arguments and matching manual; for serving, also require an installed trusted portable bozohttpd binary, an owned directory containing only intended public files and an approved local port. The configuration interpretation and serving branch are inline; select the applicable branch. Finish with the observed routing/configuration limits or verified response and shutdown evidence. Missing binary/build facts remain explicit gaps.

Define `httpd_bin` as the discovered executable. NetBSD may call this daemon `httpd`; a Linux command with that generic name may instead be Apache. Confirm identity before applying these options:

~~~bash
"$httpd_bin" -G
~~~

`-G` prints the version and exits; `-S` sets the advertised version. A header alone therefore does not prove the binary version. Compile-time feature choices can remove daemon mode, Lua, user directories, indexes or TLS; use the matching installed manual and package/build information.

## Interpret the existing process

Connect the actual options with their effects:

| Observed option | Meaning and next distinction |
|---|---|
| `-b`, `-f` | Daemon mode; `-f` implies daemon mode while retaining the foreground terminal. |
| `-i address`, `-I port` | Bind address/port in daemon mode. Without daemon mode, `-I` instead affects redirect URLs; it does not create a listener. |
| `-L prefix script` | A Lua script registers named callbacks below a URL prefix. The route is not evidence of an on-disk subdirectory or the script's complete implementation. |
| `-u`, optional `-p pubdir` | Translate `/~user/` into that user's `public_html` or selected public subdirectory, not the entire home. |
| `-X`, optional `-x index` | Generate a listing when the selected default index file is absent. `-H` hides dot entries in the listing; it does not establish access denial. |
| `-U user`, `-t root` | Switch process user/groups or chroot separately. Paths with chroot refer to the resulting root. Environment clearing has a separate `-e` override. |
| `-P path` | Write the daemon PID file at this pathname; the filename is neither the PID nor an automatic development-mode setting. |
| `-s` | Send logs to stderr. |

The final directory argument supplies the ordinary document root, with additional routing options considered separately. Process arguments describe intended configuration; actual responses and the current process establish what is running. JSON body fields called `code` are not the HTTP status line. A rejected request does not prove that every application input path is safe.

When Basic authentication matters, verify the installed build. NetBSD's default support differs from the portable distribution, where it is excluded unless enabled at build time. A `.htpasswd` file alone does not establish enforcement, and documented directory protection does not recursively protect subdirectories. Use the actual HTTP response for a selected owned resource; do not assume an error page proves a complete proxy configuration.

## Serve the selected static directory

Define `serve_dir` as its absolute path and `port` as an approved unused unprivileged TCP port. Run as the ordinary owner in the foreground:

~~~bash
"$httpd_bin" -f -s -i 127.0.0.1 -I "$port" "$serve_dir"
~~~

This binds the selected IPv4 loopback address. Check a known file with a local HTTP client and compare its response/body to the intended artifact. Bind failure, missing daemon-mode support and unreadable files are distinct failures. Stop the foreground server after the requested use and verify the listener ended; retain only necessary logs. User-directory translation, executable handlers and external exposure require their own explicit configuration and task scope.

Reference: [bozohttpd options and portable build differences](https://man.netbsd.org/NetBSD-9.5/bozohttpd.8).
