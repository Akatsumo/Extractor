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


async def course_extract(session, cookies, batch_id):
    lectures = []
    url = f'https://online.kpiasdelhi.com/courses/running_contents/{batch_id}/'

    params = {
        'content_type': [3, 4, 5, 7, 8]  
    } 
    response = session.get(url, cookies=cookies, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    tests = soup.find_all('li', class_='relative flex justify-between gap-x-6 px-4 py-5 hover:bg-gray-50')
    
    for test in tests:
        test_name = test.find('p', class_='text-sm font-semibold leading-6 text-gray-900').get_text(strip=True)
        link = f"https://online.kpiasdelhi.com{test.find('a', href=True)['href']}"
        
        response = session.get(link, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        div = soup.find('div', class_='mt-6 py-2 px-4 sm:px-6 lg:px-0 max-w-5xl mx-auto flex justify-center')
        if div:
            button = div.find('button', {'x-on:click': True})
            if button:
                x_on_click = button.get('x-on:click')
                url_match = re.search(r"window\.open\('([^']+)'", x_on_click)

                if url_match:
                    download_url = url_match.group(1)
                    lectures.append(f"{test_name}: {download_url}")
                else:
                    print("URL not found in the 'x-on:click' attribute.")
            else:
                print("Button with 'x-on:click' attribute not found.")
        else:
            print("The div with the specified class was not found.")

    return lectures



    

# ----------------------- Cdsjourney-Command ----------------------- #


@app.on_message(filters.command("kp"))
async def kpias_login(_, message):
    user_id = message.from_user.id
    try:
        session = requests.Session()
        login_url = 'https://online.kpiasdelhi.com/login/?next='
        response = session.get(login_url)
           
        headers = {
          'Referer': login_url,
        }

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
            response = session.post(login_url, data=data, headers=headers, cookies=cookies)

            if response.status_code != 200:
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            sessionid = session.cookies.get('sessionid')   
            print(sessionid)
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
            batch_list += f"`{course_id}`  -   **{course_title}**\n\n"

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
        lectures = await asyncio.create_task(course_extract(session, cookies, batch_id))
        end_time = time.time()

        duration_seconds = end_time - start_time
        elapsed = get_time(duration_seconds)

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w") as f:
            f.write("\n".join(lectures))

        caption = f"**App Name** : `KPIAS Delhi`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed}`"
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


