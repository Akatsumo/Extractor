import os
import time
import re
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


lectures, v_count, p_count = [], 0, 0
# --------------------------- Get-Org-ID --------------------------- #

async def classplus_org_id(org_id, session):
    async with session.get(f"https://{org_id}.courses.store") as response:
        html_content = await response.text()
        org_id_match = re.search(r'"orgId":(\d+)', html_content)
        name_match = re.search(r'"name":"([^"]+)"', html_content)
        org_id = org_id_match.group(1) if org_id_match else None
        name = name_match.group(1) if name_match else None
        return org_id, name

# --------------------------- Formats-Urls --------------------------- #

async def format_urls(content_name, video_thumb, drm_procted):
    global lectures

    if "cpvideocdn.testbook.com" in video_thumb:
        video_id = video_thumb.split('/')[4]
        video_url = f"https://cpvod.testbook.com/{video_id}/playlist.m3u8"

    elif "media-cdn.classplusapp.com" in video_thumb:
        parts = video_thumb.split('/')

        if "drm" in video_thumb:
            video_id = video_thumb.split('/')[5]
            video_url = f"https://media-cdn.classplusapp.com/drm/{video_id}/playlist.m3u8"
            
        elif "tencdn" in video_thumb:
            video_id = parts[-2]
            video_url = f'https://tencdn.classplusapp.com/{video_id}/master.m3u8'

        elif "cc" in video_thumb or "lc" in video_thumb:
            video_url = video_thumb.replace("thumbnail.png", "master.m3u8")
            
        elif "snapshots" in video_thumb and len(parts) >= 8:
            parts[3] = "alisg-cdn-a.classplusapp.com"
            parts = [p for i, p in enumerate(parts) if i not in [4, 6, 7]]
            video_url = f"{'/'.join(parts)}/master.m3u8"

        elif "vod-9a3dfb" in video_thumb:
            video_id = url.split('/')[5]
            video_url = f'https://media-cdn.classplusapp.com/alisg-cdn-a.classplusapp.com/{video_id}/master.m3u8'

        elif "videos" in video_thumb and len(parts) == 6 and "4b06bf8d61c41f8310af9b2624459378203740932b456b07fcf817b737fbae27" in video_thumb:
            parts[3] = "alisg-cdn-a.classplusapp.com"
            parts[4] = "b08bad9ff8d969639b2e43d5769342cc62b510c4345d2f7f153bec53be84fe35"
            file_name = parts[-1]
            parts[-1] = file_name.replace(".jpeg", "/master.m3u8")
            video_url = "/".join(parts)
        else:
            return

    else:
        return

    lectures.append(f"{content_name}: {video_url}")


# --------------------------- Course-Content --------------------------- #

async def course_content(session, headers, batch_id, msg, folder_id="0", org_id=None):
    global lectures, v_count, p_count

    encoded_data = main_func.encode_base64(
        f'{{"courseId":{batch_id},"tutorId":null,"orgId":{org_id},"categoryId":null}}'
    )
    params = {"folderId": folder_id, "limit": "500", "offset": "0"}
    response = session.get(
        f"https://api.classplusapp.com/v2/course/preview/content/list/{encoded_data}",
        headers=headers,
        params=params,
    )

    content_data = response.json().get("data", [])
    if not content_data:
        return lectures, v_count, p_count

    for content in content_data:
        content_id = content.get("id")
        content_name = content.get("name")
        content_type = content.get("contentType")

        if content_type == 1:
            print("----- > Folder")
            await course_content(session, headers, batch_id, msg, content_id, org_id)
        elif content_type == 2:
            print("----- > Video")
            video_thumb = content.get("thumbnailUrl")
            video_type = content.get("drmProtected")
            if not video_thumb:
                continue
            v_count += 1
            await format_urls(content_name, video_thumb, video_type)
        elif content_type == 3:
            print("----- > PDF")
    return lectures, v_count, p_count


# --------------------------- Classplus-Access --------------------------- #

async def classplus_access(_, message, user_id=None):
    user_id = user_id or message.from_user.id
    session = requests.Session()
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "EN",
        "api-version": "22",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    }

    try:
        msg = await message.reply_text("**Send me the Classplus APK ORG ID**")
        input_msg = await app.listen(user_id=user_id)
        apk_org_id = input_msg.text.strip()
        await input_msg.delete()

        import aiohttp
        async with aiohttp.ClientSession() as aio_session:
            org_id, apk_name = await classplus_org_id(apk_org_id, aio_session)

        if not org_id:
            return await message.reply_text("Invalid APK Org ID.")

        encoded_data = main_func.encode_base64(
            f'{{"tutorId":null,"orgId":{org_id},"categoryId":null}}'
        )
        url = f"https://api.classplusapp.com/v2/course/preview/similar/{encoded_data}"
        params = {
            "filterId": "[1]",
            "sortId": "[7]",
            "subCatList": "",
            "mainCategory": "0",
            "limit": "500",
            "offset": "0",
        }

        response = session.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch batches.")

        courses = response.json().get("data", {}).get("coursesData", [])
        if not courses:
            return await msg.edit_text("No batches found for this Org ID.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in courses:
            name = course.get("name", "N/A").strip()
            course_id = course.get("id", "N/A")
            batch_list += f"`{course_id}` - **{name}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"classplus_batchList_{user_id}.txt"
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

        batch_name = next((c["name"] for c in courses if str(c["id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, headers, batch_id, msg, org_id=org_id))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No content found in this batch.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `{apk_name} | Classplus`\n"
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


