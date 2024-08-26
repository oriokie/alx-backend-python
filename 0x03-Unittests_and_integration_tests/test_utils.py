#!/usr/bin/env python3
"""A module for testing the utils module."""

import unittest
from typing import Dict, Tuple, Union, Any, Type
from unittest.mock import patch, Mock
from parameterized import parameterized

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests the `access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": {"c": 3}}}, ("a", "b", "c"), 3),
    ])
    def test_access_nested_map(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...],
        expected: Union[Dict, int],
    ) -> None:
        """Tests `access_nested_map`'s output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError, "'a'"),
        ({"a": 1}, ("a", "b"), KeyError, "'b'"),
        ({"a": {"b": 2}}, ("a", "b", "c"), KeyError, "'c'"),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...],
        exception: Type[Exception],
        expected_message: str,
    ) -> None:
        """Tests `access_nested_map`'s exception raising."""
        with self.assertRaises(exception) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Tests the `get_json` function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
        ("http://invalid.io", {"error": "Not Found"}),
    ])
    @patch("requests.get")
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict[str, Any],
        mock_get: Mock,
    ) -> None:
        """Tests `get_json`'s output."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)
        mock_response.json.assert_called_once()


class TestMemoize(unittest.TestCase):
    """Tests the `memoize` function."""

    def test_memoize(self) -> None:
        """Tests `memoize`'s output and caching behavior."""
        class TestClass:
            def __init__(self):
                self.a_method_call_count = 0

            @memoize
            def a_property(self):
                return self.a_method()

            def a_method(self):
                self.a_method_call_count += 1
                return 42

        test_class = TestClass()

        # First call should compute the value
        self.assertEqual(test_class.a_property, 42)
        self.assertEqual(test_class.a_method_call_count, 1)

        # Subsequent calls should use cached value
        self.assertEqual(test_class.a_property, 42)
        self.assertEqual(test_class.a_property, 42)
        self.assertEqual(test_class.a_method_call_count, 1)

    def test_memoize_different_instances(self) -> None:
        """Tests `memoize` with different class instances."""
        class TestClass:
            def __init__(self, value):
                self.value = value

            @memoize
            def a_property(self):
                return self.value * 2

        instance1 = TestClass(21)
        instance2 = TestClass(50)

        self.assertEqual(instance1.a_property, 42)
        self.assertEqual(instance2.a_property, 100)


if __name__ == "__main__":
    unittest.main()
