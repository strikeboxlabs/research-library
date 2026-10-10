# Binary Password Safe and LUKS inputs

Use only for the selected container format. These modules consume binary files, unlike ordinary line-based hash modes, and both reviewed implementations disable potfile support. Keep explicit private recovery output and its artifact mapping; `--show` is not the result-retrieval procedure here.

Define `wordlist` as the existing candidate file, `session` as a unique name, `seconds` as the runtime budget, and `recovered` as a fresh private output file for this artifact.

## Password Safe v3

Define `database` as an intact working copy of the binary database:

~~~bash
umask 077
hashcat -m 5200 -a 0 "$database" "$wordlist" --session "$session" --runtime "$seconds" --status --outfile "$recovered" --outfile-format 2
~~~

Preserve the explicit output and final status. Verify a recovered candidate by opening a copy with a compatible Password Safe client. File-size/signature errors call for checking binary transfer and format/version, not treating the file as line-based hashes.

## LUKS1

First inspect an image copy with `cryptsetup luksDump`. The reviewed `14600` parser requires **LUKS version 1**, supported cipher/hash settings, readable enabled-keyslot material and encrypted payload data. Do not feed a LUKS2 image or a text dump into this mode.

Define `image` as the intact binary LUKS1 image copy:

~~~bash
umask 077
hashcat -m 14600 -a 0 "$image" "$wordlist" --session "$session" --runtime "$seconds" --status --outfile "$recovered" --outfile-format 2
~~~

Prefer the complete image. The parser seeks to keyslot material and to the payload offset, then reads 512 bytes of encrypted payload. A header-only backup can lack required data. Arkham's `dd bs=512 count=4097` assumes that image's 4096-sector payload offset; it is not a universal extraction size. Preserve source layout and check all required byte ranges if a reduced working artifact is necessary.

Inspect loaded keyslot count, rejected-format diagnostics and final recovery state. An unsupported slot/format or truncated image is not an exhausted candidate search. Verify each recovered candidate against the original-format image copy with cryptsetup's passphrase test before claiming recovery; the Hashcat module uses an entropy check on decrypted payload data. Do not overwrite headers, change keyslots or mount read-write to validate a candidate.

Primary implementations: [Password Safe v3](https://github.com/hashcat/hashcat/blob/master/src/modules/module_05200.c), [LUKS1](https://github.com/hashcat/hashcat/blob/master/src/modules/module_14600.c); [cryptsetup open/test-passphrase](https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-open.8.adoc).
