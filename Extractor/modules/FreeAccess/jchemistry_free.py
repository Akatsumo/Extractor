import os
import time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


# --------------------------- Course-Content --------------------------- #

async def course_content(session, batch_id, course_ids):
    lectures, v_count, p_count = [], 0, 0
    for id in course_ids:
        response_data = session.get(
            f"https://jchemistry-api.edmingle.com/nuSource/api/v1/public/tutor/class/curriculum/{id}?institution_bundle_id={batch_id}"
        )
        if response_data.status_code != 200:
            continue

        resources_data = (
            response_data.json().get("course_curriculum", {}).get("resources", [])
        )
        if not resources_data:
            continue

        for resource in resources_data:
            section_name = resource.get("section_name", "N/A")
            for rs in resource.get("resources", []):
                material_id = rs.get("material_id")
                material_name = rs.get("material_name", "N/A")
                material_type = rs.get("type", "N/A")
                is_drm = rs.get("is_drm")
                drm_url = rs.get("drm_url")
                vimeo_url = rs.get("vimeo_url")
                is_enterprise_drm = rs.get("is_enterprise_drm")
                vdocipher_video_id = rs.get("vdocipher_video_id")
                is_videocrypt_drm = rs.get("is_videocrypt_drm")
                videocrypt_video_id = rs.get("videocrypt_video_id")

                if material_type == "video/mp4":
                    url = (
                        f"https://jchemistry-api.edmingle.com/vimeo/{vimeo_url}" if vimeo_url
                        else f"https://vz-70c947c6-972.b-cdn.net/{drm_url}/playlist.m3u8" if is_drm
                        else vdocipher_video_id if is_enterprise_drm
                        else f"https://www.videocrypt.in/drm/{videocrypt_video_id}" if is_videocrypt_drm
                        else None
                    )
                    if url:
                        v_count += 1
                        lectures.append(f"{section_name} | {material_name}: {url}")

                elif material_type == "application/pdf":
                    url = f"https://jchemistry-api.edmingle.com/nuSource/api/v1/student/materials/{material_id}"
                    params = {"class_id": id}
                    headers = {
                        "apikey": "22ed8e8b83fced47fdc6f317dbbae9ad",
                        "orgid": "267"
                    }
                    response = session.get(url, headers=headers, params=params)
                    if response.status_code != 200:
                        continue
                    pdf_url = response.json().get("material", {}).get("url")
                    if pdf_url:
                        p_count += 1
                        lectures.append(f"{section_name} | {material_name}: {pdf_url}")

    return lectures, v_count, p_count


# --------------------------- J-Chemsity-Access --------------------------- #

async def jchemistry_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    msg = await message.reply_text("**Fetching All J Chemistry Batches, Please Wait...**")

    try:
        response = session.get("https://jchemistry-api.edmingle.com/nuSource/api/v1/institute/157/courses")
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch J Chemistry batches")

        course_data = response.json().get("institute_courses", [])
        if not course_data:
            return await msg.edit_text("No course data found.")

        batch_data = []
        batch_list = "📚 **Available Batches:**\n\n"
        for course in course_data:
            course_bundle = course.get("course_bundles")
            if not course_bundle:
                continue
            for bundle in course_bundle:
                batch_data.append({
                    "course_id": bundle.get("institution_bundle_id"),
                    "name": bundle.get("bundle_name"),
                    "course_ids": bundle.get("course_ids"),
                })
                batch_list += f"`{bundle.get('institution_bundle_id')}` - **{bundle.get('bundle_name')}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"Jchemistry_batchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
        else:
            await msg.edit_text(f"{batch_list}\n{caption}")

        input1 = await app.listen(user_id=user_id, timeout=30)
        batch_id = input1.text.strip()
        await input1.delete()
        if batch_file:
            await batch_file.delete()

        batch_name, course_ids = next(((course["name"], course["course_ids"]) for course in batch_data if str(course["course_id"]) == batch_id),(None, None),)

        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")
        if not course_ids:
            return await msg.edit_text("No Course Content Found")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id, course_ids))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
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
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("**⏳ Oops! Time's Up, You didn’t reply in time.**")
    except Exception as e:
        await message.reply_text(f"**Error**: `{e}`")


