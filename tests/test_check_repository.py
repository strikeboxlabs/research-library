import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_repository.py"
SPEC = importlib.util.spec_from_file_location("check_repository", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="cli-repo-check-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skill = self.root / "skills" / "example"
        self.skill.mkdir(parents=True)
        self.write(self.skill / "SKILL.md", "---\nname: example\ndescription: Investigate an example.\n---\n\nRead the available references.\n")

    def write(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_valid_links_and_ignored_local_sources(self):
        self.write(self.root / "README.md", "[skill](skills/example/SKILL.md)\n")
        self.write(self.root / "work" / "raw.md", "[missing](absent.md)\n")
        report = CHECKER.check_repository(self.root)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["local_links_checked"], 1)

    def test_missing_target_is_reported(self):
        self.write(self.root / "README.md", "[missing](absent.md)\n")
        self.assertTrue(any("Missing link" in error for error in CHECKER.check_repository(self.root)["errors"]))

    def test_runtime_cannot_depend_on_authoring_files(self):
        self.write(self.root / "authoring.md", "Authoring only.\n")
        self.write(self.skill / "reference.md", "[outside](../../authoring.md)\n")
        self.assertTrue(any("Runtime link escapes skill" in error for error in CHECKER.check_repository(self.root)["errors"]))

    def test_unresolved_runtime_template_is_reported(self):
        self.write(self.skill / "reference.md", "Use {{tool}}.\n")
        self.assertTrue(any("Unfinished runtime placeholder" in error for error in CHECKER.check_repository(self.root)["errors"]))

    def test_unclosed_fence_is_reported(self):
        self.write(self.root / "README.md", "~~~bash\nprintf 'example'\n")
        self.assertTrue(any("Unclosed code fence" in error for error in CHECKER.check_repository(self.root)["errors"]))


if __name__ == "__main__":
    unittest.main()
