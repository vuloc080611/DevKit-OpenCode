import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate  # noqa: E402


class ValidateScriptTests(unittest.TestCase):
    def test_strip_jsonc_preserves_urls_inside_strings(self) -> None:
        raw = """{
  // top comment
  "$schema": "https://opencode.ai/config.json",
  "note": "keep /* not a comment */ and // slashes" /* trailing */
}"""
        parsed = json.loads(validate.strip_jsonc_comments(raw))
        self.assertEqual(parsed["$schema"], "https://opencode.ai/config.json")
        self.assertEqual(parsed["note"], "keep /* not a comment */ and // slashes")

    def test_check_markdown_links_ignores_code_fences_and_flags_broken(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "real.md").write_text("# Real\n", encoding="utf-8")
            doc = root / "doc.md"
            doc.write_text(
                "[ok](real.md)\n```md\n[ignored](missing-inside-fence.md)\n```\n[bad](missing.md)\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            orig_root = validate.ROOT
            validate.ROOT = root
            try:
                validate.check_markdown_links(doc, errors)
            finally:
                validate.ROOT = orig_root

            self.assertEqual(len(errors), 1)
            self.assertIn("missing.md", errors[0])

    def test_validate_commands_requires_valid_skill_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cmd_dir = Path(tmp)
            (cmd_dir / "orphan.md").write_text(
                "---\ndescription: Broken command\nagent: plan\n---\n\nUse `nonexistent-skill`.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            validate.validate_commands(["grill-me"], errors, commands_dir=cmd_dir)
            self.assertEqual(len(errors), 1)
            self.assertIn("must reference at least one valid skill", errors[0])

    def test_repo_passes_full_validation(self) -> None:
        self.assertEqual(validate.main(), 0)


if __name__ == "__main__":
    unittest.main()
