---
name: dotnet
description: Select a .NET SDK/runtime and build or run a reviewed Linux project with explicit restore and launch behavior. Use when a DLL, project, target framework or inherited build settings causes confusing execution failures.
---

# Separate inspection, build and execution

Inspect the environment from the intended working directory:

~~~bash
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
~~~

A runtime can run a compatible compiled application but does not provide the SDK needed to build a project. `global.json` can select an SDK based on the working directory and its ancestors; the selected SDK version is distinct from the project's `TargetFramework`. Preserve a recovered project's framework before considering migration. Do not install an obsolete runtime merely because a historical writeup used it.

Distinguish modern .NET targets from **.NET Framework 4.x**. A project targeting `net48` or declaring `<TargetFrameworkVersion>v4.8</TargetFrameworkVersion>` targets Windows .NET Framework; it is not the same runtime as `net8.0`. A Visual Studio retarget prompt changes project requirements, not just build configuration. Selecting Release does not resolve platform/API compatibility, and copying a Windows executable to Linux does not make it portable. Inspect framework, native dependencies and Windows APIs before choosing the build host or proposing a migration. See Microsoft's [runtime/platform distinction](https://learn.microsoft.com/en-us/dotnet/standard/choosing-core-framework-server).

Read the `.csproj`, imports, referenced projects and applicable `Directory.Build.props`/`.targets` before invoking build tools on unfamiliar material. MSBuild tasks, package build assets and compiler analyzers can execute during restore/build. Running an arbitrary project under privileged `dotnet` grants that build/application the same execution context. A build is not passive decompilation.

For a reviewed fixture, define `project` as its absolute `.csproj` path, `configuration` as the chosen configuration and `framework` as an actual target from the project. Restore dependencies explicitly with the intended NuGet configuration when needed; `dotnet restore "$project"` can contact feeds and change caches/`obj`. After successful restore:

~~~bash
dotnet build "$project" --no-restore --configuration "$configuration" --framework "$framework" &&
dotnet run --project "$project" --no-build --configuration "$configuration" --framework "$framework" --no-launch-profile
~~~

`--no-build` also suppresses implicit restore; it can run stale output if build inputs/options differ. `--no-launch-profile` avoids unexpected settings from `launchSettings.json`. Put application arguments after `--`. A successful build does not establish successful application startup, listening, authentication or task completion. Conversely, an executable left in `bin/` after a failed build may be stale or belong to a project that finished before another target failed. Retain the build status, failed target and artifact identity; its presence is not a successful rebuild or a reason to run it.

For an existing framework-dependent application, `dotnet "$application_dll"` launches the actual assembly; `dotnet run` selects a project. Define the DLL path and retain its matching `.runtimeconfig.json`, `.deps.json`, dependencies and content where supplied. Missing framework, wrong architecture, absent native library and incomplete deployment are different failure classes. Not every managed DLL has an application entrypoint.

A PE-labelled managed DLL can be portable; native dependencies and platform-specific APIs can still prevent Linux execution. Preserve stderr/exit status and verify the intended application's observable result before changing target frameworks or rebuilding.

Resolve SDK/build differences with [dotnet environment](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet), [build](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build), [run](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run), [SDK selection](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json), [MSBuild execution boundaries](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-security-best-practices), [deployment](https://learn.microsoft.com/en-us/dotnet/core/deploying/).
