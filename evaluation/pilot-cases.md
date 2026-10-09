# Worked-guidance pilot: Linux cases

**Status: prepared, not executed on Linux.** This is evaluator material. Keep it, setup files and answer keys outside the worker's readable workspace. Follow the [comparison method](README.md#compare-worker-outcomes): equal tools, documentation access, budgets and reset fixtures; only the skill condition receives the selected skill folder. The baseline cannot read the repository. Use values different from the worked examples and grade outcomes rather than command imitation.

## GDB: assertion and missing evidence

Prepare this evaluator-owned `sample.c` in a fresh fixture directory on Linux with a compiler and GDB:

~~~c
#include <assert.h>
#include <stddef.h>
static int item_at(const int *items, size_t length, size_t index) {
    assert(index < length);
    return items[index];
}
int main(void) {
    const int items[] = {10, 20, 30};
    const size_t count = sizeof items / sizeof items[0];
    return item_at(items, count, count);
}
~~~

Compile and save the owned child's core at the assertion without changing host core-dump policy:

~~~bash
cc -g -O0 -o sample sample.c
gdb -q -nx -batch -iex 'set auto-load off' -ex 'set startup-with-shell off' -ex 'set disable-randomization off' -ex run -ex 'generate-core-file sample.core' ./sample
~~~

Verify that compilation and core generation succeeded. Missing tools or debugging restrictions make the case unavailable, not passed. Supply the worker with matching source, executable, core and build provenance.

Request: “Explain this program's recorded failure and distinguish what the core proves from anything still uncertain. Do not run or modify the program.”

Success identifies the assertion, actual argument values (3 and 3 here), and available caller/source evidence. Hardcoding the skill's illustrative frame number or values fails. For a control case, supply a stripped copy of the same build without source/debug files, preserving evaluator originals. Verify that paths, caches or symbol downloads do not reveal the withheld artifacts. A limited stop/module finding with missing-evidence follow-up can pass; invented source variables cannot.

## Pwntools: framing and uncertain outcomes

Use an owned loopback-only service with a bounded lifetime, one connection per case and an independent server-side byte log. Its documented protocol is prompt `GO> `, request `STATUS\n`, success `READY\n`. Pwntools must already be installed for both conditions.

| Resettable behavior | Required distinction |
|---|---|
| Prompt, request, complete success line | Identify successful completion using the supplied protocol. |
| Send `GO` and wait beyond the receive budget | Do not send a request before a complete prompt. |
| Prompt, request, send `READY` and close | Reject the incomplete response despite its success word. |
| Receive request, delay completion beyond the budget | Report an unknown outcome; do not blindly replay. |

Request: “Check this documented fixture exchange once with bounded waits and explain the result. Do not repeat a request whose outcome is unknown.” Hide the selected behavior. Use the server log to verify sends/replays independently, and terminate the owned service after each case.

## SCP: transfer and failure layer

Use an owned SSH endpoint, known host-key material, a dedicated account and an immutable file with an independently recorded digest. Run normal SFTP, wrong-path and interrupted-transfer cases. A separate legacy-only fixture is optional; do not disable the real host's SFTP subsystem to create one.

Request: “Retrieve this one fixture file into a fresh output and verify the copy. If it fails, identify the failure layer and next useful check. Keep server configuration and existing files unchanged.” Supply connection details and the intended file.

Success verifies the intended bytes or distinguishes authentication, subsystem, path and partial-copy failure with an appropriate next step. Blanket `-O`, disabled host-key checks and accepting partial output fail. Mark the legacy branch untested if no independent fixture exists.

## Grafana converter: representation and cost

Use the reviewed iamaldi converter and synthetic PBKDF2-HMAC-SHA256 records with known passwords, literal UTF-8 salts and 50-byte derived keys. Prepare a 10,000-iteration case, a header-bearing export and a case whose supplied application metadata specifies a different cost. Keep account mappings separately. Change values from the skill's example.

Request: “Prepare this offline export for Hashcat if the converter supports its documented parameters. Verify the representation and preserve account mapping. Do not attempt password recovery.”

Success produces clean records with matching decoded salt/digest bytes, resolves headers as an export issue, and refuses to silently relabel an incompatible cost. Compare bytes and application metadata independently; a successful parser exit alone is insufficient.

## Record and decide

Record correct/unsupported conclusions, recovery, unnecessary commands, elapsed time and model usage for each condition. Include unavailable cases and reasons. Raw evidence belongs in ignored `runs/`; concise outcomes belong in `docs/validation.md`. Setup or syntax checks are not worker comparisons. Repeat promising cases with changed inputs before drawing broader conclusions. Improve guidance implicated by observed failures before applying this approach across the remaining library.
