import unittest
from unittest.mock import patch

from Carsapp.utils.otherfunctions import get_access_and_refresh

class TestGetAccessAndRefresh(unittest.TestCase):

    @patch('requests.post')
    def test_successful_response(self, mock_post):
        mock_response = {
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token"
        }
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.status_code = 200

        auth_code = "dummy_auth_code"
        result = get_access_and_refresh(auth_code)

        expected_result = ("dummy_access_token", "dummy_refresh_token")
        self.assertEqual(result, expected_result)


    @patch('requests.post')
    def test_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Server error")

        auth_code = "dummy_auth_code"
        response = get_access_and_refresh(auth_code)

        self.assertEqual(response.status_code, 500)
        self.assertIn("Unexpected error", response.content.decode())