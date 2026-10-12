---
name: finger-user-enum
description: Interpret acquired finger-user-enum results and inspect the installed script's help. Use when Solaris replies, aliases, parser assumptions or missing completion evidence overstate account discovery.
---

# Interpret the captured Finger result

Read this entire SKILL.md before acting. Select an existing captured result and its original invocation; this task needs no conditional resources. Finish with the queried names, actual reply identities, classifier limitations and completion evidence. A filtered positive line is not authentication or proof of an exact account-name match.

Define `finger_enum_bin` as the existing trusted script invocation. Inspect its help without sending a query:

~~~bash
"$finger_enum_bin" -h
~~~

A missing Perl module is a prerequisite gap, not a service result. Match the capture to the actual version and options. In v1.0, `-U` reads usernames and `-T` reads targets; these are distinct inputs. The banner's worker count is concurrency, and its query timeout is not a whole-run deadline. A relay changes the network vantage. Record these facts from the existing capture rather than inferring them from default values.

The v1.0 classifier uses Solaris-oriented patterns, flattens line breaks and treats an unrecognised nonempty reply as positive. A query can return several accounts or a display-name match. Compare the requested name with the reply's actual login column; a heading and several names do not prove that the requested spelling is an OS login. A TTY, idle time or remote-host field describes the service's reply, not current SSH credential validity.

The script hides negative, empty and timed-out results in ordinary output. Its exception path labels connection failures as timeouts too. An absent positive line therefore does not establish account absence. It performs one receive of at most10000 bytes, so a printed response is not necessarily the complete protocol conversation. Resolve unfamiliar classification using already acquired positive/negative baseline replies from the same daemon; retain an uncertainty when those are missing.

Require the actual completion footer and query count before claiming coverage of an input list. A start banner and selected positives establish only the visible results. Report transport failures, incomplete capture and parser uncertainty separately, without turning this interpretation into password testing or an unrequested discovery run.

See the author's [v1.0 documentation](https://pentestmonkey.net/tools/user-enumeration/finger-user-enum) and [classifier implementation](https://github.com/pentestmonkey/finger-user-enum/blob/master/finger-user-enum.pl) when the captured format differs.
