---
name: az
description: Recover one selected Azure Storage blob with Azure CLI from an explicitly configured Azurite development endpoint. Use when cloud defaults, connection-string routing or partial downloads obscure a local emulator result.
---

# Recover a selected development blob

Read this entire SKILL.md before acting. Establish the development endpoint, known account/credential context and selected blob. Read [emulator recovery](references/emulator-recovery.md) fully before the procedure. Finish with actual endpoint, object identity, download status and verified bytes or a concrete prerequisite gap.

Check `az version` and the installed `az storage blob show --help` / `download --help`. This task uses an existing emulator and CLI; it does not install old containers or start services. A server release date does not by itself determine a compatible client version.
