import re
import os
import time
import json
import asyncio
import aiohttp
from Extractor import app
from pyrogram import filters
from Extractor.core.main_func import get_time



# ------------------------- Requirements ------------------------- #

async def classplus_org_id(org_id, session):
    async with session.get(f"https://{org_id}.courses.store") as response:
        html_content = await response.text()
        org_id_match = re.search(r'"orgId":(\d+)', html_content)
        name_match = re.search(r'"name":"([^"]+)"', html_content)
        org_id = org_id_match.group(1) if org_id_match else None
        name = name_match.group(1) if name_match else None
    return org_id, name


async def otp_login(session, org_code, org_id, phone):
    url = "https://api.classplusapp.com/v2/otp/generate"
    data = {
        "countryExt": "91",
        "orgCode": org_code,
        "viaSms": "1",
        "viaEmail": "0",
        "retry": 0,
        "orgId": org_id,
        "otpCount": 0,
        "mobile": phone
    }
    
    response = await session.post(url, json=data)
    output = await response.json()
    
    if output.get("status") == "success":  
        sessionId = output["data"]["sessionId"]
        return sessionId  
    else:
        return None  



async def verify_otp(session, otp_num, org_id, phone, sessionID):
    url = "https://api.classplusapp.com/v2/users/verify"
    data = {
        "otp": otp_num,
        "countryExt": "91",
        "sessionId": sessionID,
        "orgId": org_id,
        "fingerprintId": "",
        "mobile": phone
    }

    response = await session.post(url, json=data)
    output = await response.json()

    if output.get("status") == "success":  
        return output.get("token")  
    else:
        return None


# ------------------------- Extracts-Login-Links ------------------------- #

async def fetch_json(session, url, headers, params=None):
    async with session.get(url, headers=headers, params=params) as response:
        data = await response.read()
        return json.loads(data)

async def fetch_video_url(session, headers, content_id):
    url = 'https://api.classplusapp.com/cams/uploader/video/jw-signed-url'
    output_video = await fetch_json(session, url, headers, {'contentId': content_id})
    return output_video.get('url', 'URL Not Found')

async def extract_links(session, headers, course_id, folder_id=0):
    try:
        lectures = []
        url = f"https://api.classplusapp.com/v2/course/content/get?courseId={course_id}&folderId={folder_id}&storeContentEvent=false"
        output1 = await fetch_json(session, url, headers)
        
        tasks = []
        for content in output1.get("data", {}).get("courseContent", []):
            if content["contentType"] == 1:
                tasks.append(extract_links(session, headers, course_id, content["id"]))
            elif content["contentType"] == 2:
                tasks.append(fetch_video_url(session, headers, content.get('contentHashId', '')))
            elif content["contentType"] == 3:
                lectures.append(f"{content['name']}: {content.get('url', 'URL Not Found')}")
        
        results = await asyncio.gather(*tasks)
        for content, result in zip(output1.get("data", {}).get("courseContent", []), results):
            if content["contentType"] == 2:
                lectures.append(f"{content['name']}: {result}")
            elif content["contentType"] == 1:
                lectures.extend(result)

        live_class_url = "https://api.classplusapp.com/v2/course/live/list/videos"
        live_data = await fetch_json(session, live_class_url, headers, {"type": "2", "entityId": course_id, "limit": "", "offset": "0"})
        
        live_tasks = []
        if "data" in live_data and "list" in live_data["data"]:
            for item in live_data["data"]["list"]:
                live_tasks.append(fetch_video_url(session, headers, item.get("contentHashId", "N/A")))

            live_results = await asyncio.gather(*live_tasks)
            for item, result in zip(live_data["data"]["list"], live_results):
                lectures.append(f"{item.get('name', 'N/A')}: {result}")

        return lectures
    except Exception as e:
        print(f"Error In Extract Links: {e}")
        return []





@app.on_message(filters.command("cp"))
async def classplus_login(_, message):
    user_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        try:
            msg = await message.reply_text(
                "**🔑 For access, please transmit your OrgID & Phone in the correct sequence:**\n\n"
                "🔒 **Send like this:** `OrgID*Phone`"
            )
            input1 = await app.listen(user_id, timeout=30)
        except:
            return await message.reply_text("⏳ Timeout! Please try again.")

        try:
            if "*" in input1.text:
                org_code, phone_no = input1.text.split("*")
                org_id, name = await classplus_org_id(org_code, session)

                if org_code.isalpha() and phone_no.isdigit() and len(phone_no) == 10:
                    sessionID = await otp_login(session, org_code, org_id, phone_no)

                    await msg.edit_text("**📝 Now send your ClassPlus OTP**")
                    input2 = await app.listen(user_id, timeout=30)
                    otp_code = input2.text.strip()
                    token = await verify_otp(session, otp_code, org_id, phone_no, sessionID)
                else:
                    return await msg.edit_text("bruh, i think you are dumped 🤔 ")
            else:
                token = input1.text.strip()

            url = "https://api.classplusapp.com/v2/courses?tabCategoryId=1&categoryId=[]&"
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "en",
                "api-version": "52",
                "x-access-token": token
            }

            response = await session.get(url, headers=headers)

            if response.status != 200:
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            data = await response.json()
            courses = data.get("data", {}).get("courses", [])

            if not courses:
                return await msg.edit_text("📭 **No courses found for your account.**")

            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            batch_map = {}

            for course in courses:
                batch_list += f"`{course.get('id')}`  -   **{course.get('name')}**\n\n"
                batch_map[course.get("id")] = course.get("name")

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            input3 = await app.listen(user_id)
            course_id = input3.text.strip()
            await input3.delete()

            batch_name = batch_map.get(course_id, "Unknown Batch")

            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
            start_time = time.time()
            lectures = await asyncio.create_task(extract_links(session, headers, course_id))
            end_time = time.time()
            elapsed = round(end_time - start_time, 2)

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(lectures))

            caption = ("**App Name** : `{name.title()}`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`")
            me = await app.get_me()
            big_file_id = me.photo.big_file_id
            thumb = await asyncio.create_task(app.download_media(big_file_id))

            await app.send_document(
                chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb
            )

            os.remove(file_name)
            await msg.delete()
            await message.reply_text(f"✅ **Done**\n\n✏️ **Token** : `{token}`")

        except Exception as e:
            await message.reply_text(f"**Error:** `{str(e)}`")

        finally:
            await session.close()







