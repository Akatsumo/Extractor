import cloudscraper  # Replace requests with cloudscraper
import datetime, pytz, re, aiofiles, os, base64, io
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode
from pyrogram import filters
from Extractor import app
from concurrent.futures import ThreadPoolExecutor
import threading

appname = "Utkarsh"
txt_dump = 8075872851
txt_dump2 = 8075872851

def decrypt(enc):
    try:
        enc = b64decode(enc)
        Key = '%!$!%_$&!%F)&^!^'.encode('utf-8')
        iv = '#*y*#2yJ*#$wJv*v'.encode('utf-8')
        cipher = AES.new(Key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(enc), AES.block_size)
        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

async def save_urls(app, user_id, m, all_urls, start_time, bname, batch_id):
    try:
        bname = await sanitize_bname(bname)
        file_path = f"{bname}.txt"
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        minutes, seconds = divmod(duration.total_seconds(), 60)
        user = await app.get_users(user_id)
        contact_link = f"[{user.first_name}](tg://openmessage?user_id={user_id})"
        all_text = "\n".join(all_urls)
        video_count = len(re.findall(r'\.(m3u8|mpd|mp4)', all_text))
        pdf_count = len(re.findall(r'\.pdf', all_text))
        drm_video_count = len(re.findall(r'\.(videoid|mpd|testbook)', all_text))
        enc_pdf_count = len(re.findall(r'\.pdf\*', all_text))
        caption = (
            f"**APP NAME :** UTKARSH \n\n **Batch Name :** {batch_id} - {bname} \n\n "
            f"TOTAL LINK - {len(all_urls)} \n Video Links - {video_count - drm_video_count} \n "
            f"Total Pdf - {pdf_count} \n"
        )
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.writelines([url + '\n' for url in all_urls])
        
        copy = await m.reply_document(document=file_path, caption=caption)
        await app.send_document(txt_dump, file_path, caption=caption)
        os.remove(file_path)
    except Exception as e:
        await m.reply_text(f"Error saving URLs: {e}")

async def sanitize_bname(bname, max_length=50):
    bname = re.sub(r'[\\/:*?"<>|\t\n\r]+', '', bname).strip()
    if len(bname) > max_length:
        bname = bname[:max_length]
    return bname

