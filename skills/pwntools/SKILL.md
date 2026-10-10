---
name: pwntools
description: Use pwntools for framed process/TCP exchanges, cyclic offsets and exact integer-to-byte reconstruction. Diagnose timeout, EOF, width and byte-order mistakes.
---

# Pwntools protocol exchanges and bytes

Read this entire SKILL.md before acting. For an exchange, establish the endpoint, framing and complete-response condition; for cyclic lookup or packing, establish the generating parameters or actual field layout first. Finish with the verified response, offset or exact bytes and length; timeout, missing layout or partial output remains unresolved.

Use Python 3 and the installed pwntools environment. A local `process` launches the supplied program; `remote` connects to the selected endpoint. Choose from the actual task, rather than turning a failed connection into a different execution mode. Set explicit timeouts and keep binary protocol data as `bytes`.

For a line-oriented protocol, wait for the exact prompt before sending, then require a positively identified complete response. Adapt this function with `request`, a nonempty `prompt`, and a newline-terminated `success_line`, all as bytes. The host/port must identify the intended service:

~~~python
from pwn import remote

def exchange(host, port, request, prompt, success_line):
    tube = remote(host, port, timeout=5)
    try:
        banner = tube.recvuntil(prompt, timeout=5)
        if not banner.endswith(prompt):
            raise TimeoutError("Expected prompt was not received")
        tube.sendline(request)
        reply = tube.recvline(timeout=5)
        if not reply:
            raise TimeoutError("No complete response line")
        if not reply.endswith(b"\n"):
            raise RuntimeError("Incomplete response at EOF")
        if reply != success_line:
            raise RuntimeError("Unexpected protocol response")
        return reply
    finally:
        tube.close()
~~~

For an owned fixture that prompts with `READY> ` and answers `PING` with `OK\n`, call `exchange(host, port, b"PING", b"READY> ", b"OK\n")`. These are **illustrative protocol values**, not commands to send to an arbitrary service. Interpret the exchange as follows:

| Observation | Meaning and next action |
|---|---|
| Complete prompt, then `b"OK\n"` | The defined exchange completed. Continue to the next documented protocol state. |
| `recvuntil` returns `b""` | The prompt was not completed before timeout; partial bytes remain buffered. Check the expected delimiter, endpoint and service state. The function stops before sending. |
| Response read returns `b""` | No complete line before timeout. The request was already sent; its effect is unknown. Check state before reconnecting/replaying a mutating request. |
| `b"OK"` followed by EOF | With default incomplete-line behavior, `recvline` returns that fragment. Reject it as incomplete, even though it contains the success word. |
| `EOFError` or complete `b"ERR\n"` | Transport closure and an application response are different outcomes. Preserve that distinction and inspect the protocol stage; neither establishes success. |

The function closes on every completed/failed exchange. If a protocol requires an ongoing session, keep one tube open and perform the same framing checks at each state rather than reconnecting after each line. For multiline replies, consume their documented completion marker; absence of a rejection phrase is insufficient.

`sendline` appends the tube's newline; use `send` for exact bytes and `recvn` for a known byte count. `sendlineafter` combines receive and send, so it can send after the receive times out; use an explicit checked receive when synchronization matters. Avoid arbitrary sleeps and unrestricted `interactive()` in unattended jobs.

For controlled offset measurement, `cyclic(length, n=4)` and `cyclic_find(observed_bytes, n=4)` must share alphabet and subsequence width. Supply captured bytes in memory order; integer lookup depends on endianness. Default pwntools cyclic patterns differ from Metasploit patterns. A match locates input bytes, not proof of instruction-pointer control. Record the generating parameters, transport framing, exact observation and termination condition.

## Reconstruct integer fields with known byte order

Use the artifact's architecture and actual field offsets/widths, not the apparent order of hexadecimal digits in a decompiler. For **illustrative** adjacent unsigned little-endian fields of eight and seven bytes:

~~~python
from pwn import pack

data = pack(0x4847464544434241, word_size=64, endianness="little", sign=False)
data += pack(0x4f4e4d4c4b4a49, word_size=56, endianness="little", sign=False)
print(len(data), data)
~~~

The illustrative result is `15 b'ABCDEFGHIJKLMNO'`. `p64` always packs eight bytes; a seven-byte field needs its actual width. Explicit arguments avoid inherited context defaults. Confirm adjacency and any padding before concatenating fields, then compare length and bytes with the artifact. Keep bytes until a text encoding is established. Blindly removing the last byte or stripping NULs may discard real data; a terminator is a property of the format, not of integer packing. Consult [packing semantics](https://docs.pwntools.com/en/stable/util/packing.html) for width, signedness and out-of-range errors.

Consult [tube behavior](https://docs.pwntools.com/en/stable/tubes.html) for timeout/EOF configuration and [cyclic patterns](https://docs.pwntools.com/en/stable/util/cyclic.html) when matching a generator to a lookup.
