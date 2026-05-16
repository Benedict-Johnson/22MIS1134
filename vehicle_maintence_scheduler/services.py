import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from vehicle_maintence_scheduler.models import Depot, VehicleTask
from vehicle_maintence_scheduler.logging_helper import get_auth_token, log as Log


async def fetch_depots() -> list[Depot]:
    await Log("backend", "info", "service", "fetchDepots request started")

    token = await get_auth_token()
    if not token:
        await Log("backend", "error", "service", "fetchDepots missing auth token")
        raise Exception("Failed to retrieve auth token")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://4.224.186.213/evaluation-service/depots",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = response.json()
        await Log("backend", "info", "service", "fetchDepots request success")
        raw = data.get("depots", data)
        return [Depot(**d) for d in raw]
    except Exception as e:
        await Log("backend", "error", "service", f"fetchDepots failed: {e}")
        raise Exception("Failed to fetch depots")


async def fetch_vehicles() -> list[VehicleTask]:
    await Log("backend", "info", "service", "fetchVehicles request started")

    token = await get_auth_token()
    if not token:
        await Log("backend", "error", "service", "fetchVehicles missing auth token")
        raise Exception("Failed to retrieve auth token")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://4.224.186.213/evaluation-service/vehicles",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = response.json()
        await Log("backend", "info", "service", "fetchVehicles request success")
        raw = data.get("vehicles", data)
        return [VehicleTask(**v) for v in raw]
    except Exception as e:
        await Log("backend", "error", "service", f"fetchVehicles failed: {e}")
        raise Exception("Failed to fetch vehicles")
