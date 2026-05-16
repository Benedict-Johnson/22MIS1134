import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from notification_app_be.models import Notification
from notification_app_be.logging_helper import get_auth_token, log as Log


async def fetch_notifications() -> list[Notification]:
    await Log("backend", "info", "service", "fetchNotifications request started")

    token = await get_auth_token()
    if not token:
        await Log("backend", "error", "service", "fetchNotifications missing auth token")
        raise Exception("Failed to retrieve auth token")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://4.224.186.213/evaluation-service/notifications",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = response.json()
        await Log("backend", "info", "service", "fetchNotifications request success")
        raw = data.get("notifications", data)
        return [Notification(**n) for n in raw]
    except Exception as e:
        await Log("backend", "error", "service", f"fetchNotifications failed: {e}")
        raise Exception("Failed to fetch notifications")
