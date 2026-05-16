import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from fastapi import FastAPI, HTTPException
from vehicle_maintence_scheduler.services import fetch_depots, fetch_vehicles
from vehicle_maintence_scheduler.knapsack import optimize_tasks
from vehicle_maintence_scheduler.models import OptimizationResult
from vehicle_maintence_scheduler.logging_helper import log as Log

app = FastAPI(title="Vehicle Maintenance Scheduler")


@app.get("/api/v1/optimize/{depot_id}", response_model=OptimizationResult)
async def optimize_depot(depot_id: int):
    await Log("backend", "info", "controller", f"Optimization requested for depot: {depot_id}")

    try:
        depots, vehicles = await asyncio.gather(fetch_depots(), fetch_vehicles())
    except Exception:
        await Log("backend", "error", "controller", "Failed to fetch data from APIs")
        raise HTTPException(status_code=502, detail="Failed to fetch data from upstream APIs")

    target = next((d for d in depots if d.ID == depot_id), None)
    if not target:
        await Log("backend", "warn", "controller", f"Depot not found: {depot_id}")
        raise HTTPException(status_code=404, detail="Depot not found")

    await Log("backend", "info", "controller", f"Running knapsack for depot {depot_id}")
    result = optimize_tasks(target.MechanicHours, vehicles)
    await Log("backend", "info", "controller", f"Optimization completed for depot {depot_id}")

    return OptimizationResult(
        depotId=target.ID,
        mechanicHours=target.MechanicHours,
        totalImpact=result["totalImpact"],
        totalDuration=result["totalDuration"],
        unusedHours=result["unusedHours"],
        selectedTasks=result["selectedTasks"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("vehicle_maintence_scheduler.app:app", host="0.0.0.0", port=3000, reload=True)
