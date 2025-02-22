from Extractor import app
from pyrogram import filters, enums
from Extractor.core import script
from Extractor.modules import appx
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ------------------------ Buttons ------------------------ # 

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🧰 Tools", callback_data="help_"),
        InlineKeyboardButton("🔗 Support", url="https://t.me/DevsHubChat")
    ]])

button = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏘 Home", callback_data="home_")
    ]])

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📢 Channel", url="https://t.me/DevsLaboratory")
    ]])

# ------------------------ Start ------------------------ # 

@app.on_message(filters.command("start"))
async def start_(_, message):
    name = message.from_user.mention
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_photo(
            photo=script.PHOTO,
            caption=script.START_TEXT.format(name),
            reply_markup=buttons
        )
    else:
        await message.reply_text("I am Alive Master.")



# ------------------------ Callback-Data ------------------------ # 

@app.on_callback_query()
async def handle_callback(_, query):
    name = query.from_user.mention

    if query.data == "home_":
        await query.message.edit_text(
            script.START_TEXT.format(name),
            reply_markup=buttons
        )
    elif query.data == "help_":
        await query.message.edit_text(
            script.HELP_TEXT,
            reply_markup=button
        )
    elif query.data.startswith("appx"):
        data = query.data.split("_")[1]
        task = data.split("*")
        name, api = task[1].split("#")
        if task[0] == "v2":
            await query.answer("waito...", show_alert=True)
            await appx.appex_v3_txt(app, query.message, user_id, api, name)
        else:
            await query.answer("waito...", show_alert=True)
            await appx.appex_v3_txt(app, query.message, user_id, api, name)



