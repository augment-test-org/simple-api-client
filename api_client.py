#!/usr/bin/env python3
"""
Simple API client with bearer token authentication.
Reads token from a local file and makes authenticated API calls.
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class APIClient:
    def __init__(self, token_file="token.txt", base_url=None):
        """
        Initialize API client with token from file.

        Args:
            token_file (str): Path to file containing bearer token
            base_url (str): Base URL for API calls (optional)
        """
        self.token_file = token_file
        self.base_url = base_url or os.getenv('API_BASE_URL', '')
        self.token = self._load_token()
        self.session = requests.Session()

        if self.token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            })

    def _load_token(self):
        """Load bearer token from file."""
        token_path = Path(self.token_file)

        if not token_path.exists():
            print(f"Warning: Token file '{self.token_file}' not found.")
            print(f"Please create the file with your bearer token.")
            return None

        try:
            with open(token_path, 'r') as f:
                token = f.read().strip()
                if not token:
                    print(f"Warning: Token file '{self.token_file}' is empty.")
                    return None
                return token
        except Exception as e:
            print(f"Error reading token file: {e}")
            return None

    def get(self, endpoint, params=None):
        """Make GET request to API endpoint."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.get(url, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {e}'}

    def post(self, endpoint, data=None, json_data=None):
        """Make POST request to API endpoint."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.post(url, data=data, json=json_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {e}'}

    def put(self, endpoint, data=None, json_data=None):
        """Make PUT request to API endpoint."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.put(url, data=data, json=json_data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {e}'}

    def delete(self, endpoint):
        """Make DELETE request to API endpoint."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.delete(url)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {e}'}

    def _handle_response(self, response):
        """Handle API response and return JSON or error info."""
        try:
            # Try to parse JSON response
            json_response = response.json()

            if response.status_code >= 400:
                return {
                    'error': f'HTTP {response.status_code}',
                    'message': json_response.get('message', 'Unknown error'),
                    'details': json_response
                }

            return json_response

        except json.JSONDecodeError:
            # If response is not JSON, return text content
            if response.status_code >= 400:
                return {
                    'error': f'HTTP {response.status_code}',
                    'message': response.text or 'Unknown error'
                }

            return {'content': response.text}


def main():
    """Example usage of the API client."""
    print("API Client Example")
    print("=" * 50)

    # Initialize client
    client = APIClient()

    if not client.token:
        print("No valid token found. Please check your token.txt file.")
        return

    print(f"Token loaded successfully (first 10 chars): {client.token[:10]}...")
    print(f"Base URL: {client.base_url or 'Not set'}")

    # Example API calls (uncomment and modify as needed)

    # Example GET request
    # print("\nMaking GET request...")
    # response = client.get('/api/users')
    # print(json.dumps(response, indent=2))

    # Example POST request
    # print("\nMaking POST request...")
    # data = {'name': 'Test User', 'email': 'test@example.com'}
    # response = client.post('/api/users', json_data=data)
    # print(json.dumps(response, indent=2))

    print("\nAPI client is ready to use!")
    print("Modify the main() function to add your specific API calls.")


if __name__ == "__main__":
    main()
