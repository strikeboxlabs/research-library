---
name: cargo
description: Build and run a selected existing Rust CLI with Cargo, controlling manifest, binary, profile and dependency resolution. Use when a tool ships as a Cargo project and build success, execution and output claims need separation.
---

# Build the intended package and binary

Read this entire file before acting. Identify the reviewed project and intended binary before building. Finish with the manifest, profile, toolchain and build artifact or actual run result; compiling a tool does not validate what its algorithm claims.

Define `manifest` as the absolute `Cargo.toml` path and `binary` as its declared binary target. For a release build using the existing lockfile:

~~~bash
cargo build --manifest-path "$manifest" --locked --release --bin "$binary"
~~~

This selects the project explicitly instead of finding an unintended parent manifest. A workspace may also need `-p PACKAGE` to select the package. `--release` chooses an optimized profile; it does not mean a historical performance claim applies to this host/input. Build warnings are not necessarily failures, but a produced executable still needs the task's functional check.

`--locked` rejects missing or changed dependency resolution; it is not offline mode. `--frozen` combines locked resolution with no network, and can fail when required dependencies are absent locally. Resolve that as a provisioning decision rather than silently changing dependencies. A selected target triple also needs its compiler/linker and runtime support; a successful host build is not cross-platform validation.

Cargo builds can execute project/dependency build scripts and compiler-time procedural code. Review the actual project and use the intended build environment; `cargo check` is not a promise of zero code execution. Do not run an unknown project as root to solve a cache-permission error.

When the task separately authorizes executing the tool, `cargo run` can rebuild and then launch it. Arguments after `--` go to the program:

~~~bash
cargo run --manifest-path "$manifest" --locked --release --bin "$binary" -- --help
~~~

Even `--help` executes that program, whose implementation determines the effect. For a real operation, replace it with the reviewed tool arguments and evaluate the actual output against known inputs. A recovered candidate, timing line or successful process exit is not proof of correctness without the corresponding check.

See [Cargo build](https://doc.rust-lang.org/cargo/commands/cargo-build.html), [run](https://doc.rust-lang.org/cargo/commands/cargo-run.html) and [build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html).
