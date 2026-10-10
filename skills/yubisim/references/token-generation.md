# Token input, counter state and validator behavior

Use only token material supplied for the selected authorized account/test. Establish that the verifier actually uses Yubico OTP, then identify its AES key, secret/private ID, public ID requirements and last accepted counter. These are not interchangeable with an SSH private key or an OATH seed. Keep a private baseline and a writable working token file; the simulator overwrites that working file after generation.

The original parser expects these five lines, exact labels/order, lowercase hex and platform-compatible line endings. This is an **illustrative template**, not usable token material:

~~~text
Yubisim Token 0.1
Public ID: <12 modhex characters>
Secret AES Key: <32 lowercase hex characters>
Secret ID: <12 lowercase hex characters>
Counter: <decimal state from 0 to 65535>
~~~

Replace every placeholder. Public ID uses `cbdefghijklnrtuv`; it is distinct from the encrypted secret ID. Do not copy a writeup's public ID unless the actual verifier ignores it. OpenBSD's documented backend checks the decrypted private ID, key/checksum and counter; another validator can also bind the public prefix. Mismatched key/ID cannot be repaired by a larger counter.

The source loads `Counter`, simulates insertion by incrementing it, then generates one button press and saves the updated counter. Thus a loaded state C produces a usage counter C+1, not C. A subsequent process run continues from the saved state. Do not wrap the counter or assume the parser's 16-bit range establishes every verifier's/hardware's usable range.

Define `java_bin`, `class_dir`, `token_file` and a fresh protected `otp_file` as in the entrypoint. If the existing build requires a compatible dependency classpath, define `simulator_classpath` as that complete classpath instead of `class_dir` (colon-separated on Linux):

~~~bash
umask 077
"$java_bin" -cp "$simulator_classpath" yubi_simulator "$token_file" > "$otp_file"
~~~

The intended output is one modhex OTP: this implementation uses a 12-character public prefix plus 32 encrypted characters. Validate format without echoing the token publicly. The source prints before saving, so output can exist even when persistence fails; require a zero exit and updated protected state before treating generation as complete. Parse errors, incompatible line endings, missing JAXB classes and unwritable files are different failure stages.

For a requested validator test, submit one fresh value through its intended existing input channel. A backend's successful acceptance may advance server state; blind retries or rolling back the local file can cause replay rejection. OpenBSD `login_yubikey` compares `(usage_counter << 8) | session_counter` to its stored decimal value, then saves the accepted value. Decode that representation instead of copying the entire stored integer into the simulator's usage field. **Illustrative:** stored 3841 encodes usage 15 and session 1; loading simulator state 15 produces usage 16, session 1, hence 4097 for this backend. Confirm the actual backend/version and current state first. Do not select an arbitrarily huge counter to force acceptance; it can invalidate later physical-token use. Coordinate test state or reprovisioning when that effect matters.

For SSH with an additional OTP factor, distinguish local key unlocking, accepted key with partial success and the required server challenge. Submit only to the intended factor prompt; generation does not prove the preceding key was accepted. A rejection needs backend logs/identity/state diagnosis, not repeated token generation. Report generation, persistence, factor acceptance and final session separately.

Sources for recovery: [simulator parser/state transitions](https://github.com/dorchain/yubisim/blob/master/yubi_simulator.java), [Yubico OTP fields](https://developers.yubico.com/OTP/OTPs_Explained.html), [OpenBSD validator](https://man.openbsd.org/login_yubikey.8) and [counter encoding](https://github.com/openbsd/src/blob/master/libexec/login_yubikey/login_yubikey.c).
