import os, time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


# --------------------------- Course-Content --------------------------- #

async def course_content(session, course_id):
    lectures = []
    v_count = 0
    p_count = 0

    url = f"https://online.kpiasdelhi.com/api/v2.4/courses/{course_id}/contents/"

    while url:
        async with session.get(url) as response:
            if response.status != 200:
                break

            contents_data = await response.json()

        url = contents_data.get("next")

        content_results = contents_data.get("results", {}).get("contents", [])

        for result in content_results:
            chapter = result.get("chapter_slug", "Unknown").split("-")[0]
            title = result.get("title", "Unknown")
            content_type = result.get("content_type")
            video_url = result.get("video_url")
            attachment_url = result.get("attachment_url")

            class_link = attachment_url if content_type == "Attachment" else video_url

            if not class_link:
                continue

            try:
                async with session.get(class_link) as class_response:
                    if class_response.status != 200:
                        continue

                    class_data = await class_response.json()

                streams = class_data.get("streams", [])

                if not streams:
                    continue

                if video_url:
                    class_url = streams[0].get("hls_url")
                    v_count += 1
                else:
                    class_url = streams[0].get("doc_url")
                    p_count += 1

                lectures.append(f"{chapter} | {title} : {class_url}")

            except Exception as e:
                print("Error fetching class:", e)
                continue

    return lectures, v_count, p_count



# --------------------------- KP-IAS-Access --------------------------- #

async def kpias_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    try:
        msg = await message.reply_text("**Fetching All KP IAS Batches, Please Wait...**")
        response = session.post("https://online.kpiasdelhi.com/api/v2.4/products/")

        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch KP IAS batches")

        batch_data = response.json().get("results", {}).get("products", [])
        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('courses')[0]}` - **{course.get('title', 'Unknown Batch')}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"KP-IAS-BatchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
        else:
            await msg.edit_text(f"{batch_list}\n{caption}")

        input2 = await app.listen(user_id=user_id, timeout=30)
        batch_id = input2.text.strip()
        await input2.delete()
        if batch_file:
            await batch_file.delete()

        batch_name = next((course["title"] for course in data if str(course["courses"][0]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '_')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `KP IAS`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )
        await main_func.send_file(app, file_name, user_id, caption, thumb)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("**⏳ Oops! Time's Up, You didn’t reply in time.**")
    except Exception as e:
        await message.reply_text(f"**Error**: `{e}`")

  
