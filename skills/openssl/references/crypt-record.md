# Reproduce an observed crypt-record stage

Use this branch when the actual script selects `openssl passwd`, not a generic message digest or AES operation. Establish the selected input, algorithm, salt and all downstream transformations. `-1` emits MD5-crypt (`$1$...`), not a raw MD5 digest; `-apr1`, `-5` and `-6` select different records. Reproducing an existing legacy format is not a recommendation for new password storage.

Define `input_file` as the authorized password-list input, `salt` as the observed salt and `records` as a fresh private output:

~~~bash
umask 077
openssl passwd -help
openssl passwd -1 -salt "$salt" -in "$input_file" >"$records"
~~~

Check status before using records. File input is a password list, so multiple input lines can produce multiple records. Match the actual producer options; table mode can include cleartext and must not be added to ordinary evidence. Keep input/records private.

If the job feeds this output to md5sum, the digest covers the **printed record stream**, including its terminating newline(s), not the raw password or decoded record bytes:

~~~bash
md5sum --binary -- "$records"
~~~

Retain the digest field separately from its filename/mode columns. Capturing producer output directly preserves newlines that shell command substitution strips. Diagnose byte/platform differences with a public disposable input before touching actual secrets. A reproduced local digest does not prove that a scheduled job ran, that the resulting archive is complete or that its logs conceal source data.

Reference: [OpenSSL passwd](https://docs.openssl.org/3.5/man1/openssl-passwd/).