def fetch_subject_ids(batch_id, token, headers, scraper):
    try:
        data4 = {
            'tile_input': f'{{"course_id": {batch_id},"revert_api":"1#0#0#1","parent_id":0,"tile_id":"0","layer":1,"type":"course_combo"}}',
            'csrf_name': token
        }
        Key = '%!$!%_$&!%F)&^!^'.encode('utf-8')
        iv = '#*y*#2yJ*#$wJv*v'.encode('utf-8')
        cipher = AES.new(Key, AES.MODE_CBC, iv)
        padded_data = pad(data4['tile_input'].encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        encoded_data = base64.b64encode(encrypted_data).decode()
        data4['tile_input'] = encoded_data
        res4 = scraper.post("https://online.utkarsh.com/web/Course/tiles_data", headers=headers, data=data4).json()
        response = res4.get("response", "").replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
        res4_dec = decrypt(response)
        if not res4_dec:
            return [], {}
        res4_json = json.loads(res4_dec)
        subject = res4_json.get("data", [])
        subject_ids = [str(item["id"]) for item in subject]
        subject_titles = {str(item["id"]): item["title"] for item in subject}
        return subject_ids, subject_titles
    except Exception as e:
        print(f"Error fetching subject IDs: {e}")
        return [], {}

def fetch_topic_ids(subject_id, batch_id, token, headers, scraper):
    try:
        data5 = {
            'tile_input': f'{{"course_id":{subject_id},"layer":1,"page":1,"parent_id":{batch_id},"revert_api":"1#0#0#1","tile_id":"0","type":"content"}}',
            'csrf_name': token
        }
        Key = '%!$!%_$&!%F)&^!^'.encode('utf-8')
        iv = '#*y*#2yJ*#$wJv*v'.encode('utf-8')
        cipher = AES.new(Key, AES.MODE_CBC, iv)
        padded_data = pad(data5['tile_input'].encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        encoded_data = base64.b64encode(encrypted_data).decode()
        data5['tile_input'] = encoded_data
        res5 = scraper.post("https://online.utkarsh.com/web/Course/tiles_data", headers=headers, data=data5).json()
        response = res5.get("response", "").replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
        decres5 = decrypt(response)
        if not decres5:
            return [], []
        res5l = json.loads(decres5)
        resp5 = res5l.get("data", {})
        if not resp5:
            return [], []
        res5list = resp5.get("list", [])
        topic_ids = [str(id["id"]) for id in res5list]
        return topic_ids, res5list
    except Exception as e:
        print(f"Error fetching topic IDs: {e}")
        return [], []

def fetch_urls(subject_id, batch_id, topic_id, token, headers, url_lock, all_urls, scraper):
    try:
        local_urls = []
        data5 = {
            'tile_input': f'{{"course_id":{subject_id},"parent_id":{batch_id},"layer":2,"page":1,"revert_api":"1#0#0#1","subject_id":{topic_id},"tile_id":0,"topic_id":{topic_id},"type":"content"}}',
            'csrf_name': token
        }
        Key = '%!$!%_$&!%F)&^!^'.encode('utf-8')
        iv = '#*y*#2yJ*#$wJv*v'.encode('utf-8')
        cipher = AES.new(Key, AES.MODE_CBC, iv)
        padded_data = pad(data5['tile_input'].encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        encoded_data = base64.b64encode(encrypted_data).decode()
        data5['tile_input'] = encoded_data
        res6 = scraper.post("https://online.utkarsh.com/web/Course/tiles_data", headers=headers, data=data5).json()
        response = res6.get("response", "").replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
        decres6 = decrypt(response)
        if not decres6:
            return
        res6l = json.loads(decres6)
        resp5 = res6l.get("data", {})
        if not resp5:
            return
        res6list = resp5.get("list", [])
        subtopic_ids = [str(id["id"]) for id in res6list]
        
        for subtopic_id in subtopic_ids:
            data6 = {
                'layer_two_input_data': f'{{"course_id":{subject_id},"parent_id":{batch_id},"layer":3,"page":1,"revert_api":"1#0#0#1","subject_id":{topic_id},"tile_id":0,"topic_id":{subtopic_id},"type":"content"}}',
                'content': 'content',
                'csrf_name': token
            }
            encoded_data = base64.b64encode(data6['layer_two_input_data'].encode()).decode()
            data6['layer_two_input_data'] = encoded_data
            res6 = scraper.post("https://online.utkarsh.com/web/Course/get_layer_two_data", headers=headers, data=data6).json()
            response = res6.get("response", "").replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
            decres6 = decrypt(response)
            if not decres6:
                continue
            res6_json = json.loads(decres6)
            res6data = res6_json.get('data', {})
            if not res6data:
                continue
            res6_list = res6data.get('list', [])
            
            for item in res6_list:
                title = item.get("title").replace("||", "-").replace(":", "-")
                bitrate_urls = item.get("bitrate_urls", [])
                url = None
                for url_data in bitrate_urls:
                    if url_data.get("title") == "720p":
                        url = url_data.get("url")
                        break
                    elif url_data.get("name") == "720x1280.mp4":
                        url = url_data.get("link") + ".mp4"
                        url = url.replace("/enc/", "/plain/")
                if url is None:
                    url = item.get("file_url")
                if url and not url.endswith('.ws'):
                    if url.endswith(("_0_0", "_0")):
                        url = "https://apps-s3-jw-prod.utkarshapp.com/admin_v1/file_library/videos/enc_plain_mp4/{}/plain/720x1280.mp4".format(url.split("_")[0])
                    elif not url.startswith("https://") and not url.startswith("http://"):
                        url = f"https://youtu.be/{url}"
                    cc = f'{title}: {url}'
                    local_urls.append(cc)
        
        with url_lock:
            all_urls.extend(local_urls)
    except Exception as e:
        print(f"Error fetching URLs: {e}")




async def handle_utk_logic(app, m, user_id):
    user_id = user_id if user_id else m.from_user.id
    try:
        editable = await m.reply_text("Send **ID & Password** in this manner otherwise app will not respond.\n\nSend like this:-  **ID*Password**")
        input1 = await app.listen(chat_id=user_id)
        raw_text = input1.text
        await input1.delete()
        
        scraper = cloudscraper.create_scraper()  # Initialize cloudscraper
        token = scraper.get('https://online.utkarsh.com/web/home/get_states').json().get("token")
        if not token:
            await editable.edit("Failed to retrieve CSRF token")
            return
        
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'origin': 'https://online.utkarsh.com',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'csrf_name={token}; ci_session=tb0uld02neaa4ujs1g4idb6l8bmql8jh'
        }
        
        if '*' in raw_text:
            ids, ps = raw_text.split("*")
            data = f"csrf_name={token}&mobile={ids}&url=0&password={ps}&submit=LogIn&device_token=null"
            log_response = scraper.post('https://online.utkarsh.com/web/Auth/login', headers=headers, data=data).json()
            response = log_response.get("response", "").replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
            dec_log = decrypt(response)
            if not dec_log:
                await editable.edit("Login failed: Decryption error")
                return
            dec_logs = json.loads(dec_log)
            error_message = dec_logs.get("message", "Unknown error")
            status = dec_logs.get('status', False)
            if status:
                await editable.edit(f"**User authentication successful.**")
            else:
                await editable.edit(f'Login Failed - {error_message}')
                return
        else:
            await editable.edit("**Please Send id password in this manner** \n\n**Id*Password")
            return

        data2 = f"type=Batch&csrf_name={token}&sort=0"
        res2 = scraper.post('https://online.utkarsh.com/web/Profile/my_course', headers=headers, data=data2).json()
        response = res2.get("response", "").replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
        decrypted_res = decrypt(response)
        if not decrypted_res:
            await editable.edit("Failed to decrypt course data")
            return
        dc = json.loads(decrypted_res)
        dataxxx = dc.get('data', {})
        bdetail = dataxxx.get("data", [])
        
        cool = ""
        FFF = "**BATCH-ID -      BATCH NAME **"
        Batch_ids = ''
        for item in bdetail:
            id = item.get("id")
            batch = item.get("title")
            price = item.get("mrp")
            aa = f" `{id}`      - **{batch} ✳️ {price}**\n\n"
            if len(f'{cool}{aa}') > 4096:
                cool = ""
            cool += aa
            Batch_ids += str(id) + '&'
        Batch_ids = Batch_ids.rstrip('&')
        
        login_msg = f'<b>{appname} Login Successful ✅</b>\n'
        login_msg += f'**Utkarsh**\n<b>ID Password :- </b><code>{raw_text}</code>\n\n'
        login_msg += f'\n\n<b>BATCH ID ➤ BATCH NAME</b>\n\n{cool}#Utkarsh'
        copiable = await app.send_message(txt_dump2, login_msg)
        await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
        
        editable1 = await m.reply_text(f"**Now send the Batch ID to Download**\n\n**For All batch -** `{Batch_ids}`")
        user_id = int(m.chat.id)
        input2 = await app.listen(chat_id=user_id)
        await input2.delete()
        await editable.delete()
        await editable1.delete()
        
        if "&" in input2.text:
            batch_ids = input2.text.split('&')
        else:
            batch_ids = [input2.text]

        url_lock = threading.Lock()
        for batch_id in batch_ids:
            start_time = datetime.datetime.now()
            bname = next((x['title'] for x in bdetail if str(x['id']) == batch_id), None)
            if not bname:
                await m.reply_text(f"Batch ID {batch_id} not found")
                continue
            
            subject_ids, subject_titles = fetch_subject_ids(batch_id, token, headers, scraper)
            all_urls = []
            
            for u in subject_ids:
                xx = await m.reply_text(f"<b><i>Processing Subject: {subject_titles.get(u, 'Unknown')}** âœ“</b></i>")
                topic_ids, _ = fetch_topic_ids(u, batch_id, token, headers, scraper)
                if not topic_ids:
                    await xx.edit(f"No topics found for subject {subject_titles.get(u, 'Unknown')}")
                    await xx.delete()
                    continue
                
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = [
                        executor.submit(fetch_urls, u, batch_id, t, token, headers, url_lock, all_urls, scraper)
                        for t in topic_ids
                    ]
                    for future in futures:
                        future.result()  # Wait for all threads to complete
                
                await xx.edit(f"**Completed processing subject: {subject_titles.get(u, 'Unknown')}**")
                await xx.delete()
            
            if all_urls:
                await save_urls(app, user_id, m, all_urls, start_time, bname, batch_id)
        
        logout = scraper.get("https://online.utkarsh.com/web/Auth/logout", headers=headers)
        if logout.status_code == 200:
            print("**LogOut Successful**")
        else:
            print("Logout failed")
    except Exception as e:
        await m.reply_text(f"Error in bot logic: {e}")
