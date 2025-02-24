import re
import os
import time
import json
import aiohttp
import asyncio
import cloudscraper
from Extractor import app
from pyrogram import filters 
from Extractor.core.main_func import appx_decrypt, get_time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📢 Channel", url="https://t.me/DevsLaboratory")
    ]])



# --------------------------- Appex-V3 --------------------------- #

async def appex_down(session, message, hdr1, api, raw_text2, f, msg):
    try:
        global v_count, p_count
        vt = ""                
        async with session.get(f"https://{api}/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={f}", headers=hdr1) as response:
            respo = await response.read()
            data = json.loads(respo)
            b_data2 = data.get('data', [])
                
        for data in b_data2:
            tid = data.get("topicid")
                    
            if tid:
                async with session.get(f"https://{api}/get/livecourseclassbycoursesubtopconceptapiv3?topicid={tid}&start=-1&courseid={raw_text2}&subjectid={f}", headers=hdr1) as response:
                    res4 = await response.json()
                    topicid = res4.get("data", [])
                        
            for data in topicid:
                type = data.get('material_type')
                tid = data.get("Title")
                if type == 'VIDEO':
                    if data.get('pdf_link'):
                        p_count += 1
                        plink = data.get('pdf_link').split(':')
                        if len(plink) == 2:
                            bp = appx_decrypt(plink[0])
                            vs = f"{bp}"
                    if data.get('ytFlag') == 0 and data.get('ytFlagWeb') == 0:
                        v_count += 1
                        dlink = next((link['path'] for link in data.get('download_links', []) if link.get('quality') == "720p"), None)
                        if dlink:
                            b = appx_decrypt(dlink.split(':')[0])
                            cool2 = f"{b}"
                    elif data.get('ytFlag') == 1 and data.get('ytFlagWeb') == 0:
                        v_count += 1
                        dlink = data.get('file_link')
                        if dlink:
                            b = appx_decrypt(dlink.split(':')[0])
                            cool2 = f"https://youtu.be/{b}"
                    elif data.get('ytFlag') == 1 and data.get('ytFlagWeb') == 1:
                        v_count += 1
                        dlink = data.get('file_link')
                        if dlink:
                            b = appx_decrypt(dlink.split(':')[0])
                            cool2 = f"https://youtu.be/{b}"
                    vt += f"{tid} : {cool2}\n{tid} : {vs}\n" if data.get('pdf_link') else f"{tid} : {cool2}\n"
    
                elif type == 'PDF':
                    p_count += 1
                    bp = appx_decrypt(data.get("pdf_link", "").split(':')[0])
                    vt += f"{tid} : {bp}\n"

            counter += 1
            if counter % 8 == 0 and (prev_v_count != v_count or prev_p_count != p_count):
                await msg.edit_text(f"**Extracting Videos Links Please Wait  📥**\n\n🍿 **Total Video**  - `{v_count}`\n📝 **Total Pdf**  - `{p_count}`")                
    except Exception as e:
        print(str(e))
    
    return vt



