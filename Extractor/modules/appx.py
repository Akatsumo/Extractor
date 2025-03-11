import re
import os
import time
import json
import aiohttp
import asyncio
from Extractor import app
from pyrogram import filters 
from Extractor.core.main_func import appx_decrypt, get_time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📢 Channel", url="https://t.me/DevsLaboratory")
    ]])



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
                            print(output)
                        
                            if not output:
                                continue
                        
                            title = output.get("Title", "Unknown Video")
                            encrypted_links = output.get("encrypted_links", [])
                            video_path, video_key = None, None
                        
                            try:
                                if encrypted_links:
                                    video_path = appx_decrypt(encrypted_links[0].get("path", "").split(":")[0])
                                    video_key = appx_decrypt(encrypted_links[0].get("key", "").split(":")[0])       
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


            




# --------------------------- Appex-V2 --------------------------- #

async def course_content(session, api, headers, token, course_id, parent_id=-1):
    try:
        lectures = []
        response = await session.get(f"https://{api}/get/folder_contentsv2?course_id={course_id}&parent_id={parent_id}", headers=headers)
        data_list = json.loads(await response.read()).get("data", [])
        
        for data in data_list:
            try:
                title = data.get("Title", "Unknown Title")
                material_type = data.get("material_type", "")
                pdf_link = data.get("pdf_link", "")
                pdf_key = data.get("pdf_encryption_key", "")
                
                if material_type == "FOLDER":
                    lectures.extend(await course_content(session, api, headers, token, course_id, data['id']))
                elif material_type == "PDF" and pdf_link:
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
                    params = {"course_id": course_id, "video_id": data.get("id"), "ytflag": data.get("ytFlag"), "folder_wise_course": data.get("folder_wise_course")}
                    headers = {
                      "Host": api,
                      "Authorization": token,
                      "Auth-Key": "appxapi",
                      "User-ID": "",
                      "User-Agent": "Mozilla/5.0 (Linux; Android 15; CPH2585) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.36"
                    }
                    response = await session.get(url, headers=headers, params=params)
                    output = (await response.json()).get("data", {})
                    
                    if not output:
                        continue
                    
                    title = output.get("Title", "Unknown Video")
                    encrypted_links = output.get("encrypted_links", [])
                    video_path, video_key = None, None
                    
                    try:
                        if encrypted_links:
                            video_path = appx_decrypt(encrypted_links[0].get("path", "").split(":")[0])
                            video_key = appx_decrypt(encrypted_links[0].get("key", "").split(":")[0])       
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
              #  else:
              #      lectures.append(title)
            except Exception as e:
                print(f"Error processing item {data}: {e}")
                continue
        
        return lectures
    except Exception as e:
        print(f"Error in course content function: {e}")
        return []



async def appex_v2_txt(app, message, user_id, api, name):
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

            response = await session.get(f"https://{api}/get/get_all_purchases?userid&item_type=10", headers=headers)
            batch_data = (await response.json()).get("data", [])

            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            batch_map = {}
            for data in batch_data:
                for cdata in data['coursedt']:
                    batch_list += f"`{cdata['id']}`  -   **{cdata['course_name']}**\n\n"
                    batch_map[cdata['id']] = cdata['course_name']

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id)
            course_id = input2.text.strip()
            await input2.delete()

            batch_name = batch_map.get(course_id, "Unknown Batch")
            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            start_time = time.time()
            lectures = await asyncio.create_task(course_content(session, api, headers, token, course_id))
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


# --------------------------- Appex-Command --------------------------- #


@app.on_message(filters.command("appx")) 
async def appx_logins(_, message):
    user_id = message.from_user.id
    msg = await message.reply_text("📝 Please Provide Your Appx API URL.")

    input_msg = await app.listen(user_id=user_id)
    raw_text = input_msg.text
    await input_msg.delete()

    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌿 Appx V2", callback_data=f"appx_v2*{raw_text}"), 
         InlineKeyboardButton("🌴 Appx V3", callback_data=f"appx_v3*{raw_text}")]
    ])    

    mm = await msg.edit_text("🕹 **Select Your Appx API Version:**", reply_markup=buttons)
    await asyncio.sleep(10)
    await mm.delete()

