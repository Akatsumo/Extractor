import asyncio
import re, os, time
import json, aiohttp
from Extractor import app
from pyrogram import filters
from urllib.parse import urlparse
from pyromod.exceptions import ListenerTimeout
from Extractor.core import script, core_func, appxmethod, main_func 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjkzNTExOSIsImVtYWlsIjoicGV5YXZhMjI4NUBkcm9wZXNvLmNvbSIsInRpbWVzdGFtcCI6MTc2MTc1MjA4NywidGVuYW50VHlwZSI6InVzZXIiLCJ0ZW5hbnROYW1lIjoicGFybWFyYWNhZGVteV9kYiIsInRlbmFudElkIjoiIiwiZGlzcG9zYWJsZSI6ZmFsc2V9.NQEDBZxK98d2mMhsqnhsk4952XMGzkeyyZJOS9FV_Is"

# --------------------------- Appex-V3 --------------------------- #
async def full_cource(session, headers):
    url = "https://parmaracademyapi.classx.co.in/get/courselist?start=0"
    response = await session.get(url, headers=headers)
    if response.status != 200:
        print("Failed to fetch all batches v3")
        return None
    full_batch = json.loads(await response.read()).get("data", [])
    return full_batch



async def course_extract(session, api, headers, token, course_id):
    lectures, v_count, p_count = [], 0, 0

    response = await session.get(f"https://{api}/get/allsubjectfrmlivecourseclass?courseid={course_id}", headers=headers)
    if response.status != 200:
        return lectures, v_count, p_count

    subject_output = json.loads(await response.read()).get("data", [])
    if not subject_output:
        return lectures, v_count, p_count

    for subject in subject_output:
        response = await session.get(f"https://{api}/get/alltopicfrmlivecourseclass?courseid={course_id}&subjectid={subject['subjectid']}", headers=headers)
        if response.status != 200:
            continue

        output_data = json.loads(await response.read()).get("data", [])
        for data in output_data:
            topic_id = data.get("topicid")
            response = await session.get(
                f"https://{api}/get/livecourseclassbycoursesubtopconceptapiv3?topicid={topic_id}&start=-1&courseid={course_id}&subjectid={subject['subjectid']}",
                headers=headers
            )
            if response.status != 200:
                continue

            output_topic = json.loads(await response.read()).get("data", [])
            for data in output_topic:
                title = data.get("Title", "Unknown Title")
                material_type = data.get("material_type", "")

                if material_type == "PDF":
                    domain_map = {
                        "static-db-v2.appx.co.in": "appx-content-v2.classx.co.in",
                        "static-db.appx.co.in": "appxcontent.kaxa.in"
                    }

                    for pdf_link, is_encrypted_key, encryption_key, encryption_version in [
                        ("pdf_link", "is_pdf_encrypted", "pdf_encryption_key", "pdf_encryption_version"),
                        ("pdf_link2", "is_pdf2_encrypted", "pdf2_encryption_key", "pdf2_encryption_version"),
                    ]:
                        if data.get(pdf_link):
                            p_count += 1
                            doc_url = main_func.appx_decrypt(data.get(pdf_link).split(":")[0])
                            parsed = urlparse(doc_url)
                            pdf_url = f"https://{domain_map.get(parsed.netloc, parsed.netloc)}{parsed.path}"

                            if data.get(is_encrypted_key) == "1" and data.get(encryption_key):
                                pdf_key = data.get(encryption_key)
                                lectures.append(f"{title}: {pdf_url}*{pdf_key}")
                            else:
                                lectures.append(f"{title}: {pdf_url}")

                elif material_type == "VIDEO":
                    v_count += 1
                    durl = None

                    if data.get("ytFlag") == 0:
                        durl = f"https://{api}/appx/{data.get('id')}.{course_id}.1.zip?token={token}"
                    elif data.get("ytFlag") == 1 and data.get("file_link"):
                        durl = main_func.appx_decrypt(data.get("file_link").split(":")[0])

                    if durl:
                        lectures.append(f"{title}: {durl}")

    return lectures, v_count, p_count





# --------------------------- Appex-Version 3 --------------------------- #

