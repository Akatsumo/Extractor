import os, time
import asyncio
import requests 
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


async def course_content(session, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0
    response_data = session.get(f"https://coral-app-eymnu.ondigitalocean.app/api/student/course/public/detail/{batch_id}")
    fetch_data = response_data.json().get("data", [])
    if not fetch_data:
        return lectures, v_count, p_count
        
    for item in fetch_data:
        for lesson in item.get("lessons", []):
            title = lesson.get("lesson_title", "No Lesson Title")
            for c in lesson.get("lesson_contents", []):
                if c.get("content_status") != "Queue" and c.get("content_url"):
                    lectures.append(f"{title} | {item.get('content_title','No Content')}: https://vz-c8c7763d-df6.b-cdn.net/{c['content_url']}/playlist.m3u8")
                    v_count += 1
                    
            for rc in lesson.get("lesson_recorded_classes", []):
                if rc.get("content_status") != "Queue" and rc.get("recording_url"):
                    lectures.append(f"{title} | {rc.get('topic','No Topic')}: https://vz-c8c7763d-df6.b-cdn.net/{rc['recording_url']}/playlist.m3u8")
                    v_count += 1
        

    return lectures, v_count, p_count


async def geologicalConcepts_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()

    try:
        msg = await message.reply_text("Fetching All Geological Concepts Batches. Please Wait...")
        api_url = f"https://coral-app-eymnu.ondigitalocean.app/api/student/course/public/list"
        response = session.get(api_url)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Geological Concepts batches")

        data = response.json().get("data", [])
        if not data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in data:
            batch_list += f"`{course.get('course_id')}` - **{course.get('title')}**\n"
            
        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None
        
        if len(batch_list) > 4000:
            batch_list_name = f"{keyword_str}_batchList_{user_id}.txt"
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

        batch_name = next((course["title"] for course in data if str(course["course_id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id, msg))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Geological Concepts`\n"
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



