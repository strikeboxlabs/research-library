---
name: certipy
description: Enumerate AD CS configuration, request selected certificates, authenticate with a PFX, recover through a permitted key-credential write and update selected UPNs from Linux. Use to connect template/CA findings to enrollment prerequisites, issuance results and current certificate-mapping behavior.
---

# Follow the certificate operation through its stages

Read this entire file before acting, then the complete reference for the selected task. Use ly4k's Certipy AD CS tool, often packaged as `certipy-ad`; an executable named `certipy` can be unrelated. Define `certipy_bin` as the verified invocation and inspect its banner/subcommand help.

| Task | Required working reference |
|---|---|
| Directory/CA collection, ESC1/ESC3/ESC9 interpretation and missing evidence | [Findings and collection](references/findings.md) |
| Certificate enrollment, agent requests, pending issuance or PFX authentication | [Enrollment and authentication](references/enrollment-and-authentication.md) |
| Selected KeyCredentialLink recovery or UPN changes for a mixed Kerberos stack test | [Shadow credentials and UPN changes](references/shadow-and-upn.md) |

Select the relevant identity and endpoints before the operation: the DC supplies directory/Kerberos services, the CA handles enrollment, and the eventual application authorizes service access. These may be different hosts. Template display names, internal names and CA configuration names are different inputs.

A useful result identifies which stage is established: configuration finding, permitted enrollment, issued certificate with matching private key, authenticated principal/TGT, or later service access. Do not substitute an ESC label, a request ID or a PFX filename for that evidence. A historical SAN-based path also depends on current strong-mapping policy and the certificate's actual SID/mapping data.

Version generations differ in commands, findings and defaults. Check the selected subcommand's installed help when the source and image disagree. Keep collected reports, private keys and caches in the task's private output location. Existing complete context need not be reread for every retry; recheck state when an observation or environment change makes it stale.

Use [upstream documentation](https://github.com/ly4k/Certipy/wiki) for an uncovered version-specific operation.