async def appex_v3_txt(app, message, user_id, api, name):
    global v_count, p_count
    
    try:
        raw_url = f"https://{api}/post/userLogin"
        headers = {
            "Auth-Key": "appxapi",
            "User-Id": "-2",
            "Authorization": "",
            "User_app_category": "",
            "Language": "en",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "okhttp/4.9.1"
        }
        info = {"email": "", "password": ""}
        
        msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
        try:
            input1 = await app.listen(user_id, timeout=30)  
            raw_text = input1.text
        except:
            return await message.reply_text("⏳ Timeout! Please try again.")
                      
        if "*" in raw_text:           
            info["email"], info["password"] = raw_text.split("*")
        else:
            return await msg.edit_text("😒 **Bruh Send ID Pass in Correct Form**")         
            
        await input1.delete(True)        
        async with aiohttp.ClientSession() as session:
            async with session.post(raw_url, data=info, headers=headers) as response:
                if response.status != 200:
                    return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
                
                res = await response.read()
                output = json.loads(res)
                userid = output["data"]["userid"]
                token = output["data"]["token"]
                
            headers = {
                "Host": api,
                "Client-Service": "Appx",
                "Auth-Key": "appxapi",
                "User-Id": userid,
                "Authorization": token
            }
        
            await msg.edit_text("✅ **Login Successfully**")
        
            async with session.get(f"https://{api}/get/mycourseweb?userid={userid}", headers=headers) as response:
                respo = await response.read()
                data = json.loads(respo)
                b_data = data.get('data', [])
        
            FFF = "**BATCH-ID  -  BATCH NAME**\n\n"
            for data in b_data:
                FFF += f"`{data['id']}`   -   **{data['course_name']}**\n\n"
        
            await msg.edit_text(f"{FFF}\n\n📊**Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id)
            raw_text2 = input2.text
            await input2.delete(True)
            batch_name = name
            for data in b_data:
                if data['id'] == raw_text2:
                    batch_name = data['course_name']
                    break
        
            scraper = cloudscraper.create_scraper()
            html = scraper.get(f"https://{api}/get/allsubjectfrmlivecourseclass?courseid={raw_text2}", headers=headers).content
            output0 = json.loads(html)
            subjID = output0["data"]

            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Full Batch", callback_data="full"), InlineKeyboardButton("Subject wise", callback_data="sub")]])
            mm = await msg.edit_text("🕹 Select Your Preferred Mode 👇", reply_markup=buttons)
            r = await mm.wait_for_click(from_user_id=user_id)
            if r.data == 'full':
                ss = [sub["subjectid"] for sub in subjID]
            elif r.data == 'sub':
                ff = "**SUBJ-ID  -  SUBJ-NAME**\n\n"
                for sub in subjID:
                    ff += f"`{sub['subjectid']}`   -   **{sub['subject_name']}**\n\n"
                await msg.edit_text(f"{ff}**📊Now send the SUBJECT ID to Download, \nIf you want to Download Multipe subjects then Send SUBJ ID like  `12&23&65`**")
                input3 = await app.listen(user_id=user_id)
                ss = input3.text.split('&')
                await input3.delete(True)

            start_time = time.time()
            await msg.edit_text("**Extracting Videos Links Please Wait  📥 **")
            vt = ""
        
            tasks = [appex_down(session, message, headers, api, raw_text2, s, msg) for s in ss]
            results = await asyncio.gather(*tasks)
            for result in results:
                vt += result
        
            end_time = time.time()
            duration_seconds = end_time - start_time
            elapsed = get_time(duration_seconds)

            file_name = batch_name.replace("/", "") if '/' in batch_name else batch_name
            file_path = f"{file_name}_{user_id}.txt"
            caption = f"**App Name** :- `{name}`\n**Batch Name** : `{batch_name}`\n\n🍿 **Total Video** : `{v_count}`\n📝 **Total pdf** : `{p_count}`\n⌚️ **Time Taken** : `{elapsed}`"
            with open(file_path, 'a') as f:
                f.write(f"{vt}")
                
            me = await app.get_me()
            big_file_id = me.photo.big_file_id
            thumb = await asyncio.create_task(app.download_media(big_file_id))
            await app.send_document(chat_id=message.chat.id, document=file_path, caption=caption, thumb=thumb, reply_markup=keyboard)
            await msg.delete()
            os.remove(file_path)
            await asyncio.sleep(2)
            await message.reply_text(f"✅ Done\n\n📝**User ID** : `{userid}`\n✏️ **Token** : `{token}`")

        await session.close()
        
    except Exception as e:
        print(f"Error : {str(e)}")
        await message.reply_text(f"**Error** : `{e}`")


# --------------------------- Appex-V2 --------------------------- #

async def course_content(session, api, headers, token, course_id, parent_id=-1):
    try:
        lectures = []
        response = await session.get(f"https://{api}/get/folder_contentsv2?course_id={course_id}&parent_id={parent_id}", headers=headers)
        data_list = (await response.json()).get("data", [])
        
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
                    
                    for link in encrypted_links:
                        if link.get("quality") == "360p":
                            try:
                                video_path = appx_decrypt(link.get("path", "").split(":")[0])
                                video_key = appx_decrypt(link.get("key", "").split(":")[0])
                                break
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
                else:
                    lectures.append(title)
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
                input1 = await app.listen(user_id, timeout=30)
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

            response = await session.get(f"https://{api}/get/get_all_purchases?userid=""&item_type=10", headers=headers)
            batch_data = (await response.json()).get("data", [])

            batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            batch_map = {}
            for data in batch_data:
                for cdata in data['coursedt']:
                    batch_list += f"`{cdata['id']}`  -   **{cdata['course_name']}**\n\n"
                    batch_map[cdata['id']] = cdata['course_name']

            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id)
            course_id = input2.text.strip()
            await input2.delete()

            batch_name = batch_map.get(course_id, "Unknown Batch")
            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

            start_time = time.time()
            lectures = await asymcio.create_task(course_content(session, api, headers, token, course_id))
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

    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")


# --------------------------- Appex-Command --------------------------- #


@app.on_message(filters.command("appx")) 
async def appx_logins(_, message):
    user_id = message.from_user.id
    msg = await message.reply_text("📝 Please Provide Your Appx API URL.")

    input_msg = await app.listen(user_id)
    raw_text = input_msg.text
    await input_msg.delete(True)
    def extract_parts(url):
        match = re.search(r'(\w+?)(api)?\.classx\.co\.in', url)
        if match:
            name = match.group(1)
            original_subdomain = match.group(0)
            return name, original_subdomain
        return None, None

    name, api = extract_parts(raw_text)
    if not name or not api:
        return await msg.edit_text("❌ **Invalid API URL! Please try again.**")

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌿 Appx V2", callback_data=f"appx_v2*{name}#{api}"), 
         InlineKeyboardButton("🌴 Appx V3", callback_data=f"appx_v3*{name}#{api}")]
    ])    
    mm = await msg.edit_text("🕹 **Select Your Appx API Version:**", reply_markup=buttons)
    await asyncio.sleep(10)
    await mm.delete()








