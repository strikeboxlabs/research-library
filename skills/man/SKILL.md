---
name: man
description: Locate and read the installed manual for a selected command or configuration format. Use when section ambiguity, pager behavior or a mismatched manual makes an option interpretation uncertain.
---

# Read the matching installed manual

Read this entire SKILL.md before acting. Require trusted man-db, its installed manual collection and formatter. Define `page` as the topic name and `section` as the intended section, such as 1 for commands or 5 for formats. Finish with the selected document and supported interpretation, retaining missing-page/rendering gaps.

~~~bash
man --version
man -w "$section" "$page"
man -P cat "$section" "$page"
~~~

Check each status and read the relevant complete section. The path query locates source; the final command renders using cat instead of an interactive pager. Default lookup shows the first matching section, which may be another topic. A successful render does not establish the running binary's version or behavior. Correlate package/manual provenance before applying its options. Missing manuals are distinct from missing executables. Keep trusted configuration/search paths; formatting acquired manual sources is not passive text reading.

See [man-db lookup and rendering](https://manpages.debian.org/bookworm/man-db/man.1.en.html).
