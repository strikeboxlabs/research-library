# Inspect an acquired PAM module statically

Use the entrypoint's inventory/export procedure with the actual object copy. Preserve its acquisition identity, digest and matched configuration snapshot. A familiar basename or another machine's configuration cannot prove package integrity, manual installation or that these bytes were loaded by the selected service.

Select the discovered `pam_sm_authenticate` symbol or its unique entry address, then export the relevant callees using DecompileSelected.java. Follow the real return value, saved PAM data and later account/credential hooks separately; assigning zero through a pointer does not invariably prove the function returns success on every path.

Map the authentication token's source to comparisons and any file read. Recover the original format bytes, field widths, destination capacity and scan return handling. A `%[^\n]` scans a nonempty sequence up to a newline; it does not consume that newline or establish NUL termination when conversion failed. Trace file-open failure, unreadable/empty input, close and fallback branches before asserting fail-open or fail-closed behavior. Distinguish acquired byte size from string length and a loop's comparison bound.

Identify secret-dependent early exits or delays as a static review finding. Preserve their location and branch conditions without building a candidate-recovery loop or testing authentication. Wall-clock differences between two different hosts include process startup, PAM stack, prompt handling and scheduling; a single observation does not establish a cause.

Read the selected service's complete PAM stack, including applicable includes/substacks. Simple `sufficient` success short-circuits only if no prior required module failed; a failure is ignored and processing continues. Authentication and account stacks are separate. Keep arguments such as `nodelay` tied to the module that implements them rather than assuming a universal PAM option.

Finish with selected function addresses, supported token/file/return flow, effective-stack uncertainty and unresolved analysis. Compare provenance with a trusted matching package/configuration baseline as a separate integrity task; do not load the specimen to resolve a decompiler ambiguity.

See [Linux-PAM stack controls](https://github.com/linux-pam/linux-pam/blob/master/doc/man/pam.conf-syntax.xml), [authentication module interface](https://github.com/linux-pam/linux-pam/blob/master/doc/man/pam_sm_authenticate.3.xml) and [glibc formatted input](https://sourceware.org/glibc/manual/latest/html_node/Formatted-Input-Functions.html).
