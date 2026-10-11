---
name: jar
description: Inspect, create or update selected Java archives with the JDK jar tool. Use when staging roots, service-provider resources or configuration edits must preserve member paths and distinguish packaging from runtime and signature results.
---

# Package and inspect the selected archive

Read this entire SKILL.md before acting. Select listing, creation from a reviewed staging tree, or replacement of one exact member in a copy. Require fresh destinations and inspected inputs; finish with the candidate's member/content checks and unresolved signature or runtime requirements.

Check `jar --version` and `jar --help`; older JDKs use short options. Define `original` as the saved JAR:

~~~bash
jar --list --file "$original"
~~~

Listing does not authenticate or execute the archive. Inspect its manifest and signature metadata before a requested edit. Changing signed bytes can invalidate verification; use the application's established rebuild/signing process rather than removing signatures to conceal the mismatch.

For intended archive creation, define `staging` as a reviewed directory containing exactly the compiled classes/resources to package and `created_jar` as a fresh path outside that directory:

~~~bash
jar --create --file "$created_jar" -C "$staging" .
jar --list --file "$created_jar"
~~~

Check creation status before accepting the listing. `-C` makes the selected tree the archive root; inspect package directories and resource paths, rather than packaging a whole source checkout by convenience. Source/configuration files can otherwise be included unintentionally. A service-provider configuration beneath `META-INF/services/` is distinct from the default manifest and an executable Main-Class; inspect its provider names and matching classes without loading them. Jar does not compile Java, instantiate providers or establish that the runtime discovers them. Preserve actual class/resource content and JDK compatibility as separate checks.

For a reviewed unsigned archive or an intermediate candidate awaiting that signing process, define `candidate` as a fresh path, `edit_root` as the directory holding the replacement and `member` as its exact relative archive name:

~~~bash
test ! -e "$candidate" && cp -- "$original" "$candidate" &&
jar --update --file "$candidate" -C "$edit_root" "$member"
jar --list --file "$candidate"
~~~

Check update status before accepting the listing. `-C` selects the replacement's filesystem root, not a new archive prefix. Inspect the candidate's selected resource and intended parser result; a member listing does not verify its bytes, application compatibility or signature. Keep the original and failed candidate separate. See the [JDK jar manual](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jar.html).
