---
name: getfacl
description: Explain Linux POSIX ACL permissions and directory access failures with getfacl. Use when named users, ACL masks, default ACLs or parent traversal make an ls permission summary misleading.
---

# Read the ACL for the failing identity and path

Read this entire SKILL.md before acting. Establish the exact path and process identity, inspect access entries and applicable masks, and inspect parents or default entries only when traversal or inheritance is the question. Finish with the supported access explanation or the specific missing identity/path evidence.

Define `path` as the exact absolute file or directory involved. Record the relevant process's effective UID and groups; `id` without an argument describes the current shell, which may differ from a service or an existing session after group changes.

~~~bash
id
getfacl -p -n -e -- "$path"
~~~

`-p` retains the absolute path, `-n` keeps numeric identities and `-e` displays effective-rights comments. Preserve owner/group headers and diagnostics. On a filesystem without POSIX ACL support, basic mode-derived entries do not prove an extended ACL exists. An unreadable path is incomplete evidence.

Consider this **illustrative** directory ACL fragment:

~~~text
# owner: 0
# group: 2000
user::rwx
user:1001:rwx                  #effective:r-x
group::r-x                    #effective:r-x
mask::r-x
other::---
~~~

UID 1001's named entry grants only `r-x` after the mask, despite its raw `rwx`. The owning group 2000 also has `r-x`; a list of named users is not the complete access population. The mask limits named users, the owning group and named groups, while owner and other entries are outside that mask. With an ACL mask, the group-class bits shown by `ls -l` represent the mask rather than simply the owning group's entry.

Match the owner first, then a matching named user, then applicable groups, then others. A matching named-user denial does not fall through to a more permissive group or other entry. Check the actual numeric identity and memberships before attributing the failure to the ACL.

# Separate this directory, its parents and newly created children

Directory `x` permits traversal/search; `r` permits listing names. Reaching a file requires search permission on every parent. A readable directory listing does not establish that its files can be opened, and a readable file ACL does not overcome an inaccessible ancestor. Run the same bounded inspection on the relevant parents until the failing component is established; avoid a recursive whole-tree dump for one failed open.

Inspect inheritance separately when that is the question:

~~~bash
getfacl -p -n -e -d -- "$path"
~~~

A directory's `default:` ACL influences new children, subject to creation-mode rules; it does not grant access to the directory itself or retrofit existing children. Do not infer an absent default ACL solely from ordinary output when `POSIXLY_CORRECT` is set; `-d` explicitly requests it.

Report the path, process identity, matching ACL entry, mask and parent condition that support the diagnosis. If those allow the requested access but the operation still fails, investigate the relevant mount, security module or application constraint. POSIX ACL inspection is one layer; it does not establish a successful open or authorize changing permissions. See the [tool manual](https://man7.org/linux/man-pages/man1/getfacl.1.html) and [ACL access rules](https://man7.org/linux/man-pages/man5/acl.5.html).
