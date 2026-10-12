# Interpret CPython2.7 references in native code

Require the selected acquired extension/source identity, architecture and matching CPython ABI. Read native code without importing the specimen; importing a shared extension executes its initialization. A decompiler's generic integer/pointer types and generated local names need confirmation from actual instructions and API signatures.

For a reviewed installed CPython2.7 interpreter `python2_bin`, this isolated observation uses only the standard library and a new local list:

~~~bash
"$python2_bin" -c 'import sys; print(sys.version); a = ["sample"]; print(sys.getrefcount(a)); b = a; print(sys.getrefcount(a)); del b; print(sys.getrefcount(a))'
~~~

The call itself temporarily holds a reference. `b = a` aliases the **list**, not its contained string; deleting b removes that binding while a still retains the list. Compare the observed changes rather than imposing a universal absolute count on a different environment. This observation does not establish the lifetime or heap layout of an extension's objects. See [CPython2.7 getrefcount](https://github.com/python/cpython/blob/v2.7.18/Doc/library/sys.rst).

For the selected native function, trace each API result, owner and control-flow exit using its matching contract. New references carry a release responsibility; borrowed references require a live owner, and a stealing API transfers responsibility. In CPython2.7, `PyObject_GetAttrString` returns a new reference while `PyList_GetItem` returns a borrowed item; the same item obtained through `PySequence_GetItem` carries a new reference instead. Track the container and returned item separately. API failure paths must preserve their actual NULL/-1 checks and exceptions. See [C API ownership](https://github.com/python/cpython/blob/v2.7.18/Doc/c-api/intro.rst) and [list API](https://github.com/python/cpython/blob/v2.7.18/Doc/c-api/list.rst).

An observed decrement followed by a zero-count branch to a type deallocator can be reconstructed `Py_DECREF`; it is not evidence that every raw pointer remains valid afterward. The type's deallocator runs when the count reaches zero; cyclic garbage collection is a separate mechanism. Deallocation can invoke Python code, so account for the state of containers and references across those calls. A missing increment or apparent extra decrement is an ownership finding to reconcile against every path, not proof of a particular allocator reuse or exploit outcome. See [reference-count operations](https://github.com/python/cpython/blob/v2.7.18/Doc/c-api/refcounting.rst).

Finish with the selected function/call addresses, confirmed API contracts, ownership balance on relevant paths and unresolved type/alias/caller facts. Source adjacency and allocation order alone do not prove physical heap adjacency or that a later object occupies an earlier slot. A generic Python demonstration cannot validate a native extension's runtime behavior.
