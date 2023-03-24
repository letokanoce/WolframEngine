import uvicorn
import asyncio


async def main():
    uvicorn.run("service:app", host="0.0.0.0", port=3200, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
