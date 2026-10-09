---
name: go
description: Build reviewed Go CLI projects with explicit module, toolchain and target context. Use when dependency repair, go.mod edits, workspace selection or compile-versus-run confusion affects a reproducible tool build.
---

# Establish the module before building

Work in the intended source checkout. Read `go.mod`, `go.sum` and any selected `go.work`, including `replace` directives and local dependencies. On toolchains supporting automatic selection, inspect without permitting an automatic toolchain download:

~~~bash
GOTOOLCHAIN=local go version
GOTOOLCHAIN=local go env GOMOD GOWORK GOOS GOARCH CGO_ENABLED GOPROXY GOTOOLCHAIN
~~~

The normal `GOTOOLCHAIN=auto` behavior can select/download a newer compiler required by the module/workspace. A too-old local toolchain is a diagnosed prerequisite, not a reason to rewrite the project's `go` directive. A parent workspace can alter dependency selection; use `GOWORK=off` only when intentionally building the module independently.

The command is `go mod tidy`, not `go.mod tidy`. Tidy reconciles dependencies across the module, adds/removes requirements and checksums, and can download modules. It is a source change, not merely an installation step. Inspect its diff when it is actually needed. `go mod download` fetches dependencies; `go build` may also fetch missing modules.

For a reviewed single-command module with the required toolchain available, define `binary` as a fresh absolute output path:

~~~bash
go build -mod=readonly -o "$binary" .
~~~

`.` builds the package, including applicable files. Building only `main.go` can omit companion files. `-mod=readonly` prevents required `go.mod` edits; it is not an offline switch or a no-write guarantee for caches/checksums. If the project deliberately uses vendored dependencies, preserve that mode with `-mod=vendor` instead of overriding it. Inspect `GOOS`/`GOARCH`, build tags and cgo/compiler requirements on executable-format or linking errors.

Compilation does not run the resulting CLI, but `go run` does. `go generate` explicitly runs source-defined commands and is not an automatic build prerequisite. Run the built tool only after reviewing its actual options/defaults; a program named `squidscan` can start a full scan without arguments, so even an assumed `--help` invocation is unsafe if its source never parses options.

Bamboo's linked scanner hardcodes its proxy, target loopback, worker count and port range. A successful build establishes only a build result, not correct target selection or reliable open-port classification. Record source revision, toolchain, dependency changes and output identity separately from any later network test.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Bamboo pp. 2–3. Sources: [Go command reference](https://go.dev/cmd/go/), [modules](https://go.dev/ref/mod), [toolchain selection](https://go.dev/doc/toolchain), [reviewed scanner source](https://gist.githubusercontent.com/xct/597d48456214b15108b2817660fdee00/raw/f1fff423d457655b0740699acf4a61126804d16f/squidscan.go).
