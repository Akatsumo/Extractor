import re
import os
import time
import asyncio
import requests
from Extractor import app
from pyrogram import filters 
from bs4 import BeautifulSoup
from Extractor.core.main_func import get_time


cookies = {}

# ----------------------- Course-Extract ----------------------- #

async def course_extract(session, batch_url, headers, cookies):
    lectures = []
    headers.update({'referer': 'https://www.cdsjourney.com/student-dashboard/home/'})
    response = session.get(f"https://www.cdsjourney.com{batch_url}", headers=headers, cookies=cookies)
    
    if response.status_code != 200:
        return await msg.edit_text("😒 **Login failed, incorrect batch credentials.**")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    subject_data = []
    
    for subject in soup.find_all('a', href=True):
        if '/student-dashboard/subject/' in subject['href']:
            subject_name = subject.find('img')['alt'] if subject.find('img') else 'No Subject Name'
            subject_link = subject['href']
            subject_data.append({'Subject Name': subject_name, 'Subject Link': subject_link})

    for subject in subject_data:
        print(f"Subject Name: {subject['Subject Name']}")
        subject_url = subject['Subject Link']
        headers.update({'referer': f'https://www.cdsjourney.com{batch_url}'})
        response = session.get(f"https://www.cdsjourney.com{subject_url}", headers=headers, cookies=cookies)
    
        if response.status_code != 200:
           return await msg.edit_text("😒 **Login failed, incorrect subject credentials.**")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='card')
   
        for card in cards:
            subject_name = card.find('span', class_='btn btn-header-link').get_text(strip=True).split('\n')[0].strip()
            zoom_link_tag = card.find('span', class_='btn btn-primary btn-sm radius-sm no-animation')
            if zoom_link_tag:
                zoom_link = zoom_link_tag['onclick'].split('\'')[1]  # Extract Zoom link from the onclick attribute
            else:
                zoom_link = None 
                
            lectures.append(f"{subject_name}: {zoom_link}")   
    
    return lectures



    

# ----------------------- Cdsjourney-Command ----------------------- #


@app.on_message(filters.command("kp"))
async def kpias_login(_, message):
    user_id = message.from_user.id
    try:
        session = requests.Session()
        response = session.get("https://online.kpiasdelhi.com/login/")

        csrf_token = session.cookies.get('csrftoken')
        sessionid = session.cookies.get('sessionid')
        cookies = {'csrftoken': csrf_token}

        msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")

        try:
            input1 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")
            
        if "*" in input1.text.strip():
            username, password = input1.text.split("*")
          
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'username': username,
                'password': password
            }

            response = session.post("https://online.kpiasdelhi.com/login/", cookies=cookies, data=data)

            if response.status_code != 200:
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            sessionid = session.cookies.get('sessionid')   
        else:
            sessionid = input1.text.strip()

        cookies.update({'sessionid': sessionid})

        await input1.delete()       
        await msg.edit_text("✅ **Login Successful**")

        response = session.get('https://online.kpiasdelhi.com/api/v2.4/courses/?page=1&per_page=20', cookies=cookies)

        if response.status_code != 200:
            return await msg.edit_text("😒 **Failed to fetch live classes.**")

        data = response.json()
        batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
        for course in data['results']:
            course_id = course['id']
            course_title = course['title']
            batch_list += f"{course_id}  -   **{course_title}**\n\n"

        await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")

        try:
            input2 = await app.listen(user_id=user_id, timeout=30)
            batch_id = int(input2.text.strip()) 
            await input2.delete()
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        batch_name = next((course["title"].replace("/", "") for course in data['results'] if int(course["id"]) == batch_id), "")

        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures = await asyncio.create_task(course_extract(session, batch_name, cookies))
        end_time = time.time()

        duration_seconds = end_time - start_time
        elapsed = get_time(duration_seconds)

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w") as f:
            f.write("\n".join(lectures))

        caption = f"**App Name** : `KP IAS`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed}`"
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


