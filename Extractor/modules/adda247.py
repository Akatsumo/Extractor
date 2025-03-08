import re
import os
import time
import json
import aiohttp
import asyncio
from Extractor import app
from pyrogram import filters 
from Extractor.core.main_func import get_time



# ----------------------- CSRF Token ----------------------- #

async def csrf_token(session):
  url = "https://userapi.adda247.com/csrf/token?src=aweb"
  response = await session.get(url)
  data = await response.json()
  if data["success"]:
    return data["data"]
  else:
    return None


headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "cp-origin": "11",
    "dname": "Chrome on Windows Desktop",
    "login_type": "1",
    "origin": "https://www.adda247.com",
    "priority": "u=1, i",
    "referer": "https://www.adda247.com/",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "x-auth-token": "fpoa43edty5",
    "x-csrf-token": "",
    "x-jwt-token": ""
}

  
# ----------------------- Course Extractor ----------------------- #

async def course_extract(session, headers, course_id):
    lectures = []

    try:
        params = {
            'purchasedPackage': course_id,
            'src': 'aweb'
        }

        response = await session.post(
            "https://store.adda247.com/api/v1/ppc/package/bookmark",
            headers=headers,
            params=params
        )
        response_json = await response.json()

        package_output = response_json.get('data', {}).get('bookmarkedPackages', [])
        
        for package in package_output:
            package_id = package.get('packageId')
            title = package.get('title')

            params = {
                'packageId': package_id,
                'contentType': 'ONLINE_LIVE_CLASSES',
                'pageNo': 0,
                'src': 'aweb'
            }

            response = await session.post(
                "https://store.adda247.com/api/v1/syllabus/ppc/subjects",
                headers=headers,
                params=params
            )
            response_json = await response.json()
            syllabus_output = response_json.get('data', {}).get('syllabus', [])

            for syllabus in syllabus_output:
                syllabus_id = syllabus.get('packageId')
                syllabus_level = syllabus.get('level')

                params = {
                    'packageId': package_id,
                    'contentType': 'ONLINE_LIVE_CLASSES',
                    'syllabusId': syllabus_id,
                    'level': syllabus_level,
                    'pageNo': 0,
                    'src': 'aweb'
                }

                response = await session.post(
                    "https://store.adda247.com/api/v1/syllabus/ppc/getSubjectGroupAndChapter",
                    headers=headers,
                    params=params
                )
                response_json = await response.json()
                subject_output = response_json.get('data', {}).get('syllabus', [])

                for subject in subject_output:
                    subject_id = subject.get('packageId')
                    subject_level = subject.get('level')

                    params = {
                        'contentType': 'ONLINE_LIVE_CLASSES',
                        'packageId': package_id,
                        'level': subject_level,
                        'syllabusId': subject_id,
                        'pageNo': 0,
                        'pageSize': 20,
                        'status': 1,
                        'src': 'aweb'
                    }

                    response = await session.post(
                        "https://liveclasses.adda247.com/api/v1/ppc/OLC/content",
                        headers=headers,
                        params=params
                    )
                    response_json = await response.json()
                    content_output = response_json.get('data', {}).get('content', [])

                    for content in content_output:
                        name = content.get('name', 'Unknown')
                        url = content.get('url', 'No URL')

                        lectures.append(f"{name}: {url}")

                        pdf_file_id = content.get('pdfFileName')
                        if pdf_file_id:
                            lectures.append(f"{name}: https://store.adda247.com/{pdf_file_id[0]}")

    except Exception as e:
        print(f"Error In Course Extract: {e}")

    return lectures






# ----------------------- Adda-Command ----------------------- #

@app.on_message(filters.command("adda"))
async def adda_txt(_, message):
    user_id = message.from_user.id
    try:
        async with aiohttp.ClientSession() as session:
            login_url = "https://userapi.adda247.com/v2/login?src=aweb"
            crf_token = await csrf_token(session)
            print(crf_token)
            headers.update({"x-csrf-token": crf_token})
            
            msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")                                     
            try:
                input1 = await app.listen(user_id=user_id, timeout=30)
                if "*" in input1.text:
                    email, password = input1.text.split("*")
                    response = await session.post(login_url, data={"email": email, "providerName": "email", "sec": password}, headers=headers)
                    
                    #if response.status != 200:
                    #   return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

                    output = await response.json()
                    print(output)
                    login_token = output["data"]
                    token = output["jwtToken"] if output["jwtToken"] else "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrdW1hcmFiaGlzaGVra3VtYXI0NTRAZ21haWwuY29tIiwiYXVkIjoiMjEyNzc5NDEiLCJpYXQiOjE3NDE0MjY0MjcsImlzcyI6ImFkZGEyNDcuY29tIiwibmFtZSI6IkFCSElTSEVLIEtVTUFSICIsImVtYWlsIjoia3VtYXJhYmhpc2hla2t1bWFyNDU0QGdtYWlsLmNvbSIsInBob25lIjoiOTE0MjY3ODA5OSIsInVzZXJJZCI6ImFkZGEudjEuMzQ3Zjk5ZmRlNTE5ZmVjOTNmZTFhZWIyZmEwNTc3ZjUiLCJpc01hc3RlckxvZ0luIjpmYWxzZSwibG9naW5BcGlWZXJzaW9uIjoyfQ.mOw-oAV4W9RpfhmkFgMXGWjNrqvhnLqbYb7JUWM7DhtiiSO_Ehu9FmnDaGRHSYUos0AbhmnJR_f-K_HanUA0pQ"
                    headers.update({"login_token": login_token})      
                else:
                    token = input1.text.strip()
            except:
                return await message.reply_text("⏳ Timeout! Please try again.")

            await input1.delete()            
            await msg.edit_text("✅ **Login Successful**")

            headers.update({"x-jwt-token": token})
            params = {
              "pageNumber": 0,
              "pageSize": 10,
              "src": "aweb"
            }
            response = await session.get(f"https://store.adda247.com/api/v2/ppc/package/purchased", headers=headers, params=params)
            if response.status != 200:
              return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            batch_data = await response.json()["data"]
            
            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            batch_map = {}
            for data in batch_data:
                batch_list += f"`{data['id']}`  -   **{data['title']}**\n\n"
                batch_map[data['id']] = data['title']

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id)
            course_id = input2.text.strip()
            await input2.delete()

            batch_name = batch_map.get(course_id, "Unknown Batch")
            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            start_time = time.time()
            lectures = await asyncio.create_task(course_extract(session, headers, course_id))                                   
            end_time = time.time()
            duration_seconds = end_time - start_time
            elapsed = get_time(duration_seconds)

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(lectures))

            caption = f"**App Name** : `{name.title()}`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`"
            me = await app.get_me()
            big_file_id = me.photo.big_file_id
            thumb = await asyncio.create_task(app.download_media(big_file_id))

            await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
            os.remove(file_name)
            await msg.delete()
            await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        await session.close()
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")

      
