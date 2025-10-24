import os
import time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


async def course_content(session, headers, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0

    response_data = session.post(
        "https://testpaperlive.com/api/app/v2/package_chapter_list",
        data=f"package_id={batch_id}",
        headers=headers
    )
    if response_data.status_code != 200:
        return lectures, v_count, p_count

    topic_data = response_data.json().get("data", [])
    if not topic_data:
        return lectures, v_count, p_count

    for topic in topic_data:
        chapter_id = topic.get("id")
        response_data = session.post(
            "https://testpaperlive.com/api/app/v2/package_chapter_item_list",
            data=f"package_ch_id={chapter_id}",
            headers=headers
        )
        if response_data.status_code != 200:
            return lectures, v_count, p_count

        fatch_data = response_data.json().get("data", [])
        if not fatch_data:
            continue

        for item in fatch_data: 
            item_id = item.get("id")
            item_name = item.get("name")
            item_type = item.get("type")
            post_data = {"item_id": item_id, "type": item_type}

            response = session.posy(
                f"https://testpaperlive.com/api/app/item_data_list",
                headers=headers,
                data=post_data
            )
            item_data = response.json()

            if item_type == "video":
                url = f"https://youtu.be/{item_data.get('data').get('video').get('youtube_id')}"
                v_count += 1
                lectures.append(f"{item_name}: {url}")
            else:
                url = item_data.get("data").get("notes").get("notes")
                p_count += 1
                lectures.append(f"{item_name}: {url}")

    return lectures, v_count, p_count


async def testpaper_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    token = "137653HlQcjwDDHHgnCDXEUqYm5jtPy5ti1FGeCqjBNwMW"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': "okhttp/4.11.0",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
    }

    try:
        msg = await message.reply_text("Fetching All Test Paper Batches. Please Wait...")

        if not token:
            await msg.edit_text("🔑 Enter login credentials (Mobile*Password or Token):")
            input1 = await app.listen(user_id=user_id, timeout=30)
            raw_text = input1.text.strip()
            await input1.delete()

            if "*" in raw_text:
                user_id_input, password = raw_text.split("*")
                payload = f"mobile={user_id_input}&password={password}&device_type=android&device_token=test&app_version=1.0.42&app_version_code=42"
                response = session.post(
                    "https://testpaperlive.com/api/app/v2/login",
                    data=payload,
                    headers=headers
                )
                if response.status_code != 200:
                    return await msg.edit_text("Failed to Fetch Test Paper Token.")
                token = response.json().get("data").get("token")

        headers.update({"auth": token}) 

        response_data = session.get("https://testpaperlive.com/api/app/v2/home", headers=headers)
        if response_data.status_code != 200:
            return await msg.edit_text("Failed to fetch Test Paper batches")

        batch_data = response_data.json().get("data", {}).get("package_list", [])

        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('id')}` - **{course.get('name')}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"TestPaper_batchList_{user_id}.txt"
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

        batch_name = next((course["name"] for course in batch_data if str(course["id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, headers, batch_id, msg))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Study IQ`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )
        await main_func.send_file(app, file_name, user_id, caption, thumb)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("⏰ You didn’t reply in time. Please try again.")
    except Exception as e:
        await message.reply_text(f"Error: `{e}`")
