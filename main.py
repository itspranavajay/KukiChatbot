from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import requests
import os
import re


API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("TOKEN", None) 
KUKI_API = os.environ.get("KUKI_API", None) 
MONGO_URL = os.environ.get("MONGO_URL", None)


bot = Client(
    "KukiBot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]


@bot.on_message(
    filters.command("setupchat", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def addchat(_, message): 
    kukidb = MongoClient(MONGO_URL)
    
    kuki = kukidb["KukiDb"]["Kuki"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_kuki = kuki.find_one({"chat_id": message.chat.id})
    if not kuki:
        toggle.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"✅ | Successfully\nKuki Chatbot of this Group is set to @{message.chat.username}\n Requested by [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n© @MetaVoid")
    else:
        await message.reply_text(f"Already Setup Kuki Chatbot of this Group Is @{message.chat.username}")


@bot.on_message(
    filters.command("removechat", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def rmchat(_, message): 
    kukidb = MongoClient(MONGO_URL)
    
    kuki = kukidb["KukiDb"]["Kuki"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_kuki = kuki.find_one({"chat_id": message.chat.id})
    if not is_kuki:
        await message.reply_text("Already Kuki ChatBot Disable")
    else:
        kuki.delete_one({"chat_id": message.chat.id})
        await message.reply_text("✅ | Kuki Chatbot is disable!")


@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):
  msg = message.text
  chat_id = message.chat.id

  kukidb = MongoClient(MONGO_URL)
    
  kuki = kukidb["KukiDb"]["Kuki"] 

  is_kuki = kuki.find_one({"chat_id": message.chat.id})
  if is_kuki:

      Kuki =   requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()

      moezilla = f"{Kuki['reply']}"

      self = await bot.get_me()
      bot_id = self.id
      if not message.reply_to_message.from_user.id == bot_id:
          return
      
      await client.send_chat_action(message.chat.id, "typing")
      await message.reply_text(moezilla)


@bot.on_message(
    filters.text
    & ~filters.reply
    & filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):
  msg = message.text
  chat_id = message.chat.id

  Kuki =   requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()

  moezilla = f"{Kuki['reply']}"
      
  await client.send_chat_action(message.chat.id, "typing")
  await message.reply_text(moezilla)


@bot.on_message(
    filters.command("chat", prefixes=["/", ".", "?", "-"]))
async def kukiai(client: Client, message: Message):

  msg = message.text.replace(message.text.split(" ")[0], "")
    
  Kuki =   requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()

  moezilla = f"{Kuki['reply']}"
      
  await client.send_chat_action(message.chat.id, "typing")
  await message.reply_text(moezilla)





@bot.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click here",
                url=f"t.me/kukichatbot?start")]])
        await message.reply("Contact me in PM",
                            reply_markup=buttons)
        
    else:
        buttons = [[InlineKeyboardButton("Support", url="https://t.me/metavoidsupport"),
                    InlineKeyboardButton("Channel", url="https://t.me/metavoid"),
                    InlineKeyboardButton("Repo", url="https://github.com/metavoidteam/kukichatbot")
                    ]]
        Photo = "https://telegra.ph/file/b04509cc8486f23690bba.jpg"
        await message.reply_photo(Photo, caption=f"Hello [{message.from_user.first_name}](tg://user?id={message.from_user.id}), Machine Learning Chat Bot that can talk about any topic in any language\n /help - Help Commands\n Powered By @MetaVoid", reply_markup=InlineKeyboardMarkup(buttons))



@bot.on_message(filters.command(["help"], prefixes=["/", "!"]))
async def help(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click here",
                url=f"t.me/kukichatbot?start=help_")]])
        await message.reply("Contact me in PM",
                            reply_markup=buttons)
        
    else:    
        await message.reply_text("/start - Start The Bot\n/chat - Send a message to this bot\n/setupchat - Active Kuki Chatbot In Group\n/removechat - Disable Kuki Chatbot In Group")





bot.run()

