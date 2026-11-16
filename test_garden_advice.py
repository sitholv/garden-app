"""Test advice separately from input so interface changes cannot alter it."""

import contextlib
import importlib
import io
import unittest

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


if __name__ == "__main__":
    unittest.main()
