from .models import VehicleTask


def optimize_tasks(mechanic_hours: int, tasks: list[VehicleTask]) -> dict:
    n = len(tasks)
    dp = [[0] * (mechanic_hours + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        task = tasks[i - 1]
        for w in range(1, mechanic_hours + 1):
            if task.Duration <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - task.Duration] + task.Impact)
            else:
                dp[i][w] = dp[i - 1][w]

    # backtrack
    w = mechanic_hours
    selected: list[VehicleTask] = []
    total_duration = 0
    total_impact = 0

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            task = tasks[i - 1]
            selected.append(task)
            total_duration += task.Duration
            total_impact += task.Impact
            w -= task.Duration

    return {
        "selectedTasks": selected,
        "totalDuration": total_duration,
        "totalImpact": total_impact,
        "unusedHours": mechanic_hours - total_duration,
    }
