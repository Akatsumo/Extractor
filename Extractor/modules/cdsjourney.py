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
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}


async def gen_csrftoken(session):
    url = "https://www.cdsjourney.com/"
    response = session.get(url) 
    if response.status_code == 200:
        cookies = response.cookies
        csrftoken = cookies.get('csrftoken')
        return csrftoken
    else:
        return "VDZ6IlzPnwNO75M2-yVBzCnFrWvZTcoXz-CYxO215xop5h5GTF-z6pvpsyovHFxcwUL"

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

@app.on_message(filters.command("cds"))
async def cdsjourney_login(_, message):
    user_id = message.from_user.id
    try:
        session = requests.Session()
        csrf_token = await gen_csrftoken(session)
        print(csrf_token)
        cookies = {'csrftoken': csrf_token}
        login_url = "https://www.cdsjourney.com/login-or-register/"

        msg = await message.reply_text("🔑 **Send your Email or Phone Number to receive OTP:**")
        try:
            input1 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        identifier = input1.text.strip()

        if not (identifier.isdigit() and len(identifier) == 10) and '@' not in identifier:
            return await msg.edit_text("❌ Please enter a valid Email or 10-digit Phone Number.")

        data = {
            'csrfmiddlewaretoken': csrf_token,
            'loginEmail': identifier
        }

        response = session.post(login_url, headers=headers, cookies=cookies, data=data)
        if response.status_code != 200:
            return await msg.edit_text("😒 **Login failed. Invalid Email/Phone.**")
            
        if response.json()["type"] == "register":
            return await msg.edit_text("❌ Please enter a valid Email or 10-digit Phone Number.")

        await msg.edit_text("📨 **OTP sent. Please enter the OTP:**")
        try:
            input2 = await app.listen(user_id=user_id, timeout=300)
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        otp = input2.text.strip()
        await input2.delete()

        headers.update({'referer': 'https://www.cdsjourney.com/login/?next=/student-dashboard/subject/84/'})
        data = {
            'csrfmiddlewaretoken': csrf_token,
            'loginPhone2': identifier,
            'sent-OTP': otp,
            'first-name': '',
            'mobile': ''
        }

        response = session.post("https://www.cdsjourney.com/verify-quiz-otp/", headers=headers, cookies=cookies, data=data)
        sessionid = response.cookies.get('sessionid', None)
        await input1.delete()

        if response.status_code != 200 or not sessionid:
            return await msg.edit_text("❌ **Login failed. OTP may be incorrect.**")

        cookies.update({'sessionid': sessionid})
        headers.update({'referer': 'https://www.cdsjourney.com/student-dashboard/purchase-order-list/'})
        await msg.edit_text("✅ **Login Successfully. Fetching your courses...**")

        response = session.get('https://www.cdsjourney.com/student-dashboard/home/', headers=headers, cookies=cookies)
        if response.status_code != 200:
            return await msg.edit_text("😒 **Failed to fetch live classes.**")

        soup = BeautifulSoup(response.text, 'html.parser')
        seen_courses = set()
        batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
        batch_data = {}
        s_no = 1

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

        if not batch_data:
            return await msg.edit_text("❌ No batch data found.")

        await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")

        try:
            input3 = await app.listen(user_id=user_id, timeout=30)
            batch_id = int(input3.text.strip()) 
            await input3.delete()
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")

        batch_url = batch_data.get(batch_id, {}).get('batch_url')
        batch_name = batch_data.get(batch_id, {}).get('batch_name')

        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("📥 **Extracting Course Content, Please Wait...**")

        start_time = time.time()
        lectures = await course_extract(session, batch_url, headers, cookies)
        elapsed = get_time(time.time() - start_time)

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w") as f:
            f.write("\n".join(lectures))

        caption = f"**App Name** : `CDS JOURNEY`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed}`"

        await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption)
        os.remove(file_name)
        await msg.delete()
        await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{sessionid}`")

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{str(e)}`")
        print(f"Error: {str(e)}")




