import importlib.util
from pathlib import Path
import shutil
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

    def test_runtime_cannot_depend_on_another_installed_skill(self):
        other = self.root / "skills" / "other"
        self.write(other / "SKILL.md", "---\nname: other\ndescription: Another tool.\n---\n")
        self.write(self.skill / "reference.md", "[other skill](../other/SKILL.md)\n")
        report = CHECKER.check_repository(self.root)
        self.assertEqual(report["skills_checked"], 2)
        self.assertTrue(any("Runtime link escapes skill" in error for error in report["errors"]))

    def test_each_skill_folder_needs_its_own_entrypoint(self):
        self.write(self.root / "skills" / "orphan" / "guide.md", "A guide without discovery metadata.\n")
        self.assertTrue(any("Skill folder has no SKILL.md" in error for error in CHECKER.check_repository(self.root)["errors"]))

    def test_source_ids_in_skill_local_provenance(self):
        provenance = self.skill / "references" / "provenance.md"
        self.write(provenance, "- S1: A source.\n\nClaim supported by S2.\n")
        self.assertTrue(any("Undefined source IDs" in error for error in CHECKER.check_repository(self.root)["errors"]))
        self.write(provenance, "- S1: A source.\n\nClaim supported by S1.\n")
        self.assertEqual(CHECKER.check_repository(self.root)["errors"], [])

    def test_template_links_are_checked_after_materialising(self):
        template = self.root / "authoring" / "skill.template.md"
        self.write(template, "[provenance](references/provenance.md)\n")
        report = CHECKER.check_repository(self.root)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["template_links_deferred"], 1)
        self.write(self.skill / "guide.md", template.read_text(encoding="utf-8"))
        self.assertTrue(any("Missing link" in error for error in CHECKER.check_repository(self.root)["errors"]))

    def test_published_skills_pass_when_copied_without_the_repository(self):
        published = sorted((SCRIPT.parents[1] / "skills").glob("*/SKILL.md"))
        self.assertTrue(published, "At least one independently installable skill must exist")
        for entrypoint in published:
            with self.subTest(skill=entrypoint.parent.name):
                isolated = self.root / "isolated" / entrypoint.parent.name
                shutil.copytree(entrypoint.parent, isolated / "skills" / entrypoint.parent.name)
                report = CHECKER.check_repository(isolated)
                self.assertEqual(report["skills_checked"], 1)
                self.assertEqual(report["errors"], [])

    def test_unresolved_runtime_template_is_reported(self):
        self.write(self.skill / "reference.md", "Use {{tool}}.\n")
        self.assertTrue(any("Unfinished runtime placeholder" in error for error in CHECKER.check_repository(self.root)["errors"]))

    def test_unclosed_fence_is_reported(self):
        self.write(self.root / "README.md", "~~~bash\nprintf 'example'\n")
        self.assertTrue(any("Unclosed code fence" in error for error in CHECKER.check_repository(self.root)["errors"]))


if __name__ == "__main__":
    unittest.main()
