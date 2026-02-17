import asyncio
from server import setup_and_run_server

async def main():
    await setup_and_run_server("localhost", 12345)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Serveur arrete")