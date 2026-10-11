"""Decode exactly the 16 decimal IPv6 address octets of an acquired SNMP index."""
import ipaddress
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: decode_ipv6_index.py OCTET.OCTET... (exactly 16 octets)')
fields = sys.argv[1].split('.')
if len(fields) != 16 or any(not re.fullmatch(r'[0-9]{1,3}', f) for f in fields):
    raise SystemExit('expected exactly 16 decimal octets, without OID/type/length/value')
numbers = [int(f, 10) for f in fields]
if any(n > 255 for n in numbers):
    raise SystemExit('octets must be in 0..255')
address = ipaddress.IPv6Address(bytes(numbers))
print(address.compressed)
print('loopback=' + str(address.is_loopback))
print('link_local=' + str(address in ipaddress.IPv6Network('fe80::/10')))
print('unique_local=' + str(address in ipaddress.IPv6Network('fc00::/7')))
