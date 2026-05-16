import asyncio
from .logger import log


async def main():
    result = await log("backend", "info", "service", "logger middleware initialized")
    if result["success"]:
        import sys
        sys.stdout.write("Log test executed successfully.\n")
    else:
        import sys
        sys.stderr.write(f"Log test failed: {result.get('error')}\n")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
