# Prepare a native-password verifier

Use mode `300` only when the producing account/plugin establishes the MySQL 4.1-style `mysql_native_password` format. This also occurs in MariaDB. A database product name or 40 hex characters alone is insufficient; other authentication plugins use different formats or external authentication. Keep the account's user **and host**, plugin, server version and acquired value associated.

A stored native-password verifier commonly has a leading `*` followed by 40 hexadecimal characters. The reviewed Hashcat mode-300 decoder expects exactly **40 hex characters**, without that storage `*`, SQL/HTML quoting, usernames or aggregation separators. Prepare a separate working file with one complete digest per line and retain the original account mapping. Remove only the verified storage wrapper; do not strip arbitrary characters until a malformed input loads. Reject truncated/empty values for this procedure.

Set `mode=300`, then use the entrypoint's bounded text-record run and matching potfile/`--show` procedure. The algorithm is SHA-1 of the **binary** SHA-1 digest of the password bytes. It differs from single SHA-1 (`100`) and from hashing the hexadecimal text of an inner digest. Establish password-byte encoding before independently checking a recovered candidate.

The upstream public self-test pairs the ASCII candidate `hashcat` with `fcf7c1b8749cf99d88e5f34271d636178fb5d130`. This is a format/reference pair, not an account credential. A candidate matching an acquired database verifier does not establish a Windows password or current database login; any cross-service reuse claim needs separate authorised evidence. Do not copy `--force` from a walkthrough to bypass backend failures.

Sources: [Hashcat mode-300 parser and self-test](https://github.com/hashcat/hashcat/blob/master/src/modules/module_00300.c), [double-SHA-1 kernel](https://github.com/hashcat/hashcat/blob/master/OpenCL/m00300_a0-pure.cl), [MariaDB native-password behavior](https://mariadb.com/docs/server/reference/plugins/authentication-plugins/authentication-plugin-mysql_native_password).
