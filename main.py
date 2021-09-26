from pyrogram.types import (
  Message, 
)
from pyrogram import filters, Client 
import requests
import os

API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
TOKEN = os.environ.get("TOKEN", None) 


kuki = Client(
      bot_token=TOKEN,
      api_id=API_ID,
      api_hash=API_HASH,
)

@kuki.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):
  msg = message.text
  chat_id = message.chat.id

  Kuki =   requests.get(f"https://kuki-api.tk/api/botname/owner/message={msg}").json()

  moezilla = f"{Kuki['reply']}"
      
  await client.send_chat_action(message.chat.id, "typing")
  await message.reply_text(moezilla)


messageprivate = '''
Hi, I'm Kuki Chat Bot
'''

messagegroup = '''
Hi, I'm Kuki Chat Bot
'''





@kuki.on_message(filters.command("start"))
async def start(_, message):
    self = await kuki.get_me()
    busername = self.username
    if message.chat.type != "private":
        await message.reply_text(messagegroup)
        return
    else:
        buttons = [[InlineKeyboardButton("Github", url="https://github.com/MoeZilla/KukiChatBot"),
                    ]]
        await message.reply_text(messageprivate, reply_markup=InlineKeyboardMarkup(buttons))




kuki.run()
