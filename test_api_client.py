#!/usr/bin/env python3
"""
Basic tests for the API client.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, Mock
from api_client import APIClient


class TestAPIClient(unittest.TestCase):
    """Test cases for APIClient class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary token file for testing
        self.temp_token_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_token_file.write('test_token_12345')
        self.temp_token_file.close()

        self.test_token_path = self.temp_token_file.name
        self.test_base_url = 'https://api.test.com'

    def tearDown(self):
        """Clean up after each test method."""
        # Remove temporary token file
        if os.path.exists(self.test_token_path):
            os.unlink(self.test_token_path)

    def test_init_with_valid_token_file(self):
        """Test APIClient initialization with valid token file."""
        client = APIClient(token_file=self.test_token_path, base_url=self.test_base_url)

        self.assertEqual(client.token, 'test_token_12345')
        self.assertEqual(client.base_url, self.test_base_url)
        self.assertIn('Authorization', client.session.headers)
        self.assertEqual(client.session.headers['Authorization'], 'Bearer test_token_12345')

    def test_init_with_missing_token_file(self):
        """Test APIClient initialization with missing token file."""
        client = APIClient(token_file='nonexistent_token.txt', base_url=self.test_base_url)

        self.assertIsNone(client.token)
        self.assertEqual(client.base_url, self.test_base_url)

    def test_init_with_empty_token_file(self):
        """Test APIClient initialization with empty token file."""
        # Create empty token file
        empty_token_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        empty_token_file.write('')
        empty_token_file.close()

        try:
            client = APIClient(token_file=empty_token_file.name, base_url=self.test_base_url)
            self.assertIsNone(client.token)
        finally:
            os.unlink(empty_token_file.name)

    @patch('api_client.requests.Session.get')
    def test_get_request_success(self, mock_get):
        """Test successful GET request."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success', 'data': [1, 2, 3]}
        mock_get.return_value = mock_response

        client = APIClient(token_file=self.test_token_path, base_url=self.test_base_url)
        result = client.get('/api/test')

        self.assertEqual(result, {'status': 'success', 'data': [1, 2, 3]})
        mock_get.assert_called_once()

    @patch('api_client.requests.Session.get')
    def test_get_request_error(self, mock_get):
        """Test GET request with error response."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'Not found'}
        mock_get.return_value = mock_response

        client = APIClient(token_file=self.test_token_path, base_url=self.test_base_url)
        result = client.get('/api/nonexistent')

        self.assertIn('error', result)
        self.assertEqual(result['error'], 'HTTP 404')
        self.assertEqual(result['message'], 'Not found')

    @patch('api_client.requests.Session.post')
    def test_post_request_success(self, mock_post):
        """Test successful POST request."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 123, 'status': 'created'}
        mock_post.return_value = mock_response

        client = APIClient(token_file=self.test_token_path, base_url=self.test_base_url)
        result = client.post('/api/users', json_data={'name': 'Test User'})

        self.assertEqual(result, {'id': 123, 'status': 'created'})
        mock_post.assert_called_once()

    def test_url_construction(self):
        """Test URL construction with different base URLs and endpoints."""
        client = APIClient(token_file=self.test_token_path, base_url='https://api.test.com/')

        # Test with mock to avoid actual HTTP calls
        with patch('api_client.requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            client.get('/api/test')

            # Check that the URL was constructed correctly
            args, kwargs = mock_get.call_args
            expected_url = 'https://api.test.com/api/test'
            self.assertEqual(args[0], expected_url)

    def test_handle_response_non_json(self):
        """Test handling of non-JSON responses."""
        with patch('api_client.requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("No JSON object could be decoded", "Plain text response", 0)
            mock_response.text = "Plain text response"
            mock_get.return_value = mock_response

            client = APIClient(token_file=self.test_token_path, base_url=self.test_base_url)
            result = client.get('/api/text')

            self.assertEqual(result, {'content': 'Plain text response'})


class TestAPIClientIntegration(unittest.TestCase):
    """Integration tests that don't require actual API calls."""

    def test_environment_variable_loading(self):
        """Test that environment variables are loaded correctly."""
        with patch.dict(os.environ, {'API_BASE_URL': 'https://env.test.com'}):
            # Create temporary token file
            temp_token_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_token_file.write('env_test_token')
            temp_token_file.close()

            try:
                client = APIClient(token_file=temp_token_file.name)
                self.assertEqual(client.base_url, 'https://env.test.com')
                self.assertEqual(client.token, 'env_test_token')
            finally:
                os.unlink(temp_token_file.name)


def run_tests():
    """Run all tests and display results."""
    print("Running API Client Tests")
    print("=" * 50)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAPIClient))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIClientIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} error(s) occurred")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
