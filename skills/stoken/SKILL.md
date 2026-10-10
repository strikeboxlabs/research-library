---
name: stoken
description: Import an authorized RSA SecurID-compatible software token and generate its tokencode with stoken. Use for 81-digit CTF or SDTID inputs, token/PIN state and clock-offset diagnosis.
---

# Software-token state and tokencodes

Read this entire SKILL.md before acting; reuse complete current context. Establish the selected token, required device/password/PIN inputs and configuration destination. Preserve import/generation status; a generated code is not proof of server acceptance. For a suspected clock mismatch, read [explicit time selection](references/time-selection.md) fully before that procedure.

Define `token_file` as the private acquired token file and `rcfile` as a fresh absolute configuration path in an existing private directory. Use the installed stoken, not a TOTP generator:

~~~bash
umask 077
stoken version
stoken import --file="$token_file" --rcfile="$rcfile"
stoken show --rcfile="$rcfile"
stoken tokencode --rcfile="$rcfile"
~~~

Import accepts a raw 81-digit compressed token format (CTF), supported token URI or SDTID XML. A matching length is only a format lead: import must validate it. `--file` reads raw token material; `--rcfile` selects stoken's state file, including saved PIN data. They are not interchangeable. Default import writes `~/.stokenrc`; the explicit fresh path separates this token from an existing one. Do not add `--force` to resolve an unexpected overwrite or expiry failure.

Supply prompts according to the actual token provisioning. Device binding, token decryption password, local storage password and authentication PIN are distinct. An empty local password or PIN `0000` from a worked case is not a universal configuration. If the task calls for caching this token's known PIN, run `stoken setpin --rcfile="$rcfile"`; it changes that state file. Omitting it leaves prompting where required. Avoid `show --seed`, token strings or PIN/password arguments in ordinary evidence: these expose reusable material.

For unattended generation, `stoken tokencode --batch --rcfile="$rcfile"` fails when another prompt is needed. `--stdin` supports one required input, not a stream satisfying both password and PIN prompts. A missing prerequisite stays incomplete. Keep codes private and use the observed backend contract; token validity, time, PIN, replay policy and user authorization can each cause rejection.

References: [stoken usage](https://github.com/stoken-dev/stoken#usage), [upstream manual](https://github.com/stoken-dev/stoken/blob/main/stoken.1), [prompt and time implementation](https://github.com/stoken-dev/stoken/blob/main/src/cli.c).
