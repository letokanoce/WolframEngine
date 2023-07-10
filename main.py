import uvicorn
import asyncio


async def main():
    uvicorn.run("app.service:app", host="0.0.0.0", port=3002, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