async def appex_v3_txt(app, message, user_id, api, name, token=token):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Auth-Key": "appxapi",
                "User-Id": "",
                "Authorization": "",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "okhttp/4.9.1"
            }

            if not token:
                msg = await message.reply_text("🔑 Enter login credentials (Id*Password or Token):")                                     
                input1 = await app.listen(user_id=user_id, timeout=30)
                if "*" in input1.text:
                    email, password = input1.text.split("*")
                    response = await session.post(f"https://{api}/post/userLogin", data={"email": email, "password": password}, headers=headers)
                    if response.status != 200:
                        return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

                    output = await response.json()
                    userid, token = output["data"]["userid"], output["data"]["token"]
                    if not token or not userid:
                        return await msg.edit_text("😒 **Invalid response from API.**")
                    headers.update({"User-Id": userid, "Authorization": token}) 
                else:
                    token = input1.text.strip()
                await input1.delete()
                
            msg = await message.reply_text(f"Fetching All {name.title()} Batches, Please Wait...")    
            headers.update({"Authorization": token})
            if len(token) <= 100:  
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
            else:
                await msg.edit_text("✅ **Login Successful.**")

            batch_data = await full_cource(session, headers)
            if not batch_data:
                await appex_v2_txt(app, message, user_id, api, name, token, msg)
                return
                
            batch_list = "📚 **Available Batches:**\n\n"
            for data in batch_data:
                batch_list += f"`{data['id']}`  -   **{data['course_name']}**\n"

            await msg.edit_text(f"{batch_list}\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id, timeout=30)
            course_id = input2.text.strip()
            await input2.delete()

            batch_name = next((course["course_name"] for course in batch_data if str(course["id"]) == course_id), None)
            if not batch_name:
                return await msg.edit_text("Invalid Batch ID. Please try again.")
                
            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            start_time = time.time()
            lectures, v_count, p_count = await asyncio.create_task(course_extract(session, api, headers, token, course_id))                                   
            end_time = time.time()

            if not lectures:
                return await msg.edit_text("No batch content found.")

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(lectures))

            elapsed = main_func.get_time(end_time - start_time)
            caption = (
                f"**App Name** : `{name.title()}`\n"
                f"**Batch Name** : `{batch_name}`\n\n"
                f"📜 **Total Materials** : `{len(lectures)}`\n"
                f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
                f"⌚️ **Time Taken** : `{elapsed}`"
            )

            await main_func.send_file(app, file_name, user_id, caption)
            await msg.delete()

        await session.close()
    except ListenerTimeout:
        await message.reply_text("⏰ You didn’t reply in time. Please try again.")
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")


    
# --------------------------- Appex-V2-Course-Content --------------------------- #

async def course_content(session, api, headers, token, course_id, parent_id=-1):
    lectures, v_count, p_count = [], 0, 0

    response = await session.get(
        f"https://{api}/get/folder_contentsv2?course_id={course_id}&parent_id={parent_id}",
        headers=headers
    )

    if response.status != 200:
        return lectures, v_count, p_count

    data_list = (await response.json()).get("data", [])
    if not data_list:
        return lectures, v_count, p_count

    for data in data_list:
        title = data.get("Title", "Unknown Title")
        material_type = data.get("material_type")

        if material_type == "FOLDER":
            sub_lectures, sub_v_count, sub_p_count = await course_content(
                session, api, headers, token, course_id, data["id"]
            )
            lectures.extend(sub_lectures)
            v_count += sub_v_count
            p_count += sub_p_count

        elif material_type == "PDF":
            domain_map = {
                "static-db-v2.appx.co.in": "appx-content-v2.classx.co.in",
                "static-db.appx.co.in": "appxcontent.kaxa.in"
            }

            for pdf_link, is_encrypted_key, encryption_key, encryption_version in [
                ("pdf_link", "is_pdf_encrypted", "pdf_encryption_key", "pdf_encryption_version"),
                ("pdf_link2", "is_pdf2_encrypted", "pdf2_encryption_key", "pdf2_encryption_version"),
            ]:
                if data.get(pdf_link):
                    p_count += 1
                    doc_url = main_func.appx_decrypt(data.get(pdf_link).split(":")[0])
                    parsed = urlparse(doc_url)
                    pdf_url = (
                        f"https://{domain_map[parsed.netloc]}{parsed.path}"
                        if parsed.netloc in domain_map
                        else doc_url
                    )

                    if data.get(is_encrypted_key) == "1" and data.get(encryption_key):
                        pdf_key = data.get(encryption_key)
                        lectures.append(f"{title}: {pdf_url}*{pdf_key}")
                    else:
                        lectures.append(f"{title}: {pdf_url}")

        elif material_type == "VIDEO":
            v_count += 1
            durl = None

            if data.get("ytFlag") == 0:
                durl = f"https://{api}/appx/{data.get('id')}.{course_id}.1.zip?token={token}"

            elif data.get("ytFlag") == 1 and data.get("file_link"):
                durl = main_func.appx_decrypt(data.get("file_link").split(":")[0])

            if durl:
                video_url = f"{title}: {durl}"
                lectures.append(video_url)

    return lectures, v_count, p_count

                        
