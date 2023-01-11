import Constants as keys
from telethon import TelegramClient

api_id = keys.PERSONAL_API
api_hash = keys.PERSONAL_HASH
client = TelegramClient('anon', api_id, api_hash)

async def main():

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

with client:
    client.loop.run_until_complete(main())