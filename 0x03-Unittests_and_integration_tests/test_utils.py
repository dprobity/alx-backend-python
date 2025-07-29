#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map - Task 0"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests access_nested_map returns the right value"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b":2}}, ("a", "b"), 2),
    ])

    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

     # New Task 1 test
    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised for missing keys"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")




class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, payload, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = payload
        mock_get.return_value = mock_response

        result = get_json(url)

        mock_get.assert_called_once_with(url)
        self.assertEqual(result, payload)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            value1 = obj.a_property
            value2 = obj.a_property

            self.assertEqual(value1, 42)
            self.assertEqual(value2, 42)
            mock_method.assert_called_once()

    

if __name__ == "__main__":
    unittest.main()