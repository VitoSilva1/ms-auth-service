from typing import Optional

import httpx

from app.core.config import settings


class UserServiceUnavailable(Exception):
    """Raised when the user service cannot process the authentication request."""


def authenticate_user(email: str, password: str) -> Optional[dict]:
    payload = {"email": email, "password": password}
    headers = {"X-Internal-Secret": settings.INTERNAL_API_KEY}
    url = f"{settings.USER_SERVICE_URL.rstrip('/')}/users/internal/authenticate"

    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=5.0)
    except httpx.RequestError as exc:
        raise UserServiceUnavailable("User service is unreachable") from exc

    if response.status_code == 401:
        return None

    if response.is_success:
        return response.json()

    detail_message: Optional[str] = None
    try:
        body = response.json()
        detail = body.get("detail")
        if isinstance(detail, list):
            detail_message = ", ".join(str(item) for item in detail)
        elif isinstance(detail, str):
            detail_message = detail
    except ValueError:
        if response.text:
            detail_message = response.text.strip()

    status_info = f"User service returned status {response.status_code}"
    if detail_message:
        status_info = f"{status_info}: {detail_message}"

    raise UserServiceUnavailable(status_info)
