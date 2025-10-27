import os
import time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


async def course_content(session, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0
  
    resp = session.get(f"https://jchemistry-api.edmingle.com/nuSource/api/v1/public/tutor/courses/all/{batch_id}")
    if resp.status_code != 200:
        await msg.edit_text("Failed to fetch course list.")
        return lectures, v_count, p_count

    courses = resp.json().get("courses", [])
    if not courses:
        await msg.edit_text("No courses found for this batch.")
        return lectures, v_count, p_count

    for course in courses:
        course_name = course.get("name")
        course_id = course.get("course_id")
        if not course_id:
            continue

        res = session.get(f"https://jchemistry-api.edmingle.com/nuSource/api/v1/public/tutor/class/curriculum/{course_id}?institution_bundle_id={batch_id}")
        if res.status_code != 200:
            continue

        curriculum = res.json().get("course_curriculum", {}).get("resources", [])
        if not curriculum:
            continue

        for section_group in curriculum:
            for section in section_group.get("sections", []):
                for item in section.get("resources", []):
                    item_type = item.get("type", "")
                    item_name = item.get("material_name", "Unknown")

                    if item_type == "video/mp4":
                        v_count += 1
                        if item.get("is_drm"):
                            url = f"https://jchemistry-api.edmingle.com/vimeo/{item.get('vimeo_url', '')}"
                        else:
                            url = f"https://vz-70c947c6-972.b-cdn.net/{item.get('drm_url', '')}/playlist.m3u8"
                        lectures.append(f"{course_name} | {item_name} : {url}")

                    elif item_type == "application/pdf":
                        p_count += 1
                        pdf_url = item.get("pdf_url", "")
                        lectures.append(f"{course_name} | {item_name} : {pdf_url}")

    return lectures, v_count, p_count



async def jchemistry_access(_, message, user_id=None):
    user_id = user_id or message.from_user.id
    session = requests.Session()

    try:
        msg = await message.reply_text("Fetching J Chemistry batches... Please wait a moment.")
        response = session.get("https://jchemistry-api.edmingle.com/nuSource/api/v1/institute/157/courses")
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch J Chemistry batches.")

        institute_data = response.json().get("institute_courses", [])
        if not institute_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        all_batches = []

        for institute in institute_data:
            course_bundles = institute.get("course_bundles", [])
            for bundle in course_bundles:
                batch_id = bundle.get("institution_bundle_id")
                batch_name = bundle.get("bundle_name")
                if batch_id and batch_name:
                    batch_list += f"`{batch_id}` - **{batch_name}**\n"
                    all_batches.append({"id": str(batch_id), "name": batch_name})

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"JChemistry_batchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
        else:
            await msg.edit_text(f"{batch_list}\n{caption}")

        input2 = await app.listen(user_id=user_id, timeout=60)
        batch_id = input2.text.strip()
        await input2.delete()
        if batch_file:
            await batch_file.delete()

        batch_name = next((b["name"] for b in all_batches if b["id"] == batch_id), None)
        if not batch_name:
            return await msg.edit_text("Invalid Batch ID. Please try again.")

        await msg.edit_text(f"📥 Extracting Course Content, Please Wait...")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id, msg))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No content found in this batch.")

        file_name = f"{batch_name.replace('/', '_')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `J Chemistry`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )
        await main_func.send_file(app, file_name, user_id, caption, thumb)
        os.remove(file_name)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("⏰ You didn’t reply in time. Please try again.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
