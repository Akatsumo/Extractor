import os 
import asyncio
import aiohttp
from Extractor import app
from pyrogram import filters 




@app.on_message(filters.command(""))
async def khan_login(_, message):
    user_id = message.from_user.id
    try:
        async with aiohttp.ClientSession() as session:
            login_url = "https://api.khanglobalstudies.com/cms/login"
            data = {
              "phone": "",
              "password": "",
              "remember": True
            }
            
            msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")                                     
            try:
                input1 = await app.listen(user_id, timeout=30)
                if "*" in input1.text:
                    phone, password = input1.text.split("*")
                    response = await session.post(login_url, data={"phone": phone, "password": password}, headers=headers)
                    if response.status != 200:
                        return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

                    output = await response.json()
                    token = output["token"]      
                else:
                    token = input1.text.strip()
            except:
                return await message.reply_text("⏳ Timeout! Please try again.")

            await input1.delete()
            headers = {
              "Host": "api.khanglobalstudies.com",
              "Authorization": f"Bearer {token}",
              "Accept": "application/json",
              }
            await msg.edit_text("✅ **Login Successful**")

            response = await session.get(f"https://api.khanglobalstudies.com/cms/user/v2/courses", headers=headers)
            batch_data = await response.json()

            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            batch_map = {}
            for data in batch_data:
                batch_list += f"`{data['id']}`  -   **{data['title']}**\n\n"
                batch_map[data['id']] = {"name": data['title'], "slug": data["slug"])

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id)
            course_id = input2.text.strip()
            await input2.delete()

            slug, batch_name = batch_map.get(course_id, "Unknown Batch")
            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            start_time = time.time()
            lectures = await asyncio.create_task(course_extract(session, headers, slug))                                   
            end_time = time.time()
            duration_seconds = end_time - start_time
            elapsed = get_time(duration_seconds)

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(lectures))

            caption = f"**App Name** : `{name.title()}`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`"
            me = await app.get_me()
            big_file_id = me.photo.big_file_id
            thumb = await asyncio.create_task(app.download_media(big_file_id))

            await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
            os.remove(file_name)
            await msg.delete()
            await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        await session.close()
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")



