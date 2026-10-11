---
name: go
description: Build reviewed Go CLI projects and inspect Go binary evidence. Use when module imports, generated bindings, subprocess calls, randomness assumptions or unchecked errors undermine a reproducible result.
---

# Go build and binary evidence

Read this entire skill before acting; complete current context need not be re-read. Select a reviewed source build or static inspection of an owned binary. Before building, establish the module, required toolchain and dependency inputs below. For embedded metadata, decompiler output, random-number APIs or decoder evidence, read [static binary evidence](references/static-binary-evidence.md) fully; it is conditional on that task. Complete with the build exit status, output identity and toolchain, or the static findings and remaining evidence gaps. A build result does not establish execution.

## Establish the module before building

Work in the intended source checkout. Read `go.mod`, `go.sum` and any selected `go.work`, including `replace` directives and local dependencies. On toolchains supporting automatic selection, inspect without permitting an automatic toolchain download:

~~~bash
GOTOOLCHAIN=local go version
GOTOOLCHAIN=local go env GOMOD GOWORK GOOS GOARCH CGO_ENABLED GOPROXY GOTOOLCHAIN
~~~

The normal `GOTOOLCHAIN=auto` behavior can select/download a newer compiler required by the module/workspace. A too-old local toolchain is a diagnosed prerequisite, not a reason to rewrite the project's `go` directive. A parent workspace can alter dependency selection; use `GOWORK=off` only when intentionally building the module independently.

The command is `go mod tidy`, not `go.mod tidy`. Tidy reconciles dependencies across the module, adds/removes requirements and checksums, and can download modules. It is a source change, not merely an installation step. Inspect its diff when it is actually needed. `go mod download` fetches dependencies; `go build` may also fetch missing modules.

For a reviewed single-command module with the required toolchain available, define `binary` as a fresh absolute output path:

~~~bash
GOTOOLCHAIN=local go build -mod=readonly -o "$binary" .
~~~

`.` builds the package, including applicable files. Building only `main.go` can omit companion files. `-mod=readonly` prevents required `go.mod` edits; it is not an offline switch or a no-write guarantee for caches/checksums. If the project deliberately uses vendored dependencies, preserve that mode with `-mod=vendor` instead of overriding it. Inspect `GOOS`/`GOARCH`, build tags and cgo/compiler requirements on executable-format or linking errors.

Compilation does not run the resulting CLI, but `go run` does. `go generate` explicitly runs source-defined commands and is not an automatic build prerequisite. Run the built tool only after reviewing its actual options/defaults; a program named `squidscan` can start a full scan without arguments, so even an assumed `--help` invocation is unsafe if its source never parses options.

A scanner can hardcode its proxy, target loopback, worker count and port range. A successful build establishes only a build result, not correct target selection or reliable open-port classification. Record source revision, toolchain, dependency changes and output identity separately from any later network test.

## Resolve generated imports within the project

When generated bindings import a bare package name, inspect the module declaration and the generated package's actual directory/import path. A package name is not automatically its module import path. Keep generated source under the project, or use an intentional local module/workspace dependency with its own module metadata. Do not move application packages into `GOROOT/src` to imitate an old walkthrough. Review generator package-prefix settings before regenerating; tidy cannot infer the intended local package from an unrelated path.

## Trace whether a constructed command actually runs

While reading source, distinguish `exec.Command(name, args...)` from methods that launch it: `Run`, `Start`, `Output` and `CombinedOutput`. Command construction alone starts nothing; `Start` also needs `Wait` to establish completion. `exec.Command{...}` is not a valid call to the standard-library function, so a rendered snippet containing that syntax does not establish executable source.

Go's exec package does not normally invoke a shell. An explicit `/bin/sh -c` changes that: the command string is parsed by the shell. Trace any untrusted value into that string and then to the actual launch method. Formatting a value inside quoted shell text is not equivalent to passing it as a separate argument. For a logging operation, writing the data through Go file APIs avoids introducing a shell solely for echo/redirection.

Check earlier and later effects independently. `os.Create` truncates an existing file before later processing. A scanner loop can stop on an error as well as EOF; inspect `scanner.Err()`. Also inspect subprocess errors and exit handling before treating a returned text such as **illustrative** `Log file processed` as proof that every line or command succeeded. The server's working directory controls relative output paths, not the remote client's directory.

See [os/exec](https://pkg.go.dev/os/exec), [os.Create](https://pkg.go.dev/os#Create), [Scanner.Err](https://pkg.go.dev/bufio#Scanner.Err), [modules](https://go.dev/ref/mod), the [Go command reference](https://go.dev/cmd/go/) and [toolchain selection](https://go.dev/doc/toolchain).
