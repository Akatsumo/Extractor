import os, asyncio
import requests, time
from Extractor import app
from Extractor.core import main_func


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


async def course_content(session, batch_id, msg):
    response_data = session.get(f"https://backend.studyiq.net/app-content-ws/v2/course/getDetails?courseId={batch_id}", headers=get_headers(session))
    fetch_data = response_data.json().get("data", [])
    if not fetch_data:
        return await msg.edit_text("No Batch data Content found.")

    lectures = []
    for item in fetch_data:
        name = item.get("name", "")
        video = item.get("videoUrl")
        pdf = item.get("textUploadUrl")
        if video:
            lectures.append(f"{name}: {video}")
        if pdf:
            lectures.append(f"{name}: {pdf}")
            
    return lectures





async def studyiq_access(_, message, user_id):
    user_id = user_id if user_id else message.from_user.id
    try:
        msg = await message.reply_text("Enter a study IQ keyword\nExample: upsc, books etc.")
        input1 = await app.listen(user_id=user_id, timeout=30) 
        keyword_str = input1.text
        await input1.delete()
        api_url = f"https://www.studyiq.net/api/web/searchbycourses?keyword={keyword_str}"
        response = requests.get(api_url)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch study iq batches")
            
        data = response.json().get("data", [])
        if not data:
            return await msg.edit_text("No course data found.")
            
        batch_List = "📚 **Available Batches:**\n\n"
        for course in data:
            batch_List += f"`{course.get('course_id')}` - **{course.get('course_title')}**\n"
            
        if len(batch_List) > 4000:  
            batchListName = f"{keyword_str}_batchList_{user_id}.txt"
            with open(batchListName, "w") as f:
                f.write("\n".join(batch_List[::-1]))
            await message.reply_doucment(batchListName)
            await msg.edit_text(f"**📊 Now send the Batch ID to Download**")
        else:
            await msg.edit_text(f"{batch_list}\n**📊 Now send the Batch ID to Download**")
            
        input2 = await app.listen(user_id=user_id, timeout=30)
        batch_id = input2.text.strip()
        await input2.delete()
        batch_name = next((course["course_title"] for course in data if int(course["course_id"]) == int(batch_id)), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
        start_time = time.time()
        lectures = await asyncio.create_task(course_content(session, batch_id, msg))
        end_time = time.time()

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = f"**App Name** : `Study IQ`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed}`"

        me = await app.get_me()
        thumb = await app.download_media(me.photo.big_file_id)
        await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
        os.remove(file_name)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("Oops! You didn't reply in time. ⏰")
    except Exception as e:
        await message.reply_text(f"Error: `{e}`")
           
        
        
            





    







    
    
