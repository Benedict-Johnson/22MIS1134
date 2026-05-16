import httpx
from .auth import get_auth_token
from .validators import validate_log_params


async def log(stack: str, level: str, package_name: str, message: str) -> dict:
    try:
        is_valid, error = validate_log_params(stack, level, package_name, message)
        if not is_valid:
            return {"success": False, "error": error}

        token = await get_auth_token()
        if not token:
            return {"success": False, "error": "Failed to retrieve auth token"}

        payload = {
            "stack": stack,
            "level": level,
            "package": package_name,
            "message": message,
        }

        async with httpx.AsyncClient() as client:
            await client.post(
                "http://4.224.186.213/evaluation-service/logs",
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
