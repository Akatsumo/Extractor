import os, time
import asyncio
import requests 
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout

# --------------------------- Course-Content --------------------------- #

async def course_content(session, headers, userId, batch_id):
    lectures, v_count, p_count = [], 0, 0
    response_data = session.get(f"http://api.chandrainstitute.com/live/api.php/app/list/subjects/videos/all/{batch_id}", headers=headers)
    if response_data.status_code != 200:
        return lectures, v_count, p_count
        
    subject_data = response_data.json().get("response", [])
    if not subject_data:
        return lectures, v_count, p_count
        
    for subject in subject_data:
        subject_name = subject.get("subject_name", "N/A").strip().split(":")[1]
        subject_id = subject.get("subject_id")
        data = {
          "course_id": batch_id,
          "subject_id": subject_id,
          "u_id": userId
        }
        response_data = session.post("http://api.chandrainstitute.com/api/v2/api.php/get/class/all/chapters/list", data=data, headers=headers)
        if response_data.status_code != 200:
          continue
        chapter_data = response_data.json().get("response", [])
        if not chapter_data:
          continue
        for chapter in chapter_data:
          chapter_type = chapter.get("chapter_type")
          chapter_name = chapter.get("chapter_name")
          yt_id = chapter.get("youtubeId")
          vimeo_url = chapter.get("vimeo_url")
          if chapter_type == "LECTURE":
            v_count += 1
            v_url = vimeo_url if vimeo_url else f"https://youtu.be/{yt_id}"
            lectures.append(f"{subject_name} | {chapter_name}: {v_url}")
          
    return lectures, v_count, p_count


# --------------------------- StudyIQ-Access --------------------------- #

async def studyiq_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    headers = {
        "Auth": "7b81679d-a829-4476-8dcf-9c3bb4e0c80a"
        "Content-Type": "application/json",
        "User-Agent": "okhttp/4.9.0"
    }
    token = "e4bnfW8GSIC4O4Lpa_ZXax:APA91bGJWbPt4nzDf4HyRgolquBIukYeRNcYCtq1cgbpbOWszyuCd-aWdu7PIp-KBwImte54R1oMSEst2X8G3zFFV2mp-qp1cQJQp_xK2vSyT5LXhauKp5_W6IlZKL_6qD8FpjqGdXCb"
    userId = "886842"
    try:
        if not token:
          msg = await message.reply_text("🔑 Enter login credentials (Mobile*Password or Token)")
          input1 = await app.listen(user_id=user_id, timeout=30)
          raw_data = input1.text.strip()
          await input1.delete()

          if "*" in raw_data:
            mobile, password = raw_data.split("*")
            response = session.get("https://api.chandrainstitute.com/laravel-api/api/v1/login", data={"mobile": mobile, "password": password})
            if response.status_code != 200:
              return await msg.edit_text("😒 Login failed, incorrect credentials.")
            userId = response.json().get("response").get("id")
            token = response.json().get("response").get("token")
          else:
            token = raw_data
            
        headers.update({"token": token})
        data = {
          "user_id": userId,
          "course_type": "videos",
          "payment_type": "unpaid"
        }
        await msg.edit_text("**Fetching All Chandra Institute Batches, Please Wait...**")
      
        response = session.get("http://api.chandrainstitute.com/live/api.php/app/get/all/course", data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch StudyIQ batches")

        batch_data = response.json().get("response", [])
        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('cp_id')}` - **{course.get('title')}**\n"
            
        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None
        
        if len(batch_list) > 4000:
            batch_list_name = f"ChandraInstitute_batchList_{user_id}.txt"
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

        batch_name = next((course["title"] for course in batch_data if str(course["cp_id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, headers, userId, batch_id))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Chandra Institute`\n"
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


