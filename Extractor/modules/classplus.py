import re
import os
import time
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

async def extract_links(session, headers, course_id, folder_id=0):
    try:
        lectures = []
        url = f"https://api.classplusapp.com/v2/course/content/get?courseId={course_id}&folderId={folder_id}&storeContentEvent=false"
        response1 = await session.post(url, headers=headers)
        output1 = json.loads(await response1.read())
        for content in output1.get("data", {}).get("courseContent", []):
            if content["contentType"] == 1:
                lectures.extend(await extract_links(session, headers, course_id, content["id"]))
            elif content["contentType"] == 2:
                id = content.get('contentHashId', '')
                response = await session.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params={'contentId': id})
                output_video = json.loads(await response.read())
                lectures.append(f"{content['name']}: {output_video['url']}")               
                
            elif content["contentType"] == 3:
                lectures.append(f"{content['name']}: {content['url']}")
            
        return lectures
    except Exception as e:
        print(f"Error: {e}")
        return []
    



@app.on_message(filters.command("cp"))
async def classplus_login(_, message):
    user_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        try:
            msg = await message.reply_text("**🔑 For access, please transmit your OrgID & Phone in the correct sequence:**\n\n🔒 **Send like this:** `OrgID*Phone`")
            input1 = await app.listen(user_id, timeout=30)

            if "*" not in input1.text:
                return await message.reply_text("😒 **Login failed, incorrect credentials.**")

            org_code, phone_no = input1.text.split("*")
            org_id, name = await classplus_org_id(org_code, session)

            if org_code.isalpha() and phone_no.isdigit() and len(phone_no) == 10:
                sessionID = await otp_login(session, org_code, org_id, phone_no)

                await msg.edit_text("**📝 Now send your ClassPlus OTP**")
                input2 = await app.listen(user_id, timeout=30)
                otp_code = input2.text.strip()
                token = await verify_otp(session, otp_code, org_id, phone_no, sessionID)
            else:
                token = phone_no

            if not token:
                return await msg.edit_text("Failed Token!!")

            
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

            caption = (f"**App Name** : `{name.title()}`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`")
            
            me = await app.get_me()
            big_file_id = me.photo.big_file_id
            thumb = await asyncio.create_task(app.download_media(big_file_id))

            await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
            os.remove(file_name)
            await msg.delete()
            await message.reply_text(f"✅ **Done**\n\n✏️ **Token** : `{token}`")

        except asyncio.TimeoutError:
            await message.reply_text("⏳ Timeout! Please try again.")
        except Exception as e:
            await message.reply_text(f"**Error:** `{str(e)}`")
        finally:
            await session.close()





