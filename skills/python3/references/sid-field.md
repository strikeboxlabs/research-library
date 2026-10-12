# Decode one acquired binary SID field

Require a trusted Python3 interpreter and one complete raw AD objectSid value in a local ordinary file. Extract/unfold/decode its LDIF base64 field first, retaining the DN and account association; a grep of all objectSid lines loses that association. Define `sid_file` as the selected absolute file and `python_bin` as the trusted interpreter:

~~~bash
"$python_bin" -I -S - "$sid_file" <<'PY'
import sys

with open(sys.argv[1], 'rb') as source:
    data = source.read(69)
if len(data) < 8 or len(data) > 68:
    sys.exit('invalid SID size')
revision, count = data[:2]
if revision != 1 or not 1 <= count <= 15:
    sys.exit('unsupported SID revision/count')
if len(data) != 8 + 4 * count:
    sys.exit('SID count/length mismatch')
authority = int.from_bytes(data[2:8], 'big')
authority_text = (str(authority) if authority <= 0xffffffff
                  else f'0x{authority:012x}')
subauthorities = [int.from_bytes(data[i:i+4], 'little')
                  for i in range(8, len(data), 4)]
print('-'.join(['S', str(revision), authority_text]
               + [str(value) for value in subauthorities]))
PY
status=$?
~~~

This checks the revision, declared variable count and exact byte length before interpretation. It handles the six-byte authority separately from little-endian 32-bit subauthorities; it does not reverse the whole buffer or assume a fixed number of account fields. Truncated input, extra bytes and unsupported headers produce no SID result. Format validity does not authenticate the acquired data or identify its account.

For an established AD domain account, its final subauthority is the account RID. Do not remove the last component from every arbitrary SID to invent a domain SID. Query the actual domain object's objectSid, or correlate the account prefix with independent domain evidence. A host name, similar CN or nearby display line does not establish that association.

References: [SID structure and count](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/f992ad60-0fe4-4b87-9fed-beb478836861), [SID/account relationship](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/78eb9013-1c3a-4970-ad1f-2b1dad588a25), [decimal/hexadecimal string authority](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/c92a27b1-c772-4fa7-a432-15df5f1b66a1), and [.NET binary interpretation](https://source.dot.net/System.Security.Principal.Windows/System/Security/Principal/SID.cs.html).
