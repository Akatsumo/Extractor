import os
import asyncio
import aiohttp
import time
from Extractor import app
from pyrogram import filters
from Extractor.core.main_func import get_time


async def course_extract(session, headers, params, course_id):
    params.update({"course_id": course_id})
    lesson_url = "https://myrisingindia.in/api_2cderep6masrlen/api/sections"
    response = await session.get(lesson_url, headers=headers, params=params)
    response_output = await response.json()
    for subject in response_output:
        subject_id = subject['subject_id']
        params.update({"subject_id": subject_id})
  
        
    return lectures
    
    




@app.on_message(filters.command("rising"))
async def myrising_login(_, message):
    user_id = message.from_user.id
    try:
        async with aiohttp.ClientSession() as session:
            login_url = "https://myrisingindia.in/api_2cderep6masrlen/api/login"
          
            headers = {
              "user-agent": "Dart/2.19 (dart:io)",
              "accept-encoding": "gzip",
              "host": "myrisingindia.in"
            }
  
            msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
            try:
                input1 = await app.listen(user_id=user_id, timeout=30)
            except:
                return await msg.edit_text("⏳ Timeout! Please try again.")

            if "*" in input1.text.strip():
               username, password = input1.text.split("*")
               params = {
                  "username": username,
                  "password": password,
               }
               response = await session.post(login_url,headers=headers, params=params)

               if response.status != 200:
                  return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
                 
               output_response = await response.json()
               token = output_response["data"]["token"] 
            else:
               token = input1.text.strip()
          
            await input1.delete()
            params = {
              'auth_token': token
            }
            await msg.edit_text("✅ **Login Successful**")
          
            response = await session.get('https://myrisingindia.in/api_2cderep6masrlen/api_new/my_courses', headers=headers, params=params)        
            batch_data = await response.json()

            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
           
            for data in batch_data:
                batch_id = data["id"]
                batch_name = data["title"]
                batch_list += f"`{batch_id}`  -   **{batch_name}**\n\n"

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            try:
                input2 = await app.listen(user_id=user_id, timeout=30)
                course_id = input2.text.strip()
                await input2.delete()
            except:
                return await message.reply_text("⏳ Timeout! Please try again.")

            batch_name = next((course["title"].replace("/", "") for course in batch_data if int(course["id"]) == int(course_id)), "")
            if not batch_name:
                return await msg.edit_text("**Invalid Batch ID. Please try again.**")

            
            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
            start_time = time.time()
            lectures = await asyncio.create_task(course_extract(session, headers, params, course_id))
            end_time = time.time()
            elapsed = get_time(end_time - start_time)

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(lectures))

            caption = f"**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`"
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
