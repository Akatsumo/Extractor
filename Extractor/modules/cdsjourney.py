
import re
import os
import time
import json
import asyncio
import requests
from Extractor import app
from pyrogram import filters 
from bs4 import BeautifulSoup
from Extractor.core.main_func import get_time


cookies = {}


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'referer': ''   
}


async def gen_csrftoken(session):
    url = "https://www.cdsjourney.com/"
    response = session.get(url) 
    if response.status_code == 200:
        cookies = response.cookies
        csrftoken = cookies.get('csrftoken')
        return csrftoken
    else:
        return None

# ----------------------- Course-Extract ----------------------- #

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
        class_id = topic.get("id", "Unknown")
        url = topic.get("lessonUrl", "Url Not Found")
        if "youtube" == topic.get("lessonExt", ""):
            lectures.append(f"{name}: http://www.youtube.com/embed/{url}")
            
        elif "brightcove" == topic.get("lessonExt", ""):
            params = {
              'view': 'List',
              'batch_type': 'my',
              'id': '2158',
              'type': 'class',
              'class_id': class_id
            }
            response = session.get("https://web.careerwill.com/_next/data/RqQQCO-Y8ngCTaHq8KW2p/player.json", cookies=cookies, params=params)
            stream_token = response.json()['pageProps']['streamToken']['token']
            lesson_url = response.json()['pageProps']['classDetailsData']['lessonUrl']
            lectures.append(f"{name}: https://edge.api.brightcove.com/playback/v1/accounts/6206459123001/videos/{lesson_url}/master.m3u8?bcov_auth={stream_token}")
    
        else:
            lectures.append(f"{name}: {url}")
   
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



    

# ----------------------- Cdsjourney-Command ----------------------- #


@app.on_message(filters.command("cds"))
async def cdsjourney_login(_, message):
    user_id = message.from_user.id
    try:
        session = requests.Session()
        csrf_token = await gen_csrftoken(session) if await gen_csrftoken(session) else ""
        cookies = {'csrftoken': csrf_token}
        headers = {'referer': 'https://www.cdsjourney.com/'}
        login_url = "https://www.cdsjourney.com/login-or-register/"

        msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")

        try:
            input1 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        data = {
            'csrfmiddlewaretoken': csrf_token,
            'loginEmail': input1.text.strip()
        }

        response = session.post(login_url, headers=headers, cookies=cookies, data=data)

        if response.status_code != 200:
            return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

        await msg.edit_text("**Login successful, please enter OTP sent to your phone**")

        try:
            input2 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        headers.update({'referer': 'https://www.cdsjourney.com/login/?next=/student-dashboard/subject/84/'})

        data = {
            'csrfmiddlewaretoken': csrf_token,
            'loginPhone2': input1.text.strip(),
            'sent-OTP': input2.text.strip(),
            'first-name': '',
            'mobile': ''
        }

        response = session.post("https://www.cdsjourney.com/verify-quiz-otp/", headers=headers, cookies=cookies, data=data)

        if response.status_code != 200:
            return await msg.edit_text("😒 **Login failed, incorrect OTP.**")

        sessionid = response.cookies.get('sessionid', None)
        cookies.update({'sessionid': sessionid})
        headers.update({'referer': 'https://www.cdsjourney.com/student-dashboard/purchase-order-list/'})

        await msg.edit_text("✅ **Login Successful**")

        response = session.get('https://www.cdsjourney.com/student-dashboard/home/', headers=headers, cookies=cookies)

        if response.status_code != 200:
            return await msg.edit_text("😒 **Failed to fetch live classes.**")

        soup = BeautifulSoup(response.text, 'html.parser')
        seen_courses = set()

        batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
        batch_data = {}
        s_no = 1  # Initialize serial number
        for button in soup.find_all('a', class_='join-now-link', text='View'):
            parent_div = button.find_parent('div', class_='card-body')
            if parent_div:
                course_name = parent_div.find('h4').get_text(strip=True)
                course_link = button['href']
                if course_link not in seen_courses:
                    seen_courses.add(course_link)
                    batch_list += f"{s_no}  -   **{course_name}**\n\n"
                    batch_data[s_no] = {'batch_name': course_name, 'batch_url': course_link}
                    s_no += 1
            else:
                return await msg.edit_text("No batch data found.")

        await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")

        try:
            input2 = await app.listen(user_id=user_id, timeout=30)
            batch_id = int(input2.text.strip()) 
            await input2.delete()
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        batch_url = batch_data.get(batch_id, {}).get('batch_url')
        batch_name = batch_data.get(batch_id, {}).get('batch_name')

        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
        start_time = time.time()
        lectures = await asyncio.create_task(course_content(session, batch_url))
        end_time = time.time()
        duration_seconds = end_time - start_time
        elapsed = get_time(duration_seconds)

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w") as f:
            f.write("\n".join(lectures))

        caption = f"**App Name** : `CDS JOURNEY`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed}`"
        me = await app.get_me()
        big_file_id = me.photo.big_file_id
        thumb = await asyncio.create_task(app.download_media(big_file_id))

        await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
        os.remove(file_name)
        await msg.delete()

        await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{sessionid}`")

    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")
        print(f"Error: {str(e)}")



