import os, time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout

categories = [
    {"id": 0, "batchCat_name": "All"},
    {"id": 58, "batchCat_name": "SSC"},
    {"id": 22, "batchCat_name": "Banking"},
    {"id": 7, "batchCat_name": "Teaching"},
    {"id": 8, "batchCat_name": "Defence"},
    {"id": 62, "batchCat_name": "State Exams"},
    {"id": 2, "batchCat_name": "Subject Special"},
    {"id": 35, "batchCat_name": "Recorded Batches"},
    {"id": 3, "batchCat_name": "UPSC IAS/PCS"},
    {"id": 40, "batchCat_name": "Railway⁄JE⁄ITI/Engg."},
    {"id": 42, "batchCat_name": "Free Batches"}
]


async def course_content(base_url, session, cookies, batch_type, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0

    params = {"batch_type": batch_type, "view": "List", "interface_id": "1", "id": batch_id, "type": "class", "topic_id": ""}

    def fetch_data(topic_id):
        nonlocal v_count, p_count

        params["topic_id"] = topic_id
        response = session.get(f"{base_url}/class.json", cookies=cookies, params=params)
        data = response.json().get("pageProps", {})
        classes_results = data.get("batchClassData", {}).get("classes", [])
        notes_results = data.get("notesData", {}).get("notesDetails", [])

        for topic in classes_results:
            name = topic.get("lessonName", "Unknown")
            class_id = topic.get("id", "Unknown")
            url = topic.get("lessonUrl", "Url Not Found")
            ext = topic.get("lessonExt", "")

            if ext in ["youtube", "brightcove", "vdocrypt"]:
                player_params = {
                    "batch_type": "my",
                    "view": "Grid",
                    "id": batch_id,
                    "type": "class",
                    "class_id": class_id
                }
                player_res = session.get(f"{base_url}/player.json", cookies=cookies, params=player_params)
                player_json = player_res.json().get("pageProps", {})
                details = player_json.get("classDetailsData")

                if not details:
                    continue
                v_count += 1

                if ext == "youtube":
                    video_id = details.get("lessonUrl", "")
                    lectures.append(f"{name}: https://www.youtube.com/embed/{video_id}")

                elif ext == "brightcove":
                    stream_token = player_json.get("streamToken", {}).get("token")
                    lesson_url = details.get("lessonUrl", "")
                    lectures.append(f"{name}: https://edge.api.brightcove.com/playback/v1/accounts/6206459123001/videos/{lesson_url}/master.m3u8?bcov_auth={stream_token}")

                elif ext == "vdocrypt":
                    video_link = details.get("lessonUrl", "")
                    lectures.append(f"{name}: https://crwilladmin.com/drm/{video_link}")

            else:
                v_count += 1
                lectures.append(f"{name}: {url}")

        for note in notes_results:
            name = note.get("docTitle", "Unknown")
            url = note.get("docUrl", "")
            if url:
                p_count += 1
                lectures.append(f"{name}: {url}")

    response = session.get(f"{base_url}/class.json", cookies=cookies, params=params)
    topic_results = response.json().get("pageProps", {}).get("topics", [])

    if not topic_results:
        return lectures, v_count, p_count

    for topic in topic_results:
        topic_id = topic.get("id", "")
        fetch_data(topic_id)

    return lectures, v_count, p_count


async def careerwill_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json"
    }
    
    base_url = "https://web.careerwill.com/_next/data/d6TLWFsLIZYvlrxcFML9V"
    cookies = {}
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NjEzMjc3ODQsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiIiLCJpZCI6IlVsSm5lRkpyTjNwNVZ6SkdVR1JTVGsweFRucFVRVDA5IiwiZmlyc3RfbmFtZSI6IlExSkNWVEpXYm5CRmJrVlVSM0ZOUWxCVVFUTnVRVDA5IiwiZW1haWwiOiJkbHB1YjFKVFpuWlNVVEpIUW1KaGIyZGxRamNyTjNseFREUnNaMnQyZDFvM2F6TmhOMXBHVDBObmN6MD0iLCJwaG9uZSI6IlowZGpiMkZ6Y0ZaSE5qUnVTWE4wTldKdE9VWm9VVDA5IiwiYXZhdGFyIjoiIiwicmVmZXJyYWxfY29kZSI6IlpIWnlabEJtZUhWSU0xWTRSSEZxV2pKQmVrUjRkejA5IiwiZGV2aWNlX3R5cGUiOiJ3ZWIiLCJkZXZpY2VfdmVyc2lvbiI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDEuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImRldmljZV9tb2RlbCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDEuMC4wLjAgU2FmYXJpLzUzNy4zNiIsInJlbW90ZV9hZGRyIjoiMTIyLjE2Mi4xNDQuMTA4LDEyMi4xNjIuMTQ0LjEwIn19.LxVcuNucqPgh7W2aUxEkk2ak5Lkf8m67fFmmCk7RQGhL1KWO16f6qE8M88ai_GH9ZzZ23D4Jza9vbYAUGe0Hb17mcpJaAb9Qwzt4x5d1OSqHEbpzwQzfA2dk1vgDFeTMI8H7wVO3UVsHkTsXTQtfFOrcfsA3DLjmRiECfF4U3QnNeLqmIP2ZOyA3_0vFUrGt6u2sHga-EY5AmG6aZSCYurMhmBYLtQy4sceh8yC6B9pwrcishsH96EPiMxn-iJMbDqtcsj3SlTzsgOfaz3Sk6EzLLd-co1duOTQ5eKeE1nC4jVvycMA4QGno4Rkyy1J-7PBPgEZJ6eL9f2I5v8utWQ" 

    try:
        msg = await message.reply_text("Fetching all Careerwill categories... Please wait!")

        if not token:
            login_url = "https://wbspec.crwilladmin.com/api/v1/login"
            headers["cwkey"] = main_func.get_enc_key()
            msg = await message.reply_text("🔑 Enter login credentials (Mobile*Password or Token)")
            input1 = await app.listen(user_id=user_id, timeout=30)
            if "*" in input1.text:
                userid, password = input1.text.split("*")
                response = session.post(login_url, headers=headers, json={"userid": userid, "pwd": password})
                if response.status_code != 200:
                    return await msg.edit_text("😒 Login failed, incorrect credentials.")
                token = response.json().get("data", {}).get("token")
                await input1.delete()

        cookies.update({"token": token})

        # Show categories
        category_text = "📚 **Available Categories:**\n\n"
        for cat in categories:
            category_text += f"`{cat['id']}` - **{cat['batchCat_name']}**\n"

        await msg.edit_text(f"{category_text}\n**📊 Now send the Category ID to download.**")
        input2 = await app.listen(user_id=user_id, timeout=30)
        category_id = input2.text.strip()
        await input2.delete()

        batch_type = next((cat["batchCat_name"] for cat in categories if str(cat["id"]) == category_id), None)
        if not batch_type:
            return await msg.edit_text("**Invalid Category ID. Please try again.**")

        params = {"batch_type": batch_type, "view": "Grid", "interface_id": "1", "cat_id": category_id}
        response = session.get(f"{base_url}/live-classes.json", headers=headers, cookies=cookies, params=params)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Careerwill batches.")

        batch_data = response.json().get("pageProps", {}).get("liveClasses", [])
        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('id')}` - **{course.get('batchName')}**\n"

        caption = "**📊 Now send the Batch ID to Download**"
        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"Careerwill_batchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
        else:
            await msg.edit_text(f"{batch_list}\n{caption}")

        input3 = await app.listen(user_id=user_id, timeout=30)
        batch_id = input3.text.strip()
        await input3.delete()
        if batch_file:
            await batch_file.delete()

        batch_name = next((course["batchName"] for course in batch_data if str(course["id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(
            course_content(base_url, session, cookies, batch_type, batch_id, msg)
        )
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Careerwill`\n"
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
        await message.reply_text(f"⚠️ Error: `{e}`")




