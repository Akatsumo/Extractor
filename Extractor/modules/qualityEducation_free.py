
import os
import time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


async def course_content(session, headers, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0
    response_data = session.get(f"https://test.qualityeducation.in/api/combo-get/318096/{batch_id}", headers=headers)
    if response_data.status_code != 200:
        return lectures, v_count, p_count
    fetch_data = response_data.json().get("data", {}).get("video", [])
    if not fetch_data:
        return lectures, v_count, p_count

    for item in fetch_data:
        video_id = item.get("id")
        if not video_id:
            continue

        response_data = session.get(f"https://test.qualityeducation.in/api/subject-get/{video_id}", headers=headers)
        if response_data.status_code != 200:
            continue
        subject_data = response_data.json().get("data", [])
        if not subject_data:
            continue
            
        for subject in subject_data:
            subject_id = subject.get("id")
            if not subject_id:
                continue

            response_data = session.get(f"https://test.qualityeducation.in/api/subject-get/{video_id}/{subject_id}", headers=headers)
            if response_data.status_code != 200:
                continue
            topic_data = response_data.json().get("data", [])
            if not topic_data:
                continue

            for topic in topic_data:
                topic_name = topic.get("topic_name", "Untitled")
                pdf_url = topic.get("pdf_link")
                video_url = topic.get("quality_1080") or topic.get("quality_720")

                if video_url:
                    lectures.append(f"{topic_name}: {video_url}")
                    v_count += 1
                if pdf_url:
                    lectures.append(f"{topic_name}: {pdf_url}")
                    p_count += 1

    return lectures, v_count, p_count



async def qualityEducation_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    headers = {
        "Host": "test.qualityeducation.in",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.7"
    }

    try:
        msg = await message.reply_text("Fetching all Quality Education batches, please wait...")
        response = session.get("https://test.qualityeducation.in/api/video-category-get", headers=headers)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Quality Education batches.")

        data = response.json().get("data", [])
        if not data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in data:
            batch_list += f"`{course.get('id')}` - **{course.get('category_name', 'Unnamed')}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to download**"
        batch_file = None
        
        if len(batch_list) > 4000:
            batch_list_name = f"QualityEducation_batchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
        else:
            await msg.edit_text(f"{batch_list}\n{caption}")

        input_msg = await app.listen(user_id=user_id, timeout=30)
        batch_id = input_msg.text.strip()
        await input_msg.delete()
        if batch_file:
            await batch_file.delete()

        batch_name = next((course["category_name"] for course in data if str(course["id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("Invalid Batch ID. Please try again.")

        await msg.edit_text("📥 Extracting Course Content, please wait...")
        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content, session, headers, batch_id, msg)
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No batch content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Quality Education`\n"
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
        await message.reply_text(f"Error: `{str(e)}`")


