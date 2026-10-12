---
name: lxc
description: Import a reviewed LXD image archive and verify its identity in a selected image store with lxc. Use when archive layout, aliases, project or remote context obscures the imported image.
---

# Import the selected LXD image

Read this entire SKILL.md before acting. Require a trusted image artifact, an already configured owned LXD server and its intended project. Check the destination before importing; finish with the returned full fingerprint and image metadata in that same store. Importing an image does not start an instance.

This is LXD's `lxc` client, rather than the separate `lxc-*` tools of liblxc. Check `lxc --version`, `lxc image import --help` and the selected client configuration. Define `remote` as the exact configured owned server name, `project` as its intended existing project, `image_archive` as a reviewed unified LXD image file and `image_alias` as a fresh alias:

~~~bash
lxc remote list
lxc image list "$remote:" --project "$project"
lxc image import "$image_archive" "$remote:" --alias "$image_alias" --project "$project"
~~~

Check import status before reading back the image. A generic root-filesystem tarball is not necessarily a LXD image. A split image instead requires its matching metadata and rootfs files, in that order; do not replace missing metadata with an arbitrary archive. Keep source artifact hashes and producer provenance separately from a descriptive filename.

~~~bash
lxc image info "$remote:$image_alias" --project "$project"
lxc image list "$remote:" --project "$project"
~~~

Retain the full fingerprint, architecture, image type and alias association. An alias can later refer to different bytes, and a shortened list fingerprint is not the complete identity. No rows may mean the wrong remote/project, an applied filter or a failed request; distinguish those before concluding absence. An image listing neither verifies guest execution nor establishes the installed host's architecture. Do not rerun import blindly after an ambiguous interruption; inspect that exact destination first.

See Canonical's [import formats](https://canonical.com/lxd/docs/latest/howto/images_copy/), [import option contract](https://canonical.com/lxd/docs/latest/reference/manpages/lxc/image/import/) and [image information](https://canonical.com/lxd/docs/latest/howto/images_manage/).
