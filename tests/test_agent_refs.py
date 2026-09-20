import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from lint_agent_refs import lint
from lint_banned_terms import banned_terms

REPO = Path(__file__).resolve().parent.parent


class AgentRefs(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "agents", self.tmp / "agents")
        shutil.copytree(REPO / "skills", self.tmp / "skills")
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_repo_is_clean(self):
        self.assertEqual(lint(REPO), [])

    def test_repo_has_no_cursor_cloud_or_model_config_references(self):
        self.assertEqual(banned_terms(REPO), [])

    def test_banned_terms_are_reported_with_file_and_line(self):
        (self.tmp / "skills/how/SKILL.md").write_text("ok\nspawn on grok-4.6-fast-xhigh\n")
        self.assertIn("skills/how/SKILL.md:2 mentions 'grok'", banned_terms(self.tmp))

    def test_precursor_and_pagination_cursor_are_not_reported(self):
        clean = self.tmp / "clean"
        clean.mkdir()
        (clean / "note.md").write_text("a precursor to the change, origin of the bug\n")
        self.assertEqual(banned_terms(clean), [])

    def test_unknown_agent_is_reported(self):
        (self.tmp / "skills/how/SKILL.md").write_text("subagent_type: ghost\n")
        self.assertIn("skills/how/SKILL.md references unknown agent 'ghost'", lint(self.tmp))

    def test_legacy_explore_agent_is_reported(self):
        (self.tmp / "skills/zoom-in/SKILL.md").write_text("Invoke with `agentName=Explore`.\n")
        self.assertIn("skills/zoom-in/SKILL.md references unknown agent 'Explore'", lint(self.tmp))

    def test_display_name_of_comment_sicko_is_reported(self):
        (self.tmp / "skills/no-comments/SKILL.md").write_text('subagent_type: "Comment"\n')
        self.assertIn("skills/no-comments/SKILL.md references unknown agent 'Comment'", lint(self.tmp))

    def test_generalpurpose_camelcase_is_reported(self):
        (self.tmp / "skills/why/SKILL.md").write_text("subagent_type: generalPurpose\n")
        self.assertIn("skills/why/SKILL.md references unknown agent 'generalPurpose'", lint(self.tmp))

    def test_general_purpose_resolves_to_repo_agent(self):
        (self.tmp / "skills/why/SKILL.md").write_text("subagent_type: general-purpose\n")
        self.assertEqual(lint(self.tmp), [])

    def test_removing_general_purpose_agent_is_reported(self):
        (self.tmp / "agents/general-purpose.md").unlink()
        self.assertIn("skills/how/SKILL.md references unknown agent 'general-purpose'", lint(self.tmp))

    def test_backticked_subagent_type_form_is_checked(self):
        (self.tmp / "skills/how/SKILL.md").write_text("- `subagent_type`: `ghost`\n")
        self.assertIn("skills/how/SKILL.md references unknown agent 'ghost'", lint(self.tmp))

    def test_agent_without_model_pin_is_reported(self):
        f = self.tmp / "agents/reviewer.md"
        f.write_text(f.read_text().replace("model: claude-sonnet-5\n", ""))
        self.assertIn("agents/reviewer.md must set model: claude-sonnet-5", lint(self.tmp))

    def test_agent_with_wrong_effort_is_reported(self):
        f = self.tmp / "agents/explorer.md"
        f.write_text(f.read_text().replace("effort: medium", "effort: max"))
        self.assertIn("agents/explorer.md must set effort: medium", lint(self.tmp))

    def test_spawn_time_model_override_is_reported(self):
        (self.tmp / "skills/how/SKILL.md").write_text("- `model`: grok\n")
        self.assertIn("skills/how/SKILL.md passes model at spawn, overriding the agent pin", lint(self.tmp))

    def test_install_writes_only_under_dot_claude(self):
        home = self.tmp / "home"
        home.mkdir()
        subprocess.run([str(REPO / "install.sh")], env={**os.environ, "HOME": str(home)}, check=True, capture_output=True)
        self.assertEqual(sorted(p.name for p in home.iterdir()), [".claude"])
        self.assertEqual(sorted(p.name for p in (home / ".claude").iterdir()), ["agents", "skills"])
        self.assertTrue((home / ".claude/agents/explorer.md").exists())
        self.assertTrue((home / ".claude/skills/how/SKILL.md").exists())
        self.assertIn("model: claude-sonnet-5", (home / ".claude/agents/explorer.md").read_text())

    def test_install_skips_existing_without_force(self):
        home = self.tmp / "home"
        (home / ".claude/agents").mkdir(parents=True)
        (home / ".claude/agents/explorer.md").write_text("mine")
        run = lambda *a: subprocess.run([str(REPO / "install.sh"), *a], env={**os.environ, "HOME": str(home)}, check=True, capture_output=True, text=True).stdout
        self.assertIn("skip (exists): explorer.md", run())
        self.assertEqual((home / ".claude/agents/explorer.md").read_text(), "mine")
        run("--force")
        self.assertIn("effort: medium", (home / ".claude/agents/explorer.md").read_text())


if __name__ == "__main__":
    unittest.main()
