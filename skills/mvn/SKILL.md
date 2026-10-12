---
name: mvn
description: Package a selected trusted Maven project with the required JDK and distinguish reactor failures, stale artifacts, assembly output and build success from runtime success.
---

# Package the selected Java project

Read this entire SKILL.md before acting. Require a trusted reviewed checkout, its requested build outcome, compatible JDK/Maven and approved dependency access. Review the POM, parent/modules, active profiles, project Maven configuration and plugin executions before building: a build executes project-controlled code. Finish with the final build status and exact resulting artifact, or the first unresolved failure.

Define `project` as the selected checkout's absolute path. From that project:

~~~bash
cd "$project" || exit
mvn --version
java -version
mvn package
status=$?
~~~

Check the JDK Maven reports, which can differ from the standalone java on PATH. `package` runs the configured lifecycle through packaging, including earlier phases and tests unless the project skips them. It does not imply that integration checks normally bound to `verify` ran. Capture the final status and reactor summary rather than accepting an early module success.

Find the artifact from the reviewed POM and actual build log. A project's assembly plugin can write an executable JAR with dependencies to a parent directory, while ordinary JAR packaging need not bundle dependencies or supply a Main-Class. Neither a guessed release filename nor any existing target file proves the latest build succeeded. Verify the exact output's path, size, modification/content identity and build relationship; do not select the first wildcard match or invoke a stale JAR after a failed build.

A dependency-version property in a partial POM is a declared value, not proof of the resolved dependency or deployed application. Follow the property into the actual dependency, parent/profile overrides and packaged artifact before attributing a library version. Compiler source/target17 also does not identify the running JVM. A downloadable build/container template remains separate from the selected deployed instance.

| Failure | Next decision |
|---|---|
| Missing POM | Confirm the selected checkout and reactor root. |
| Dependencies cannot resolve | Inspect the selected repository, network/proxy and Maven settings; retain the actual failure. |
| Unsupported compiler release or Java class version | Reconcile the project's documented JDK with Maven's JDK and the intended runtime. |
| Tests or one reactor module fail | Report that failure and any partial artifacts; do not skip tests merely to produce a success banner. |

`clean` deletes configured build outputs; use it only when removing those known artifacts is intended. `install` additionally places artifacts in the local Maven repository, while `deploy` can publish them remotely. Choose the phase matching the task rather than promoting a packaging request to publication.

An artifact and BUILD SUCCESS establish the configured build result, not application behavior or a network service outcome. Loading a JAR executes code; choose its subsequent local or service action from the separately approved task and project documentation.

References: [Maven lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html), [standard directory layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html).
