import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from notification_app_be.notification_service import fetch_notifications
from notification_app_be.priority_notifications import get_top10_priority_notifications
from notification_app_be.logging_helper import log as Log


async def main():
    await Log("backend", "info", "service", "Starting Priority Notifications Test Script")

    try:
        notifications = await fetch_notifications()
        sys.stdout.write(f"Fetched {len(notifications)} total notifications.\n")

        top10 = await get_top10_priority_notifications(notifications)

        sys.stdout.write("--- Top 10 Priority Notifications ---\n")
        for i, notif in enumerate(top10, 1):
            sys.stdout.write(f"{i}. [{notif.Type}] Score: {notif.score:.0f} - {notif.Message} ({notif.Timestamp})\n")

        await Log("backend", "info", "service", "Priority Notifications Test Script completed successfully")
    except Exception as e:
        sys.stderr.write(f"Test failed: {e}\n")
        await Log("backend", "error", "service", f"Priority Notifications Test Script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
