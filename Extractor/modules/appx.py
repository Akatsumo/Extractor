import asyncio
import re, os, time
import json, aiohttp
from Extractor import app
from pyrogram import filters
from urllib.parse import urlparse
from pyromod.exceptions import ListenerTimeout
from Extractor.core import script, core_func, appxmethod, main_func 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# --------------------------- Appex-V3 --------------------------- #

async def course_extract(session, api, headers, token, course_id):
    try:        
        lectures = []  
        response = await session.get(f"https://{api}/get/allsubjectfrmlivecourseclass?courseid={course_id}", headers=headers)
        subject_output = json.loads(await response.read()).get("data", [])
        
        for subject in subject_output: 
            response = await session.get(f"https://{api}/get/alltopicfrmlivecourseclass?courseid={course_id}&subjectid={subject['subjectid']}", headers=headers)
            output_data = json.loads(await response.read()).get("data", [])
                            
            for data in output_data:
                topic_id = data.get("topicid")
                response = await session.get(f"https://{api}/get/livecourseclassbycoursesubtopconceptapiv3?topicid={topic_id}&start=-1&courseid={course_id}&subjectid={subject['subjectid']}", headers=headers)
                output_topic = json.loads(await response.read()).get("data", [])
                                         
                for data in output_topic:
                    try:
                        title = data.get("Title", "Unknown Title")
                        material_type = data.get("material_type", "")
                        pdf_link = data.get("pdf_link", "")
                        pdf_key = data.get("pdf_encryption_key", "")
                        
                        if material_type == "PDF" and pdf_link:
                            try:
                                pdf = appx_decrypt(pdf_link.split(":")[0])
                                if pdf_key:
                                    pdf_key = appx_decrypt(pdf_key.split(":")[0])
                                    lectures.append(f"{title}: {pdf}*{pdf_key}")
                                else:
                                    lectures.append(f"{title}: {pdf}")
                            except Exception as decrypt_error:
                                print(f"Error decrypting PDF for {title}: {decrypt_error}")
                    
                        elif material_type == "VIDEO":
                            url = f"https://{api}/get/fetchVideoDetailsById"
                            params = {
                                "course_id": course_id,
                                "video_id": data.get("id"),
                                "ytflag": data.get("ytFlag"),
                                "folder_wise_course": data.get("folder_wise_course")
                            }
                            video_headers = {
                                "Host": api,
                                "Authorization": token,
                                "Auth-Key": "appxapi",
                                "User-ID": "",
                                "User-Agent": "Mozilla/5.0 (Linux; Android 15; CPH2585) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.36"
                            }
                            response = await session.get(url, headers=video_headers, params=params)
                            output = (await response.json()).get("data", {})                    
                        
                            if not output:
                                continue
                        
                            title = output.get("Title", "Unknown Video")
                            encrypted_links = output.get("encrypted_links", [])
                            video_path, video_key = None, None
                        
                            try:
                                if encrypted_links:
                                    encrypted_video = encrypted_links[0].get("path")
                                    encrypted_key = encrypted_links[0].get("key")
                                    video_path = appx_decrypt(encrypted_video.split(":")[0]) if encrypted_video else ""
                                    video_key = appx_decrypt(encrypted_key.split(":")[0]) if encrypted_key else ""      
                            except Exception as decrypt_error:
                                print(f"Error decrypting video for {title}: {decrypt_error}")
                        
                            pdf_link = output.get("pdf_link", "")
                            pdf_key = output.get("pdf_encryption_key", "")
                        
                            try:
                                pdf_link = appx_decrypt(pdf_link.split(":")[0]) if pdf_link else None
                                pdf_key = appx_decrypt(pdf_key.split(":")[0]) if pdf_key else None
                            except Exception as decrypt_error:
                                print(f"Error decrypting PDF for {title}: {decrypt_error}")
                                pdf_link, pdf_key = None, None
                        
                            video_info = f"{title}: {video_path}*{video_key}" if video_path and video_key else f"{title}: {video_path}" if video_path else ""
                            pdf_info = f"{title}: {pdf_link}*{pdf_key}" if pdf_link and pdf_key else f"{title}: {pdf_link}" if pdf_link else ""
                        
                            if video_info and pdf_info:
                                lectures.append(f"{video_info}\n{pdf_info}")
                            elif video_info:
                                lectures.append(video_info)
                            elif pdf_info:
                                lectures.append(pdf_info)
                   #     else:
                   #         lectures.append(title)
                    except Exception as e:
                        print(f"Error processing item {data}: {e}")
                        continue
                           
        return lectures
    except Exception as e:
        print(f"Error in course content function: {e}")
        return []





async def appex_v3_txt(app, message, user_id, api, name):
    try:
        async with aiohttp.ClientSession() as session:
            login_url = f"https://{api}/post/userLogin"
            headers = {
                "Auth-Key": "appxapi",
                "User-Id": "",
                "Authorization": "",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "okhttp/4.9.1"
            }

            msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")                                     
            try:
                input1 = await app.listen(user_id=user_id, timeout=30)
                if "*" in input1.text:
                    email, password = input1.text.split("*")
                    response = await session.post(login_url, data={"email": email, "password": password}, headers=headers)
                    if response.status != 200:
                        return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

                    output = await response.json()
                    userid, token = output["data"]["userid"], output["data"]["token"]
                    headers.update({"User-Id": userid, "Authorization": token})      
                else:
                    token = input1.text.strip()
            except:
                return await message.reply_text("⏳ Timeout! Please try again.")

            await input1.delete()
            headers.update({"Authorization": token})
            await msg.edit_text("✅ **Login Successful**")

            response = await session.get(f"https://{api}/get/mycourseweb?userid", headers=headers)
            batch_data = json.loads(await response.read()).get("data", [])
            if not batch_data:
                await appex_v2_txt(app, message, user_id, api, name, token, msg)
                return
                
            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            batch_map = {}
            for data in batch_data:
                batch_list += f"`{data['id']}`  -   **{data['course_name']}**\n\n"
                batch_map[data['id']] = data['course_name']

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id)
            course_id = input2.text.strip()
            await input2.delete()

            batch_name = batch_map.get(course_id, "Unknown Batch")
            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            start_time = time.time()
            lectures = await asyncio.create_task(course_extract(session, api, headers, token, course_id))                                   
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


            




# --------------------------- Appex-V2-Course-Content --------------------------- #

async def course_content(session, api, headers, token, course_id, parent_id=-1):
    lectures, v_count, p_count = [], 0, 0

    response = await session.get(
        f"https://{api}/get/folder_contentsv2?course_id={course_id}&parent_id={parent_id}",
        headers=headers
    )

    if response.status != 200:
        return lectures, v_count, p_count

    data_list = await response.json().get("data", [])
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
                    doc_url = appx_decrypt(data.get(pdf_link))
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
                durl = appx_decrypt(data.get("file_link"))

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
                await msg.edit_text("✅ **Login Successful.**")

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
            
