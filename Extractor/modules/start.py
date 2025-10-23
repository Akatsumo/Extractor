from Extractor import app
from pyrogram import filters, enums
from Extractor.core import script, core_func, main_func, appxmethod
from Extractor.modules import appx
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

core_func.appNameDict["appx_"] = {"name": "Appx", "func": appx.appx_logins}


# ------------------------ Buttons ------------------------ # 

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🧰 Tools", callback_data="tools_"),
        InlineKeyboardButton("Contact ☎️", user_id=int("6107581019"))
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
    join = await main_func.subscribe(_, message)
    if join == 1:
        return
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
    join = await main_func.subscribe(_, query.message, user_id, name)
    if join == 1:
        return

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
    elif query.data == "manual_login":
        await query.answer("You clicked Manual Login", show_alert=True)
        await appx.appx_logins(_, query.message, user_id, False, None, None, True)
        
    elif query.data == "withoutIdPass":
        await query.answer("You clicked Without ID Pass", show_alert=True)
        buttons = main_func.get_page(0, core_func.WithoutAppDict, DictID="WithoutID-Pass", back_data="tools_", query)
        await query.message.edit_text(script.TOOLS_TEXT, reply_markup=buttons)
    
    elif query.data.startswith("page_"):
        if not main_func.allDics:
            return await query.answer("Time up!", show_alert=True)
        page = int(query.data.split("_")[2])
        DictID = query.data.split("_")[1]
        appNameDict = main_func.allDics[DictID]
        await query.message.edit_text(
            script.TOOLS_TEXT,
            reply_markup=main_func.get_page(page, appNameDict, DictID, "home_", query)
        )
    elif query.data.startswith("autoCallback#"):
        data = query.data.split("#")[1]
        if data in core_func.appNameDict or data in appxmethod.appxapis or data in core_func.videoCryptDict or data in core_func.WithoutAppDict:
            if data in appxmethod.appxapis:
                name = appxmethod.appxapis[f"{data}"]["name"]
                await query.answer(f"You clicked {name}", show_alert=True)
                api = appxmethod.appxapis[f"{data}"]["api"]
                await appx.appx_logins(_, query.message, user_id, True, api, name)
                
            elif data in core_func.videoCryptDict:
                name = core_func.videoCryptDict[f"{data}"]["name"]
                await query.answer(f"You clicked {name}", show_alert=True)
                vdocrypt = core_func.videoCryptDict[f"{data}"]["func"].VideoCryptExtractor(name)
                await vdocrypt.start_login(_, query.message, user_id)
                
            elif data in core_func.WithoutAppDict:
                name = core_func.WithoutAppDict[f"{data}"]["name"]
                await query.answer(f"You clicked {name}", show_alert=True)
                await core_func.WithoutAppDict[f"{data}"]["func"](_, query.message, user_id)
                
            else:
                await query.answer(f"You clicked {core_func.appNameDict[f"{data}"]["name"]}", show_alert=True)
                await core_func.appNameDict[f"{data}"]["func"](_, query.message, user_id)
            
        elif data in appxmethod.a_to_zList:
            await query.answer(f"You clicked {appxmethod.a_to_zList[f"{data}"]["name"]}", show_alert=True)
            def get_by_letter(data, letter):
                letter = letter.upper()
                return {k: v for k, v in data.items() if k.startswith(letter)}
            shortDict = get_by_letter(appxmethod.appxapis, appxmethod.a_to_zList[f"{data}"]["name"])
            await query.message.edit_text(
              script.TOOLS_TEXT,
              reply_markup=main_func.get_page(0, shortDict, "AppxShortDict", "tools_")
            )
            
        else:
            await query.answer("Callback Not Found!!")
        
    
        






