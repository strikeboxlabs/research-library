# Validation record

Prepared on 2026-10-31 on Windows. Python controller tests, mock-provider tests, fixture/grader calibration and source checks are distinct from actual Linux/Pi/GLM task trials.

This host has Python 3.15.2. Docker is not on PATH and WSL is not installed. No package installation, Docker build, remote Linux connection or real model request was performed. The supported controller target is Python 3.10+; exact target-version execution remains part of Linux acceptance.

The test runner exercises seeded fixture creation, independent graders, invalid outputs, bounded path handling, randomized paired plans, snapshots/resume, usage accounting, proposal restrictions, event parsing and process supervision. API calls and Docker are mocked in controller/runtime tests. Owned Python subprocess tests verify timeout and output capture mechanics. Reference command integration tests run only on Linux with their required tools and otherwise skip explicitly.

Run these checks after copying the checkout to Linux:

```bash
python3 -B test-suite/test.py
python3 -B test-suite/bench.py doctor --config test-suite/config.local.json
python3 -B test-suite/bench.py calibrate --output runs/skillbench-calibration-linux
python3 -B test-suite/bench.py smoke --config test-suite/config.local.json --output runs/skillbench-smoke-linux
```

Inspect skips instead of treating the test process's exit code as complete coverage. Symlink tests require actual filesystem support. The smoke result must pass before using the corresponding case for a model comparison. The first real-model acceptance check should be a single baseline/current pair; inspect raw finalized events, the observed model identity, exact output artifacts and nonzero token accounting.

Actual local check counts and outcomes are recorded in the repository's [validation record](../docs/validation.md). Future run artifacts remain in ignored `runs/`; this file is not evidence of a Linux or model pass.
