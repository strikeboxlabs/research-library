---
name: jar
description: Inspect Java archive members and update a selected resource in a working copy with the JDK jar tool. Use when a configuration edit must preserve archive paths and distinguish packaging from signed-content integrity.
---

# Update the selected resource in a copy

Read this entire SKILL.md before acting. Select the archive, exact member and reviewed replacement. Finish with the candidate's member/content checks and unresolved signature or runtime requirements.

Check `jar --version` and `jar --help`; older JDKs use short options. Define `original` as the saved JAR:

~~~bash
jar --list --file "$original"
~~~

Listing does not authenticate or execute the archive. Inspect its manifest and signature metadata before a requested edit. Changing signed bytes can invalidate verification; use the application's established rebuild/signing process rather than removing signatures to conceal the mismatch.

For a reviewed unsigned archive or an intermediate candidate awaiting that signing process, define `candidate` as a fresh path, `edit_root` as the directory holding the replacement and `member` as its exact relative archive name:

~~~bash
test ! -e "$candidate" && cp -- "$original" "$candidate" &&
jar --update --file "$candidate" -C "$edit_root" "$member"
jar --list --file "$candidate"
~~~

Check update status before accepting the listing. `-C` selects the replacement's filesystem root, not a new archive prefix. Inspect the candidate's selected resource and intended parser result; a member listing does not verify its bytes, application compatibility or signature. Keep the original and failed candidate separate. See the [JDK jar manual](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jar.html).
