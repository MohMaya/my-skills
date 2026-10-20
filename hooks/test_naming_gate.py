import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "naming_gate", Path(__file__).with_name("naming-gate.py")
)
assert spec and spec.loader
naming_gate = importlib.util.module_from_spec(spec)
sys.modules["naming_gate"] = naming_gate
spec.loader.exec_module(naming_gate)

SCRIPT = Path(__file__).with_name("naming-gate.py")
BAD = "data"
NOISE_TYPE = "User" + "Data"
VAGUE_FUNCTION = "process" + "Data"


def stripped(line: str, language: str = "ts") -> str:
    return naming_gate.strip(line, naming_gate.DIALECTS[language], None)[0]


class WordsTest(unittest.TestCase):
    def test_a_camel_name_splits_into_lowercase_words(self) -> None:
        self.assertEqual(naming_gate.words("retryDelayMs"), ["retry", "delay", "ms"])

    def test_an_initialism_stays_one_word(self) -> None:
        self.assertEqual(naming_gate.words("HTTPServer"), ["http", "server"])

    def test_a_snake_name_splits(self) -> None:
        self.assertEqual(naming_gate.words("process_data"), ["process", "data"])


class WhyTest(unittest.TestCase):
    def name(self, kind: str, text: str) -> naming_gate.Name:
        return naming_gate.Name(kind, text, 1)

    def test_a_vacuous_variable_is_rejected(self) -> None:
        self.assertIsNotNone(naming_gate.why(self.name("variable", BAD)))

    def test_a_name_containing_a_vacuous_word_is_fine(self) -> None:
        self.assertIsNone(naming_gate.why(self.name("variable", "metadata")))

    def test_a_type_with_a_noise_suffix_is_rejected(self) -> None:
        self.assertIsNotNone(naming_gate.why(self.name("type", NOISE_TYPE)))

    def test_a_vague_verb_with_a_generic_object_is_rejected(self) -> None:
        self.assertIsNotNone(naming_gate.why(self.name("function", VAGUE_FUNCTION)))

    def test_a_vague_verb_with_a_concrete_object_is_fine(self) -> None:
        self.assertIsNone(naming_gate.why(self.name("function", "handleClick")))

    def test_a_precise_role_is_fine(self) -> None:
        self.assertIsNone(naming_gate.why(self.name("variable", "unpaidInvoices")))


class StripTest(unittest.TestCase):
    def test_a_doc_comment_is_not_code(self) -> None:
        self.assertNotIn("const", stripped("/** const data = await fetch() */"))

    def test_a_line_comment_is_not_code(self) -> None:
        self.assertNotIn(BAD, stripped(f"// const {BAD} = compute()"))

    def test_a_string_body_is_not_code(self) -> None:
        self.assertNotIn(BAD, stripped('export const USAGE = "const data = 1"'))

    def test_a_block_comment_carries_across_lines(self) -> None:
        _, state, _ = naming_gate.strip("/* const data = 1", naming_gate.DIALECTS["ts"], None)
        self.assertIsNotNone(state)

    def test_an_escaped_quote_does_not_close_a_string(self) -> None:
        self.assertNotIn(BAD, stripped('const label = "say \\"data\\" now"'))

    def test_a_string_ending_in_an_escaped_backslash_is_closed(self) -> None:
        _, state, _ = naming_gate.strip(
            'const BACKSLASH = "\\\\";', naming_gate.DIALECTS["ts"], None
        )
        self.assertIsNone(state)

    def test_a_go_char_literal_does_not_open_a_string(self) -> None:
        _, state, _ = naming_gate.strip("quote := '\"'", naming_gate.DIALECTS["go"], None)
        self.assertIsNone(state)

    def test_a_rust_raw_string_is_one_construct(self) -> None:
        code, state, _ = naming_gate.strip(
            'let query = r#"SELECT "data" FROM t"#;', naming_gate.DIALECTS["rust"], None
        )
        self.assertIsNone(state)
        self.assertNotIn(BAD, code)


