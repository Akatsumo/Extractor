import os, time, re
import asyncio
import requests 
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


def clean_video_url(video_url):
    if not video_url:
        return None
    match = re.search(r'src="([^"]+)"', video_url)
    return match.group(1).split("?")[0]

async def course_content(session, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0
    url = f"https://civilguruji.com/api/course/getPreFetchedCourseData/{batch_id}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    course = data.get("courseData", {})
    details = course.get("courseDetail", {})
    contents = details.get("courseContents", [])
    
    for content in contents:
        module_name = content.get("courseContentName", "Unnamed Module")
        for sub in content.get("courseSubContents", []):
            sub_name = sub.get("name", "No Title")
            video_url = sub.get("videoUrl", "No Video URL")
            v_count += 1
            lectures.append(f"{module_name}|{sub_name}: {clean_video_url(video_url)}")
  
    return lectures, v_count, p_count

async def civilguriji_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()

    try:
        msg = await message.reply_text("Fetching Civil Guruji All Batches, Please Wait... ")
        url = "https://civilguruji.com/api/course/landing-page-courses"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            return await message.reply_text("Failed to fetch course data. Try again later.")

        batch_data = response.json().get("explorePageData", {}).get("data", {})
        if not batch_data:
            return await msg.edit_text("Not Found Any Batches")
            
        batch_list = "📚 **Available Batches:**\n\n"
        batch_index = {}
        for category, cat_data in batch_data.items():
            for course in cat_data.get("data", []):
                course_id = course.get("_id")
                course_name = course.get("name")
                if course_id and course_name:
                    batch_list += f"🆔 `{course_id}`  |  🎓 {course_name}\n"
                    batch_index[course_id] = course_name

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"

        if len(batch_list) > 4000:
            batch_list_name = f"civilguruji_batchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
        else:
            msg = await message.reply_text(f"{batch_list}\n{caption}")
            batch_file = None

        input2 = await app.listen(user_id=user_id, timeout=30)
        batch_id = input2.text.strip()
        await input2.delete()
        if batch_file:
            await batch_file.delete()

        batch_name = batch_index.get(batch_id)
        if not batch_name:
            return await message.reply_text("**Invalid Batch ID. Please try again.**")

        msg = await message.reply_text(f"**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id, msg))
        end_time = time.time()
        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '_')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Civil Guruji`\n"
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
