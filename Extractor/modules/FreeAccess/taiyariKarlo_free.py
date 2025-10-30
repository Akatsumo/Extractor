import os, time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


# --------------------------- Course-Content --------------------------- #

async def course_content(session, base_url, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0
    response_data = session.get(f"{base_url}/{batch_id}/lessons")
    if response_data.status_code != 200:
        return lectures, v_count, p_count

    lesson_data = response_data.json().get('documents', [])
    if not lesson_data:
        return lectures, v_count, p_count

    for lesson in lesson_data:
        fields = lesson.get("fields", {})
        subject_name = fields.get("subject", {}).get("stringValue", "N/A")
        lesson_name = fields.get("title", {}).get("stringValue", "N/A")
        lesson_id = lesson.get("name", "").split('/')[-1]

        response_data = session.get(f"{base_url}/{batch_id}/lessons/{lesson_id}/content")
        if response_data.status_code != 200:
            continue

        class_data = response_data.json().get('documents', [])
        if not class_data:
            continue

        for class_doc in class_data:
            c_fields = class_doc.get("fields", {})
            class_title = c_fields.get("title", {}).get("stringValue", "N/A")
            material_type = c_fields.get("type", {}).get("stringValue", "N/A")

            if material_type == "pdf":
                p_count += 1
                url = c_fields.get("ref", {}).get("stringValue", "N/A")
                lectures.append(f"{lesson_name} | {class_title}: {url}")

            elif material_type == "video":
                v_count += 1
                hls_url = c_fields.get("hlsUrl", {}).get("stringValue", "")
                zw_url = c_fields.get("zw_media_url", {}).get("stringValue", "")
                recordings = c_fields.get("recordings", {}).get("arrayValue", {}).get("values", [])
                url = hls_url if hls_url else zw_url
                lectures.append(f"{lesson_name} | {class_title}: {url}")

    return lectures, v_count, p_count


# --------------------------- TaiyariKrlo-Access --------------------------- #

async def taiyarKarlo_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()

    try:
        msg = await message.reply_text("**Fetching Taiyari Karlo All Batches, Please Wait...**")
        base_url = "https://firestore.googleapis.com/v1/projects/taiyari-karlo/databases/(default)/documents/courses"
        response = session.get(f"{base_url}?pageSize=5000")
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Taiyari Krlo batches")

        batch_data = response.json().get('documents', [])
        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            b_id = course.get('name', '').split('/')[-1]
            b_title = course.get("fields", {}).get('title', {}).get('stringValue', 'N/A')
            batch_list += f"`{b_id}` - **{b_title}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"TaiyariKrlo_batchList_{user_id}.txt"
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

        batch_name = next(
            (course.get("fields", {}).get('title', {}).get('stringValue', 'N/A')
             for course in batch_data if str(course.get('name', '').split('/')[-1]) == batch_id),
            None
        )
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, base_url, batch_id, msg))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Taiyari Karlo`\n"
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


