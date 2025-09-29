import re
from Extractor import app
from pyrogram import filters, enums
from Extractor.core import script, core_func, main_func
from Extractor.modules import appx
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ------------------------ Buttons ------------------------ # 

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🧰 Tools", callback_data="tools_"),
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
    user_id = query.from_user.id

    if query.data == "home_":
        await query.message.edit_text(
            script.START_TEXT.format(name),
            reply_markup=buttons
        )
    elif query.data == "tools_":
        await query.message.edit_text(
            script.TOOLS_TEXT,
            reply_markup=main_func.get_page(0, core_func.appNameDict, "CoursesName")
        )
    elif query.data.startswith("appxlogin"):
        data = query.data.split("_")[1]
        task = data.split("*")
        def extract_parts(url):
            match = re.search(r'([\w\d]+?)(api)?\.(.+)$', url)
            if match:
                name = match.group(1)
                original_subdomain = match.group(1) + (match.group(2) or '') + '.' + match.group(3)
                return name, original_subdomain
            return None, None

        name, api = extract_parts(task[1])
        if not name or not api:
            return await query.message.edit_text("❌ **Invalid API URL! Please try again.**")

        if task[0] == "v2":
            await query.answer("waito...", show_alert=True)
            await appx.appex_v2_txt(app, query.message, user_id, api, name)
        else:
            await query.answer("waito...", show_alert=True)
            await appx.appex_v3_txt(app, query.message, user_id, api, name)
            
    elif query.data.startswith("page_"):
        page = int(query.data.split("_")[2])
        DictID = query.data.split("_")[1]
        appNameDict = main_func.allDics[DictID]
        await query.message.edit_text(
            script.TOOLS_TEXT,
            reply_markup=main_func.get_page(page, appNameDict, DictID, query)
        )
    elif query.data.startswith("autoCallback#"):
        data = query.data.split("#")[1]
        if data in core_func.appNameDict:
            await query.answer(f"You clicked {core_func.appNameDict[f"{data}"]["name"]}", show_alert=True)
            await core_func.appNameDict[f"{data}"]["func"](_, query.message, user_id)
        else:
            await query.answer("Callback Not Found!!")
        
    
        






