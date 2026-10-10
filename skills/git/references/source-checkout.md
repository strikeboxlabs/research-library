# Acquire a selected upstream revision

Use this when the task calls for an upstream source checkout. Define `source_url` as the intended repository and `checkout` as a new owned path. To fetch objects before materializing the working tree:

~~~bash
git clone --no-checkout -- "$source_url" "$checkout"
git -C "$checkout" rev-parse HEAD
git -C "$checkout" remote get-url origin
~~~

Check clone status before interpreting the revision. A failed clone may leave a partial directory; do not reuse it as a complete source or delete an unrelated destination. The default branch can move between runs. Record the actual commit and remote identity; a matching repository name is not proof of a trusted publisher or reviewed code.

For a requested usable working tree, select `revision` from the intended reviewed commit/tag, inspect inherited Git configuration and checkout effects, then:

~~~bash
git -C "$checkout" checkout --detach "$revision"
git -C "$checkout" status --short
git -C "$checkout" rev-parse HEAD
~~~

Use this only in the new owned checkout; do not reset an existing working tree containing unrelated edits. Materializing files can involve configured filters, hooks and large-file handling. Submodules are separate repositories/URLs; fetching them is a separate intended step, not an automatic clone repair. Missing submodule content or a shallow/partial history needs to remain explicit.

A fetched/checked-out repository does not compile, install or run its program. Inspect the selected source/build instructions and existing runtime before those separately intended operations. Keep executable-source acquisition within the current task and endpoint protection rules; browser source review can suffice when a local checkout is unnecessary.

See [clone behavior](https://git-scm.com/docs/git-clone) and [checkout behavior](https://git-scm.com/docs/git-checkout).
