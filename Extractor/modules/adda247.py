import re
import os
import time
import json
import math
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
    'X-Auth-Token': 'fpoa43edty5',
    'X-CSRF-Token': '',
    'X-JWT-Token': '',
    'login_token': '',
    'Referer': 'https://www.adda247.com/',
    'Content-Type': 'application/json',
    'login_type': '1',
    'dName': 'Chrome on Windows Desktop'
}
  
# ----------------------- Course Extractor ----------------------- #

async def direct_links(session, headers, course_id):
    lectures = []
    params = {
        'packageId': course_id,
        'category': 'ONLINE_LIVE_CLASSES',
        'isComingSoon': 'false',
        'pageNumber': '0',
        'pageSize': '10',
        'src': 'aweb'
    }

    try:
        response = await session.get("https://store.adda247.com/api/v3/ppc/package/child", headers=headers, params=params)
        response.raise_for_status()
        response_json = await response.json()
        subject_output = response_json.get('data', {}).get('packages', [])

        total_items = response_json.get('data', {}).get('packagesCount', 0)
        page_size = 10
        page_count = math.ceil(total_items / page_size)

        for page_number in range(page_count):
            params['pageNumber'] = str(page_number)
            response = await session.get("https://store.adda247.com/api/v3/ppc/package/child", headers=headers, params=params)
            response.raise_for_status()
            response_json = await response.json()
            subject_output = response_json.get('data', {}).get('packages', [])

            for data in subject_output:
                try:
                    package_id = data.get("packageId")
                    response = await session.get(f"https://store.adda247.com/api/v1/my/purchase/OLC/{package_id}?src=aweb", headers=headers)
                    response.raise_for_status()
                    response_json = await response.json()
                    content_output = response_json.get('data', {}).get('onlineClasses', [])

                    for content in content_output:
                        name = content.get('name', 'Unknown')
                        url = content.get('url', None)
                        pdf = content.get('pdfFileName', None)
                        dpp_files = content.get('dppFileNames', [])

                        if url:
                            lectures.append(f"{name}: {url}")

                        if pdf:
                            lectures.append(f"{name}: https://store.adda247.com/{pdf}")

                        if dpp_files:
                            for dpp_file in dpp_files:
                                lectures.append(f"{name}: https://store.adda247.com/{dpp_file}")

                except Exception as e:
                    print(f"Error fetching package details for package {package_id}: {e}")
            
    except Exception as e:
        print(f"Error fetching course details: {e}")

    return lectures




# ----------------------- Direct-Links ----------------------- #

import aiohttp
import math

async def direct_links(session, headers, course_id):
    lectures = []
    params = {
        'packageId': course_id,
        'category': 'ONLINE_LIVE_CLASSES',
        'isComingSoon': 'false',
        'pageNumber': '0',
        'pageSize': '10',
        'src': 'aweb'
    }

    try:
        response = await session.get("https://store.adda247.com/api/v3/ppc/package/child", headers=headers, params=params)
        response.raise_for_status()
        response_json = await response.json()
        subject_output = response_json.get('data', {}).get('packages', [])

        total_items = response_json.get('data', {}).get('packagesCount', 0)
        page_size = 10
        page_count = math.ceil(total_items / page_size)

        for page_number in range(page_count):
            params['pageNumber'] = str(page_number)
            response = await session.get("https://store.adda247.com/api/v3/ppc/package/child", headers=headers, params=params)
            response.raise_for_status()
            response_json = await response.json()
            subject_output = response_json.get('data', {}).get('packages', [])

            for data in subject_output:
                try:
                    package_id = data.get("packageId")
                    response = await session.get(f"https://store.adda247.com/api/v1/my/purchase/OLC/{package_id}?src=aweb", headers=headers)
                    response.raise_for_status()
                    response_json = await response.json()
                    content_output = response_json.get('data', {}).get('onlineClasses', [])

                    for content in content_output:
                        name = content.get('name', 'Unknown')
                        url = content.get('url', None)
                        pdf = content.get('pdfFileName', None)
                        dpp_files = content.get('dppFileNames', [])

                        if url:
                            lectures.append(f"{name}: {url}")

                        if pdf:
                            lectures.append(f"{name}: https://store.adda247.com/{pdf}")

                        if dpp_files:
                            for dpp_file in dpp_files:
                                lectures.append(f"{name}: https://store.adda247.com/{dpp_file}")

                except Exception as e:
                    print(f"Error fetching package details for package {package_id}: {e}")
            
    except Exception as e:
        print(f"Error fetching course details: {e}")

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
            except:
                return await message.reply_text("⏳ Timeout! Please try again.")
              
            if "*" in input1.text:
                email, password = input1.text.split("*")
                response = await session.post(login_url, json={"email": email, "providerName": "email", "sec": password}, headers=headers)
                    
                if response.status != 200:
                    return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

                output = await response.json()
                login_token = output["loginToken"] 
                headers.update({"login_token": login_token})
                response = await session.post("https://userapi.adda247.com/forceLogout?src=aweb", headers=headers)
                output_response = await response.json()
                  
                if response.status != 200:
                    return await msg.edit_text("😒 **Login failed, did not fetch token.**")
                      
                token = output_response['data']['jwtToken']
                jwt_token_new = output_response['data']['jwtTokenNew']
                         
            else:
                token = input1.text.strip()
            
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

            batch_data = (await response.json())["data"]
            
            if not batch_data:
                return await msg.edit_text("No batch data found.")
            
            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            for data in batch_data:
                batch_list += f"`{data['packageId']}`  -   **{data['title']}**\n\n"

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            try:
                input2 = await app.listen(user_id=user_id, timeout=30)
                course_id = input2.text.strip()
                await input2.delete()
            except:
                return await message.reply_text("⏳ Timeout! Please try again.")

            batch_name = next((course["title"].replace("/", "") for course in batch_data if int(course["packageId"]) == int(course_id)), "")
            if not batch_name:
                return await msg.edit_text("**Invalid Batch ID. Please try again.**")

            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            maha_pack = next((item.get("mahaPack", False) for item in batch_data if item["packageId"] == course_id), False)
            start_time = time.time()
            if maha_pack:
                lectures = await asyncio.create_task(course_extract(session, headers, course_id))
            else:
                lectures = await asyncio.create_task(direct_links(session, headers, course_id)) 
            
            end_time = time.time()
            duration_seconds = end_time - start_time
            elapsed = get_time(duration_seconds)

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(lectures))

            caption = f"**App Name** : `ADDA 247`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`"
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