class DeclaredTest(unittest.TestCase):
    def declared(self, line: str, language: str = "ts") -> list[str]:
        code, _, _ = naming_gate.strip(line, naming_gate.DIALECTS[language], None)
        return [name.text for name in naming_gate.declared(code, language, 1)]

    def test_a_destructured_property_is_not_a_new_name(self) -> None:
        self.assertEqual(self.declared(f"const {{ {BAD} }} = useQuery()"), [])

    def test_a_typescript_parameter_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"function load({BAD}: Body) {{}}"))

    def test_a_typescript_generic_parameter_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"function load<T>({BAD}: T) {{}}"))

    def test_a_banned_word_in_a_string_is_not_a_name(self) -> None:
        self.assertEqual(self.declared('const USAGE = "const data = 1"'), ["USAGE"])

    def test_a_python_assignment_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"{BAD} = 1", "python"))

    def test_a_python_attribute_assignment_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"self.{BAD} = 1", "python"))

    def test_a_python_loop_target_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"for {BAD} in payload:", "python"))

    def test_a_python_keyword_argument_is_not_a_parameter(self) -> None:
        self.assertEqual(self.declared(f"load({BAD}=1)", "python"), [])

    def test_a_go_short_declaration_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"{BAD} := 1", "go"))

    def test_a_go_var_declaration_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"var {BAD} int", "go"))

    def test_a_banned_word_in_a_go_log_message_is_not_a_name(self) -> None:
        self.assertEqual(self.declared('log.Printf("data := %v", count)', "go"), [])

    def test_a_rust_let_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"let {BAD} = 1;", "rust"))

    def test_a_swift_unnamed_first_parameter_is_found(self) -> None:
        self.assertIn(BAD, self.declared(f"func load(_ {BAD}: Body) {{}}", "swift"))


class AddedTest(unittest.TestCase):
    def test_only_added_lines_keep_their_new_number(self) -> None:
        diff = "@@ -4,2 +4,3 @@\n context\n+added\n context\n"
        self.assertEqual(naming_gate.added(diff), [(5, "added")])

    def test_file_headers_are_not_added_lines(self) -> None:
        diff = "--- a/app.ts\n+++ b/app.ts\n@@ -1 +1 @@\n+const total = 1\n"
        self.assertEqual(naming_gate.added(diff), [(1, "const total = 1")])

    def test_a_content_line_starting_with_plus_keeps_its_number(self) -> None:
        diff = "@@ -0,0 +1,2 @@\n+++counter\n+const data = 1\n"
        self.assertEqual(
            naming_gate.added(diff), [(1, "++counter"), (2, "const data = 1")]
        )


class GateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.repo = Path(self.scratch.name).resolve() / "repo"
        self.repo.mkdir()
        self.git("init", "-q")

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def git(self, *args: str) -> None:
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
        )

    def run_gate(self, *paths: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *paths],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_a_new_file_with_a_vacuous_name_fails(self) -> None:
        (self.repo / "app.ts").write_text(f"const {BAD} = 1\n")
        result = self.run_gate("app.ts")
        self.assertEqual(result.returncode, 1)
        self.assertIn("app.ts:1", result.stdout)

    def test_a_clean_new_file_passes(self) -> None:
        (self.repo / "app.ts").write_text("const unpaidInvoices = 1\n")
        self.assertEqual(self.run_gate("app.ts").returncode, 0)

    def test_an_existing_name_is_not_reflagged_on_an_unrelated_edit(self) -> None:
        (self.repo / "app.ts").write_text(f"const {BAD} = 1\nexport const total = 1\n")
        self.git("add", "app.ts")
        self.git("commit", "-qm", "fixture")
        (self.repo / "app.ts").write_text(
            f"const {BAD} = 1\nexport const total = 1\nexport const tax = 1\n"
        )
        result = self.run_gate("app.ts")
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("app.ts:1", result.stdout)

    def test_a_staged_file_in_a_repository_without_commits_is_checked(self) -> None:
        (self.repo / "app.ts").write_text(f"const {BAD} = 1\n")
        self.git("add", "app.ts")
        self.assertEqual(self.run_gate("app.ts").returncode, 1)

    def test_every_language_is_checked(self) -> None:
        (self.repo / "app.py").write_text(f"{BAD} = 1\n")
        (self.repo / "app.go").write_text(f"func {VAGUE_FUNCTION}() {{}}\n")
        (self.repo / "app.rs").write_text(f"fn {VAGUE_FUNCTION}() {{}}\n")
        (self.repo / "app.swift").write_text(f"func {VAGUE_FUNCTION}() {{}}\n")
        result = self.run_gate("app.py", "app.go", "app.rs", "app.swift")
        self.assertEqual(result.returncode, 1)
        for path in ("app.py:1", "app.go:1", "app.rs:1", "app.swift:1"):
            self.assertIn(path, result.stdout)

    def test_a_generated_file_is_skipped(self) -> None:
        (self.repo / "client.ts").write_text(f"// @generated\nconst {BAD} = 1\n")
        self.assertEqual(self.run_gate("client.ts").returncode, 0)

    def test_a_naming_ignore_comment_skips_the_line(self) -> None:
        (self.repo / "app.vue.ts").write_text(
            f"const {BAD} = 1 // naming: ignore the framework owns this key\n"
        )
        self.assertEqual(self.run_gate("app.vue.ts").returncode, 0)

    def test_a_named_file_outside_the_repository_is_checked(self) -> None:
        outside = Path(self.scratch.name).resolve() / "outside.ts"
        outside.write_text(f"const {BAD} = 1\n")
        self.assertEqual(self.run_gate(str(outside)).returncode, 1)

    def test_a_missing_path_fails_loudly(self) -> None:
        self.assertEqual(self.run_gate("nope.ts").returncode, 2)

    def test_a_relative_path_from_a_subdirectory_is_found(self) -> None:
        (self.repo / "src").mkdir()
        (self.repo / "src" / "app.ts").write_text(f"const {BAD} = 1\n")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "app.ts"],
            cwd=self.repo / "src",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)

    def test_a_backslash_string_does_not_swallow_the_next_line(self) -> None:
        (self.repo / "app.ts").write_text('const BACKSLASH = "\\\\";\nconst data = 1;\n')
        result = self.run_gate("app.ts")
        self.assertEqual(result.returncode, 1)
        self.assertIn("app.ts:2", result.stdout)

    def test_a_go_char_literal_does_not_hide_the_next_line(self) -> None:
        (self.repo / "app.go").write_text("quote := '\"'\nvar data int\n")
        result = self.run_gate("app.go")
        self.assertEqual(result.returncode, 1)
        self.assertIn("app.go:2", result.stdout)

    def test_a_regex_literal_does_not_hide_the_next_line(self) -> None:
        (self.repo / "app.ts").write_text("const quoted = /[\"']/;\nconst data = 1;\n")
        result = self.run_gate("app.ts")
        self.assertEqual(result.returncode, 1)
        self.assertIn("app.ts:2", result.stdout)

    def test_a_raw_rust_string_is_not_code(self) -> None:
        (self.repo / "lib.rs").write_text('let query = r#"let data = 1"#;\n')
        self.assertEqual(self.run_gate("lib.rs").returncode, 0)

    def test_an_ignore_marker_inside_a_string_does_not_suppress(self) -> None:
        (self.repo / "app.ts").write_text(
            'const note = "naming: ignore"; const data = 1;\n'
        )
        self.assertEqual(self.run_gate("app.ts").returncode, 1)

    def test_a_block_comment_ignore_marker_suppresses(self) -> None:
        (self.repo / "app.ts").write_text("/* naming: ignore */ const data = 1;\n")
        self.assertEqual(self.run_gate("app.ts").returncode, 0)

    def test_a_block_comment_marker_across_lines_suppresses(self) -> None:
        (self.repo / "app.ts").write_text("/*\n naming: ignore */ const data = 1;\n")
        self.assertEqual(self.run_gate("app.ts").returncode, 0)

    def test_a_go_backtick_string_ending_in_a_backslash_closes(self) -> None:
        (self.repo / "app.go").write_text("q := `path\\`\nvar data int\n")
        result = self.run_gate("app.go")
        self.assertEqual(result.returncode, 1)
        self.assertIn("app.go:2", result.stdout)

    def test_a_rust_char_literal_does_not_swallow_the_file(self) -> None:
        (self.repo / "lib.rs").write_text("let q = '\"';\nlet data = 1;\n")
        result = self.run_gate("lib.rs")
        self.assertEqual(result.returncode, 1)
        self.assertIn("lib.rs:2", result.stdout)

    def test_a_rust_raw_string_ending_in_a_backslash_closes(self) -> None:
        (self.repo / "lib.rs").write_text('let p = r"path\\";\nlet data = 1;\n')
        result = self.run_gate("lib.rs")
        self.assertEqual(result.returncode, 1)
        self.assertIn("lib.rs:2", result.stdout)

    def test_an_added_line_inside_a_docstring_is_not_code(self) -> None:
        (self.repo / "doc.py").write_text('"""\nSummary.\n"""\nx = 1\n')
        self.git("add", "doc.py")
        self.git("commit", "-qm", "fixture")
        (self.repo / "doc.py").write_text('"""\nSummary.\n    data = 3\n"""\nx = 1\n')
        self.assertEqual(self.run_gate("doc.py").returncode, 0)

    def test_an_outside_file_under_a_skipped_directory_is_still_checked(self) -> None:
        outside = Path(self.scratch.name).resolve() / "build" / "outside.ts"
        outside.parent.mkdir(parents=True)
        outside.write_text(f"const {BAD} = 1\n")
        self.assertEqual(self.run_gate(str(outside)).returncode, 1)


class SkipDirsTest(unittest.TestCase):
    def test_a_repository_under_a_build_directory_is_still_checked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp).resolve() / "build" / "repo"
            repo.mkdir(parents=True)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            (repo / "app.ts").write_text(f"const {BAD} = 1\n")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "app.ts"],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
