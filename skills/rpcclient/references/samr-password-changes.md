# Change or reset one selected account password

A password reset is a real account change, not a test of whether a graph edge exists. Identify the exact account/domain and the delegated reset right, the intended new credential and affected service/logon dependencies. You generally cannot snapshot an unknown old password for automatic rollback. Establish the owner's recovery process and preserve the pre-change account flags/expiry state that matter.

Samba distinguishes change-password methods, which use an old password, from privileged set-user-information methods. Inspect `help setuserinfo2` and the installed implementation's supported information classes. The historical class 23 example is:

~~~text
setuserinfo2 selected-user 23 "NEW_PASSWORD_FOR_SELECTED_ACCOUNT"
~~~

This is an interactive rpcclient command, with placeholders to replace through the task's credential-handling process. Avoid placing real credentials in a shell `-c` argument or retained transcript/history. Class 23 is not a universal choice for all servers: supported classes, session encryption and current cryptographic policy affect the operation. Do not weaken server policy to make an old writeup's method work; choose a supported administrative path.

Read the operation's status. Authentication success before the command is not reset success. A password restriction error can mean policy/history/complexity requirements; an access-denied error concerns the selected write. After a successful result, perform only the intended controlled authentication check and account-state check. Existing tickets or sessions may remain valid and replication can delay observations on another DC.

Do not retry after an ambiguous network failure by assuming the old state remains. Check the account through the designated DC/owner process first. Password resets can affect service accounts and access to password-derived protected data; resetting again is not equivalent to restoring every prior effect.

For a normal user password change, inspect the installed `chgpasswd` variants and their old/new credential requirements. Their transport/cryptographic differences matter; they are not aliases for a delegated reset. Record the actual method and verified result, without copying the secret into evidence.

See [Samba SAMR command handling](https://github.com/samba-team/samba/blob/master/source3/rpcclient/cmd_samr.c) and [RPC client manual](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html).
