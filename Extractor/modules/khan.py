import os
import time
import aiohttp
import asyncio
from pyrogram import filters
from Extractor import app
from Extractor.core.main_func import get_time


class KhanExtractor:
    BASE_URL = "https://api.khanglobalstudies.com"
    LOGIN_URL = f"{BASE_URL}/cms/login"
    COURSES_URL = f"{BASE_URL}/v1/courses/paid"
    LESSON_URL_TEMPLATE = f"{BASE_URL}/cms/user/courses/{{slug}}/lessons"

    def __init__(self):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000))

    async def close(self):
        await self.session.close()

    async def _request(self, method: str, url: str, **kwargs):
        for attempt in range(3):
            try:
                async with self.session.request(method, url, timeout=aiohttp.ClientTimeout(total=30), **kwargs) as res:
                    if res.status == 200:
                        return await res.json()
                    else:
                        text = await res.text()
                        raise Exception(f"HTTP {res.status}: {text[:150]}")
            except asyncio.TimeoutError:
                if attempt == 2:
                    raise Exception("Request timed out.")
                await asyncio.sleep(1)
            except Exception as e:
                if attempt == 2:
                    raise
                await asyncio.sleep(1)
        return None

    async def login(self, phone: str, password: str):
        data = {"phone": phone, "password": password, "remember": True}
        output = await self._request("POST", self.LOGIN_URL, json=data)
        return output.get("token")

    async def get_batches(self, headers):
        return await self._request("GET", self.COURSES_URL, headers=headers)

    async def extract_lessons(self, headers, slug):
        url = self.LESSON_URL_TEMPLATE.format(slug=slug)
        data = await self._request("GET", url, headers=headers)
        lessons = data.get("lessons", [])
        lectures = []
        for lesson in lessons:
            lesson_name = lesson.get("name", "Unnamed Lesson")
            for video in lesson.get("videos", []):
                title = video.get("name", "Untitled Video")
                video_url = video.get("video_url", "No URL")
                lectures.append(f"{lesson_name} - {title}: {video_url}")
                for pdf in video.get("pdfs", []):
                    pdf_title = pdf.get("title", "Untitled PDF")
                    pdf_url = pdf.get("url", "No URL")
                    lectures.append(f"{pdf_title}: {pdf_url}")
        return lectures


@app.on_message(filters.command("khan"))
async def khan_handler(_, message, user_id=None):
    extractor = KhanExtractor()
    user_id =  user_id if user_id else message.from_user.id
    msg = await message.reply_text("**🔑 Please send your credentials in this format:**\n`phone*password`")
    try:
        user_input = await app.listen(user_id=user_id, timeout=45)
        if "*" not in user_input.text:
            await msg.edit_text("❌ Invalid format! Use `phone*password`.")
            return
        phone, password = user_input.text.strip().split("*")
        await user_input.delete()
        await msg.edit_text("🔐 Logging in...")
        token = await extractor.login(phone, password)
        if not token:
            return await msg.edit_text("😒 **Login failed. Invalid credentials.**")
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        await msg.edit_text("✅ Login successful!\nFetching your batches...")
        batch_data = await extractor.get_batches(headers)
        if not batch_data or not isinstance(batch_data, list):
            return await msg.edit_text("❌ No paid batches found.")
        batch_map = {}
        batch_list = "**BATCH ID  -  BATCH NAME**\n\n"
        for item in batch_data:
            batch_id = str(item.get("id"))
            name = item.get("title", "Unnamed Batch")
            slug = item.get("slug", "")
            batch_map[batch_id] = {"name": name, "slug": slug}
            batch_list += f"`{batch_id}`  -  **{name}**\n\n"
        await msg.edit_text(f"{batch_list}\n\n📊 **Send a Batch ID to extract content.**")
        batch_input = await app.listen(user_id=user_id, timeout=45)
        batch_id = batch_input.text.strip()
        await batch_input.delete()
        if batch_id not in batch_map:
            return await msg.edit_text("❌ Invalid Batch ID. Try again.")
        batch_info = batch_map[batch_id]
        slug = batch_info["slug"]
        batch_name = batch_info["name"]
        await msg.edit_text(f"📥 Extracting `{batch_name}` content... Please wait.")
        start = time.time()
        lectures = await extractor.extract_lessons(headers, slug)
        elapsed = get_time(time.time() - start)
        if not lectures:
            return await msg.edit_text("⚠️ No materials found for this batch.")
        safe_name = batch_name.replace("/", "_").strip()
        file_name = f"{safe_name}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))
        caption = f"**Batch:** `{batch_name}`\n📚 **Total Materials:** `{len(lectures)}`\n⏱ **Time Taken:** `{elapsed}`"
        me = await app.get_me()
        thumb = await app.download_media(me.photo.big_file_id)
        await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
        os.remove(file_name)
        await msg.delete()
        await message.reply_text(f"✅ Done\n\n🔑 **Token:** `{token}`")
    except asyncio.TimeoutError:
        await msg.edit_text("⌛ Timeout! Please send details within 45 seconds.")
    except Exception as e:
        await message.reply_text(f"❌ Error: `{e}`")
    finally:
        await extractor.close()
