import os, time
import asyncio
import aiohttp
from Extractor import app
from pyrogram import filters
from Extractor.core import main_func


class KhanExtractor:
    def __init__(self):
        self.login_url = "https://api.khanglobalstudies.com/cms/login"
        self.paid_courses_url = "https://api.khanglobalstudies.com/v1/courses/paid"
        self.lessons_url = "https://api.khanglobalstudies.com/cms/user/courses/{slug}/lessons"

    async def extract_lessons(self, session, headers, slug):
        try:
            async with session.get(self.lessons_url.format(slug=slug), headers=headers) as response:
                output = await response.json()
            lessons = output.get("lessons", [])
            if not lessons:
                return []
            lectures = []
            for lesson in lessons:
                for video in lesson.get("videos", []):
                    video_title = video.get("name", "No Title")
                    video_url = video.get("video_url", "No URL")
                    lectures.append(f"{video_title}: {video_url}")
                    pdfs = video.get("pdfs") or []
                    for pdf in pdfs:
                        title = pdf.get("title", "No Title")
                        url = pdf.get("url", "No URL")
                        lectures.append(f"{title}: {url}")
            return lectures
        except Exception as e:
            print(f"Error: {e}")
            return []

    async def get_batches(self, session, headers):
        async with session.get(self.paid_courses_url, headers=headers) as response:
            output = await response.json()
        batch_data = output if isinstance(output, list) else output.get("data", [])
        batch_map = {}
        batch_courses = "📚 **Available Batches:**\n\n"
        for data in batch_data:
            batch_id = str(data.get("id"))
            batch_name = data.get("title", "No Title")
            slug = data.get("slug", "")
            batch_courses += f"`{batch_id}`  -   **{batch_name}**\n"
            batch_map[batch_id] = {"name": batch_name, "slug": slug}
        return batch_courses, batch_map

    async def start_login(self, app, message, user_id=None):
        user_id = user_id or message.from_user.id
        try:
            async with aiohttp.ClientSession() as session:
                msg = await message.reply_text("🔑 Enter login credentials (Mobile*Password or Token): ")
                input1 = await app.listen(user_id=user_id, timeout=30)
                creds = input1.text.strip()
                await input1.delete()

                if "*" in creds:
                    phone, password = creds.split("*", 1)
                    async with session.post(self.login_url, json={"phone": phone, "password": password}) as response:
                        if response.status != 200:
                            return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
                        output = await response.json()
                        token = output.get("token")
                else:
                    token = creds

                headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
                batch_courses, batch_map = await self.get_batches(session, headers)
                await msg.edit_text(f"{batch_courses}\n**📊 Now send the Batch ID to Download**")

                input2 = await app.listen(user_id=user_id)
                batch_id = input2.text.strip()
                await input2.delete()
                batch_info = batch_map.get(batch_id)

                if not batch_info:
                    return await msg.edit_text("❌ Invalid Batch ID. Please try again.")

                slug = batch_info["slug"]
                batch_name = batch_info["name"]
                await msg.edit_text(f"**Extracting Course Content for `{batch_name}` Please Wait 📥**")

                start_time = time.time()
                lectures = await asyncio.create_task(self.extract_lessons(session, headers, slug))
                end_time = time.time()
                elapsed = main_func.get_time(end_time - start_time)

                file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write("\n".join(lectures[::-1]))

                caption = f"**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`"
                me = await app.get_me()
                big_file_id = me.photo.big_file_id
                thumb = await app.download_media(big_file_id)

                await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
                os.remove(file_name)
                await msg.delete()
                await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        except ListenerTimeout:
            await message.reply_text("⏳ Timeout! Please try again.")
        except Exception as e:
            await message.reply_text(f"Error: `{e}`")
        


@app.on_message(filters.command("khan"))
async def khan_handler(_, message, user_id=None):
    extractor = KhanExtractor()
    await extractor.start_login(_, message, user_id)
