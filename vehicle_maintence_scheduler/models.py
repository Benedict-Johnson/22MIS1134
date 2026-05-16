from pydantic import BaseModel


class Depot(BaseModel):
    ID: int
    MechanicHours: int


class VehicleTask(BaseModel):
    TaskID: str
    Duration: int
    Impact: int


class OptimizationResult(BaseModel):
    depotId: int
    mechanicHours: int
    totalImpact: int
    totalDuration: int
    unusedHours: int
    selectedTasks: list[VehicleTask]
