# Sucrack build features and local authentication boundaries

Use only the branch needed for the selected account check. An existing installed binary is the starting point; compiling a source copy is optional recovery, not a prerequisite for every invocation. Confirm build/revision and its actual `-h` output before relying on copied switches.

## Statistics and candidate rewriting

| Option | Meaning and consequence |
|---|---|
| `-w N` | Worker concurrency. More workers can increase authentication load and lockout risk; it is not an attempt cap. |
| `-a` | ANSI statistics display in a build compiled with statistics support. |
| `-s N` | Statistics refresh interval in seconds, also requiring statistics support. It is not a delay between authentication attempts or a runtime bound. |
| `-r` | Enable candidate rewrites. It changes the tested space beyond the supplied wordlist. |
| `-l rules` | Select supported rewrite identifiers for a rewrite-enabled run. Read this build's rule listing; case is meaningful. |

The legacy rule identifiers include upper/lower/reverse operations and first/last-letter, digit-prefix/suffix and substitution choices. A compact string such as `AFLafld` selects several rules; do not infer its actual candidate count from its length. Check the guide and installed list. If the wordlist was already expanded with Hashcat rules, omitting Sucrack rewriting preserves that selected candidate set rather than stacking two mutation systems.

In a build without `--enable-statistics`, the legacy CLI prints warnings for `-a`/`-s` and continues with the check. Omit them if the display is unnecessary. If statistics are needed and an authorized build is chosen, review the existing source and configure helper, then define `source_dir` as its absolute path and `jobs` as the chosen positive build concurrency:

~~~bash
(
  cd -- "$source_dir" || exit
  ./configure --enable-statistics && make -j "$jobs"
)
status=$?
~~~

Require successful configure/build and inspect the produced `src/sucrack` artifact and its help. Configure/Makefiles execute source; a ZIP/clone is not trust verification. A failed rebuild can leave an older binary in place. No installation or privileged build is implied, and that relative artifact path is not the controlled image's deployed absolute path.

## Prompt detection and account policy

The upstream helper starts `su <selected-user> -c <success-marker-command>` through a pseudoterminal, feeds a candidate and watches output for its password prompt and failure/success markers. This requires an account/session whose policy and shell allow that command; password correctness alone is not sufficient.

The documented environment variables are:

- `SUCRACK_SU_PATH`: the actual executable su path, when the compiled default is wrong.
- `SUCRACK_AUTH_FAILURE`: the observed authentication-failure message when the default does not match this implementation or locale.
- `SUCRACK_AUTH_SUCCESS`: the success marker used by the helper.

Only use a verified path and actual observed messages; do not guess a binary location or reinterpret an expired/locked account as a wrong password. Choose a simple unique success marker without shell metacharacters: the implementation embeds it in a shell command, and substring matching can be confused by echoed or incidental output. These settings do not generally configure every password/MFA prompt. An unexpected password prompt, extra factor, localized response or restricted shell can stall the legacy parser or invalidate an exhaustion claim.

Distinguish PAM delays from dead parser waits and worker starvation. Do not infer a safe attempt rate from a statistics refresh interval. Preserve the finite list, rewrite choice, workers, observed policy and actual stopping condition without reproducing recovered secrets in a general report. Independently verify the intended local account session when that is the requested outcome.

See the [upstream README](https://github.com/hemp3l/sucrack/blob/master/README.md), [build feature definition](https://github.com/hemp3l/sucrack/blob/master/configure.ac) and [su interaction](https://github.com/hemp3l/sucrack/blob/master/src/su.c).
