#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct value,
        and get_json is called once with the correct URL.
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct value
        from the mocked org payload.
        """
        test_url = "https://api.github.com/orgs/testorg/repos"
        payload = {"repos_url": test_url}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, test_url)

    @patch('client.get_json')

    def test_public_repos(self, mock_get_json):
        """
        Test public_repos returns expected repo names,
        with _public_repos_url and get_json patched.
        """
        test_repos_url = "https://api.github.com/orgs/testorg/repos"
        test_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        # Patch _public_repos_url to return test_repos_url
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = test_repos_url
            mock_get_json.return_value = test_repos_payload

            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            # Was _public_repos_url called?
            mock_url.assert_called_once_with()
            # Was get_json called with the repos_url?
            mock_get_json.assert_called_once_with(test_repos_url)
            # Did we get the expected list of names?
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),  # handles missing license key case
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns True if repo license matches,
        otherwise False.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and set up return values for different URLs."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Setup side effects so .json() returns correct payloads
        def side_effect(url):
            mock_response = unittest.mock.Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns the expected repo names list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos only with 'apache-2.0' license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
        
if __name__ == "__main__":
    unittest.main()

