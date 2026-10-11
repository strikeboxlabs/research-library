# Preserve returned policy and helper coverage

Use the same classic implementation, selected `server` and intentionally permitted empty-session context as SKILL.md. Inspect installed help and confirm **polenum** is available in addition to the Samba helpers. For this metadata task:

~~~bash
enum4linux -P "$server"
status=$?
~~~

Retain full stdout/stderr and status. `-P` selects password-policy information; `-a` also selects users, shares, groups, RID cycling and other enumeration. Do not add that broader mode to answer a policy question.

The reviewed wrapper invokes polenum and then rpcclient getdompwinfo. If polenum is missing, its policy function returns early: it does not automatically provide the later rpcclient fallback. Access denial, connection failure, unexpected helper output and returned partial policy are different results. The wrapper recognizes text patterns rather than providing a structured guarantee of every field.

Preserve the reported domain, minimum length, history, age, complexity flags, lockout threshold, duration and reset interval when returned; missing fields are unknown. A displayed threshold **None** is that helper/domain view at that time. It does not establish every account's effective fine-grained policy, another domain's rules, application protections or that authentication attempts have no operational effects. Read policy metadata without turning it into a permission or risk-free claim for password guessing.

An **illustrative** result with length7/history24 and thresholdNone supports those returned values only. Confirm any operational decision against administrator-provided effective policy for the selected account and service. Do not change account policy or attempt passwords to validate this read.

Reference: [classic policy function and options](https://github.com/CiscoCXSecurity/enum4linux/blob/master/enum4linux.pl).
