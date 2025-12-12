import unittest
from unittest.mock import MagicMock, patch

from app.services import auth_service


class TestAuthenticateUser(unittest.TestCase):
    def setUp(self):
        self.email = "user@example.com"
        self.password = "secret"

    def _build_response(self, *, status_code: int, is_success: bool, body=None, text: str = ""):
        response = MagicMock()
        response.status_code = status_code
        response.is_success = is_success
        response.json.return_value = body or {}
        response.text = text
        return response

    @patch("app.services.auth_service.httpx.post")
    def test_authenticate_returns_user_on_success(self, mock_post):
        user_payload = {"id": 1, "role": "admin"}
        mock_post.return_value = self._build_response(status_code=200, is_success=True, body=user_payload)

        result = auth_service.authenticate_user(self.email, self.password)

        self.assertEqual(result, user_payload)
        mock_post.assert_called_once()

    @patch("app.services.auth_service.httpx.post")
    def test_authenticate_returns_none_on_invalid_credentials(self, mock_post):
        mock_post.return_value = self._build_response(status_code=401, is_success=False)

        result = auth_service.authenticate_user(self.email, self.password)

        self.assertIsNone(result)

    @patch("app.services.auth_service.httpx.post")
    def test_authenticate_raises_on_user_service_error(self, mock_post):
        mock_post.return_value = self._build_response(
            status_code=500,
            is_success=False,
            body={"detail": ["Unexpected error"]},
        )

        with self.assertRaises(auth_service.UserServiceUnavailable) as exc:
            auth_service.authenticate_user(self.email, self.password)

        self.assertIn("User service returned status 500", str(exc.exception))

    @patch("app.services.auth_service.httpx.post")
    def test_authenticate_raises_on_network_error(self, mock_post):
        mock_post.side_effect = auth_service.httpx.RequestError("boom")

        with self.assertRaises(auth_service.UserServiceUnavailable) as exc:
            auth_service.authenticate_user(self.email, self.password)

        self.assertIn("User service is unreachable", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
