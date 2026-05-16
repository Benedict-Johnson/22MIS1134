import os
import time
import httpx
from dotenv import load_dotenv
from pathlib import Path

# Load .env from this package's directory
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)

_cached_token: str | None = None
_token_expiry: float | None = None


async def get_auth_token() -> str | None:
    global _cached_token, _token_expiry
    now = time.time()

    if _cached_token and _token_expiry and _token_expiry > now + 60:
        return _cached_token

    try:
        payload = {
            "email": os.getenv("EMAIL"),
            "name": os.getenv("NAME"),
            "rollNo": os.getenv("ROLL_NO"),
            "accessCode": os.getenv("ACCESS_CODE"),
            "clientID": os.getenv("CLIENT_ID"),
            "clientSecret": os.getenv("CLIENT_SECRET"),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://4.224.186.213/evaluation-service/auth",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            data = response.json()

        token = data.get("token") or data.get("access_token")
        if token:
            _cached_token = token
            expires_in = data.get("expiresIn", 3600)
            _token_expiry = now + expires_in
            return _cached_token

        return None
    except Exception:
        return None
