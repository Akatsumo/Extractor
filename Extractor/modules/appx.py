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


v_count = 0
p_count = 0
counter = 0

# --------------------------- Appex-V3 --------------------------- #

async def appex_down(session, message, hdr1, api, raw_text2, f, msg):
    try:
        global v_count, p_count
        prev_v_count = v_count
        prev_p_count = p_count
        vt = ""
        counter = 0
        
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
                prev_v_count = v_count
                prev_p_count = p_count

    except Exception as e:
        print(str(e))
    
    return vt



async def appex_v3_txt(app, message, api, name):
    global v_count, p_count
    user_id = message.from_user.id


    try:
        raw_url = f"https://{api}/post/userLogin"
        hdr = {
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
            await message.reply_text("⏳ Timeout! Please try again.")
            return
            
        if "*" in raw_text:           
            info["email"], info["password"] = raw_text.split("*")
        else:
            await msg.edit_text("😒 **Bruh Send ID Pass in Correct Form**")
            return
            
        await input1.delete(True)        
        async with aiohttp.ClientSession() as session:
            async with session.post(raw_url, data=info, headers=hdr) as response:
                res = await response.read()
                output = json.loads(res)
                userid = output["data"]["userid"]
                token = output["data"]["token"]
                
            hdr1 = {
                "Host": api,
                "Client-Service": "Appx",
                "Auth-Key": "appxapi",
                "User-Id": userid,
                "Authorization": token
            }
        
            await msg.edit_text("✅ **Login Successfully**")
        
            async with session.get(f"https://{api}/get/mycourseweb?userid={userid}", headers=hdr1) as response:
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
            html = scraper.get(f"https://{api}/get/allsubjectfrmlivecourseclass?courseid={raw_text2}", headers=hdr1).content
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
        
            tasks = [appex_down(session, message, hdr1, api, raw_text2, s, msg) for s in ss]
            results = await asyncio.gather(*tasks)
            for result in results:
                vt += result
        
            filename = batch_name.replace("/", "") if '/' in batch_name else batch_name
            file_path = f"{filename}_{user_id}.txt"
            end_time = time.time()
            duration_seconds = end_time - start_time
            elapsed = get_time(duration_seconds)
        
            caption = f"**App Name :- {name}\nBatch Name :-** `{batch_name}`\n\n🍿 **Total Video**: `{v_count}`\n📝 **Total pdf**: `{p_count}`\n⌚️**Time Taken**: `{elapsed}`"
            with open(file_path, 'a') as f:
                f.write(f"{vt}")
            await app.send_document(message.chat.id, document=file_path, caption=caption)
            await msg.delete()
            os.remove(file_path)
            await message.reply_text("✅ Done")
        await session.close()
        
    except Exception as e:
        print(f"Error : {str(e)}")
        await message.reply_text(f"**Error** : `{e}`")


# --------------------------- Appex-V2 --------------------------- #

async def course_content(session, scraper, api, message, raw_text2, parent_Id, hdr1, msg):
    try:
        response = await session.get(f"https://{api}/get/folder_contentsv2?course_id={raw_text2}&parent_id={parent_Id}", headers=hdr1)
        output = await response.json()
        data_list = output.get('data', [])
        vj = ""
        tasks = []
        for data in data_list:
            tasks.append(course_content2(session, scraper, api, message, raw_text2, parent_Id, hdr1, msg, data))
        results = await asyncio.gather(*tasks)
        for result in results:
            vj += result
        return vj
    except Exception as e:
        print(f"An error occurred in course_content: {str(e)}")
        raise


async def course_content2(session, scraper, api, message, raw_text2, parent_Id, hdr1, msg, data):
    global v_count, p_count
    try:
        vj = ""
        if data['material_type'] == 'FOLDER':
            folder_id = data['id']
            vj += await course_content(session, scraper, api, message, raw_text2, folder_id, hdr1, msg)

        if data['material_type'] == 'VIDEO':
            tid = data.get("Title")
            plink = data.get('pdf_link', "").split(':')            
            if len(plink) == 2:
                p_count += 1
                vs = appx_decrypt(plink[0])
                               
            if data.get('ytFlag') == 0 and data.get('ytFlagWeb') == 0:
                v_count += 1
                dlink = next((link['path'] for link in data.get('download_links', []) if link.get('quality') == "720p"), None)
                if dlink:
                    lec = appx_decrypt(dlink.split(':')[0])
                                                
            elif data.get('ytFlag') == 1 and data.get('ytFlagWeb') == 0 or data.get('ytFlag') == 1 and data.get('ytFlagWeb') == 1:
                v_count += 1
                dlink = data.get('file_link')
                if dlink:
                    b = appx_decrypt(dlink.split(':')[0])
                    lec = f"https://youtu.be/{b}"
                                
            msg = f"{tid} : {lec}\n{tid} : {vs}\n" if data.get('pdf_link') else f"{tid} : {lec}\n"
            vj += msg                        

        elif data['material_type'] == 'PDF':
            p_count += 1
            tid = data.get("Title")
            vs = appx_decrypt(data.get("pdf_link", "").split(':')[0])
            vj += f"{tid} : {vs}\n"

        return vj
    except Exception as e:
        print(f"An error occurred in course_content2: {str(e)}")
        raise


async def appex_v2_txt(app, message, api, name):
    global counter, v_count, p_count
    user_id = message.from_user.id


    async with aiohttp.ClientSession() as session:
        raw_url = f"https://{api}/post/userLogin"
        hdr = {
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
            await message.reply_text("⏳ Timeout! Please try again.")
            return
            
        if "*" in raw_text:           
            info["email"], info["password"] = raw_text.split("*")
        else:
            await msg.edit_text("😒 **Bruh Send ID Pass in Correct Form**")
            return
                  
        await input1.delete(True)
        try:
            async with session.post(raw_url, data=info, headers=hdr) as response:
                output = await response.json()
                userid = output["data"]["userid"]
                token = output["data"]["token"]
        except Exception as e:
            print(f"Error : {str(e)}")
            return await msg.edit_text("Please try again later. May be Password Wrong")

        hdr1 = {
            "Host": api,
            "Client-Service": "Appx",
            "Auth-Key": "appxapi",
            "User-Id": userid,
            "Authorization": token
        }
        await msg.edit_text("**✅ Login Successfully**")

        async with session.get(f"https://{api}/get/get_all_purchases?userid={userid}&item_type=10", headers=hdr1) as response:
            b_data = (await response.json()).get('data', [])

        FFF = "**BATCH-ID  -  BATCH NAME**\n\n"
        for data in b_data:
            for cdata in data['coursedt']:
                FFF += f"`{cdata['id']}`  -   **{cdata['course_name']}**\n\n"

        await msg.edit_text(f"{FFF}\n\n**📊Now send the Batch ID to Download**")
        input2 = await app.listen(user_id=query.from_user.id)
        raw_text2 = input2.text
        await input2.delete(True)
        batch_name = next((cdata['course_name'] for data in b_data for cdata in data['coursedt'] if cdata['id'] == raw_text2), "")
        scraper = cloudscraper.create_scraper()
        html = scraper.get(f"https://{api}/get/folder_contentsv2?course_id={raw_text2}&parent_id=-1", headers=hdr1).content
        output0 = json.loads(html)
        parent_Id = output0['data'][0]['id']
        await msg.edit_text("**Extracting Videos Links Please Wait  📥 **")
        start_time = time.time()
        vj = await course_content(session, scraper, api, message, raw_text2, parent_Id, hdr1, msg)
        end_time = time.time()
        duration_seconds = end_time - start_time
        elapsed = get_time(duration_seconds)
        
        file_name = batch_name.replace("/", "") if '/' in batch_name else batch_name     
        caption = f"**App Name** : `{name}`\n**Batch Name** : `{batch_name}`\n\n🍿 **Total Video** : `{v_count}`\n📝 **Total pdf** : `{p_count}`\n⌚️ **Time Taken** : `{elapsed}`"
        file_path = f"{file_name}_{user_id}.txt"
        with open(file_path, "a") as f:
            f.write(f"{vj}")
            
        await app.send_document(message.chat.id, document=file_path, caption=caption)
        await msg.delete()
        os.remove(file_path)
        await message.reply_text("✅ Done")

    await session.close()



# --------------------------- Appex-Command --------------------------- #

@app.on_message(filters.command("appx")) 
async def appx_logins(_, message):
    msg = await message.reply_text("Send Appx Api")
    input = await app.listen(user_id=query.from_user.id)
    raw_text = input.text
    def extract_parts(url):
        match = re.search(r'(\w+?)(api)?\.classx\.co\.in', url)
        if match:
            name = match.group(1)
            original_subdomain = match.group(0)
            return name, original_subdomain
        return None, None

    name, api = extract_parts(raw_text)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Appx V2", callback_data="appx_v2"), InlineKeyboardButton("Appx V3", callback_data="appx_v3")]])
    mm = await msg.edit_text("🕹 Select Your Appx Api Version 👇", reply_markup=buttons)
    r = await mm.wait_for_click(from_user_id=query.from_user.id)
    if r.data == 'app_v2':
       appex_v2_txt(app, message, api, name)               
    elif r.data == 'app_v3':
       appex_v3_txt(app, message, api, name) 
    else:
       pass


        



    
