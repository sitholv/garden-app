"""Test advice separately from input so interface changes cannot alter it."""

import contextlib
import importlib
import io
import subprocess
import sys
import unittest
from unittest.mock import patch

import garden_advice
from garden_advice import PLANT_ADVICE, SEASON_ADVICE, get_advice


class AdviceTests(unittest.TestCase):
    """Cover the starter example, all choices and defensive validation."""

    def test_original_example_is_preserved(self):
        """Refactoring must not change the starter's known-good output."""
        self.assertEqual(
            get_advice("summer", "flower"),
            "Water your plants regularly and provide some shade.\n"
            "Use fertiliser to encourage blooms.",
        )

    def test_all_supported_combinations(self):
        """Each season/plant pair contains its matching advice messages."""
        for season, seasonal in SEASON_ADVICE.items():
            for plant, planting in PLANT_ADVICE.items():
                with self.subTest(season=season, plant=plant):
                    self.assertEqual(
                        get_advice(season, plant), seasonal + "\n" + planting
                    )

    def test_whitespace_and_case_are_normalised(self):
        """Accidental spaces and capitalisation do not reject valid choices."""
        self.assertEqual(
            get_advice(" WINTER ", " Vegetable "),
            get_advice("winter", "vegetable"),
        )

    def test_unknown_or_empty_values_are_rejected(self):
        """Bad labels fail clearly instead of returning empty advice."""
        for season, plant in [("", "flower"), ("rainy", "flower"),
                              ("summer", "tree"), ("summer", " ")]:
            with self.subTest(season=season, plant=plant):
                with self.assertRaises(ValueError):
                    get_advice(season, plant)

    def test_non_text_values_are_rejected(self):
        """A reusable function reports bad types before string operations."""
        with self.assertRaises(TypeError):
            get_advice(None, "flower")
        with self.assertRaises(TypeError):
            get_advice("summer", 5)

    def test_import_does_not_print_or_prompt(self):
        """Importing the module is safe for tests and future interfaces."""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            importlib.reload(garden_advice)
        self.assertEqual(output.getvalue(), "")


class ConsoleTests(unittest.TestCase):
    """Check real interaction, invalid choices and deliberate cancellation."""

    def test_main_accepts_valid_choices(self):
        """Both user choices determine the final advice, not fixed defaults."""
        output = io.StringIO()
        with patch("builtins.input", side_effect=["winter", "vegetable"]):
            with contextlib.redirect_stdout(output):
                status = garden_advice.main()
        self.assertEqual(status, 0)
        self.assertIn(get_advice("winter", "vegetable"), output.getvalue())

    def test_invalid_choices_are_retried(self):
        """Bad input is explained and can be corrected for either prompt."""
        output = io.StringIO()
        entries = ["rainy", " WINTER ", "tree", " Vegetable "]
        with patch("builtins.input", side_effect=entries):
            with contextlib.redirect_stdout(output):
                garden_advice.main()
        self.assertEqual(output.getvalue().count("Choose one of:"), 2)
        self.assertIn(get_advice("winter", "vegetable"), output.getvalue())

    def test_cancel_is_clean(self):
        """Closed input and Ctrl+C do not expose implementation tracebacks."""
        for exception in [EOFError, KeyboardInterrupt]:
            with self.subTest(exception=exception.__name__):
                output = io.StringIO()
                with patch("builtins.input", side_effect=exception):
                    with contextlib.redirect_stdout(output):
                        self.assertEqual(garden_advice.main(), 0)
                self.assertIn("cancelled", output.getvalue())

    def test_real_console_entrypoint(self):
        """A separate Python process can receive piped terminal input."""
        result = subprocess.run(
            [sys.executable, "garden_advice.py"],
            input="summer\nflower\n", text=True, capture_output=True,
            check=False, timeout=5,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn(get_advice("summer", "flower"), result.stdout)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
