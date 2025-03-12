import re
import os
import time
import json
import asyncio
import cloudscraper
from Extractor import app
from pyrogram import filters 
from Extractor.core.main_func import get_time


cookies = {}


async def course_content(session, course_id):
    lectures = []
    params = {
        'view': 'List',
        'batch_type': 'my',
        'id': course_id,
        'type': 'class'
    }
        
    response = session.get("https://web.careerwill.com/_next/data/RqQQCO-Y8ngCTaHq8KW2p/class.json", cookies=cookies, params=params)
    topic_results = response.json().get('pageProps', {}).get('topics', [])
    
    if not topic_results:
        return await msg.edit_text("**Empty Batch Data. Does not exist any data in batch**")

    for topic in topic_results:
        topic_id = topic.get("id", "Unknown")
        lectures.extend(await course_extract(session, course_id, topic_id))
    
    return lectures


async def course_extract(session, course_id, topic_id):
    lectures = []
    params = {
        'view': 'List',
        'batch_type': 'my',
        'id': course_id,
        'type': 'class',
        'topic_id': topic_id
    }
        
    response = session.get("https://web.careerwill.com/_next/data/RqQQCO-Y8ngCTaHq8KW2p/class.json", cookies=cookies, params=params)
    classes_results = response.json().get('pageProps', {}).get("batchClassData", {}).get("classes", [])

    for topic in classes_results:
        name = topic.get("lessonName", "Unknown")
        url = topic.get("lessonUrl", "Url Not Found")
        if "youtube" == topic.get("lessonExt", ""):
            lectures.append(f"{name}: http://www.youtube.com/watch?v={url}")
        else:
            lectures.append(f"{name}: http://www.youtube.com/watch?v={url}")
   
    params.update({'type': 'notes', 'notes_type': 'notes'})
    response = session.get("https://web.careerwill.com/_next/data/RqQQCO-Y8ngCTaHq8KW2p/class.json", cookies=cookies, params=params)
    notes_results = response.json().get('pageProps', {}).get("notesData", {}).get("notesDetails", {})
    
    for note in notes_results:
        name = note.get("docTitle", "Unknown")
        url = note.get("docUrl", "Url Not Found")
        if url:
            lectures.append(f"{name}: {url}")
        else:
            continue
    
    return lectures




@app.on_message(filters.command("cw"))
async def careerwill_login(_, message):
    user_id = message.from_user.id
    try:
        session = cloudscraper.create_scraper()
        login_url = "https://wbspec.crwilladmin.com/api/v1/login"
        msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
        
        try:
            input1 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")
        
        token = None  

        if "*" in input1.text:
            userid, password = input1.text.split("*")
            response = session.post(login_url, json={"userid": userid, "pwd": password})

            if response.status_code != 200:
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            output = response.json()
            token = output.get("data", {}).get("token")  
            if not token:
                return await msg.edit_text("😒 **Login failed, token missing.**")
        else:
            token = input1.text.strip()  

        await input1.delete()
        cookies.update({'token': token})  
        await msg.edit_text("✅ **Login Successful**")
 
        response = session.get(
            "https://web.careerwill.com/_next/data/RqQQCO-Y8ngCTaHq8KW2p/live-classes.json?view=List&batch_type=my",
            cookies=cookies
        )
        if response.status_code != 200:
            return await msg.edit_text("😒 **Failed to fetch live classes.**")

        batch_data = response.json().get('pageProps', {}).get('myBatchData', [])
       
        if not batch_data:
            return await msg.edit_text("No batch data found.")

        batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
        for data in batch_data:
            batch_list += f"`{data['id']}`  -   **{data['batchName']}**\n\n"

        await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
        
        try:
            input2 = await app.listen(user_id=user_id, timeout=30)
            course_id = input2.text.strip()
            await input2.delete()
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        batch_name = next(
            (course["batchName"] for course in batch_data if int(course["id"]) == int(course_id)), ""
        )
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
        start_time = time.time()
        lectures = await asyncio.create_task(course_content(session, course_id))
        end_time = time.time()
        duration_seconds = end_time - start_time
        elapsed = get_time(duration_seconds)

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w") as f:
            f.write("\n".join(lectures))

        caption = f"**App Name** : `CAREERWILL`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed}`"
        me = await app.get_me()
        big_file_id = me.photo.big_file_id
        thumb = await asyncio.create_task(app.download_media(big_file_id))

        await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
        os.remove(file_name)
        await msg.delete()
        await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

    except Exception as e:
        await message.reply_text(f"Error: `{str(e)[::40]}`")
        print(f"Error: {str(e)}")





