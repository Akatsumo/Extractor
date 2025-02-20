from Extractor import app
from pyrogram import filters 
from Extractor.core import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



buttons = InlineKeyboardMarkup([
              [
                 InlineKeyboardButton("🔖 Tools", callback_data="help_"),
                 InlineKeyboardButton("🔗 Support", url="https://t.me/DevsHubChat")
              ])

button = InlineKeyboardMarkup([
              [
                 InlineKeyboardButton("🔖 Home", callback_data="home_")
              ])



@app.on_message(filters.command("start"))
async def start_(_, message):
  name = message.from_user.mention
  await message.reply_photo(photo=script.PHOTO, 
         caption=script.START_TEXT.format(name), reply_markup=buttons)




@app.on_callback_query()
async def handle_callback(_, query):
  name = query.from_user.mention
  if query.data=="home_":
    await query.message.edit_text(
          script.START_TEXT.format(name),
          reply_markup=button)

  elif query.data=="help_":
    await query.message.edit_text(
          script.HELP_TEXT,
          reply_markup=button)
        
