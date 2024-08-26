#!/usr/bin/env python3
"""A module for testing the client module."""

import unittest
from typing import Dict, List
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mockedgetjson: MagicMock) -> None:
        """Tests the `org` method."""
        mockedgetjson.return_value = resp
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org, resp)
        mockedgetjson.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: PropertyMock) -> None:
        """Tests the `_public_repos_url` property."""
        mock_org.return_value = {
            'repos_url': "https://api.github.com/users/google/repos",
        }
        gh_org_client = GithubOrgClient("google")
        self.assertEqual(
            gh_org_client._public_repos_url,
            "https://api.github.com/users/google/repos",
        )
        mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method."""
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {"name": "episodes.dart"},
                {"name": "kratu"},
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            gh_org_client = GithubOrgClient("google")
            self.assertEqual(
                gh_org_client.public_repos(),
                ["episodes.dart", "kratu"],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
        ({"license": None}, "bsd-3-clause", False),
        ({}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, l_key: str, expected: bool) -> None:
        """Tests the `has_license` method."""
        gh_org_client = GithubOrgClient("google")
        self.assertEqual(gh_org_client.has_license(repo, l_key), expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == f"https://api.github.com/orgs/google":
                return Mock(**{'json.return_value': cls.org_payload})
            elif url == cls.org_payload['repos_url']:
                return Mock(**{'json.return_value': cls.repos_payload})
            return Mock(status_code=404)

        cls.mock_get.side_effect = side_effect

    def setUp(self) -> None:
        """Sets up method fixtures before each test."""
        self.client = GithubOrgClient("google")

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    def test_public_repos_with_non_existing_license(self) -> None:
        """Tests the `public_repos` method with a non-existing license."""
        self.assertEqual(self.client.public_repos(license="non-existing"), [])

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
