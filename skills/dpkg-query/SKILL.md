---
name: dpkg-query
description: Map an observed file to Debian/Ubuntu package records and evaluate installed status and complete versions. Use when a helper's banner, a residual package entry or a vendor backport makes vulnerability matching uncertain.
---

# Match an artifact to its package record

Use on a Debian-family system with the relevant dpkg database. Define `admindir` as its verified absolute administrative directory, normally `/var/lib/dpkg`. A container, mounted image and host can have different databases. The following operations read package records; they do not run the named helper or install anything.

Define `binary` as the observed absolute path, without glob metacharacters, in that database's filesystem view:

~~~bash
dpkg-query --admindir="$admindir" -S "$binary"
~~~

Read the matching pathname and owning package together. `-S` accepts patterns: shell quoting does not make `*`, `?` or `[` literal inside its argument. Do not split blindly at the first colon because package names can include architecture qualifiers. A missing match can mean a different symlink/merged-/usr spelling, a generated or manually installed file, or the wrong database. Resolve that discrepancy before assigning a package. Ownership records do not prove current file contents or permissions.

Define `package` as the exact returned package name, retaining an architecture qualifier when present:

~~~bash
dpkg-query --admindir="$admindir" -W -f='${binary:Package}\t${Version}\t${Architecture}\t${Status}\t${source:Package}\t${source:Version}\n' "$package"
~~~

The fields are binary name, binary version, architecture, status, source name and source version. Single quotes preserve dpkg's field expressions. Keep stderr and status: query exit 1 can mean an unmatched/partially matched request; 2 is a query error. A printed version alone is insufficient. An **illustrative** `deinstall ok config-files` record is residual configuration, whereas `install ok installed` identifies an installed record. Neither establishes that a running process uses those bytes.

## Compare the right version to the right advisory

Match distribution/release and source-versus-binary package scope first. Security trackers often name the source package, which can differ from the executable and binary package. Retain the epoch and distribution revision; upstream banners omit information needed for backports. A scanner's version range is a candidate until these details agree.

Define nonempty `installed_version` from the applicable field and `fixed_version` from that release's authoritative advisory. Compare with Debian's ordering, not lexical sorting or a floating-point conversion:

~~~bash
if [ -n "$installed_version" ] && [ -n "$fixed_version" ]; then
    dpkg --compare-versions "$installed_version" ge "$fixed_version"
    comparison_status=$?
else
    comparison_status=2
fi
~~~

Status 0 satisfies this ordering, 1 does not, and 2 means the comparison is unresolved/invalid here. It is not a live exploit test or evidence that the on-disk helper is unmodified. Empty versions must not silently become sortable evidence.

For a concrete backport distinction, Debian's CVE-2022-37706 record lists a bullseye fix in `0.24.2-8+deb11u1`, while upstream fixed the issue in 0.25.4. Do not transfer that Debian threshold to Ubuntu. If the relevant vendor says the issue still needs evaluation, preserve that uncertainty instead of inventing a fixed version. Finish with artifact path, selected database, package/status, complete applicable version and advisory scope.

See the [dpkg-query manual](https://manpages.debian.org/bookworm/dpkg/dpkg-query.1.en.html), [comparison and status semantics](https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html), [Debian version format](https://manpages.debian.org/bookworm/dpkg-dev/deb-version.7.en.html) and [example source-package advisory](https://security-tracker.debian.org/tracker/CVE-2022-37706).