# --------------------------- Appex-Version 2 --------------------------- #

async def appex_v2_txt(app, message, user_id, api, name, token=None, msg=None):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Auth-Key": "appxapi",
                "User-Id": "",
                "Authorization": "",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "okhttp/4.9.1"
            }

            if not token:
                msg = await message.reply_text("🔑 Enter login credentials (Id*Password or Token):")
                input1 = await app.listen(user_id=user_id, timeout=30)

                if "*" in input1.text:
                    email, password = input1.text.split("*")
                    response = await session.post(
                        f"https://{api}/post/userLogin",
                        data={"email": email, "password": password},
                        headers=headers
                    )
                    if response.status != 200:
                        await input1.delete()
                        return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

                    data_output = await response.json()
                    userid = data_output.get("data", {}).get("userid")
                    token = data_output.get("data", {}).get("token")

                    if not token or not userid:
                        await input1.delete()
                        return await msg.edit_text("😒 **Invalid response from API.**")

                    headers.update({"User-Id": str(userid), "Authorization": token})
                else:
                    token = input1.text.strip()
                await input1.delete()

            headers.update({"Authorization": token})
            
            if len(token) <= 100:  
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
            else:
                await msg.edit_text("✅ **Login Successful**")

            response = await session.get(f"https://{api}/get/get_all_purchases?userid&item_type=10", headers=headers)
            if response.status != 200:
                return await msg.edit_text("Failed to fetch batch data.")

            json_data = await response.json()
            batch_data = json_data.get("data", [])
            if not batch_data:
                return await msg.edit_text("No Batch Data found!!")

            
            batch_list = "📚 **Available Batches:**\n\n"
            batch_map = {}
            for data in batch_data:
                for cdata in data.get("coursedt", []):
                    cid = str(cdata.get("id"))
                    cname = cdata.get("course_name", "Unnamed Course")
                    batch_list += f"`{cid}` - **{cname}**\n"
                    batch_map[cid] = cname

            await msg.edit_text(f"{batch_list}\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id, timeout=30)
            course_id = input2.text.strip()
            await input2.delete()

            batch_name = batch_map.get(course_id)
            if not batch_name:
                return await msg.edit_text("**Batch ID Not Found!!**")

            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            start_time = time.time()
            lectures, v_count, p_count = await asyncio.create_task(course_content(session, api, headers, token, course_id))
            end_time = time.time()

            if not lectures:
                return await msg.edit_text("No batch content found.")

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(lectures))

            elapsed = main_func.get_time(end_time - start_time)
            caption = (
                f"**App Name** : `{name.title()}`\n"
                f"**Batch Name** : `{batch_name}`\n\n"
                f"📜 **Total Materials** : `{len(lectures)}`\n"
                f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
                f"⌚️ **Time Taken** : `{elapsed}`"
            )

            await main_func.send_file(app, file_name, user_id, caption)
            await msg.delete()

    except ListenerTimeout:
        await message.reply_text("⏰ You didn’t reply in time. Please try again.")
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")






# --------------------------- Appex-Command --------------------------- #

@app.on_message(filters.command("appx")) 
async def appx_logins(_, message, user_id=None, callback=False, api=None, name=None, manualLogin=False):
    user_id = user_id if user_id else message.from_user.id
    if not manualLogin:
        buttons = main_func.get_page(0, appxmethod.a_to_zList, DictID="AppxShortAtoZ", back_data="home_", query=True, appx=True, withoutIdPass=False)
        if not callback:
            await message.reply_text(script.TOOLS_TEXT,
            reply_markup=buttons)
        else:
            if api and name:
                await appex_v3_txt(app, message, user_id, api, name)  
            else:
                await message.edit_text(script.TOOLS_TEXT,
                reply_markup=buttons)
    else:
        msg = await message.reply_text("📝 Please Provide Your Appx API URL.")

        input_msg = await app.listen(user_id=user_id)
        raw_text = input_msg.text
        await input_msg.delete()

    
        def extract_parts(url):
            match = re.search(r'([\w\d]+?)(api)?\.(.+)$', url)
            if match:
                name = match.group(1)
                original_subdomain = match.group(1) + (match.group(2) or '') + '.' + match.group(3)
                return name, original_subdomain
            return None, None

        name, api = extract_parts(raw_text)
        if not name or not api:
            return await msg.edit_text("❌ **Invalid API URL! Please try again.**")
        await appex_v3_txt(app, message, user_id, api, name)
        await msg.delete()
            
