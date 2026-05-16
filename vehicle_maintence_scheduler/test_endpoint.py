import httpx
import json

r = httpx.get("http://localhost:3000/api/v1/optimize/2", timeout=30.0)
print(f"Status: {r.status_code}")
data = r.json()
print(json.dumps(data, indent=2)[:1200])
