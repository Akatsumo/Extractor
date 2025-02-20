from Extractor import app
from pyrogram import filters 
from Extractor.core import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



buttons = InlineKeyboardMarkup([
              [
                 InlineKeyboardButton("🔖 Tools", callback_data="help_"),
                 InlineKeyboardButton("🔗 Support", url="https://t.me/DevsHubChat")
              ])


@app.on_message(filters.command("start"))
async def start_(_, message):
  await message.reply_photo(photo=script.PHOTO, 
         caption=script.START_TEXT, reply_markup=buttons)

