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
    """Unit tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.com", {"payload": False}),
    ])

    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """get_json should return the JSON payload provided by the mocked response"""
        # Create a fake response object with a .json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.retrun_value = mock_response

        result = get_json(test_url)

        ## Assertions
        mock_get.assert_called_once_with(test_url)          # was HTTP call made correctly?
        self.assertEqual(result, test_payload)              # did we get the payload back?


    

if __name__ == "__main__":
    unittest.main()