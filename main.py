from aiogram import Bot, Dispatcher, types
import logging
import asyncio
import sys
from utils.config import BOT_TOKEN
from aiogram.fsm.state import State, StatesGroup

class InputState(StatesGroup):
    waiting_for_name = State()
    waiting_for_pass = State()
    print_pass_key = State()
    
dp = Dispatcher()
bot = Bot(BOT_TOKEN)

async def main() -> None:
    from handlers.start import router
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    