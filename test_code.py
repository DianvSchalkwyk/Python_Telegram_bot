import asyncio
import telegram

from Constants import BOT_API


async def main():
    bot = telegram.Bot(BOT_API)
    async with bot:
        await bot.send_message(chat_id='-1001887632157', text='Hello World!')


if __name__ == '__main__':
    asyncio.run(main())