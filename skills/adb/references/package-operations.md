# Install the selected owned package

Require the intended authorized serial, one owned verified APK, manifest application ID, supported API/ABI and accepted signer. Device transport readiness is separate from installability. Keep the original APK and existing app/data state; a new signer can prevent an update to an installed package.

Define `serial` as the selected device, `apk` as the local APK and `package_id` as its actual application ID. Install a new package:

~~~bash
adb -s "$serial" install "$apk"
status=$?
~~~

Require the install result, then confirm that exact package with `adb -s "$serial" shell pm path "$package_id"`. A launch/test remains separate; the presence of an installed package does not prove its networking or application behavior. ABI, API, storage, signature and version errors need their particular diagnostic resolved. Do not use permission, downgrade or verification-bypass flags as a generic retry.

For an authorized same-package update, `install -r "$apk"` replaces the application while retaining its data, subject to signer/version compatibility. Rebuilding an archive does not recreate the original publisher's key. Uninstalling to evade a signer conflict discards the existing install/data state; use a dedicated owned test device/package when appropriate.

If uninstall is explicitly part of the selected task, use the **application ID**, not an APK filename:

~~~bash
adb -s "$serial" uninstall "$package_id"
status=$?
~~~

Without `-k` this removes package data/cache as well. `-k` requests data/cache retention, not a general backup. Record the result and verify the package's presence/absence on this serial. Removal of an absent/wrong ID does not establish removal of the intended app.

Reference: [ADB package commands](https://android.googlesource.com/platform/packages/modules/adb/+/refs/heads/main/docs/user/adb.1.md).
