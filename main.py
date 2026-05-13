import os
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database import engine, Base
from bot import router

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if router.parent_router is None:
        dp.include_router(router)
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    polling_task = asyncio.create_task(dp.start_polling(bot))
    
    yield
    
    polling_task.cancel()
    await bot.session.close()

app = FastAPI(title="LinkedIn Post Manager API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "LinkedIn Post Manager is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8511, reload=True)
