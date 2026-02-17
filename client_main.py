import asyncio
from client import run_client

async def main():
    await run_client("localhost", 12345)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client arrete")