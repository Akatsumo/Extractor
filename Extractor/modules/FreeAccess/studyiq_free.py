import os, time
import asyncio
import requests 
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout

# --------------------------- Get-Headers --------------------------- #

def get_headers(session):
    url = 'https://backend.studyiq.net/user-auth-ws/v1/auth/generate/admin'
    headers = {
        'api-key': '9A3BDDEEBD4DFB213D3C15D29126151206E47E4F',
        'content-type': 'application/json'
    }
    payload = {
        'platform': 'ADMIN',
        'id': '1013'
    }
    response = session.post(url, headers=headers, json=payload)
    token = response.json()['token']
    return {"Authorization": f"Bearer {token}"}


# --------------------------- Course-Content --------------------------- #

async def course_content(session, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0
    response_data = session.get(
        f"https://backend.studyiq.net/app-content-ws/v2/course/getDetails?courseId={batch_id}",
        headers=get_headers(session)
    )
    if response_data.status_code != 200:
        return lectures, v_count, p_count
        
    fetch_data = response_data.json().get("data", [])
    if not fetch_data:
        return lectures, v_count, p_count
        
    for item in fetch_data:
        name = item.get("name", "")
        video = item.get("videoUrl")
        pdf = item.get("textUploadUrl")
        if video:
            v_count += 1
            lectures.append(f"{name}: {video}")
        if pdf:
            p_count += 1
            lectures.append(f"{name}: {pdf}")

    return lectures, v_count, p_count


# --------------------------- StudyIQ-Access --------------------------- #

async def studyiq_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()

    try:
        msg = await message.reply_text("**Enter a StudyIQ keyword**\n**Example**: upsc, books etc.")
        input1 = await app.listen(user_id=user_id, timeout=30)
        keyword_str = input1.text.strip()
        await input1.delete()

        await msg.edit_text("**Fetching All StudyIQ Batches, Please Wait...**")
        api_url = f"https://www.studyiq.net/api/web/searchbycourses?keyword={keyword_str}"
        response = session.get(api_url)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch StudyIQ batches")

        data = response.json().get("data", [])
        if not data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in data:
            batch_list += f"`{course.get('course_id')}` - **{course.get('course_title')}**\n"
            
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

        batch_name = next((course["course_title"] for course in data if str(course["course_id"]) == batch_id), None)
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
            f.write("\n".join(lectures))

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
        await message.reply_text("**⏳ Oops! Time's Up, You didn’t reply in time.**")
    except Exception as e:
        await message.reply_text(f"**Error**: `{e}`")
