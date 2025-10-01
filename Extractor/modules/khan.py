import os
import asyncio
import aiohttp
import time
from Extractor import app
from pyrogram import filters
from Extractor.core.main_func import get_time


async def khan_extract(session, headers, slug):
    # https://api.khanglobalstudies.com/cms/lessons/lession_id
    lesson_url = f"https://api.khanglobalstudies.com/cms/user/courses/{slug}/lessons"
    response = await session.get(lesson_url, headers=headers)
    
    try:
        output = await response.json()
        lessons = output.get("lessons", [])

        if not lessons:
            print("No lessons found.")
            return []
        
        lectures = []
        
        for lesson in lessons:
            lesson_name = lesson.get("name", "No Lesson Name") 
            
            for video in lesson.get("videos", []):
                video_title = video.get("name", "No Title")
                video_url = video.get("video_url", "No URL")
                lectures.append(f"{video_title}: {video_url}\n")

                pdfs = video.get("pdfs") or []
                for pdf in pdfs:
                    title = pdf.get("title", "No Title")
                    url = pdf.get("url", "No URL")
                    lectures.append(f"{title}: {url}\n")
        
        return lectures
    
    except Exception as e:
        print(f"Error: {e}")
        return []




@app.on_message(filters.command("khan"))
async def khan_login(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
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
                input1 = await app.listen(user_id=user_id, timeout=30)
                if "*" in input1.text:
                    phone, password = input1.text.split("*")
                    async with session.post(login_url, json={"phone": phone, "password": password}) as response:
                        if response.status != 200:
                            return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

                        output = await response.json()
                        token = output.get("token", "")
                else:
                    token = input1.text.strip()
            except asyncio.TimeoutError:
                return await msg.edit_text("⏳ Timeout! Please try again.")

            await input1.delete()

            headers = {
                "Host": "api.khanglobalstudies.com",
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "access-control-allow-origin": "*"
            }

            await msg.edit_text("✅ **Login Successful**")

            async with session.get("https://api.khanglobalstudies.com/cms/user/v2/courses", headers=headers) as response:
                batch_data = await response.json()
                print(batch_data)

            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            batch_map = {}
            for data in batch_data:
                batch_id = str(data["id"])
                batch_name = data["title"]
                slug = data["slug"]
                batch_list += f"`{batch_id}`  -   **{batch_name}**\n\n"
                batch_map[batch_id] = {"name": batch_name, "slug": slug}

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")

            input2 = await app.listen(user_id=user_id)
            course_id = input2.text.strip()
            await input2.delete()

            batch_info = batch_map.get(course_id)
            if not batch_info:
                return await msg.edit_text("❌ Invalid Batch ID. Please try again.")

            slug = batch_info["slug"]
            batch_name = batch_info["name"]

            await msg.edit_text(f"**Extracting Course Content for `{batch_name}` Please Wait 📥**")

            start_time = time.time()
            lectures = await asyncio.create_task(khan_extract(session, headers, slug))
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




