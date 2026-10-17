"""Unit tests for module_x.

Written with the standard-library unittest so they run without extra
dependencies; pytest will also collect them.

Run from module_1/:
    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from module_x import (  # noqa: E402
    VALID_CUSTOMER_TIERS,
    calculate_discount,
    classify_priority,
    is_valid_project_code,
    normalize_name,
    summarize_order,
)


class TestNormalizeName(unittest.TestCase):
    def test_title_cases_lowercase_name(self):
        self.assertEqual(normalize_name("ada lovelace"), "Ada Lovelace")

    def test_title_cases_uppercase_name(self):
        self.assertEqual(normalize_name("GRACE HOPPER"), "Grace Hopper")

    def test_strips_leading_and_trailing_whitespace(self):
        self.assertEqual(normalize_name("   alan turing  "), "Alan Turing")

    def test_collapses_internal_whitespace_including_tabs_and_newlines(self):
        self.assertEqual(normalize_name("linus\t\n  torvalds"), "Linus Torvalds")

    def test_single_word(self):
        self.assertEqual(normalize_name("cher"), "Cher")

    def test_empty_string_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "name cannot be empty"):
            normalize_name("")

    def test_whitespace_only_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "name cannot be empty"):
            normalize_name(" \t\n ")

    def test_non_string_raises_type_error(self):
        for bad in (None, 123, ["ada"], b"ada"):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(TypeError, "name must be a string"):
                    normalize_name(bad)


class TestCalculateDiscount(unittest.TestCase):
    def test_each_tier_applies_its_rate(self):
        cases = {
            "standard": 100.0,
            "silver": 95.0,
            "gold": 90.0,
            "platinum": 85.0,
        }
        for tier, expected in cases.items():
            with self.subTest(tier=tier):
                self.assertEqual(calculate_discount(100.0, tier), expected)

    def test_covers_every_valid_tier(self):
        self.assertEqual(VALID_CUSTOMER_TIERS, {"standard", "silver", "gold", "platinum"})

    def test_tier_is_case_and_whitespace_insensitive(self):
        self.assertEqual(calculate_discount(100.0, "  GoLd  "), 90.0)

    def test_result_is_rounded_to_two_decimals(self):
        # 19.99 * 0.85 = 16.9915
        self.assertEqual(calculate_discount(19.99, "platinum"), 16.99)

    def test_zero_price(self):
        self.assertEqual(calculate_discount(0, "gold"), 0.0)

    def test_accepts_integer_price(self):
        self.assertEqual(calculate_discount(200, "silver"), 190.0)

    def test_negative_price_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "price cannot be negative"):
            calculate_discount(-0.01, "gold")

    def test_unknown_tier_raises_value_error_with_original_input(self):
        with self.assertRaisesRegex(ValueError, "unknown customer tier: Diamond"):
            calculate_discount(100.0, "Diamond")

    def test_empty_tier_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_discount(100.0, "")

    def test_negative_price_checked_before_tier(self):
        with self.assertRaisesRegex(ValueError, "price cannot be negative"):
            calculate_discount(-1, "not-a-tier")


class TestClassifyPriority(unittest.TestCase):
    def test_boundaries(self):
        cases = [
            (0, "low"),
            (39, "low"),
            (40, "medium"),
            (69, "medium"),
            (70, "high"),
            (89, "high"),
            (90, "urgent"),
            (100, "urgent"),
        ]
        for score, expected in cases:
            with self.subTest(score=score):
                self.assertEqual(classify_priority(score), expected)

    def test_below_range_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            classify_priority(-1)

    def test_above_range_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            classify_priority(101)

    def test_non_integer_raises_type_error(self):
        for bad in (50.0, "50", None):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(TypeError, "score must be an integer"):
                    classify_priority(bad)

    def test_bool_is_accepted_as_int(self):
        # bool is a subclass of int, so the isinstance check lets it through.
        self.assertEqual(classify_priority(True), "low")


class TestSummarizeOrder(unittest.TestCase):
    def test_empty_list_returns_zeros(self):
        self.assertEqual(summarize_order([]), {"item_count": 0, "subtotal": 0.0})

    def test_none_is_treated_as_empty(self):
        self.assertEqual(summarize_order(None), {"item_count": 0, "subtotal": 0.0})

    def test_single_item(self):
        result = summarize_order([{"quantity": 3, "unit_price": 2.5}])
        self.assertEqual(result, {"item_count": 3, "subtotal": 7.5})

    def test_multiple_items_are_summed(self):
        items = [
            {"name": "widget", "quantity": 2, "unit_price": 10.0},
            {"name": "gadget", "quantity": 1, "unit_price": 4},
        ]
        self.assertEqual(summarize_order(items), {"item_count": 3, "subtotal": 24.0})

    def test_subtotal_is_rounded_to_two_decimals(self):
        items = [{"quantity": 3, "unit_price": 0.1}]
        self.assertEqual(summarize_order(items)["subtotal"], 0.3)

    def test_subtotal_is_float_even_for_int_prices(self):
        result = summarize_order([{"quantity": 2, "unit_price": 5}])
        self.assertIsInstance(result["subtotal"], float)

    def test_missing_fields_default_to_zero(self):
        self.assertEqual(summarize_order([{}]), {"item_count": 0, "subtotal": 0.0})

    def test_zero_quantity_is_allowed(self):
        result = summarize_order([{"quantity": 0, "unit_price": 99.99}])
        self.assertEqual(result, {"item_count": 0, "subtotal": 0.0})

    def test_negative_quantity_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "quantity must be a non-negative integer"):
            summarize_order([{"quantity": -1, "unit_price": 1.0}])

    def test_non_integer_quantity_raises_value_error(self):
        for bad in (1.5, "2", None):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "quantity must be a non-negative integer"):
                    summarize_order([{"quantity": bad, "unit_price": 1.0}])

    def test_negative_unit_price_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "unit_price must be a non-negative number"):
            summarize_order([{"quantity": 1, "unit_price": -0.01}])

    def test_non_numeric_unit_price_raises_value_error(self):
        for bad in ("1.00", None):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "unit_price must be a non-negative number"):
                    summarize_order([{"quantity": 1, "unit_price": bad}])

    def test_invalid_item_after_valid_item_still_raises(self):
        items = [
            {"quantity": 1, "unit_price": 1.0},
            {"quantity": -1, "unit_price": 1.0},
        ]
        with self.assertRaises(ValueError):
            summarize_order(items)


class TestIsValidProjectCode(unittest.TestCase):
    def test_valid_codes(self):
        for code in ("AB-1234", "ZZ-0000", "QX-9999"):
            with self.subTest(code=code):
                self.assertTrue(is_valid_project_code(code))

    def test_invalid_codes(self):
        cases = [
            "",
            "AB1234",  # missing hyphen
            "AB-123",  # number too short
            "AB-12345",  # number too long
            "A-1234",  # prefix too short
            "ABC-1234",  # prefix too long
            "ab-1234",  # lowercase prefix
            "Ab-1234",  # mixed-case prefix
            "A1-1234",  # non-alpha prefix
            "AB-12a4",  # non-digit number
            "AB-1234-5",  # too many parts
            "AB--1234",  # empty middle part
            " AB-1234",  # leading whitespace
            "AB-1234 ",  # trailing whitespace
        ]
        for code in cases:
            with self.subTest(code=code):
                self.assertFalse(is_valid_project_code(code))

    def test_non_string_returns_false(self):
        for bad in (None, 1234, ["AB", "1234"]):
            with self.subTest(bad=bad):
                self.assertFalse(is_valid_project_code(bad))


if __name__ == "__main__":
    unittest.main()
